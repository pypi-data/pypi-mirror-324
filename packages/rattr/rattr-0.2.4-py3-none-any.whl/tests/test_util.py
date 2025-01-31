from __future__ import annotations

import ast
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING
from unittest import mock

import pytest

from rattr import error
from rattr.analyser.exc import RattrResultsError
from rattr.analyser.util import (
    DictChanges,
    assignment_is_one_to_one,
    class_in_rhs,
    get_annotation,
    get_assignment_targets,
    get_attrname,
    get_basename,
    get_basename_fullname_pair,
    get_contained_walruses,
    get_decorator_name,
    get_dynamic_name,
    get_first_argument_name,
    get_fullname,
    get_function_body,
    get_function_form,
    get_namedtuple_attrs_from_call,
    get_xattr_obj_name_pair,
    has_affect,
    has_annotation,
    is_blacklisted_module,
    is_call_to,
    is_excluded_name,
    is_in_builtins,
    is_list_of_call_specs,
    is_list_of_names,
    is_method_on_cast,
    is_method_on_constant,
    is_method_on_primitive,
    is_name,
    is_pip_module,
    is_relative_import,
    is_set_of_names,
    is_starred_import,
    is_stdlib_module,
    lambda_in_rhs,
    namedtuple_in_rhs,
    parse_annotation,
    parse_rattr_results_from_annotation,
    unravel_names,
    validate_rattr_results,
    walrus_in_rhs,
)
from rattr.models.context import Context, compile_root_context
from rattr.models.symbol import Call, CallArguments, CallInterface, Class, Name

if TYPE_CHECKING:
    from collections.abc import Iterator

    from rattr.analyser.types import RattrResults
    from tests.shared import ArgumentsFn, StateFn


@pytest.fixture(autouse=True)
def __set_current_file(state: StateFn) -> Iterator[None]:
    with state(current_file=Path(__file__)):
        yield


class TestUtil:
    def test_get_basename_full_name_pair(self):
        # Simple nameable
        nameable = ast.parse("name").body[0].value
        expected = ("name", "name")
        assert get_basename_fullname_pair(nameable) == expected

        # Complex/nested strictly nameable
        nameable = ast.parse("a.b[0].attr").body[0].value
        expected = ("a", "a.b[].attr")

        assert get_basename_fullname_pair(nameable) == expected

    def test_get_basename_full_name_pair_safety(self):
        # Safety off
        nameable = ast.parse("(a, b)[0].attr").body[0].value

        with pytest.raises(error.RattrLiteralInNameable):
            get_basename_fullname_pair(nameable)

        # Safety on
        nameable = ast.parse("(a, b)[0].attr").body[0].value
        expected = ("@Tuple", "@Tuple[].attr")

        assert get_basename_fullname_pair(nameable, safe=True) == expected

    def test_get_basename_full_name_pair_coverage(self, constant: str):
        # Name
        nameable = ast.parse("ast_name").body[0].value
        expected = ("ast_name", "ast_name")
        assert get_basename_fullname_pair(nameable) == expected

        # Attribute
        nameable = ast.parse("ast_name.attr").body[0].value
        expected = ("ast_name", "ast_name.attr")
        assert get_basename_fullname_pair(nameable) == expected

        # Subscript
        nameable = ast.parse("ast_name[0]").body[0].value
        expected = ("ast_name", "ast_name[]")
        assert get_basename_fullname_pair(nameable) == expected

        # Call
        nameable = ast.parse("ast_name(arg_one, arg_two)").body[0].value
        expected = ("ast_name", "ast_name()")
        assert get_basename_fullname_pair(nameable) == expected

        # Starred
        nameable = ast.parse("*ast_name").body[0].value
        expected = ("ast_name", "*ast_name")
        assert get_basename_fullname_pair(nameable) == expected

        # UnaryOp
        nameable = ast.parse("(-a)").body[0].value
        expected = ("@UnaryOp", "@UnaryOp")
        with pytest.raises(error.RattrUnaryOpInNameable):
            get_basename_fullname_pair(nameable)
        assert get_basename_fullname_pair(nameable, safe=True) == expected

        # BinOp
        nameable = ast.parse("(a + b)").body[0].value
        expected = ("@BinOp", "@BinOp")
        with pytest.raises(error.RattrBinOpInNameable):
            get_basename_fullname_pair(nameable)
        assert get_basename_fullname_pair(nameable, safe=True) == expected

        # NameConstant
        nameable = ast.parse("True").body[0].value
        expected = (constant, constant)
        with pytest.raises(error.RattrConstantInNameable):
            get_basename_fullname_pair(nameable)
        assert get_basename_fullname_pair(nameable, safe=True) == expected

        # Literal
        nameable = ast.parse("(1).to_bytes()").body[0].value
        expected = (constant, f"{constant}.to_bytes()")
        with pytest.raises(error.RattrConstantInNameable):
            get_basename_fullname_pair(nameable)
        assert get_basename_fullname_pair(nameable, safe=True) == expected

        # Comprehension
        nameable = ast.parse("[a for a in list_of_as][0]").body[0].value
        expected = ("@ListComp", "@ListComp[]")
        with pytest.raises(error.RattrComprehensionInNameable):
            get_basename_fullname_pair(nameable)
        assert get_basename_fullname_pair(nameable, safe=True) == expected

    def test_get_basename_full_name_pair_regression(self, parse):
        # Nameable is a getattr, etc call #1
        nameable = ast.parse("getattr(getattr(a, 'inner'), 'outer')").body[0].value
        expected = ("getattr", "a.inner.outer")
        assert get_basename_fullname_pair(nameable) == expected

        # Nameable is a getattr, etc call #2
        nameable = ast.parse("getattr(a, 'inner').outer").body[0].value
        expected = ("getattr", "a.inner.outer")
        assert get_basename_fullname_pair(nameable) == expected

    def test_get_basename(self):
        # Simple strictly nameable
        nameable = ast.parse("name").body[0].value
        expected = "name"

        assert get_basename(nameable) == expected

        # Complex strictly nameable
        nameable = ast.parse("a.b[0].attr").body[0].value
        expected = "a"

        assert get_basename(nameable) == expected

        # Complex strictly nameable
        nameable = ast.parse("(a, b)[0].attr").body[0].value
        expected = "@Tuple"

        with pytest.raises(error.RattrLiteralInNameable):
            assert get_basename(nameable) == expected

    def test_unravel_names(self):
        # Simple
        ravelled_names = ast.parse("a, b = 1, 2").body[0].targets[0]
        expected = ["a", "b"]

        assert list(unravel_names(ravelled_names)) == expected

        # Simple
        ravelled_names = ast.parse("(a, b), c = [1, 2], 3").body[0].targets[0]
        expected = ["a", "b", "c"]

        assert list(unravel_names(ravelled_names)) == expected

        # Complex
        ravelled_names = ast.parse("(a, b), c, d.e = 1, 2, 3, 4").body[0].targets[0]
        expected = ["a", "b", "c", "d"]

        assert list(unravel_names(ravelled_names)) == expected

    def test_unravel_names_by_fullname(self):
        # Simple
        ravelled_names = ast.parse("a, b = 1, 2").body[0].targets[0]
        expected = ["a", "b"]

        assert list(unravel_names(ravelled_names, get_name=get_fullname)) == expected

        # Simple
        ravelled_names = ast.parse("(a, b), c = [1, 2], 3").body[0].targets[0]
        expected = ["a", "b", "c"]

        assert list(unravel_names(ravelled_names, get_name=get_fullname)) == expected

        # Complex
        ravelled_names = ast.parse("(a, b), c, d.e = 1, 2, 3, 4").body[0].targets[0]
        expected = ["a", "b", "c", "d.e"]

        assert list(unravel_names(ravelled_names, get_name=get_fullname)) == expected

    def test_is_call_to(self):
        not_a_call = ast.parse("def f(): pass").body[0]
        with pytest.raises(TypeError):
            is_call_to("blah", not_a_call)

        call = ast.parse("fn(a, b, c)").body[0].value
        assert is_call_to("different_func", call) is False
        assert is_call_to("fn", call) is True

        call = ast.parse("outer(inner(a, b, c))").body[0].value
        assert is_call_to("different_func", call) is False
        assert is_call_to("inner", call) is False
        assert is_call_to("outer", call) is True

        call = ast.parse("obj.method(a, b, c)").body[0].value
        assert is_call_to("different_func", call) is False
        assert is_call_to("object.method", call) is False

        call = ast.parse("fn(a, b, c).on_result()").body[0].value
        assert is_call_to("different_func", call) is False
        assert is_call_to("on_result", call) is False
        assert is_call_to("fn", call) is False
        assert is_call_to("fn", call.func.value) is True

    def test_has_affect(self, builtins):
        _has_affect = {
            "hasattr",
            "getattr",
            "setattr",
            "delattr",
        }

        for b in builtins.difference(_has_affect):
            assert not has_affect(b)

        for b in _has_affect:
            assert has_affect(b)

        with pytest.raises(ValueError):
            has_affect("not_a_builtin")

    def test_get_xattr_obj_name_pair(self, capfd):
        # Simple
        xattr = ast.parse("getattr(a, 'b')").body[0].value
        expected = ("a", "b")

        assert get_xattr_obj_name_pair("getattr", xattr) == expected

        # Nested
        xattr = ast.parse("getattr(getattr(a, 'b'), 'c')").body[0].value
        expected = ("a.b", "c")

        assert get_xattr_obj_name_pair("getattr", xattr) == expected

        # Complex
        xattr = ast.parse("getattr(getattr(a.b[0], 'c'), 'd')").body[0].value
        expected = ("a.b[].c", "d")

        assert get_xattr_obj_name_pair("getattr", xattr) == expected

        # Warn: non string-literal name
        xattr = ast.parse("getattr(a, some_string_variable)").body[0].value
        expected = ("a", "<some_string_variable>")

        assert get_xattr_obj_name_pair("getattr", xattr, True) == expected

        _, stderr = capfd.readouterr()
        assert "error" in stderr
        assert "expects name to be a string literal" in stderr

        # Illegal: mixed nested
        xattr = ast.parse("getattr(hasattr(a, 'b'), 'c')").body[0].value

        with mock.patch("sys.exit") as _exit:
            get_xattr_obj_name_pair("getattr", xattr, True)

        _, stderr = capfd.readouterr()

        assert "object must be a name or a call to 'getattr'" in stderr
        assert _exit.call_count == 1

        # Illegal: expression
        xattr = ast.parse("getattr(a or b, 'c')").body[0].value

        with pytest.raises(TypeError):
            get_xattr_obj_name_pair("getattr", xattr)

        # Illegal: exprssion nested
        xattr = ast.parse("getattr(getattr(a1 or a2, 'b'), 'c')").body[0].value

        with pytest.raises(TypeError):
            get_xattr_obj_name_pair("getattr", xattr)

    def test_get_decorator_name(self, parse):
        # Works with ast.Name decorator
        _ast = parse(
            """
            @name_decorator
            def fn(bob: YourUncle):
                return isinstance(bob, YourUncle)
            """
        )
        decorator = _ast.body[0].decorator_list[0]
        assert get_decorator_name(decorator) == "name_decorator"

        # Works with ast.Call decorator
        _ast = parse(
            """
            @called_decorator("some decorator arg")
            @called_decorator_no_args()
            def fn(bob: YourUncle):
                return isinstance(bob, YourUncle)
            """
        )
        decorator_one = _ast.body[0].decorator_list[0]
        decorator_two = _ast.body[0].decorator_list[1]
        assert get_decorator_name(decorator_one) == "called_decorator"
        assert get_decorator_name(decorator_two) == "called_decorator_no_args"

        # Error otherwise
        decorator = parse(
            """
            x = 4       # <result>.body[0] will be ast.Assign
            """
        ).body[0]
        with pytest.raises(TypeError):
            get_decorator_name(decorator)

    def test_get_first_argument_name(self, parse):
        _ast = parse(
            """
            def func_call_no_args():
                pass
            def func_call_one_arg(arg):
                pass
            def func_call_many_args(arg_one, arg_two, arg_three):
                pass
            """
        )

        # Return empty string when there are no args
        args = _ast.body[0].args
        assert get_first_argument_name(args) == ""

        # Return first arg of one args
        args = _ast.body[1].args
        assert get_first_argument_name(args) == "arg"

        # Return first arg of many args
        args = _ast.body[2].args
        assert get_first_argument_name(args) == "arg_one"

    def test_has_annotation(self, parse):
        _ast = parse(
            """
            def no_decorators(a, b, c):
                pass

            @decorator
            def single_decorated(a, b, c):
                pass

            @decorator_one
            @decorator_two
            def multi_decorated(a, b, c):
                pass

            @called_decorator()
            def call_decorated(a, b, c):
                pass

            @nested.attribute.decorator
            def attribute_decorated(a, b, c):
                pass

            @nested.attribute.call.decorator()
            def call_attribute_decorated(a, b, c):
                pass
            """
        )

        # No decorators
        fn_def = _ast.body[0]
        assert not has_annotation("absent", fn_def)

        # Decorated
        fn_def = _ast.body[1]
        assert not has_annotation("absent", fn_def)
        assert has_annotation("decorator", fn_def)

        # Multi
        fn_def = _ast.body[2]
        assert not has_annotation("absent", fn_def)
        assert has_annotation("decorator_one", fn_def)
        assert has_annotation("decorator_two", fn_def)

        # Called
        fn_def = _ast.body[3]
        assert not has_annotation("absent", fn_def)
        assert has_annotation("called_decorator", fn_def)

        # Attribute
        fn_def = _ast.body[4]
        assert not has_annotation("absent", fn_def)
        assert has_annotation("decorator", fn_def)

        # Called attribute
        fn_def = _ast.body[5]
        assert not has_annotation("absent", fn_def)
        assert has_annotation("decorator", fn_def)

    def test_get_annotation(self, parse, capfd):
        _ast = parse(
            """
            def no_decorators(a, b, c):
                pass

            @present
            @present
            def duplicated(a, b, c):
                pass

            @present
            def normal(a, b, c):
                pass

            @present()
            def called(a, b, c):
                pass

            @present("value", "another value")
            def called_with_args(a, b, c):
                pass

            @a.b.c.present("value", "another value")
            def called_attr_with_args(a, b, c):
                pass
            """
        )

        # No decorators
        fn_def = _ast.body[0]
        assert get_annotation("absent", fn_def) is None

        # Duplicated
        fn_def = _ast.body[1]
        assert get_annotation("absent", fn_def) is None

        _, stderr = capfd.readouterr()  # clear stderr buffer
        with mock.patch("sys.exit") as _exit:
            get_annotation("present", fn_def)
        _, stderr = capfd.readouterr()

        assert "duplicated annotation" in stderr
        assert _exit.call_count == 1

        # Normal
        fn_def = _ast.body[2]
        assert get_annotation("absent", fn_def) is None

        expected = "Name(id='present', ctx=Load())"
        assert ast.dump(get_annotation("present", fn_def)) == expected

        # Called
        fn_def = _ast.body[3]
        assert get_annotation("absent", fn_def) is None

        expected = "Call(func=Name(id='present', ctx=Load()), " "args=[], keywords=[])"
        assert ast.dump(get_annotation("present", fn_def)) == expected

        # Called w/ args
        fn_def = _ast.body[4]
        assert get_annotation("absent", fn_def) is None

        if sys.version_info.major == 3 and sys.version_info.minor == 7:
            expected = (
                "Call(func=Name(id='present', ctx=Load()), "
                "args=[Str(s='value'), Str(s='another value')], keywords=[])"
            )
        elif sys.version_info.major == 3 and sys.version_info.minor == 8:
            expected = (
                "Call(func=Name(id='present', ctx=Load()), "
                "args=[Constant(value='value', kind=None), "
                "Constant(value='another value', kind=None)], keywords=[])"
            )
        else:
            expected = (
                "Call(func=Name(id='present', ctx=Load()), "
                "args=[Constant(value='value'), "
                "Constant(value='another value')], keywords=[])"
            )
        assert ast.dump(get_annotation("present", fn_def)) == expected

        # Called Attr w/ args
        fn_def = _ast.body[5]
        assert get_annotation("absent", fn_def) is None

        if sys.version_info.major == 3 and sys.version_info.minor == 7:
            expected = (
                "Call(func=Attribute(value=Attribute(value=Attribute(value="
                "Name(id='a', ctx=Load()), attr='b', ctx=Load()), attr='c', "
                "ctx=Load()), attr='present', ctx=Load()), "
                "args=[Str(s='value'), Str(s='another value')], keywords=[])"
            )
        elif sys.version_info.major == 3 and sys.version_info.minor == 8:
            expected = (
                "Call(func=Attribute(value=Attribute(value=Attribute(value="
                "Name(id='a', ctx=Load()), attr='b', ctx=Load()), attr='c', "
                "ctx=Load()), attr='present', ctx=Load()), "
                "args=[Constant(value='value', kind=None), "
                "Constant(value='another value', kind=None)], keywords=[])"
            )
        else:
            expected = (
                "Call(func=Attribute(value=Attribute(value=Attribute(value="
                "Name(id='a', ctx=Load()), attr='b', ctx=Load()), attr='c', "
                "ctx=Load()), attr='present', ctx=Load()), "
                "args=[Constant(value='value'), "
                "Constant(value='another value')], keywords=[])"
            )
        assert ast.dump(get_annotation("present", fn_def)) == expected

    def test_parse_annotation(self, parse):
        _ast = parse(
            """
            @name
            def fn(a, b, c):
                pass

            @call()
            def fn(a, b, c):
                pass

            @call("simple and evaluateable")
            def fn(a, b, c):
                pass

            @call("arg", kwarg="value")
            def fn(a, b, c):
                pass

            @call([1, 2, 3], gets={"more", "complex", "test"})
            def fn(a, b, c):
                pass

            @call(d={"a": 1, "b": 2})
            def fn(a, b, c):
                pass

            # Illegals

            @call(jeremy, james, hammond, show=TopGear)
            def fn(a, b, c):
                pass

            @call([1, 2, illegal])
            def fn(a, b, c):
                pass
            """
        )

        the_empty_result = ([], {})

        # No value, name
        fn_def = _ast.body[0]
        assert parse_annotation("absent", fn_def) == the_empty_result

        # No value, call
        fn_def = _ast.body[1]
        assert parse_annotation("absent", fn_def) == the_empty_result
        assert parse_annotation("call", fn_def) == the_empty_result

        # Simple
        fn_def = _ast.body[2]
        assert parse_annotation("absent", fn_def) == the_empty_result
        assert parse_annotation("call", fn_def) == (
            ["simple and evaluateable"],
            {},
        )

        # Keyword
        fn_def = _ast.body[3]
        assert parse_annotation("absent", fn_def) == the_empty_result
        assert parse_annotation("call", fn_def) == (
            ["arg"],
            {"kwarg": "value"},
        )

        # Complex
        fn_def = _ast.body[4]
        assert parse_annotation("absent", fn_def) == the_empty_result
        assert parse_annotation("call", fn_def) == (
            [
                [1, 2, 3],
            ],
            {"gets": set(["more", "complex", "test"])},
        )

        # Dict
        fn_def = _ast.body[5]
        assert parse_annotation("absent", fn_def) == the_empty_result
        assert parse_annotation("call", fn_def) == (
            [],
            {
                "d": {"a": 1, "b": 2},
            },
        )

        # Illegal: non-compile time evaluated
        fn_def = _ast.body[6]
        assert parse_annotation("absent", fn_def) == the_empty_result

        with mock.patch("sys.exit") as _exit:
            parse_annotation("call", fn_def)
        assert _exit.call_count == 4  # exit called once per argument

        # Illegal: nested non-compile time evaluated
        fn_def = _ast.body[7]
        assert parse_annotation("absent", fn_def) == the_empty_result

        with mock.patch("sys.exit") as _exit:
            parse_annotation("call", fn_def)
        assert _exit.call_count == 1

    def test_is_name(self):
        assert is_name("var")
        assert is_name("var.attr")

        assert is_name("*var.attr")
        assert is_name("*var.attr")

        assert is_name("*var.mth().res[].attr")
        assert is_name("a_long_var.with_underscores.in_it")
        assert is_name("var_with_2_numers_in_it_1")
        assert is_name("_protected")
        assert is_name("__private")
        assert is_name("ClassName")

        assert is_name("@BinOp")
        assert is_name("@BinOp.attr")

        assert not is_name(1234)
        assert not is_name("1234")
        assert not is_name(".var")
        assert not is_name("1_var")

        assert not is_name("")

    @pytest.mark.parametrize(
        "input, expected",
        [
            # the empty set
            (set(), True),
            # expected usage
            ({"a", "b", "c"}, True),
            ({"var.a", "var_b", "*c"}, True),
            # other empty iterable
            ([], False),
            ({}, False),
            # iterable, but wrongly typed
            ([1, 2, 3, 4], False),
            (["a", "b", "c"], False),
            # set with non-names
            ({"a", "b", "1111"}, False),
            # not an iterable
            (1234, False),
        ],
    )
    def test_is_set_of_names(self, input: object, expected: bool):
        assert is_set_of_names(input) == expected

    @pytest.mark.parametrize(
        "input, expected",
        [
            # the empty list
            ([], True),
            # expected usage
            (["a", "b", "c"], True),
            (["var.a", "var_b", "*c"], True),
            # other empty iterable
            (set(), False),
            ({}, False),
            # iterable, but wrongly typed
            ([1, 2, 3, 4], False),
            ({"a", "b", "c"}, False),
            # set with non-names
            ({"a", "b", "1111"}, False),
            # not an iterable
            (1234, False),
        ],
    )
    def test_is_list_of_names(self, input: object, expected: bool):
        assert is_list_of_names(input) == expected

    @pytest.mark.parametrize(
        "input, expected",
        testcases := [
            # typical call specs
            (([], {}), True),
            ((["a"], {}), True),
            ((["a", "b", "c"], {}), True),
            (([], {"a": "A"}), True),
            (([], {"a": "A", "b": "B"}), True),
            ((["a"], {"b": "B"}), True),
            ((["a", "b", "c"], {"d": "D"}), True),
            ((["a", "b", "c"], {"d": "D", "e": "E"}), True),
            # look like call specs, but wrongly typed
            ((["1", "b"], {"c": "d"}), False),
            ((["a", "b"], {"1": "d"}), False),
            ((["a", "b"], {"c": "1"}), False),
            (([111, "b"], {"c": "d"}), False),
            ((["a", "b"], {111: "d"}), False),
            ((["a", "b"], {"c": 111}), False),
            # entirely incorrect
            (1234, False),
            ("abcd", False),
            ((["a", "b"],), False),
        ],
        ids=[i for i, _ in enumerate(testcases)],
    )
    def test_is_call_spec(self, input: object, expected: bool):
        assert is_list_of_call_specs([("my_function", input)]) == expected

    @pytest.mark.parametrize(
        "inputs, expected",
        testcases := [
            # correct
            (
                [
                    ([], {}),
                    (["a"], {}),
                    ([], {"a": "A", "b": "B"}),
                    (["a", "b", "c"], {"d": "D", "e": "E"}),
                ],
                True,
            ),
            # mostly correct but one is wrong
            (
                [
                    ([], {}),
                    (["a"], {}),
                    ("NAUGHTY"),
                    (["a", "b", "c"], {"d": "D", "e": "E"}),
                ],
                False,
            ),
        ],
        ids=[i for i, _ in enumerate(testcases)],
    )
    def test_is_list_of_call_specs(self, inputs: object, expected: bool):
        assert is_list_of_call_specs([("func", input) for input in inputs]) == expected

    @pytest.mark.parametrize(
        "input, error",
        testcases := [
            (
                {
                    "gets": ["fail here"],
                    "sets": set(),
                    "dels": set(),
                    "calls": [],
                },
                "'rattr_results' expects a set[Identifier] for 'gets', where "
                "Identifier is a type alias for str",
            ),
            (
                {
                    "gets": set(),
                    "sets": set(),
                    "dels": set(),
                    "calls": [("fail here", ...)],
                },
                "'rattr_results' expects 'calls' to be a "
                "list[tuple[TargetName, tuple[list[PositionalArgumentName], "
                "dict[KeywordArgumentName, LocalIdentifier]]]]; "
                "where TargetName, PositionalArgumentName, KeywordArgumentName, and "
                "LocalIdentifier are type aliases for str",
            ),
        ],
        ids=[i for i, _ in enumerate(testcases)],
    )
    def test_validate_rattr_results(self, input: RattrResults, error: str):
        with pytest.raises(RattrResultsError, match=re.escape(error)):
            validate_rattr_results(input)

    def test_parse_rattr_results_from_annotation(self, parse):
        ast_module = parse(
            """
            @rattr_results(
                sets={"a"},
                gets={"b"},
                calls=[("c()", ([], {}))],
                dels={"d"}
            )
            def fn():
                pass

            @rattr_results(sets={"a", "b"})
            def fn():
                pass

            # Illegal

            @rattr_results("posarg")
            def fn():
                pass

            @rattr_results(invalid_key=1)
            def fn():
                pass

            @rattr_results(sets="invalid type")
            def fn():
                pass
            """
        )
        context = compile_root_context(ast_module)

        # Can set values
        fn_def = ast_module.body[0]
        expected = {
            "sets": {Name("a")},
            "gets": {Name("b")},
            "calls": {Call("c", args=CallArguments())},
            "dels": {Name("d")},
        }
        assert parse_rattr_results_from_annotation(fn_def, context=context) == expected

        # Defaults
        fn_def = ast_module.body[1]
        expected = {
            "sets": {Name("a"), Name("b")},
            "gets": set(),
            "calls": set(),
            "dels": set(),
        }
        assert parse_rattr_results_from_annotation(fn_def, context=context) == expected

        # Illegal: has pos arg
        fn_def = ast_module.body[2]
        with mock.patch("sys.exit") as _exit:
            parse_rattr_results_from_annotation(fn_def, context=context)
        assert _exit.call_count == 1

        # Illegal: has invalid key
        fn_def = ast_module.body[3]
        with mock.patch("sys.exit") as _exit:
            parse_rattr_results_from_annotation(fn_def, context=context)
        assert _exit.call_count == 1

        # Illegal: has invalid type
        fn_def = ast_module.body[4]
        with mock.patch("sys.exit") as _exit:
            parse_rattr_results_from_annotation(fn_def, context=context)
        assert _exit.call_count == 1

    def test_parse_rattr_results_from_annotation_complex(self, parse):
        _ast = parse(
            """
            @rattr_results(
                sets={"s.attr"},
                gets={"g.mth().res[]", "*g.attr"},
                dels={"del_me"}
            )
            def fn():
                pass

            @rattr_results(calls=[
                ("fn_a()", ([], {})),
                ("fn_b()", (["a", "b"], {})),
                ("fn_c()", (["a", ], {"c": "@Str"})),
            ])
            def fn():
                pass
            """
        )
        _ctx = compile_root_context(_ast)

        # Complex names
        fn_def = _ast.body[0]
        expected = {
            "sets": {Name("s.attr", "s")},
            "gets": {Name("g.mth().res[]", "g"), Name("*g.attr", "g")},
            "dels": {Name("del_me")},
            "calls": set(),
        }
        assert parse_rattr_results_from_annotation(fn_def, context=_ctx) == expected

        # Complex calls
        fn_def = _ast.body[1]
        expected = {
            "sets": set(),
            "gets": set(),
            "dels": set(),
            "calls": {
                Call(name="fn_a", args=CallArguments()),
                Call(name="fn_b", args=CallArguments(args=("a", "b"))),
                Call(
                    name="fn_c",
                    args=CallArguments(args=("a",), kwargs={"c": "@Str"}),
                ),
            },
        }
        assert parse_rattr_results_from_annotation(fn_def, context=_ctx) == expected

    def test_parse_rattr_results_from_annotation_follow_call(self, parse):
        _ast = parse(
            """
            def fn_a(a, b):
                return a + b

            @rattr_results(calls=[("fn_a()", (["alpha", "beta"], {}))])
            def ano():
                return "it is a lie, i do nothing!"
            """
        )
        _ctx = compile_root_context(_ast)

        target = _ctx.get("fn_a")
        fn_def = _ast.body[1]

        expected = {
            "sets": set(),
            "gets": set(),
            "dels": set(),
            "calls": {
                Call(
                    name="fn_a",
                    args=CallArguments(args=("alpha", "beta")),
                    target=target,
                ),
            },
        }

        assert parse_rattr_results_from_annotation(fn_def, context=_ctx) == expected

    def test_is_blacklisted_module(self, stdlib_modules):
        for m in stdlib_modules:
            assert not is_blacklisted_module(m)

        assert is_blacklisted_module("rattr")
        assert is_blacklisted_module("rattr.analyser.error")
        assert is_blacklisted_module("rattr.analyser.a.b.c.d.e")
        assert is_blacklisted_module("rattr.assertors.argument_names")

    def test_is_pip_module(self):
        # NOTE
        #   This is not the best test ever as it assumes that "flask" are
        #   installed and that "numpy" and "pandas" are not.
        #   However, as this test is testing code that if checking for that
        #   exact property I see no better way of testing it -- a mock would
        #   mock away the tested feature.
        assert is_pip_module("isort")
        assert is_pip_module("pytest")

        assert not is_pip_module("numpy")
        assert not is_pip_module("pandas")

        assert not is_pip_module("math")
        assert not is_pip_module("string")

    def test_is_stdlib_module(self, stdlib_modules):
        # Test against known stdlib modules
        for m in stdlib_modules:
            assert is_stdlib_module(m)

        # Test against submodules of stdlib modules
        assert is_stdlib_module("os.path")
        assert is_stdlib_module("os.path.join")
        assert is_stdlib_module("math.sin")
        assert is_stdlib_module("math.pi")

        # Technically false, but true to implementation
        assert is_stdlib_module("math.this.is.not.in.the.stdlib")

        # Test against pip/thirdparty modules
        assert not is_stdlib_module("flask")
        assert not is_stdlib_module("numpy")
        assert not is_stdlib_module("flake8")
        assert not is_stdlib_module("foobar")

        # Test against ratter/firstparty modules
        assert not is_stdlib_module("rattr")
        assert not is_stdlib_module("rattr.models.context")
        assert not is_stdlib_module("rattr.models.context._context")

        assert not is_stdlib_module("anything.dotted.anything")

    def test_is_in_builtins(self, builtins):
        for b in builtins:
            assert is_in_builtins(b)

        assert is_in_builtins("max")
        assert is_in_builtins("reversed")
        assert is_in_builtins("int")
        assert is_in_builtins("enumerate")

        assert not is_in_builtins("math.max")
        assert not is_in_builtins("foo.bar.baz")
        assert not is_in_builtins("foo_bar_baz")
        assert not is_in_builtins("")

    def test_get_function_body(self):
        # Lambda
        fn = ast.parse("fn = lambda: 2 + 3").body[0].value
        assert get_function_body(fn) == [fn.body]

        # Func
        fn = ast.parse("def fn(): pass").body[0]
        assert get_function_body(fn) == fn.body

        # Async
        fn = ast.parse("async def fn(): pass").body[0]
        assert get_function_body(fn) == fn.body

    def test_get_assignment_targets(self):
        # Assign, single
        assign = ast.parse("a = 1").body[0]
        assert get_assignment_targets(assign) == assign.targets

        # Assign, multi
        assign = ast.parse("a, b = 1, 2").body[0]
        assert get_assignment_targets(assign) == assign.targets

        # AnnAssign
        assign = ast.parse("a: int = 1").body[0]
        assert get_assignment_targets(assign) == [assign.target]

        # AugAssign
        assign = ast.parse("a += 1").body[0]
        assert get_assignment_targets(assign) == [assign.target]

    def test_get_assignment_targets_walrus(self):
        # Walrus in assign
        assign = ast.parse("a = (b := 1)").body[0]
        assert get_assignment_targets(assign) == assign.targets

        # Walrus
        assign = ast.parse("a = (b := 1)").body[0].value
        assert get_assignment_targets(assign) == [assign.target]

    def test_get_contained_walruses(self, stringify_nodes, walrus):
        walruses = get_contained_walruses(ast.parse("a = b").body[0])
        assert stringify_nodes(walruses) == []

        walruses = get_contained_walruses(ast.parse("a = (b := c)").body[0])
        assert stringify_nodes(walruses) == stringify_nodes([walrus("b := c")])

        walruses = get_contained_walruses(ast.parse("a = (x := y, m := n)").body[0])
        assert stringify_nodes(walruses) == stringify_nodes(walrus("x := y", "m := n"))

        walruses = get_contained_walruses(ast.parse("a = (b, x := y)").body[0])
        assert stringify_nodes(walruses) == stringify_nodes([walrus("x := y")])

        # Does not nest (node visitor should recurse)
        walruses = get_contained_walruses(ast.parse("a = (b, (c, x := y))").body[0])
        assert stringify_nodes(walruses) == []

    def test_assignment_is_one_to_one(self):
        is_one_to_one = {
            "x = 1",
            "x: int = 1",
            "x += 1",
        }
        is_not_one_to_one = {
            "x, y = z",
            "x, y = a, b",
            "x = y, z",
            "x += y, z",
        }

        for case in is_one_to_one:
            assert assignment_is_one_to_one(ast.parse(case).body[0])

        for case in is_not_one_to_one:
            assert not assignment_is_one_to_one(ast.parse(case).body[0])

    def test_lambda_in_rhs(self):
        # Single
        assign = ast.parse("a = lambda: 1").body[0]
        assert lambda_in_rhs(assign)

        # Multi
        assign = ast.parse("a = 1, lambda: 1").body[0]
        assert lambda_in_rhs(assign)

        # AnnAssign
        assign = ast.parse("a: SomeType = lambda: 1").body[0]
        assert lambda_in_rhs(assign)

        # AugAssign
        assign = ast.parse("a += lambda: 1").body[0]
        assert lambda_in_rhs(assign)

        # Single, not
        assign = ast.parse("a = 1").body[0]
        assert not lambda_in_rhs(assign)

        # Multi, not
        assign = ast.parse("a = 1, 2").body[0]
        assert not lambda_in_rhs(assign)

        # AnnAssign, not
        assign = ast.parse("a: SomeType = SomeType()").body[0]
        assert not lambda_in_rhs(assign)

        # AugAssign, not
        assign = ast.parse("a += 1").body[0]
        assert not lambda_in_rhs(assign)

    def test_walrus_in_rhs(self):
        # Single
        assign = ast.parse("a = (b := c)").body[0]
        assert walrus_in_rhs(assign)

        # Multi
        assign = ast.parse("a = 1, (b := c)").body[0]
        assert walrus_in_rhs(assign)

        # AnnAssign
        assign = ast.parse("a: SomeType = (b := c)").body[0]
        assert walrus_in_rhs(assign)

        # AugAssign
        assign = ast.parse("a += (b := c)").body[0]
        assert walrus_in_rhs(assign)

        # Single, not
        assign = ast.parse("a = 1").body[0]
        assert not walrus_in_rhs(assign)

        # Multi, not
        assign = ast.parse("a = 1, 2").body[0]
        assert not walrus_in_rhs(assign)

        # AnnAssign, not
        assign = ast.parse("a: SomeType = SomeType()").body[0]
        assert not walrus_in_rhs(assign)

        # AugAssign, not
        assign = ast.parse("a += 1").body[0]
        assert not walrus_in_rhs(assign)

    def test_class_in_rhs(self):
        _ctx = Context(None)
        _ctx.add(Name("x"))
        _ctx.add(Name("LooksLikeAClass"))
        _ctx.add(Class("MyClass", interface=CallInterface()))

        # No class in RHS
        assign = ast.parse("a = x").body[0]
        assert not class_in_rhs(assign, _ctx)

        assign = ast.parse("a = LooksLikeAClass()").body[0]
        assert not class_in_rhs(assign, _ctx)

        assign = ast.parse("a, b = x, LooksLikeAClass()").body[0]
        assert not class_in_rhs(assign, _ctx)

        # Class in RHS
        assign = ast.parse("a = MyClass()").body[0]
        assert class_in_rhs(assign, _ctx)

        assign = ast.parse("a, b = x, MyClass()").body[0]
        assert class_in_rhs(assign, _ctx)

    def test_is_starred_import(self):
        # Not starred: normal import
        _import = ast.parse("import math").body[0]
        assert not is_starred_import(_import)

        # Not starred: normal import
        _import = ast.parse("from math import pi").body[0]
        assert not is_starred_import(_import)

        # Not starred: normal import
        _import = ast.parse("from math import cos, sin, tan").body[0]
        assert not is_starred_import(_import)

        # Starred
        _import = ast.parse("from math import *").body[0]
        assert is_starred_import(_import)

        # Starred, relative
        _import = ast.parse("from .here.module import *").body[0]
        assert is_starred_import(_import)

    def test_is_relative_import(self):
        # Not starred: normal import
        _import = ast.parse("import math").body[0]
        assert not is_relative_import(_import)

        # Not starred: normal import
        _import = ast.parse("from math import pi").body[0]
        assert not is_relative_import(_import)

        # Not starred: normal import
        _import = ast.parse("from math import cos, sin, tan").body[0]
        assert not is_relative_import(_import)

        # Starred
        _import = ast.parse("from math import *").body[0]
        assert not is_relative_import(_import)

        # Starred, relative
        _import = ast.parse("from .here.module import *").body[0]
        assert is_relative_import(_import)

    def test_get_function_form(self):
        # No args
        fn = ast.parse("def fn(): pass").body[0]
        assert get_function_form(fn) == "'fn()'"

        # Positional arguments
        fn = ast.parse("def fn(a, b, c): pass").body[0]
        assert get_function_form(fn) == "'fn(a, b, c)'"

        # Complex
        fn = ast.parse("def fn(a, b, c=None, *args, **kwargs): pass").body[0]
        assert get_function_form(fn) == "'fn(a, b, c, *args, **kwargs)'"

    def test_is_excluded_name(self, arguments: ArgumentsFn):
        assert not is_excluded_name("sin")
        assert not is_excluded_name("_hidden_func")

        with arguments(_excluded_names={"sin"}):
            assert is_excluded_name("sin")
            assert not is_excluded_name("_hidden_func")

        with arguments(_excluded_names={"_.*"}):
            assert not is_excluded_name("sin")
            assert is_excluded_name("_hidden_func")

    def test_is_method_on_constant(self, constant: str):
        assert not is_method_on_constant("some_var")
        assert not is_method_on_constant("some_var.methodd")
        assert not is_method_on_constant("some_var[0].method")

        assert not is_method_on_constant(constant)
        assert is_method_on_constant(constant + ".methodd")
        assert is_method_on_constant(constant + ".[0].method")

    def test_is_method_on_cast(self):
        assert not is_method_on_cast("some_var")
        assert not is_method_on_cast("func")
        assert not is_method_on_cast("func")
        assert not is_method_on_cast("func().on_result")

        assert is_method_on_cast("set().union")
        assert is_method_on_cast("list().append")

    def test_is_method_on_primitive(self, constant: str):
        assert not is_method_on_primitive(constant)
        assert not is_method_on_primitive("some_var")
        assert not is_method_on_primitive("func")
        assert not is_method_on_primitive("func")
        assert not is_method_on_primitive("func().on_result")

        assert is_method_on_primitive("set().union")
        assert is_method_on_primitive("list().append")
        assert is_method_on_primitive(constant + ".methodd")
        assert is_method_on_primitive(constant + ".[0].method")

    def test_get_dynamic_name(self):
        call = ast.parse("getattr(object, 'attribute')").body[0].value
        result = get_dynamic_name("getattr", call, "{first}.{second}")
        expected = Name("object.attribute", "object")

        assert result == expected

        call = ast.parse("getattr(getattr(a, 'b'), 'c')").body[0].value
        result = get_dynamic_name("getattr", call, "{first}.{second}")
        expected = Name("a.b.c", "a")

        assert result == expected

        call = ast.parse("get_sub_attr(obj, 'attr')").body[0].value
        result = get_dynamic_name("get_sub_attr", call, "{first}.sub.{second}")
        expected = Name("obj.sub.attr", "obj")

        assert result == expected

        call = ast.parse("get_sub_attr(get_sub_attr(o, 'in'), 'out')").body[0].value
        result = get_dynamic_name("get_sub_attr", call, "{first}.mid.{second}")
        expected = Name("o.in.mid.out", "o")

        assert result == expected

        call = ast.parse("get_sub(obj, ...)").body[0].value
        result = get_dynamic_name("get_sub", call, "{first}.sub")
        expected = Name("obj.sub", "obj")

        assert result == expected

        call = ast.parse("getattr(another_function(a, 'b'), 'c')").body[0].value
        with mock.patch("sys.exit") as _exit:
            result = get_dynamic_name("getattr", call, "{first}.{second}")

        assert _exit.call_count == 1

    def test_get_attrname(self):
        attr = ast.parse("object.attribute").body[0].value
        assert get_attrname(attr) == "attribute"

        attr = ast.parse("a.b.c.d").body[0].value
        assert get_attrname(attr) == "d"

        attr = ast.parse("just_some_var").body[0].value
        assert get_attrname(attr) == "just_some_var"

        attr = ast.parse("a(arg, arg, arg).b[0].c").body[0].value
        assert get_attrname(attr) == "c"

        attr = ast.parse("def fn(): pass").body[0]
        with pytest.raises(TypeError):
            assert get_attrname(attr)

    def test_dict_changes(self):
        ir = {"a": 1, "b": 2, "c": 3, "d": 4}

        # No changes
        with DictChanges(ir) as diff:
            pass

        assert not diff.added
        assert not diff.removed

        # Changes
        with DictChanges(ir) as diff:
            ir["x"] = 99
            del ir["a"]
            del ir["b"]

        assert diff.added == {"x"}
        assert diff.removed == {"a", "b"}


class TestNamedTupleInRhs:
    def test_namedtuple_in_rhs(self):
        ast_ = ast.parse("point = namedtuple('point', ['x', 'y'])")
        assignment = ast_.body[0]
        assert namedtuple_in_rhs(assignment)

    def test_user_namedtuple_in_rhs(self):
        ast_ = ast.parse("point = user_extended.namedtuple('point', ['x', 'y'])")
        assignment = ast_.body[0]
        assert namedtuple_in_rhs(assignment)

    def test_namedtuple_not_in_rhs(self):
        ast_ = ast.parse("point = noomedtoople('point', ['x', 'y'])")
        assignment = ast_.body[0]
        assert not namedtuple_in_rhs(assignment)


class TestGetNamedTupleAttrsFromCall:
    def test_rhs_is_not_call(self):
        ast_ = ast.parse("point = 'not_a_call'")
        assignment = ast_.body[0]

        with pytest.raises(TypeError):
            get_namedtuple_attrs_from_call(assignment)

    def test_too_few_arguments(self):
        ast_ = ast.parse("point = namedtuple('point')")
        assignment = ast_.body[0]

        with pytest.raises(SystemExit):
            get_namedtuple_attrs_from_call(assignment)

    def test_too_many_arguments(self):
        ast_ = ast.parse("point = namedtuple('point', 'x', 'y')")
        assignment = ast_.body[0]

        with pytest.raises(SystemExit):
            get_namedtuple_attrs_from_call(assignment)

    def test_second_argument_is_not_a_list(self):
        ast_ = ast.parse("point = namedtuple('point', ('x', 'y'))")
        assignment = ast_.body[0]

        with pytest.raises(SystemExit):
            get_namedtuple_attrs_from_call(assignment)

    def test_second_argument_is_not_a_list_of_string_literals(self):
        # Non-string literal
        ast_ = ast.parse("point = namedtuple('point', ['x', 123])")
        assignment = ast_.body[0]

        with pytest.raises(SystemExit):
            get_namedtuple_attrs_from_call(assignment)

        # Non-literal
        ast_ = ast.parse("point = namedtuple('point', ['x', some_variable])")
        assignment = ast_.body[0]

        with pytest.raises(SystemExit):
            get_namedtuple_attrs_from_call(assignment)

    def test_attrs_from_named_tuple_call_the_empty_list(self):
        # Non-string literal
        ast_ = ast.parse("point = namedtuple('point', [])")
        assignment = ast_.body[0]

        assert get_namedtuple_attrs_from_call(assignment) == ["self"]

    def test_attrs_from_named_tuple_call_one_item(self):
        # Non-string literal
        ast_ = ast.parse("point = namedtuple('point', ['x'])")
        assignment = ast_.body[0]

        assert get_namedtuple_attrs_from_call(assignment) == ["self", "x"]

    def test_attrs_from_named_tuple_call_two_items(self):
        # Non-string literal
        ast_ = ast.parse("point = namedtuple('point', ['x', 'y'])")
        assignment = ast_.body[0]

        assert get_namedtuple_attrs_from_call(assignment) == ["self", "x", "y"]

    def test_attrs_from_named_tuple_call_multiple_items(self):
        # Non-string literal
        ast_ = ast.parse("vec4 = vec4('vector', ['a', 'b', 'c', 'd'])")
        assignment = ast_.body[0]

        expected = ["self", "a", "b", "c", "d"]
        assert get_namedtuple_attrs_from_call(assignment) == expected
