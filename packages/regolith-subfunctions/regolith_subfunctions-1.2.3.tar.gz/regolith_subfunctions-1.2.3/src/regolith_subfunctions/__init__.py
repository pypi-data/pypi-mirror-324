import json
from enum import Enum, auto
from collections import deque
from typing import Deque, Iterator, List, Match, Optional, Dict, Tuple, Any
from pathlib import Path
import re
import sys
from better_json_tools import load_jsonc

VERSION = (1, 2, 3)
__version__ = '.'.join([str(x) for x in VERSION])

# The system_tempalte regolith filter overwrites the FUNCTION_PATH variable to
# be absolute.
FUNCTIONS_PATH = Path('BP/functions')
RP_TEXTS_PATH = Path('RP/texts')
BP_TEXTS_PATH = Path('BP/texts')

SELECTOR_P = r'(?:@[a-z](?:\[[0-9a-zA-Z_ \.,\":={}\[\]\+]+\])?)|[0-9a-zA-Z_]+|(?:\"[0-9a-zA-Z_ ]*\")'
NAME_P = "[a-zA-Z_0-9]+"
FUNCTION_NAME_P = f"{NAME_P}(?:/{NAME_P})*"
INT_P = "-?[0-9]+"
EXPR_P = r'[^`\n\r]+'

JUST_DEFINE = re.compile(f"definefunction <({FUNCTION_NAME_P})>:")
SUBFUNCTION = re.compile(f"(.* )?function <({FUNCTION_NAME_P})>:")
SCHEDULE = re.compile(f"(.* )?schedule (.+) <({FUNCTION_NAME_P})>:")
FUNCTIONTREE = re.compile(
    f"functiontree <({NAME_P})><({SELECTOR_P}) ({NAME_P}) +({INT_P})\\.\\.({INT_P})>:")
FOR = re.compile(f"for <({NAME_P}) +({INT_P})\\.\\.({INT_P})(?: +({INT_P}))?>:")
UNPACK_HERE = re.compile("UNPACK:HERE")
UNPACK_SUBFUNCTION = re.compile("UNPACK:SUBFUNCTION")
VAR = re.compile(f"var +({NAME_P}) *= *({EXPR_P})")
NO_VAR = re.compile(f"> +({EXPR_P})")
ASSERT = re.compile(f"assert +({EXPR_P})")
IF = re.compile(f"if <({EXPR_P})>:")
FOREACH = re.compile(f"foreach <({NAME_P}) +({NAME_P}) +({EXPR_P})>:")
EVAL = re.compile(f"`eval: *({EXPR_P}) *`")


class SubfunctionError(Exception):
    def __init__(
            self, source_path: Path, line_number: int,
            errors: List[str] | None = None):
        errors = [] if errors is None else errors
        self.errors = [
            f"Error at {source_path.as_posix()}:{line_number}:"] + errors

    def __str__(self):
        return "\n".join(self.errors)


class UnpackMode(Enum):
    NONE = auto()
    SUBFUNCTION = auto()
    HERE = auto()


class EvalException(Exception):
    def __init__(self, errors: List[str] | None = None):
        self.errors = [] if errors is None else errors

    def __str__(self):
        return "\n".join(self.errors)


def custom_eval(expr: str, scope: Dict[str, int]):
    '''
    Custom eval calls the "eval" function with the given expression and scope.
    If it fails, it raises an EvalException with the error message.
    '''
    try:
        return eval(expr, scope)
    except Exception as e:
        raise EvalException([
            "Expression evaluation failed.",
            str(e)
        ])


def print_red(text: str):
    for t in text.split('\n'):
        print("\033[91m {}\033[00m".format(t))


def get_function_name(path: Path):
    '''
    Returns the name of a function based on its path.
    The path must be valid (relative to FUNCTIONS_PATH)
    '''
    return path.relative_to(FUNCTIONS_PATH).with_suffix("").as_posix()


def get_subfunction_path(function_path: Path, subfunction_name: str):
    return (
        function_path.with_suffix("") / subfunction_name
    ).with_suffix(".mcfunction")


def line_error_message(
        line: str, start: int, stop: int, max_len: int=50) -> tuple[str, str]:
    '''
    Returns a tuple with two strings. The first string is the line of code
    with the error marked with '^' characters. The second string is a line
    with '^' characters marking the error.
    '''
    start, stop = sorted((start, stop))
    max_len = min(len(line), max_len)
    start = max(0, start)
    stop = min(len(line), stop)
    if stop-start >= max_len:
        up = line[start:start+max_len]
        down = "^"*max_len
    elif stop-max_len-1 >= 0:
        up = line[stop-max_len:stop]
        down = " "*(stop-1-max_len) + "^"*(stop-start)
    else:
        up = line[0:max_len]
        down = " "*start + "^"*(stop-start)+" "*(max_len-stop)
    return up, down


def eval_line_of_code(line: str, scope: Dict[str, int]) -> Tuple[str, bool]:
    '''
    Replaces the EVAL blocks in a line of code and returns a tuple with the
    string result and boolean indicating if the line was changed.
    '''
    if line.startswith("#"):  # Comments aren't evaluated
        return line, False
    cursor = 0
    replace: list[tuple[int, int, str]] = []
    while cursor < len(line) and (match := EVAL.search(line[cursor:])):
        start, end = cursor+match.start(), cursor+match.end()
        try:
            replace.append((start, end, str(custom_eval(match[1], scope))))
        except EvalException as e:
            u, d = line_error_message(line, start, end, max_len=50)
            raise EvalException(e.errors + [u, d])
        cursor = end
    if len(replace) > 0:
        result_list: list[str] = []
        prev_end = 0
        for r in replace:
            result_list.append(line[prev_end:r[0]])  # prefix
            result_list.append(r[2])  # value
            prev_end = r[1]
        result_list.append(line[prev_end:])  # sufix
        return "".join(result_list), True
    return line, False


class CodeTreeNode:
    def __init__(
            self, line: str, parent: Optional['CodeTreeNode'] = None,
            is_root: bool = False, line_number: int = 0):
        self.raw_line = line
        self.line_number = line_number
        self.parent: Optional[CodeTreeNode] = parent
        self.children: List[CodeTreeNode] = []
        # The expected indentation of a child_node
        self.child_indent: int | None = None
        self.is_root = is_root

    @property
    def stripped_line(self):
        return self.raw_line.strip()

    @property
    def indent(self):
        if self.is_root:
            return -1
        indent = 0
        for c in self.raw_line.rstrip():
            if c != ' ':
                break
            indent += 1
        return indent

    def is_blank(self):
        return self.stripped_line == ""

    def recursive_print(self, indent: int=0, indent_str: str="->") -> Iterator[str]:
        '''
        Debug function to print the code tree.
        '''
        if not self.is_root:
            yield f"{indent_str * indent}{self.stripped_line}"
            indent += 1
        for child in self.children:
            yield from child.recursive_print(indent)

    def eval_and_dump(
            self, scope: Dict[str, int], source_path: Path | None,
            export_path: Path,
            *, unpack_mode: UnpackMode = UnpackMode.NONE,
            assume_file_modified: bool = False,
            allow_overwrite: bool = True):
        '''
        Evaluates all of the CHILDREN of this node, and dumps created text into
        mcfunction file. This function recursively walks the CodeTree and
        calling it on the root node evaluates entire source file.

        :param scope: The scope dictionary that contains variables.
        :param source_path: The path of the source file.
        :param export_path: The path of the file to export the evaluated code.
        :param unpack_mode: The mode of unpacking the subfunctions, HERE,
            SUBFUNCTION or (default) NONE. The HERE and SUBFUNCTION modes
            delete the source file at the end of the evaluation (its content
            is unpacked to other files).
        :param assume_file_modified: Used in recursive calls. Normally, when
            the file is not modified after the evaluation, no file is written
            (to improve performance). If this parameter is set to True, the
            file will be written even if it was not modified (which sometimes
            is useful in internal logic).
        :param allow_overwrite: Used internally in recursive calls. If set to
            False, the function will error if the file to write to already
            exists. By default this parameter is set to True, because when
            you call run 'subfunctions' filter on a file, you want to modfiy it
            but the internall calls that create the subfunctions from the file
            should check if the files aren't already created and stop if
            they are to avoid confusing situations where the same file is
            written to multiple times.
        '''
        if source_path is None:
            source_path = export_path
        evaluated_lines, file_modified, unpack_mode = self._eval(
            scope, source_path, export_path,
            unpack_mode=unpack_mode, assume_file_modified=assume_file_modified)
        if unpack_mode == UnpackMode.NONE:
            if file_modified:  # don't overwrite if file was not modified
                if not allow_overwrite:
                    if export_path.exists():
                        raise SubfunctionError(
                            source_path, self.line_number,
                            ["Attempting to overwrite a file that already "
                             "exists: ", f"{export_path.as_posix()}"])
                export_path.parent.mkdir(exist_ok=True, parents=True)
                with export_path.open('w', encoding='utf8') as f:
                    f.write("\n".join(evaluated_lines))
        else:  # UnpackMode.HERE or UnpackMode.SUBFUNCTION
            # The files have been unpacked to other locations and they should
            # be deleted
            export_path.unlink(missing_ok=True)

    def _eval(
        self, scope: Dict[str, int], source_path: Path, export_path: Path, *,
        unpack_mode: UnpackMode = UnpackMode.NONE,
        assume_file_modified: bool = False
    ) -> Tuple[List[str], bool, UnpackMode]:
        '''
        Evaluates all of the CHILDREN of this node, returns created text as a
        list of commands and a bool that indicates if the file was modified.
        It also calls eval_and_dump function if the subnodes have function
        definitions.
        '''
        evaluated_lines: List[str] = []
        file_modified = False or assume_file_modified
        for child in self.children:
            stripped_line = child.stripped_line
            is_lang = export_path.suffix == '.lang'
            if (
                    (stripped_line.startswith("##") and not is_lang) or
                    child.is_blank()):
                continue  # skip
            try:
                eval_line, line_modified = eval_line_of_code(
                    stripped_line, scope)
            except EvalException as e:
                raise SubfunctionError(
                    source_path, child.line_number, e.errors)
            file_modified = file_modified or line_modified
            if m := VAR.fullmatch(eval_line):
                self._eval_var(source_path, child, m, scope, stripped_line)
                file_modified = True
            elif m := NO_VAR.fullmatch(eval_line):
                self._eval_no_var(source_path, child, m, scope, stripped_line)
                file_modified = True
            elif (m := JUST_DEFINE.fullmatch(eval_line)) and not is_lang:
                self._eval_just_define(
                    source_path, export_path, m, scope, child)
                file_modified = True
            elif (m := SUBFUNCTION.fullmatch(eval_line)) and not is_lang:
                command = self._eval_subfunction(
                    unpack_mode, source_path, export_path, m, scope, child)
                evaluated_lines.append(command)
                file_modified = True
            elif (m := SCHEDULE.fullmatch(eval_line)) and not is_lang:
                command = self._eval_schedule(
                    unpack_mode, source_path, export_path, m, scope, child)
                evaluated_lines.append(command)
                file_modified = True
            elif m := IF.fullmatch(eval_line):
                commands = self._eval_if(
                    unpack_mode, source_path, export_path, m, scope, child,
                    stripped_line)
                evaluated_lines.extend(commands)
                file_modified = True
            elif m := FOR.fullmatch(eval_line):
                commands = self._eval_for(
                    unpack_mode, source_path, export_path, m, scope, child)
                evaluated_lines.extend(commands)
                file_modified = True
            elif m := FOREACH.fullmatch(eval_line):
                commands = self._eval_foreach(
                    unpack_mode, source_path, export_path, m, scope, child,
                    stripped_line)
                evaluated_lines.extend(commands)
                file_modified = True
            elif (m := FUNCTIONTREE.fullmatch(eval_line)) and not is_lang:
                commands = self._eval_functiontree(
                    unpack_mode, source_path, export_path, m, scope, child)
                evaluated_lines.extend(commands)
                file_modified = True
            elif m := ASSERT.fullmatch(eval_line):
                self._eval_assert(source_path, child, m, scope, stripped_line)
                file_modified = True
            elif (m := UNPACK_HERE.fullmatch(eval_line)) and not is_lang:
                export_path = self._eval_unpack_here(
                    source_path, export_path, child)
                unpack_mode = UnpackMode.HERE
                file_modified = True
            elif (
                    (m := UNPACK_SUBFUNCTION.fullmatch(eval_line)) and
                    not is_lang):
                self._eval_unpack_subfunction(source_path, child)
                unpack_mode = UnpackMode.SUBFUNCTION
                file_modified = True
            else:  # Regular command
                # Evaluating lines is not allowed in UNPACK:HERE or
                # UNPACK:SUBFUNCTION
                if unpack_mode in (UnpackMode.SUBFUNCTION, UnpackMode.HERE):
                    raise SubfunctionError(
                        source_path, child.line_number,
                        ["Using regular commands is not allowed directly in "
                         "functions using UNPACK:HERE or UNPACK:SUBFUNCTION!"])

                evaluated_lines.append(eval_line)
                # The indentation for "Regular command" is allowed only if
                # there is a comment at the top. This feature allows to write
                # comments about certain sections of the code but still lets
                # the Subfunctions preprocessor to detect errors like mistyped
                # block headers (like 'definefunction', 'for', 'if', etc.)
                if (
                        len(child.children) > 0 and
                        not stripped_line.startswith('#')):
                    raise SubfunctionError(
                        source_path, child.line_number,
                        ["Unexpected indentation."])
                commands, commands_modified, _ = child._eval(
                    scope, source_path, export_path,
                    unpack_mode=unpack_mode, assume_file_modified=assume_file_modified)
                evaluated_lines.extend(commands)
                file_modified = file_modified or commands_modified
        return evaluated_lines, file_modified, unpack_mode

    def _eval_functiontree(
            self, unpack_mode: UnpackMode, source_path: Path,
            export_path: Path, match: Match[str],
            scope: Dict[str, int], child: 'CodeTreeNode') -> List[str]:
        if unpack_mode in (UnpackMode.SUBFUNCTION, UnpackMode.HERE):
            raise SubfunctionError(
                source_path, child.line_number,
                ["Using 'functiontree' keyword is not allowed in "
                 "functions using UNPACK:HERE or UNPACK:SUBFUNCTION!"])
        m_name: str = match[1]
        m_selector: str = match[2]
        m_score: str = match[3]
        m_min = int(match[4])
        m_max = int(match[5])

        def yield_splits(
                list_: List[int], is_root_block: bool=True
        ) -> Iterator[Tuple[int, int, int, int, bool]]:
            if len(list_) <= 1:
                return
            split = len(list_)//2
            left, right = list_[:split], list_[split:]
            yield list_[0], left[-1], right[0], list_[-1], is_root_block
            yield from yield_splits(left, False)
            yield from yield_splits(right, False)

        leaf_values: List[int] = [i for i in range(m_min, m_max)]
        result: list[str] = []
        for left_min, left_max, right_min, right_max, is_root_block in \
                yield_splits(leaf_values):
            # Sorting items in case of reverse iteration
            left_min, left_max, right_min, right_max = sorted(
                (left_min, left_max, right_min, right_max))
            branch_content: list[str] = []
            branch_path = get_subfunction_path(
                export_path, f'{m_name}_{left_min}_{right_max}')
            left_prefix = (
                f'execute if score {m_selector} {m_score} matches '
                f'{left_min}..{left_max} run '
            )
            right_prefix = (
                f'execute if score {m_selector} {m_score} matches '
                f'{right_min}..{right_max} run '
            )

            # Left branch half
            left_branch_path = get_subfunction_path(
                export_path, f'{m_name}_{left_min}_{left_max}')
            if left_min != left_max:  # go deeper into tree branches
                left_suffix = (
                    f'function {get_function_name(left_branch_path)}')
                branch_content.append(left_prefix + left_suffix)
            else:  # leaf node
                scope[m_score] = left_min
                evaluated_commands, _, _ = child._eval(
                    scope, source_path, left_branch_path,
                    unpack_mode=unpack_mode)
                if len(evaluated_commands) == 1:
                    branch_content.append(left_prefix + evaluated_commands[0])
                else:  # More than one in normal case (possible edge case: 0)
                    if left_branch_path.exists():
                        raise SubfunctionError(
                            source_path, child.line_number,
                            ["Attempting to overwrite a file that already "
                             "exists: ", f"{left_branch_path.as_posix()}"])
                    left_suffix = (
                        f'function {get_function_name(left_branch_path)}')
                    left_branch_path.parent.mkdir(exist_ok=True, parents=True)
                    with left_branch_path.open('w', encoding='utf8') as f:
                        f.write('\n'.join(evaluated_commands))
                    branch_content.append(left_prefix + left_suffix)
            # Right branch half
            right_branch_path = get_subfunction_path(
                export_path, f'{m_name}_{right_min}_{right_max}')
            if right_min != right_max:  # go deeper into tree branches
                right_suffix = (
                    f'function {get_function_name(right_branch_path)}')
                branch_content.append(right_prefix + right_suffix)
            else:  # leaf node
                scope[m_score] = right_min
                evaluated_commands, _, _ = child._eval(
                    scope, source_path, right_branch_path,
                    unpack_mode=unpack_mode)
                if len(evaluated_commands) == 1:
                    branch_content.append(right_prefix + evaluated_commands[0])
                else:  # More than one in normal case (possible edge case: 0)
                    if right_branch_path.exists():
                        raise SubfunctionError(
                            source_path, child.line_number,
                            ["Attempting to overwrite a file that already "
                             "exists: ", f"{right_branch_path.as_posix()}"])
                    right_suffix = (
                        f'function {get_function_name(right_branch_path)}')
                    right_branch_path.parent.mkdir(exist_ok=True, parents=True)
                    with right_branch_path.open('w', encoding='utf8') as f:
                        f.write('\n'.join(evaluated_commands))
                    branch_content.append(right_prefix + right_suffix)
            if is_root_block:
                result.extend(branch_content)
            else:
                if branch_path.exists():
                    raise SubfunctionError(
                        source_path, child.line_number,
                        ["Attempting to overwrite a file that already "
                         "exists: ", f"{branch_path.as_posix()}"])
                branch_path.parent.mkdir(exist_ok=True, parents=True)
                with branch_path.open('w', encoding='utf8') as f:
                    f.write('\n'.join(branch_content))
        return result

    def _eval_for(
            self, unpack_mode: UnpackMode, source_path: Path,
            export_path: Path, match: Match[str], scope: Dict[str, int],
            child: 'CodeTreeNode') -> List[str]:
        '''
        Evaluates a 'for' loop. Returns a list of commands generated by the
        loop.
        '''
        m_var = match[1]
        m_min = int(match[2])
        m_max = int(match[3])
        m_step = 1 if match[4] is None else int(match[4])
        result: List[str] = []
        for i in range(m_min, m_max, m_step):
            scope[m_var] = i
            evaluated_lines, _, _ = child._eval(
                scope, source_path, export_path,
                unpack_mode=unpack_mode)
            result.extend(evaluated_lines)
        return result

    def _eval_foreach(
            self, unpack_mode: UnpackMode, source_path: Path,
            export_path: Path, match: Match[str], scope: Dict[str, int],
            child: 'CodeTreeNode', stripped_line: str) -> List[str]:
        '''
        Evaluates a 'for' loop. Returns a list of commands generated by the
        loop.
        '''
        m_index = match[1]
        m_var = match[2]
        result: List[str] = []
        try:
            m_iterable = custom_eval(match[3], scope)
        except EvalException as e:
            start, stop = match.regs[3]
            u, d = line_error_message(
                stripped_line, start, stop, max_len=50)
            raise SubfunctionError(
                source_path, child.line_number,
                e.errors + [u, d])
        for i, v in enumerate(m_iterable):
            scope[m_index] = i
            scope[m_var] = v
            evaluated_lines, _, _ = child._eval(
                scope, source_path, export_path,
                unpack_mode=unpack_mode)
            result.extend(evaluated_lines)
        return result

    def _eval_if(
            self, unpack_mode: UnpackMode, source_path: Path,
            export_path: Path, match: Match[str], scope: Dict[str, int],
            child: 'CodeTreeNode', stripped_line: str) -> List[str]:
        '''
        Evaluates an 'if' block. Returns a list of generated commands if the
        condition is true, otherwize returns an empty list.
        '''
        try:
            m_condition = bool(custom_eval(match[1], scope))
        except EvalException as e:
            start, stop = match.regs[1]
            u, d = line_error_message(
                stripped_line, start, stop, max_len=50)
            raise SubfunctionError(
                source_path, child.line_number,
                e.errors + [u, d])
        if m_condition:
            evaluated_lines, _, _ = child._eval(
                scope, source_path, export_path,
                unpack_mode=unpack_mode)
            return evaluated_lines
        return []

    def _eval_subfunction(
            self, unpack_mode: UnpackMode, source_path: Path, export_path: Path,
            match: Match[str], scope: Dict[str, int], child: 'CodeTreeNode') -> str:
        '''
        Evaluates a 'subfunction' command. Returns a line of code for
        the parent function.
        '''
        if unpack_mode in (UnpackMode.SUBFUNCTION, UnpackMode.HERE):
            raise SubfunctionError(
                source_path, child.line_number,
                ["Using 'function' keyword is not allowed in "
                 "functions using UNPACK:HERE or UNPACK:SUBFUNCTION!"])
        subfunction_name = f'{get_function_name(export_path)}/{match[2]}'
        prefix = "" if match[1] is None else match[1]
        subfunction_path = get_subfunction_path(export_path, match[2])
        child.eval_and_dump(
            scope, source_path, subfunction_path,
            unpack_mode=UnpackMode.NONE, assume_file_modified=True,
            allow_overwrite=False)
        return f"{prefix}function {subfunction_name}"

    def _eval_schedule(
            self, unpack_mode: UnpackMode, source_path: Path, export_path: Path,
            match: Match[str], scope: Dict[str, int], child: 'CodeTreeNode') -> str:
        '''
        Evaluates a 'subfunction' command. Returns a line of code for
        the parent function.
        '''
        if unpack_mode in (UnpackMode.SUBFUNCTION, UnpackMode.HERE):
            raise SubfunctionError(
                source_path, child.line_number,
                ["Using 'schedule' keyword is not allowed in "
                 "functions using UNPACK:HERE or UNPACK:SUBFUNCTION!"])
        subfunction_name = f'{get_function_name(export_path)}/{match[3]}'
        schedule_args = match[2]
        prefix = "" if match[1] is None else match[1]
        subfunction_path = get_subfunction_path(export_path, match[3])
        child.eval_and_dump(
            scope, source_path, subfunction_path,
            unpack_mode=UnpackMode.NONE, assume_file_modified=True,
            allow_overwrite=False)
        return f"{prefix}schedule {schedule_args} {subfunction_name}"

    def _eval_just_define(
            self, source_path: Path, export_path: Path, match: Match[str],
            scope: Dict[str, int], child: 'CodeTreeNode'):
        '''Evaluates a 'definefunction' command.'''
        subfunction_path = get_subfunction_path(export_path, match[1])
        child.eval_and_dump(
            scope, source_path, subfunction_path,
            unpack_mode=UnpackMode.NONE, assume_file_modified=True,
            allow_overwrite=False)

    def _eval_unpack_here(
            self, source_path: Path, export_path: Path,
            child: 'CodeTreeNode') -> Path:
        '''
        Evaluates the UNPACK:HERE command and returns the path of the file.
        '''
        if not self.is_root or child.line_number != 1:
            raise SubfunctionError(
                source_path, child.line_number,
                ["'UNPACK:HERE' can be used only at the "
                 "first line of code of a function!"])
        # Replace the path with a path of a fake file to change the
        # target directory of the defined functions
        return export_path.parent.with_suffix(".mcfunction")

    def _eval_unpack_subfunction(
            self, source_path: Path, child: 'CodeTreeNode'):
        '''Evaluates UNPACK:SUBFUNCTION command.'''
        if not self.is_root or child.line_number != 1:
            raise SubfunctionError(
                source_path, child.line_number,
                ["'UNPACK:SUBFUNCTION' can be used only at the "
                 "first line of code of a function!"])

    def _eval_assert(
            self, source_path: Path, child: 'CodeTreeNode', match: Match[str],
            scope: Dict[str, int], stripped_line: str):
        '''Evaluates 'assert' command.'''
        m_expr = match[1]
        try:
            if not custom_eval(m_expr, scope):
                u, d = line_error_message(  # 7 = len("assert ")
                    stripped_line, 7, len(stripped_line), max_len=50)
                raise SubfunctionError(
                    source_path, child.line_number,
                    ["Assertion failed:", u, d])
        except EvalException as e:
            u, d = line_error_message(
                stripped_line, 0, len(stripped_line), max_len=50)
            raise SubfunctionError(
                source_path, child.line_number,
                e.errors + [u, d])

    def _eval_no_var(
            self, source_path: Path, child: 'CodeTreeNode',
            match: Match[str], scope: Dict[str, int], stripped_line: str):
        '''Evaluates '>' command.'''
        m_expr = match[1]
        try:
            custom_eval(m_expr, scope)
        except EvalException as e:
            u, d = line_error_message(
                stripped_line, 0, len(stripped_line), max_len=50)
            raise SubfunctionError(
                source_path, child.line_number,
                e.errors + [u, d])

    def _eval_var(
            self, source_path: Path, child: 'CodeTreeNode', match: Match[str],
            scope: Dict[str, int], stripped_line: str):
        '''Evaluates 'var' command.'''
        m_name = match[1]
        m_expr = match[2]
        try:
            scope[m_name] = custom_eval(m_expr, scope)
        except EvalException as e:
            u, d = line_error_message(
                stripped_line, 0, len(stripped_line), max_len=50)
            raise SubfunctionError(
                source_path, child.line_number,
                e.errors + [u, d])


class CodeTree:
    def __init__(self, source_path: Path):
        with source_path.open('r', encoding='utf8') as f:
            text = f.read()
        self.root: CodeTreeNode = CodeTreeNode("", is_root=True)
        self.root.child_indent = 0
        self._init_children(text, source_path)

    def _init_children(self, text: str, source_path: Path):
        node_stack: Deque[CodeTreeNode] = deque([self.root])
        blank_counter = 0
        for i, line in enumerate(text.splitlines()):
            line = CodeTreeNode(line, line_number=i+1)
            stack_top: CodeTreeNode = node_stack[-1]
            if line.is_blank():
                blank_counter += 1
                continue
            if line.indent > stack_top.indent:
                if stack_top.child_indent is None:
                    stack_top.child_indent = line.indent
                if line.indent != stack_top.child_indent:
                    raise SubfunctionError(
                        source_path, i,
                        [f"Indentation error: expected indent "
                         f"length is {stack_top.child_indent} but the actual "
                         f"value is {line.indent}."])
                for _ in range(blank_counter):
                    stack_top.children.append(
                        CodeTreeNode("", stack_top, line_number=i+1))
                stack_top.children.append(line)
                line.parent = stack_top
                node_stack.append(line)
            elif line.indent <= stack_top.indent:
                while (
                        stack_top.child_indent is None or
                        line.indent < stack_top.child_indent):
                    node_stack.pop()
                    stack_top = node_stack[-1]
                if stack_top.child_indent != line.indent:
                    raise SubfunctionError(
                        source_path, i,
                        [f"Indentation error: expected indent "
                         f"length is {stack_top.child_indent} but the actual "
                         f"value is {line.indent}."])
                for _ in range(blank_counter):
                    stack_top.children.append(
                        CodeTreeNode("", stack_top, line_number=i+1))
                stack_top.children.append(line)
                line.parent = stack_top
                node_stack.append(line)
            blank_counter = 0

    def __str__(self):
        return "\n".join(self.root.recursive_print(0))


def main():
    '''
    The main function used by the subfunctions regolith filter.
    '''
    try:
        config: dict[str, Any] = json.loads(sys.argv[1])
        assert isinstance(config, dict)
    except Exception:
        config = {}
    # Add scope
    scope: dict[str, Any] = {'true': True, 'false': False}
    scope_path = Path('data') / config.get(
        'scope_path', 'subfunctions/scope.json')
    try:
        file_scope = load_jsonc(scope_path).data
        assert isinstance(file_scope, dict)
        scope = scope | file_scope
    except:
        print_red(
            f"Unable to read scope from {scope_path.as_posix()}. "
            "Replaced with default scope. "
            "You can set it in config.json file in the filter settings in "
            "'scope_path' property.")
    edit_lang_files = config.get('edit_lang_files', False)
    # glob pattern result changed to list to avoid going over newly created
    # files
    walk_files = list(FUNCTIONS_PATH.rglob("*.mcfunction"))
    if edit_lang_files:
        walk_files += list(RP_TEXTS_PATH.glob("*.lang"))
        walk_files += list(BP_TEXTS_PATH.glob("*.lang"))
    try:
        for path in walk_files:
            tree = CodeTree(path)
            tree.root.eval_and_dump(scope, path, path)
    except SubfunctionError as e:
        for err in e.errors:
            print_red(err)
        sys.exit(1)
