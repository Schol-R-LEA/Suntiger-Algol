#!/usr/bin/env python
#-*- coding: iso-8859-1 -*-
################################################################################
#
# Parameter/return value type checking for Python 3000 using function annotations.
#
# (c) 2008, Dmitry Dvoinikov <dmitry@targeted.org>
# Distributed under BSD license.
#
# Samples:
#
# from typecheck import *
#
# @typecheck
# def foo(i: int, x = None, s: str = "default") -> bool:
#     ...
#
# @typecheck
# def foo(*args, k1: int, k2: str = "default", k3 = None) -> nothing:
#     ...
#
# @typecheck
# def foo(ostream: with_attr("write", "flush"), f: optional(callable) = None):
#     ...
#
# divisible_by_three = lambda x: x % 3 == 0
# @typecheck
# def foo(i: by_regex("^[0-9]+$")) -> divisible_by_three:
#     ...
#
# @typecheck
# def reverse_2_tuple(t: (str, bytes)) -> (bytes, str):
#     ...
#
# @typecheck
# def reverse_3_list(t: [int, float, bool]) -> [bool, float, int]:
#     ...
#
# @typecheck
# def extract_from_dict(d: dict_of(int, str), k: tuple_of(int)) -> list_of(str):
#     ...
#
# @typecheck
# def set_level(level: one_of(1, 2, 3)):
#     ...
#
# The (6 times longer) source code with self-tests is available from:
# http://www.targeted.org/python/recipes/typecheck3000.py
#
################################################################################

__all__ = [ "typecheck", "optional", "with_attr", "by_regex", "callable",
            "anything", "nothing", "tuple_of", "list_of", "dict_of", "one_of",

            "TypeCheckError", "TypeCheckSpecificationError",
            "InputParameterError", "ReturnValueError" ]

################################################################################

import inspect
import functools
import re

callable = lambda x: hasattr(x, "__call__")
anything = lambda x: True
nothing = lambda x: x is None

################################################################################

class TypeCheckError(Exception): pass
class TypeCheckSpecificationError(Exception): pass
class InputParameterError(TypeCheckError): pass
class ReturnValueError(TypeCheckError): pass

################################################################################

class Checker(object):

    class NoValue:
        def __str__(self):
            return "<no value>"
    no_value = NoValue()

    _registered = []

    @classmethod
    def register(cls, predicate, factory):
        cls._registered.append((predicate, factory))

    @classmethod
    def create(cls, value):
        if isinstance(value, cls):
            return value
        for predicate, factory in cls._registered:
            if predicate(value):
                return factory(value)
        else:
            return None

    def __call__(self, value):
        return self.check(value)

################################################################################

class TypeChecker(Checker):

    def __init__(self, cls):
        self._cls = cls

    def check(self, value):
        return isinstance(value, self._cls)

Checker.register(inspect.isclass, TypeChecker)

################################################################################

iterable = lambda x: hasattr(x, "__iter__")

class IterableChecker(Checker):

    def __init__(self, cont):
        self._cls = type(cont)
        self._chks = tuple(Checker.create(x) for x in iter(cont))

    def check(self, value):
        if not iterable(value):
            return False
        vals = tuple(iter(value))
        return isinstance(value, self._cls) and len(self._chks) == len(vals) and \
               functools.reduce(lambda r, c_v: r and c_v[0].check(c_v[1]),
                                zip(self._chks, vals), True)

Checker.register(iterable, IterableChecker)

################################################################################

class CallableChecker(Checker):

    def __init__(self, func):
        self._func = func

    def check(self, value):
        return bool(self._func(value))

Checker.register(callable, CallableChecker)

################################################################################

class OptionalChecker(Checker):

    def __init__(self, check):
        self._check = Checker.create(check)

    def check(self, value):
        return value is Checker.no_value or value is None or self._check.check(value)

optional = OptionalChecker

################################################################################

class WithAttrChecker(Checker):

    def __init__(self, *attrs):
        self._attrs = attrs

    def check(self, value):
        for attr in self._attrs:
            if not hasattr(value, attr):
                return False
        else:
            return True

with_attr = WithAttrChecker

################################################################################

class ByRegexChecker(Checker):

    def __init__(self, regex):
        self._regex = re.compile(regex)

    def check(self, value):
        return isinstance(value, str) and self._regex.match(value) is not None

by_regex = ByRegexChecker

################################################################################

class TupleOfChecker(Checker):

    def __init__(self, check):
        self._check = Checker.create(check)

    def check(self, value):
        return isinstance(value, tuple) and \
               functools.reduce(lambda r, v: r and self._check.check(v), value, True)

tuple_of = TupleOfChecker

################################################################################

class ListOfChecker(Checker):

    def __init__(self, check):
        self._check = Checker.create(check)

    def check(self, value):
        return isinstance(value, list) and \
               functools.reduce(lambda r, v: r and self._check.check(v), value, True)

list_of = ListOfChecker

################################################################################

class DictOfChecker(Checker):

    def __init__(self, key_check, value_check):
        self._key_check = Checker.create(key_check)
        self._value_check = Checker.create(value_check)

    def check(self, value):
        return isinstance(value, dict) and \
               functools.reduce(lambda r, t: r and self._key_check.check(t[0]) and \
                                             self._value_check.check(t[1]),
                                value.items(), True)

dict_of = DictOfChecker

################################################################################

class OneOfChecker(Checker):

    def __init__(self, *values):
        self._values = values

    def check(self, value):
        return value in self._values

one_of = OneOfChecker

################################################################################

def typecheck(method):

    argspec = inspect.getfullargspec(method)
    if not argspec.annotations:
        return method

    default_arg_count = len(argspec.defaults or [])
    non_default_arg_count = len(argspec.args) - default_arg_count

    method_name = method.__name__
    arg_checkers = [None] * len(argspec.args)
    kwarg_checkers = {}
    return_checker = None
    kwarg_defaults = argspec.kwonlydefaults or {}

    for n, v in argspec.annotations.items():
        checker = Checker.create(v)
        if checker is None:
            raise TypeCheckSpecificationError("invalid typecheck for {0}".format(n))
        if n in argspec.kwonlyargs:
            if n in kwarg_defaults and \
               not checker.check(kwarg_defaults[n]):
                raise TypeCheckSpecificationError("the default value for {0} is incompatible "
                                                  "with its typecheck".format(n))
            kwarg_checkers[n] = checker
        elif n == "return":
            return_checker = checker
        else:
            i = argspec.args.index(n)
            if i >= non_default_arg_count and \
               not checker.check(argspec.defaults[i - non_default_arg_count]):
                raise TypeCheckSpecificationError("the default value for {0} is incompatible "
                                                  "with its typecheck".format(n))
            arg_checkers[i] = (n, checker)

    def typecheck_invocation_proxy(*args, **kwargs):

        for check, arg in zip(arg_checkers, args):
            if check is not None:
                arg_name, checker = check
                if not checker.check(arg):
                    raise InputParameterError("{0}() has got an incompatible value "
                                              "for {1}: {2}".format(method_name, arg_name,
                                                                    str(arg) == "" and "''" or arg))

        for arg_name, checker in kwarg_checkers.items():
            kwarg = kwargs.get(arg_name, Checker.no_value)
            if not checker.check(kwarg):
                raise InputParameterError("{0}() has got an incompatible value "
                                          "for {1}: {2}".format(method_name, arg_name,
                                                                str(kwarg) == "" and "''" or kwarg))

        result = method(*args, **kwargs)

        if return_checker is not None and not return_checker.check(result):
            raise ReturnValueError("{0}() has returned an incompatible "
                                   "value: {1}".format(method_name, str(result) == "" and "''" or result))

        return result

    functools.update_wrapper(typecheck_invocation_proxy, method)

    return typecheck_invocation_proxy

################################################################################
# EOF

