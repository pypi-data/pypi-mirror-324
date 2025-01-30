"""
Python bindings for the bootest C++ testing library.
"""
from __future__ import annotations
import typing
__all__ = ['list_tests', 'register_test', 'run_all_tests', 'run_test']
def list_tests() -> dict[str, list[str]]:
    """
    List all registered tests and their suites.
    """
def register_test(suite_name: str, test_name: str, test_fn: typing.Callable, setup_fn: typing.Callable = None, teardown_fn: typing.Callable = None) -> None:
    """
    Register a test case with optional setup and teardown functions.
    """
def run_all_tests() -> int:
    """
    Run all registered tests.
    """
def run_test(test_name: str) -> int:
    """
    Run a single test by its name.
    """
