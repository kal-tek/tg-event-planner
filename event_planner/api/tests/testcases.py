import random
import unittest
from collections.abc import Callable, Iterable, Iterator, Mapping, Sized
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

import django.test
import factory.random
import rest_framework.test
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from .. import factories
from ..factories.user import KNOWN_PASSWORD

# This magic variable, ensures that the stack trace for our assertions,
# don't enter this module, but only show up on the callers
__unittest = True  # pylint: disable=invalid-name


class ReverseMixin(unittest.TestCase):
    @staticmethod
    def reverse(*args: Any, **kwargs: Any) -> str:
        """Django reverse, but with query parameters support."""
        query = kwargs.pop("query", {})
        url = reverse(*args, **kwargs)
        if query:
            url += "?" + urlencode(query)
        return url


class MoreAssertsMixin(unittest.TestCase):
    # pylint: disable=invalid-name
    # ruff: noqa: N802

    @contextmanager
    def assertConstant(self, func: Callable[[], Any]) -> Iterator[None]:
        """Ensure that the argument callable does not change."""
        value_start = func()
        yield
        value_end = func()

        self.assertEqual(
            value_start,
            value_end,
            (
                f"Callable result changed.\n"
                f"Initial value: {value_start}\n"
                f"Final value: {value_end}"
            ),
        )

    @contextmanager
    def assertBecomesNone(self, func: Callable[[], Any | None]) -> Iterator[None]:
        """Ensure that the argument callable is not None before and None after."""
        value_start = func()
        self.assertIsNotNone(value_start, "Callable is already None")
        yield
        value_end = func()
        self.assertIsNone(
            value_end,
            (
                f"Callable result did not become None.\n"
                f"Initial value: {value_start}\n"
                f"Final value: {value_end}"
            ),
        )

    @contextmanager
    def assertBecomesNotNone(self, func: Callable[[], Any | None]) -> Iterator[None]:
        """Ensure that the argument callable is None before and not None after."""
        value_start = func()
        self.assertIsNone(
            value_start,
            "Callable result is already not None. Initial value: {value_start}\n",
        )
        yield
        value_end = func()
        self.assertIsNotNone(
            value_end,
            (
                f"Callable result did not become not None.\n"
                f"Initial value: {value_start}\n"
                f"Final value: {value_end}"
            ),
        )

    @contextmanager
    def assertIncreasesBy(
        self,
        increment: int,
        func: Callable[[], int],
    ) -> Iterator[None]:
        """Ensure that the given expression value is incremented by the given value."""
        value_start = func()
        yield
        value_end = func()

        self.assertEqual(
            value_start + increment,
            value_end,
            (
                f"Callable result did not increase by {increment}.\n"
                f"Initial value: {value_start}\n"
                f"Final value: {value_end}"
            ),
        )

    @contextmanager
    def assertDecreasesBy(
        self,
        decrement: int,
        func: Callable[[], int],
    ) -> Iterator[None]:
        """Ensure that the given expression value is incremented by the given value."""
        value_start = func()
        yield
        value_end = func()

        self.assertEqual(
            value_start - decrement,
            value_end,
            (
                f"Callable result did not decreased by {decrement}.\n"
                f"Initial value: {value_start}\n"
                f"Final value: {value_end}"
            ),
        )

    @contextmanager
    def assertNotRaises(self, exc_type: type[Exception]) -> Iterator[None]:
        """Ensure that the exception type provided is not raised."""
        try:
            yield None
        except exc_type:  # pragma: no cover
            msg = f"{exc_type.__name__} raised"
            raise self.failureException(
                msg,
            ) from exc_type  # pragma: no cover

    def assertErrorCodes(
        self,
        response_data: Mapping[str, Any],
        error_map: Mapping[str, Iterable[str]],
    ) -> None:
        """Ensure that the response_data has the same errors declared in error_map."""
        self.assertCountEqual(response_data.keys(), error_map.keys())
        for attribute, error_codes in error_map.items():
            if isinstance(response_data[attribute], str):
                response_error_codes = [response_data[attribute]]
            else:
                response_error_codes = list(response_data[attribute])

            self.assertCountEqual(response_error_codes, error_codes)

    def assertIsFile(self, path: Path) -> None:
        """Ensure that path resolves to an existing file."""
        self.assertTrue(path.resolve().is_file(), f"File does not exist: {path}")

    def assertSameSize(self, arg1: Sized, arg2: Sized) -> None:
        """Ensure the given arguments have the same size."""
        self.assertEqual(len(arg1), len(arg2))

    def assertNoUpdates(self, context: CaptureQueriesContext) -> None:
        """Ensure that no update queries were issued."""
        for query in context.captured_queries:
            sql = query["sql"]
            self.assertFalse(
                sql.startswith("UPDATE "),
                f"Update query emitted.\n{sql}",
            )

    def assertNoInserts(self, context: CaptureQueriesContext) -> None:
        """Ensure that no insert queries were issued."""
        for query in context.captured_queries:
            sql = query["sql"]
            self.assertFalse(
                sql.startswith("INSERT INTO "),
                f"Insert query emitted.\n{sql}",
            )

    def assertNoMutations(self, context: CaptureQueriesContext) -> None:
        """Ensure that no insert or update queries were issued."""
        self.assertNoUpdates(context)
        self.assertNoInserts(context)


class TestCase(MoreAssertsMixin, django.test.TestCase):
    def setUp(self) -> None:
        """
        Set up.

        - Seed data for factories.
        """
        random.seed(4)
        factory.random.reseed_random(4)


class APITestCase(rest_framework.test.APITestCase, TestCase):
    def setUp(self) -> None:
        """
        Set up.

        - Seed data for factories.
        - Create a test users.
        """
        super().setUp()
        self.normie = factories.UserFactory(
            is_staff=False,
            is_superuser=False,
            is_active=True,
            with_known_password=True,
        )
        self.superuser = factories.UserFactory(
            is_staff=True,
            is_superuser=True,
            is_active=True,
            with_known_password=True,
        )
        self.known_password = KNOWN_PASSWORD
