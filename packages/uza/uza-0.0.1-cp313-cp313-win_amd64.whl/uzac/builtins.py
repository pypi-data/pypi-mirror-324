from __future__ import annotations
from dataclasses import dataclass, field
from operator import (
    add,
    and_,
    eq,
    ge,
    gt,
    le,
    lt,
    mod,
    mul,
    ne,
    not_,
    or_,
    pow,
    truediv,
)
from typing import Callable, List, Optional
from uzac.type import (
    ArrowType,
    type_any,
    type_bool,
    type_int,
    type_float,
    type_string,
    type_array,
    type_void,
)

from uzac.ast import Identifier, Value

_builtins: dict[str, BuiltIn] = {}


def get_builtin(identifier: Identifier) -> Optional[BuiltIn]:
    """
    Returns a _BuiltIn_ with the given who's name matches the _identifier_
    if it exists.
    """
    return _builtins.get(identifier.name)


@dataclass(frozen=True)
class BuiltIn:
    """
    A BuiltIn is a function that is part of the standard library.
    """

    identifier: str
    interpret: Callable[..., Value]  # tree walk interpretation in python
    type_signatures: List[ArrowType]  # len == 1 if not polymorphic
    arity: int = field(init=False)
    is_op_code: bool = field(
        default=False
    )  # if true, emits specific opcode instead of CALL_NATIVE

    def __post_init__(self):
        # adds itself to the dict that holds all the builtins
        _builtins[self.identifier] = self
        object.__setattr__(self, "arity", len(self.type_signatures[0].param_types))

    def __str__(self) -> str:
        return f"BuiltIn({self.identifier}, {self.type_signatures})"


# ARITHMETIC FUNCTIONS

_bi_arith_types = [
    ArrowType([type_int, type_int], type_int),
    ArrowType([type_float, type_float], type_float),
    ArrowType([type_int, type_float], type_float),
    ArrowType([type_float, type_int], type_float),
]
_bi_string_concat = ArrowType([type_string, type_string], type_string)

bi_add = BuiltIn("+", add, [*_bi_arith_types, _bi_string_concat])


def _sub_or_neg(*args):
    if len(args) == 1:
        return -args[0]
    return args[0] - args[1]


bi_sub = BuiltIn(
    "-",
    _sub_or_neg,
    [
        *_bi_arith_types,
        ArrowType([type_int], type_int),
        ArrowType([type_float], type_float),
    ],
)
bi_mul = BuiltIn("*", mul, [*_bi_arith_types])
bi_div = BuiltIn("/", truediv, [*_bi_arith_types])
bi_mod = BuiltIn("%", mod, [ArrowType([type_int, type_int], type_int)])
bi_pow = BuiltIn("**", pow, [*_bi_arith_types])
bi_max = BuiltIn("max", max, [*_bi_arith_types])
bi_min = BuiltIn("min", min, [*_bi_arith_types])


# IO FUNCTIONS


def _lower_str_bool(func, **kwargs):
    """
    Hack to turn boolean strings into lower case
    """

    def decorated(*args):
        new_args = map(lambda a: str(a).lower() if isinstance(a, bool) else a, args)
        new_args = map(lambda a: "V O I D" if a is None else a, new_args)
        return func(*new_args, **kwargs)

    return decorated


_bi_print_type = ArrowType([type_any], type_void)

bi_print = BuiltIn("print", _lower_str_bool(print, end=""), [_bi_print_type])
bi_println = BuiltIn("println", _lower_str_bool(print), [_bi_print_type])


def _read_file(file_name):
    with open(file_name) as file:
        return file.read()


bi_readAll = BuiltIn("readAll", _read_file, [ArrowType([type_string], type_string)])

# BOOLEAN STUFF

_bool_func_type = ArrowType([type_any, type_any], type_bool)
_bool_cmp_overloads = [
    ArrowType([type_int, type_int], type_bool),
    ArrowType([type_float, type_float], type_bool),
    ArrowType([type_int, type_float], type_bool),
    ArrowType([type_float, type_int], type_bool),
]

bi_and = BuiltIn("and", and_, [_bool_func_type])
bi_or = BuiltIn("or", or_, [_bool_func_type])
bi_eq = BuiltIn("==", eq, [_bool_func_type])
bi_ne = BuiltIn("!=", ne, [_bool_func_type])
bi_lt = BuiltIn("<", lt, _bool_cmp_overloads)
bi_le = BuiltIn("<=", le, _bool_cmp_overloads)
bi_gt = BuiltIn(">", gt, _bool_cmp_overloads)
bi_ge = BuiltIn(">=", ge, _bool_cmp_overloads)

bi_not = BuiltIn("not", not_, [ArrowType([type_bool], type_bool)])

# TYPE CONVERSION FUNCTIONS

bi_to_int = BuiltIn(
    "toInt",
    int,
    [
        ArrowType([type_float], type_int),
        ArrowType([type_string], type_int),
        ArrowType([type_int], type_int),
    ],
    is_op_code=True,
)

bi_to_float = BuiltIn(
    "toFloat",
    float,
    [
        ArrowType([type_float], type_float),
        ArrowType([type_int], type_float),
        ArrowType([type_string], type_float),
    ],
    is_op_code=True,
)

bi_to_string = BuiltIn(
    "toString",
    str,
    [
        ArrowType([type_int], type_string),
        ArrowType([type_float], type_string),
        ArrowType([type_string], type_string),
    ],
    is_op_code=True,
)


bi_new_list = BuiltIn("list", list, [ArrowType([], type_array)])
bi_len = BuiltIn("len", len, [ArrowType([type_array | type_string], type_int)])
bi_append = BuiltIn(
    "append",
    list.append,
    [
        ArrowType(
            [type_array, type_string | type_int | type_float | type_array], type_void
        )
    ],
)


def _del_item(array, idx):
    del array[idx]


bi_append = BuiltIn(
    "removeAt", _del_item, [ArrowType([type_array, type_int], type_void)]
)
bi_append = BuiltIn("copy", list.copy, [ArrowType([type_array], type_array)])
bi_sort = BuiltIn("sort", list.sort, [ArrowType([type_array], type_void)])
