import streamlit_authenticator as stauth


def authenticate_user(credential: dict, cookie: dict, preauthorized: dict, pos: str):
    """Generate an widget for user login.

    Args:
        credential (dict): Contain user registered in system.
        cookie (dict): Contain cookies information.
        preauthorized (dict): Contain emails of registered users.
        pos (str): Position of login widget. Main or sidebar.

    Returns:
        str: Returns the name if login success or None otherwise.
        Bool: Returns the status of login.

    """

    authenticator = stauth.Authenticate(
        credential, cookie.name, cookie.key, cookie.expiry_days, preauthorized
    )
    name, auth_status, username = authenticator.login("Login", pos)

    if auth_status:
        authenticator.logout("Logout", pos)
        return name, True
    elif auth_status is False:
        return None, False

    return None, None
