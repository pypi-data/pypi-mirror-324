import webbrowser

import click
import requests

from src.urls.auth import AuthURL
from src.utils.credentials import cred
from src.utils.log import setup_logger

logger, log_entry = setup_logger(__name__)


@click.group(name="auth")
def auth_group():
    """Authentication commands"""
    pass


@auth_group.command(name="verify")
def verify():
    """Verify the credential token"""
    if cred.verify():
        click.echo("Credential token is valid")
    else:
        click.echo("Credential token is invalid")


@auth_group.command(name="logout")
def logout():
    """Log out from Steev"""
    # if not cred.logged_in:
    #     click.echo("You are not logged in")
    #     return

    headers = {
        "Authorization": f"Bearer {cred.token['access_token']}",
        "Content-Type": "application/json",
    }
    data = {"refresh": cred.token["refresh_token"]}

    response = requests.post(AuthURL.logout, json=data, headers=headers)
    logger.debug(f"Logout response: {response.status_code}")
    logger.debug(f"Logout response: {response.text}")
    if response.status_code == 205:
        cred.clear()
        click.echo("Successfully logged out")
    else:
        click.echo("Logout failed")


@auth_group.command(name="login")
def login():
    """Log in to Steev using Google OAuth"""
    import time

    # Create session

    resp = requests.get(AuthURL.session_create)
    if resp.status_code != 200:
        click.echo(click.style("Failed to access steev server", fg="red"), err=True)
        return
    session_id = resp.json()["session_id"]

    # Open browser
    login_url = f"{AuthURL.google_login}?next={AuthURL.login_session(session_id)}"

    click.echo("Choose authentication method:")
    options = [
        "Log in with web browser(Login from local)",
        "Paste an auth token(Login from remote server)",
    ]

    click.echo("\n")

    # Handle arrow key navigation
    def get_user_choice(options):
        current_selection = 0
        while True:
            # Clear previous lines and reprint options
            click.echo("\033[F" * (len(options) + 1))
            for i, option in enumerate(options):
                if i == current_selection:
                    click.echo(click.style(f"> {option}", fg="green"))
                else:
                    click.echo(f"  {option}")

            # Get keypress
            c = click.getchar()

            # Handle arrow keys
            if c == "\x1b[A":  # Up arrow
                current_selection = (current_selection - 1) % len(options)
            elif c == "\x1b[B":  # Down arrow
                current_selection = (current_selection + 1) % len(options)
            elif c == "\r":  # Enter
                return str(current_selection + 1)

    auth_method = get_user_choice(options)

    # Clear the two lines above
    click.echo("\033[F\033[K" * 3, nl=False)
    click.echo(
        "Choose authentication method:"
        f"\t{click.style('browser', fg='green') if auth_method == '1' else click.style('token', fg='green')}"
    )

    if auth_method == "1":
        click.echo("\nBrowser window opened for Google login.")
        webbrowser.open(login_url)
        click.echo("You can close the browser window after successful login.\n")
        # Poll for session completion
        for i in range(30):
            spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            click.echo(
                f"\rWaiting for login to complete... {spinner[i%len(spinner)]}",
                nl=False,
            )
            time.sleep(0.5)

            # Check session status
            resp = requests.get(AuthURL.session_token(session_id))
            if resp.status_code == 200:
                data = resp.json()
                cred.update_data(
                    {
                        "user": data["user"],
                        "email": data["email"],
                        "token": {
                            "access_token": data["access_token"],
                            "refresh_token": data["refresh_token"],
                            "access_exp": data["access_exp"],
                        },
                    },
                    save=True,
                )
                click.echo("\nLogin successful! You can close the browser window.")
                click.echo(cred)
                return

        click.echo("\nLogin timed out. Please try again.")
    else:
        click.echo(f"Access to the url {login_url}?remote=true")
        token = click.prompt("Please paste your auth token", type=str)
        cred.update_refresh_token(token)
        cred.refresh()
        click.echo("Login successful!")
        return


@auth_group.command(name="status")
def status():
    """Show the current login status"""
    click.echo(cred)


@auth_group.command(name="refresh")
def refresh():
    """Refresh the credential token"""
    if cred.refresh():
        click.echo("Credential token refreshed")
    else:
        click.echo(click.style("Credential token refresh failed", fg="red"), err=True)
