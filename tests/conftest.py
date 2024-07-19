from asyncio.subprocess import PIPE
import os
import signal
import subprocess
from typing import Any, TypedDict
import pytest


@pytest.fixture(scope="session", autouse=True)
def some_session_setup():
    print("Set up something across the session")
    yield
    print("Tear down something across the session")


def pytest_runtest_setup(item: pytest.Item):
    # called for running each test in 'a' directory
    print("Setting up", item)


def pytest_addoption(parser: pytest.Parser):
    some_custom_plugin_options = parser.getgroup("some_custom_plugin_options")
    some_custom_plugin_options.addoption(
        "--custom_plugin_option_1",
        action="store",
        default=None,
        help="Just some config for custom plugin 1"
    )
    some_custom_plugin_options.addoption(
        "--custom_plugin_option_2",
        action="store",
        default=None,
        help="Just some config for custom plugin 2"
    )


def pytest_collection_modifyitems(session: pytest.Session, config: pytest.Config, items: pytest.Item):
    pass


class CustomConfigType(TypedDict):
    """pytest-bq config definition type."""

    custom_plugin_option_1: str
    custom_plugin_option_2: str


def get_config(request: pytest.FixtureRequest) -> CustomConfigType:
    """Return a dictionary with config options."""

    def get_conf_option(option: str) -> Any:
        option_name = "" + option
        return request.config.getoption(option_name) or request.config.getini(
            option_name
        )

    config: CustomConfigType = {
        "custom_plugin_option_1": get_conf_option("custom_plugin_option_1"),
        "custom_plugin_option_2": get_conf_option("custom_plugin_option_2"),
    }
    return config


def fixture_that_runs_bq_emulator_factory(
    custom_plugin_option_1: str,
    custom_plugin_option_2: str,
):
    @pytest.fixture(scope="session", autouse=True)
    def fixture_that_runs_bq_emulator(
        request: pytest.FixtureRequest,
    ):
        config = get_config(request)
        print(f"Say hiiiii at first test function that uses this fixture - and config is {config}")
        # bigquery_emulator_proc = subprocess.run(["/opt/homebrew/bin/bigquery-emulator", "--project", "kira-test", "--dataset", "kira_categorical", "--port", "9050"])
        print("Starting bq emulator in BG")
        process = subprocess.Popen(["/opt/homebrew/bin/bigquery-emulator", "--project", "kira-test", "--dataset", "kira_categorical", "--port", "9050"], stdout=PIPE, stderr=PIPE)
        print("Running bq emulator in BG")
        yield
        print("Killing bq emulator in BG")
        process.terminate()
        print("Killed bq emulator in BG")
        print(f"Say byeeeee at end of tests - and config is {config}")

    return fixture_that_runs_bq_emulator


fixture_that_runs_bq_emulator = fixture_that_runs_bq_emulator_factory(custom_plugin_option_1="custom_plugin_option_1_val", custom_plugin_option_2="custom_plugin_option_2_val")


def fixture_that_provides_bq_local_client_factory(
    custom_plugin_option_1: str,
    custom_plugin_option_2: str,
):
    @pytest.fixture(scope="session")
    def fixture_that_provides_bq_local_client(
        request: pytest.FixtureRequest,
    ):
        config = get_config(request)
        print(f"In the bqlocal fixture {config}")
        from google.api_core.client_options import ClientOptions
        from google.auth.credentials import AnonymousCredentials
        from google.cloud import bigquery
        # fixture_that_runs_bq_emulator = request.getfixturevalue("fixture_that_runs_bq_emulator")
        endpoint = f"http://localhost:9050"
        bq_client = bigquery.Client(
            "kira-test",
            client_options=ClientOptions(api_endpoint=endpoint),
            credentials=AnonymousCredentials(),
        )
        yield bq_client
        print(f"Exiting bqlocal fixture - and config is {config}")

    return fixture_that_provides_bq_local_client


fixture_that_provides_bq_local_client = fixture_that_provides_bq_local_client_factory(custom_plugin_option_1="custom_plugin_option_1_val", custom_plugin_option_2="custom_plugin_option_2_val")
