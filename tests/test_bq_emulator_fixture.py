from google.api_core.client_options import ClientOptions
from google.auth.credentials import AnonymousCredentials
from google.cloud import bigquery


# def test_bq_emulator_fixture(fixture_that_runs_bq_emulator):
#     endpoint = f"http://localhost:9050"
#     bq_client = bigquery.Client(
#         "kira-test",
#         client_options=ClientOptions(api_endpoint=endpoint),
#         credentials=AnonymousCredentials(),
#     )
#     job = bq_client.query("SELECT 1+1")
#     # print(f"{list(job.result())[0][0]=}")
#     assert list(job.result())[0][0] == 2


def test_bq_emulator_fixture(fixture_that_provides_bq_local_client):
    job = fixture_that_provides_bq_local_client.query("SELECT 1+1")
    # print(f"{list(job.result())[0][0]=}")
    assert list(job.result())[0][0] == 2
