# pylint: disable=logging-fstring-interpolation
import argparse
import logging
import sys

try:
    from ert.shared.version import __version__ as everest_version
except ImportError:
    everest_version = "0.0.0"
from everest.bin.config_branch_script import config_branch_entry
from everest.bin.everconfigdump_script import config_dump_entry
from everest.bin.everest_script import everest_entry
from everest.bin.everexport_script import everexport_entry
from everest.bin.everlint_script import lint_entry
from everest.bin.kill_script import kill_entry
from everest.bin.monitor_script import monitor_entry
from everest.bin.visualization_script import visualization_entry
from everest.plugins.everest_plugin_manager import EverestPluginManager


def _create_dump_action(dumps, extended=False):
    # Action for aiding user, --help stype
    class _DumpAction(argparse.Action):
        def __init__(
            self,
            option_strings,
            dest=argparse.SUPPRESS,
            default=argparse.SUPPRESS,
            help=None,
        ):
            super().__init__(
                option_strings=option_strings,
                dest=dest,
                default=default,
                nargs=0,
                help=help,
            )

        def __call__(
            self,
            parser,
            namespace,
            values,
            option_string=None,
        ):
            print(dumps(extended=extended))
            parser.exit()

    return _DumpAction


def _build_args_parser():
    """Build arg parser"""
    arg_parser = argparse.ArgumentParser(
        description="Tool for performing reservoir management optimization",
        usage=(
            "everest <command> [<args>]\n\n"
            "The most commonly used everest commands are:\n"
            f"{EverestMain.methods_help()}\n\n"
            "Run everest <command> --help for more information on a command"
        ),
    )
    arg_parser.add_argument("command", help="Subcommand to run")
    arg_parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {everest_version}",
    )
    return arg_parser


class EverestMain:
    def __init__(self, args):
        parser = _build_args_parser()
        # Parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        parsed_args = parser.parse_args(args[1:2])
        if not hasattr(self, parsed_args.command):
            parser.error("Unrecognized command")

        # Setup logging from plugins:
        EverestPluginManager().add_log_handle_to_root()
        logger = logging.getLogger(__name__)
        logger.info(f"Started everest with {parsed_args}")
        # Use dispatch pattern to invoke method with same name
        getattr(self, parsed_args.command)(args[2:])

    @classmethod
    def methods_help(cls):
        """Return documentation of the public methods in this class"""
        pubmets = [m for m in dir(cls) if not m.startswith("_")]
        pubmets.remove("methods_help")  # Current method should not show up in desc
        maxlen = max(len(m) for m in pubmets)
        docstrs = [getattr(cls, m).__doc__ for m in pubmets]
        doclist = [
            m.ljust(maxlen + 1) + d for m, d in zip(pubmets, docstrs, strict=False)
        ]
        return "\n".join(doclist)

    def run(self, args):
        """Start an optimization case base on given config file"""
        everest_entry(args)

    def monitor(self, args):
        """Monitor a running optimization case base on given config file"""
        monitor_entry(args)

    def kill(self, args):
        """Kill a running optimization case base on given config file"""
        kill_entry(args)

    def gui(self, args):
        """Start the graphical user interface (Removed)"""
        print("The gui command has been removed. Please use the run command instead.")

    def export(self, args):
        """Export data from a completed optimization case"""
        everexport_entry(args)

    def lint(self, args):
        """Validate a config file"""
        lint_entry(args)

    def render(self, args):
        """Display the configuration data loaded from a config file"""
        config_dump_entry(args)

    def branch(self, args):
        """Construct possible restart config file"""
        config_branch_entry(args)

    def results(self, args):
        """Start everest visualization plugin"""
        visualization_entry(args)


def start_everest(args=None):
    """Main entry point for the everest application"""
    args = args or sys.argv
    EverestMain(args)
