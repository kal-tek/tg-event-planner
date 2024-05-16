from . import testcases


class LoadDataTests(testcases.TestCase):
    fixtures: list[str] = []

    @staticmethod
    def test_loaddata() -> None:
        """
        Triggers fixture loading.

        If any fixture is not up to date, the test fails.
        """
