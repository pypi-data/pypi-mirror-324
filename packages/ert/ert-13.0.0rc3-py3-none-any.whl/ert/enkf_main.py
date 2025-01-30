from __future__ import annotations

import json
import logging
import os
import time
from collections.abc import Iterable, Mapping
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import orjson
import pandas as pd
import xarray as xr
from numpy.random import SeedSequence

from ert.config.ert_config import create_forward_model_json
from ert.config.forward_model_step import ForwardModelStep
from ert.config.model_config import ModelConfig
from ert.substitutions import Substitutions, substitute_runpath_name

from .config import ExtParamConfig, Field, GenKwConfig, ParameterConfig, SurfaceConfig
from .config.design_matrix import DESIGN_MATRIX_GROUP
from .run_arg import RunArg
from .runpaths import Runpaths

if TYPE_CHECKING:
    from .storage import Ensemble

logger = logging.getLogger(__name__)


def _backup_if_existing(path: Path) -> None:
    if not path.exists():
        return
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%SZ")
    new_path = path.parent / f"{path.name}_backup_{timestamp}"
    path.rename(new_path)


def _value_export_txt(
    run_path: Path, export_base_name: str, values: Mapping[str, Mapping[str, float]]
) -> None:
    path = run_path / f"{export_base_name}.txt"
    _backup_if_existing(path)

    if len(values) == 0:
        return

    with path.open("w") as f:
        for key, param_map in values.items():
            for param, value in param_map.items():
                if isinstance(value, (int | float)):
                    print(f"{key}:{param} {value:g}", file=f)
                else:
                    print(f"{key}:{param} {value}", file=f)


def _value_export_json(
    run_path: Path, export_base_name: str, values: Mapping[str, Mapping[str, float]]
) -> None:
    path = run_path / f"{export_base_name}.json"
    _backup_if_existing(path)

    if len(values) == 0:
        return

    def parse_value(value: float | int | str) -> float | int | str:
        if isinstance(value, float | int):
            return value
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    # Hierarchical
    json_out: dict[str, float | dict[str, float | int | str]] = {
        key: {
            inner_key: parse_value(inner_value)
            for inner_key, inner_value in param_map.items()
        }
        for key, param_map in values.items()
    }

    # Disallow NaN from being written: ERT produces the parameters and the only
    # way for the output to be NaN is if the input is invalid or if the sampling
    # function is buggy. Either way, that would be a bug and we can report it by
    # having json throw an error.
    json.dump(
        json_out, path.open("w"), allow_nan=False, indent=0, separators=(", ", " : ")
    )


def _generate_parameter_files(
    parameter_configs: Iterable[ParameterConfig],
    export_base_name: str,
    run_path: Path,
    iens: int,
    fs: Ensemble,
    iteration: int,
) -> None:
    """
    Generate parameter files that are placed in each runtime directory for
    forward-model jobs to consume.

    Args:
        parameter_configs: Configuration which contains the parameter nodes for this
            ensemble run.
        export_base_name: Base name for the GEN_KW parameters file. Ie. the
            `parameters` in `parameters.json`.
        run_path: Path to the runtime directory
        iens: Realisation index
        fs: Ensemble from which to load parameter data
    """
    exports: dict[str, dict[str, float]] = {}

    for node in parameter_configs:
        # For the first iteration we do not write the parameter
        # to run path, as we expect to read if after the forward
        # model has completed.
        if node.forward_init and iteration == 0:
            continue
        export_values = node.write_to_runpath(Path(run_path), iens, fs)
        if export_values:
            exports.update(export_values)
        continue

    _value_export_txt(run_path, export_base_name, exports)
    _value_export_json(run_path, export_base_name, exports)


def _manifest_to_json(ensemble: Ensemble, iens: int, iter: int) -> dict[str, Any]:
    manifest = {}
    # Add expected parameter files to manifest
    for param_config in ensemble.experiment.parameter_configuration.values():
        assert isinstance(
            param_config,
            ExtParamConfig | GenKwConfig | Field | SurfaceConfig,
        )
        if param_config.forward_init and ensemble.iteration == 0:
            assert param_config.forward_init_file is not None
            file_path = substitute_runpath_name(
                param_config.forward_init_file, iens, iter
            )
            manifest[param_config.name] = file_path
    # Add expected response files to manifest
    for respons_config in ensemble.experiment.response_configuration.values():
        for input_file in respons_config.expected_input_files:
            manifest[f"{respons_config.response_type}_{input_file}"] = (
                substitute_runpath_name(input_file, iens, iter)
            )

    return manifest


def _seed_sequence(seed: int | None) -> int:
    # Set up RNG
    if seed is None:
        int_seed = SeedSequence().entropy
        logger.info(
            "To repeat this experiment, "
            "add the following random seed to your config file:"
        )
        logger.info(f"RANDOM_SEED {int_seed}")
    else:
        int_seed = seed
    assert isinstance(int_seed, int)
    return int_seed


def save_design_matrix_to_ensemble(
    design_matrix_df: pd.DataFrame,
    ensemble: Ensemble,
    active_realizations: Iterable[int],
    design_group_name: str = DESIGN_MATRIX_GROUP,
) -> None:
    assert not design_matrix_df.empty
    for realization_nr in active_realizations:
        row = design_matrix_df.loc[realization_nr][DESIGN_MATRIX_GROUP]
        ds = xr.Dataset(
            {
                "values": ("names", list(row.values)),
                "transformed_values": ("names", list(row.values)),
                "names": list(row.keys()),
            }
        )
        ensemble.save_parameters(
            design_group_name,
            realization_nr,
            ds,
        )


def sample_prior(
    ensemble: Ensemble,
    active_realizations: Iterable[int],
    parameters: list[str] | None = None,
    random_seed: int | None = None,
) -> None:
    """This function is responsible for getting the prior into storage,
    in the case of GEN_KW we sample the data and store it, and if INIT_FILES
    are used without FORWARD_INIT we load files and store them. If FORWARD_INIT
    is set the state is set to INITIALIZED, but no parameters are saved to storage
    until after the forward model has completed.
    """
    random_seed = _seed_sequence(random_seed)
    t = time.perf_counter()
    parameter_configs = ensemble.experiment.parameter_configuration
    if parameters is None:
        parameters = list(parameter_configs.keys())
    for parameter in parameters:
        config_node = parameter_configs[parameter]
        if config_node.forward_init:
            continue
        logger.info(
            f"Sampling parameter {config_node.name} for realizations {active_realizations}"
        )
        for realization_nr in active_realizations:
            ds = config_node.sample_or_load(
                realization_nr,
                random_seed=random_seed,
                ensemble_size=ensemble.ensemble_size,
            )
            ensemble.save_parameters(parameter, realization_nr, ds)

    ensemble.refresh_ensemble_state()
    logger.debug(f"sample_prior() time_used {(time.perf_counter() - t):.4f}s")


def create_run_path(
    run_args: list[RunArg],
    ensemble: Ensemble,
    user_config_file: str,
    env_vars: dict[str, str],
    env_pr_fm_step: dict[str, dict[str, Any]],
    forward_model_steps: list[ForwardModelStep],
    substitutions: Substitutions,
    templates: list[tuple[str, str]],
    model_config: ModelConfig,
    runpaths: Runpaths,
    context_env: dict[str, str] | None = None,
) -> None:
    if context_env is None:
        context_env = {}
    t = time.perf_counter()
    runpaths.set_ert_ensemble(ensemble.name)
    for run_arg in run_args:
        run_path = Path(run_arg.runpath)
        if run_arg.active:
            run_path.mkdir(parents=True, exist_ok=True)
            for source_file, target_file in templates:
                target_file = substitutions.substitute_real_iter(
                    target_file, run_arg.iens, ensemble.iteration
                )
                try:
                    file_content = Path(source_file).read_text("utf-8")
                except UnicodeDecodeError as e:
                    raise ValueError(
                        f"Unsupported non UTF-8 character found in file: {source_file}"
                    ) from e

                result = substitutions.substitute_real_iter(
                    file_content,
                    run_arg.iens,
                    ensemble.iteration,
                )
                target = run_path / target_file
                if not target.parent.exists():
                    os.makedirs(
                        target.parent,
                        exist_ok=True,
                    )
                target.write_text(result)

            _generate_parameter_files(
                ensemble.experiment.parameter_configuration.values(),
                model_config.gen_kw_export_name,
                run_path,
                run_arg.iens,
                ensemble,
                ensemble.iteration,
            )

            path = run_path / "jobs.json"
            _backup_if_existing(path)

            forward_model_output: dict[str, Any] = create_forward_model_json(
                context=substitutions,
                forward_model_steps=forward_model_steps,
                user_config_file=user_config_file,
                env_vars={**env_vars, **context_env},
                env_pr_fm_step=env_pr_fm_step,
                run_id=run_arg.run_id,
                iens=run_arg.iens,
                itr=ensemble.iteration,
            )
            with open(run_path / "jobs.json", mode="wb") as fptr:
                fptr.write(
                    orjson.dumps(
                        forward_model_output,
                        option=orjson.OPT_NON_STR_KEYS | orjson.OPT_INDENT_2,
                    )
                )
            # Write MANIFEST file to runpath use to avoid NFS sync issues
            data = _manifest_to_json(ensemble, run_arg.iens, run_arg.itr)
            with open(run_path / "manifest.json", mode="wb") as fptr:
                fptr.write(
                    orjson.dumps(
                        data, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_INDENT_2
                    )
                )

    runpaths.write_runpath_list(
        [ensemble.iteration], [real.iens for real in run_args if real.active]
    )

    logger.debug(f"create_run_path() time_used {(time.perf_counter() - t):.4f}s")
