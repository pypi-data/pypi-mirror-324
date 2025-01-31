""" Code for auto-generating ArgumentParsers from functions """

import argparse
import inspect
import re

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import get_type_hints


@dataclass
class ReplCommand:
    """Class definition for a provided CLI REPL command"""

    command: Callable = None
    help_txt: str = ""
    parser: argparse.ArgumentParser = None
    def_kwargs: dict = field(default_factory=dict)


@dataclass
class CommandMeta:
    """Class representing the content of a docstring"""

    func: Callable = None
    """ Function to assemble the docstring meta from """

    register_cmd: Callable[..., ReplCommand] = None
    """ Function reference to registry command """

    summary: str = ""
    """ First line of the docstring """

    additional: str = ""
    """ Additional lines after the summary and before other notations """

    additional_lines: list[str] = field(default_factory=list)
    """ Raw output of docstring lines for additional """

    args: dict[str, str] = field(default_factory=dict)
    """ Arg comments """

    args_lines: list[str] = field(default_factory=list)
    """ Raw output of docstring lines for args """

    returns: dict[str, str] = field(default_factory=dict)
    """ Return comments """

    returns_lines: list[str] = field(default_factory=list)
    """ Raw output of docstring lines for returns """

    yields: dict[str, str] = field(default_factory=dict)
    """ Yields comments """

    yields_lines: list[str] = field(default_factory=list)
    """ Raw output of docstring lines for yields """

    examples: dict[str, str] = field(default_factory=dict)
    """ Examples comments """

    examples_lines: list[str] = field(default_factory=list)
    """ Raw output of docstring lines for examples """

    raises: dict[str, str] = field(default_factory=dict)
    """ Raises comments """

    raises_lines: list[str] = field(default_factory=list)
    """ Raw output of docstring lines for raises """

    type_hints: dict[str, type] = field(default_factory=dict)
    """ Type hints retrieved from inspect """

    sig_parms: dict[str, inspect.Parameter] = field(default_factory=dict)
    """ Signature of function """

    flag_names: dict[str, list[str]] = field(default_factory=dict)
    """ Flag names to use for the ReplCommand.parser arguments embedded in the docstring """

    def __post_init__(self) -> None:

        if not self.func:
            return

        self.type_hints = get_type_hints(self.func)
        self.sig_parms = dict(inspect.signature(self.func).parameters)

        docstring = self.get_docstring()

        header_re = re.compile(r"[A-Z].*?:$")

        if not docstring:
            return self

        doc_parts = docstring.split("\n")

        cur_header = ""

        def get_header(header: str) -> str:
            nonlocal header_re
            header_name = header_re.findall(header)[0]

            return header_name.lower().replace(":", "")

        for part in doc_parts:
            if header_re.search(part):
                cur_header = get_header(part)
                cur_header += "_lines"
                continue

            if cur_header and hasattr(self, cur_header):
                prop = getattr(self, cur_header)
                if isinstance(prop, list):
                    prop.append(part)

            elif not self.summary:
                self.summary = part
            else:
                self.additional_lines.append(part)

        self.parse_lines()
        self.parse_flags()

    def get_docstring(self) -> str | None:
        """Retrieve docstring from function or, if not available, from inherited classes

        Returns:
            str | None: Docstring value
        """

        if not self.func:
            return

        if hasattr(self.func, "__doc__") and self.func.__doc__:
            return self.func.__doc__

        if not hasattr(self.func, "__name__") or not hasattr(self.func, "__self__"):
            return

        fname = self.func.__name__
        fn_self = getattr(self.func, "__self__")

        if not hasattr(fn_self, "__class__"):
            return

        cls = getattr(fn_self, "__class__")
        if not hasattr(cls, "__bases__"):
            return

        bases = getattr(cls, "__bases__")

        cls_fn = getattr(cls, fname)

        cls_sig = inspect.signature(cls_fn)

        for base in bases:
            if not hasattr(base, fname):
                continue

            base_fn = getattr(base, fname)

            if not inspect.signature(base_fn) == cls_sig:
                continue

            if not hasattr(base_fn, "__doc__"):
                continue

            doc = getattr(base_fn, "__doc__")

            if doc:
                return doc

    def gen_command(self) -> ReplCommand:
        """Generate a ReplCommand object from the provided function

        Raises:
            ValueError: If no registry command is provided

        Returns:
            ReplCommand: A ReplCommand object with the function and parser
        """

        if not self.register_cmd:
            raise ValueError("No registry command provided, cannot proceed")

        help_text = self.summary
        full_help = self.summary + self.additional

        repl_cmd = self.register_cmd(
            cmd_name=self.func.__name__,
            cmd_func=self.func,
            help_txt=help_text,
            use_parser=True,
            description=full_help,
        )

        if not self.sig_parms:
            return repl_cmd

        for arg, parm in self.sig_parms.items():
            arg_type = self.type_hints.get(arg, str)

            flag_name = self.flag_names.get(arg)

            cmd_init = {"help": self.args.get(arg)}

            if arg_type == bool:
                cmd_init["action"] = (
                    "store_false" if parm.default is True else "store_true"
                )

            if arg_type not in [str, bool]:
                cmd_init["type"] = arg_type

            if isinstance(arg_type, type) and isinstance(parm.default, arg_type):
                cmd_init["default"] = parm.default

            if isinstance(arg_type, list):
                cmd_init["nargs"] = "+"

            if cmd_init:
                repl_cmd.parser.add_argument(flag_name, **cmd_init)

            else:
                repl_cmd.parser.add_argument(flag_name)

        return repl_cmd

    def is_arg_optional(self, arg: str) -> bool:
        """Check if an argument is optional

        Args:
            arg (str): Argument name

        Returns:
            bool: True if the argument is optional
        """

        param = self.sig_parms.get(arg)
        if param is None:
            print(
                f"[WARNING]: function signature not assigned for {self.func.__name__}.{arg}"
            )
            return False
        return param.default != param.empty

    def parse_flags(self) -> None:
        """Parse the flag names from the arguments of the function signature"""

        if not self.args:
            return

        for arg in self.args:
            flag = arg.replace("_", "-")
            if self.is_arg_optional(arg):
                flag = "--" + flag

            self.flag_names[arg] = flag

    def parse_lines(self) -> None:
        """Parse the lines of the docstring into the appropriate sections"""

        if self.args_lines:
            self.parse_arg_strs()

        for header in ["additional", "returns", "yields", "examples", "raises"]:
            lines = getattr(self, f"{header}_lines")
            if lines:
                header_str = "\n".join(lines)
                setattr(self, header, header_str)

    def get_param_str(self, param: inspect.Parameter) -> str:
        """Get a string representation of the parameter

        Args:
            param (inspect.Parameter): Parameter to get the string representation of

        Returns:
            str: String representation of the parameter
        """

        optional = param.default != param.empty
        opt_str = ""
        if optional:
            opt_str = (", " if param.annotation else "") + "optional"

        return f"({param.annotation}{opt_str})"

    def parse_arg_strs(self) -> None:
        """Parse the argument strings from the docstring"""
        # pylint: disable=C0301
        arg_re = re.compile(
            r"(?P<arg_name>[a-zA-Z_]\w*)\s*(?P<type_hint>\(\w+(?:, optional)*\)):(?P<arg_text>\s*.+?$)"
        )
        # pylint: enable=C0301

        args = defaultdict(list)
        cur_arg = ""

        for line in self.args_lines:
            arg_match = arg_re.search(line)
            if arg_match:
                cur_arg, arg_type, arg_text = arg_match.groupdict().values()
                param = self.sig_parms.get(cur_arg)

                if param:
                    arg_type = self.get_param_str(param)
                args[cur_arg].append(f"{arg_type}{arg_text}")
            elif cur_arg:
                args[cur_arg].append(line)

        for arg, param in self.sig_parms.items():
            if arg not in args:
                args[arg].append(self.get_param_str(param))

        arg_strs = {arg: "\n".join(lines) for arg, lines in args.items()}
        self.args.update(arg_strs)
