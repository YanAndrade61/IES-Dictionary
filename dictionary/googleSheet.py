import ssl
from gspread_pandas import Spread, Client
from google.oauth2 import service_account
from pandas import Dataframe


def get_google_client(gcp_account: dict):
    """Create a connection with google client.

    Args:
        gcp_account (dict): The credentials of Google Cloud Platform service account.

    Returns:
        Client: The client connection.

    """

    ssl._create_default_https_context = ssl._create_unverified_context

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = service_account.Credentials.from_service_account_info(
        gcp_account, scopes=scope
    )

    client = Client(scope=scope, creds=credentials)
    return client


def get_spreadsheet(spreadsheetname: str, client: Client):
    """Load a spreadsheet from Google sheets.

    Args:
        spreadsheetname (str): Spreadsheet to open.
        client (Client): Client to acess Google sheets.

    Returns:
        Spread: Spreadsheet of Google sheets.

    """

    spread = Spread(spreadsheetname, client=client)
    return spread
