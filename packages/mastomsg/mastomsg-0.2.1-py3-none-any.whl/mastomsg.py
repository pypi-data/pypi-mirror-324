from mastodon import Mastodon
from configparser import ConfigParser
from datetime import datetime, timedelta, timezone, UTC
from mastodon.errors import MastodonError
import typer
import os
from functools import reduce
from typing_extensions import Annotated

CONFIG_PATH = os.path.expanduser("~/.config/mastomsg.conf")
scopes = ['read', 'write', 'admin:read']
config = ConfigParser()
api: Mastodon

def check_valid_config()->bool:
    # check for a valid config File
    global config

    try:
        config.read(CONFIG_PATH)
    except:
        # No file found
        print(f"Configuration file {CONFIG_PATH} not found. Running configuration.")
        return False
    try:
        config['DEFAULT']['url']
        config['DEFAULT']['client_id']
        config['DEFAULT']['client_secret']
        config['DEFAULT']['access_token']
    except:
        print("Configuration seems corrupt. Running setup.")
        return False
    return True

def setup():
    """
    Store mastodon instance info.
    The connection details will be stored in CONFIG_PATH
    """
    global config, scopes
    url = typer.prompt("What's your Mastodon instance URL (for example https://masto.example.org)")
    account_name = typer.prompt("Please enter the email of the account you want to authenticate (must be an admin account)")

    config['DEFAULT']['url'] = url
    config['DEFAULT']['email'] = account_name

    # Setting up an APP
    try:
        config['DEFAULT']['client_id'] != ""
        config['DEFAULT']['client_secret'] != ""
    except:
        app = create_application(url)
        config['DEFAULT']['client_id'] = app[0]
        config['DEFAULT']['client_secret'] = app[1]

    # now do the oauth dance
    mastodon = Mastodon(client_id=config['DEFAULT']['client_id'],
        client_secret=config['DEFAULT']['client_secret'],
        api_base_url = config['DEFAULT']['url'])
    auth_url = mastodon.auth_request_url(scopes = scopes)
    print(f"""
        Please open
        {auth_url}
        in your browser and sign in with your account
        """)
    token = typer.prompt("Please enter the token that your Mastodon instance has given you")

    # now create the actual access token
    access_token = mastodon.log_in(config['DEFAULT']['email'], code=token, scopes=scopes)
    config['DEFAULT']['access_token'] = access_token

    # now test the login
    print("Testing the login")
    if connect():
        # write the config to the disc
        try:
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, "w+") as conffile:
                config.write(conffile)
            return True
        except BaseException as ex:
            print("Could not write config file")
            print(repr(ex))
        return False


def create_application(url: str) -> tuple:
    global scopes
    app = Mastodon.create_app(
        client_name='mastomessage',
        api_base_url = url,
        scopes = scopes,
    )
    return app

def connect()->bool:
    global api, config
    api = Mastodon(access_token=config['DEFAULT']['access_token'],
        api_base_url=config['DEFAULT']['url'],
        client_id=config['DEFAULT']['client_id'],
        client_secret=config['DEFAULT']['client_secret'],
        version_check_mode="none"
    )
    try:
        api.app_verify_credentials()
        return True
    except:
        return False

def parse_time(timestr: str)->timedelta:
    # we support integers followed by single letter markers
    #     d: days
    #     h: hours

    timestr = timestr.strip()
    length:int = 0
    try:
        length = int(timestr[:-1])
    except:
        print(f"{timestr} has an invalid format.")
        raise typer.Exit()
    if length == 0:
       print("Please enter a longer duration than 0.")
       raise typer.Exit()

    modifier = timestr[-1]
    match modifier:
        case "d":
            return timedelta(days=length)
        case "h":
            return timedelta(hours=length)
        case _:
            print("Please use one of the supported modifiers.")
            raise typer.Exit()

def message(
    text: Annotated[str, typer.Argument(help="The message to send out via DM to the respective people")],
    age:Annotated[str, typer.Option(help="The age of the accounts to target. Age is given as days '10d' or hours '5h'.")]="", #more to come
    lastactive:Annotated[str, typer.Option(help="targets accounts that have not been active (as in having sent a post) for a defined time. Time is given as days '10d' or hours '5h'.")]="",
    handles:Annotated[str, typer.Option(help="A list of specific users to send a message to separated by comma. Only local part is relevant.")]="",
    pretend: Annotated[bool,typer.Option(help="Don't actually send the message, just give out list of recipients"),] = False,
): #more to come

    global api
    if not(check_valid_config()):
        while not setup():
            redo = typer.prompt("Retry setup? y/n")
            if redo.lower() != "y":
                break
    else:
        if not connect():
            print(f"Something is wrong with your login info. If the problem persists remove your config file {CONFIG_PATH} an redo the authentication")

    # check that only one selector is chosen
    selected = len(list(filter(lambda x: x!="",[age, lastactive, handles])))
    if selected>1:
        print("Please only pick one selector.")

    if selected==0:
        print("No recipients given. Please pick one option to select recipients")
        raise typer.Exit()

    # do message validation before it goes out:
    if not "@{target.username}" in text and not "@{target.acct}" in text:
        print("The message text does not contain a mention of the user so it wouldn't reach them.")
        prepend = typer.prompt("Should I prepend the mention to your text? y/n")
        if prepend.lower() != "y":
            print("Okay, quitting.")
            raise typer.Exit()
        else:
          text = "@{target.username}: "+text

    # these accounts will get the message
    targets = []

    #if age is given
    if age != "":
        delta = parse_time(age)
        accounts_age = datetime.now(UTC)-delta
        first_slice = api.admin_accounts_v2(origin="local",status="active")
        all_accounts = api.fetch_remaining(first_slice)
        targets = [account for account in all_accounts if account['created_at']> accounts_age]

    #if lastactive is given
    if lastactive != "":
        delta = parse_time(lastactive)
        passive_since = datetime.now(UTC)-delta
        first_slice = api.admin_accounts_v2(origin="local",status="active")
        all_accounts = api.fetch_remaining(first_slice)
        for account in all_accounts:
            try:
                if account['account']['last_status_at'].replace(tzinfo=UTC)< passive_since:
                    targets.append(account)
            except:
                # this means no post has been made
                pass


    # if handles are given
    if handles != "":
        split_handles = set(handles.replace(" ","").split(","))

        for h in split_handles:
            try:
                acc = api.account_lookup(h)
                targets.append(acc)
            except MastodonError:
                print(f"Could not find user {h}")
                raise typer.Exit()

    # now create the actual posts
    # right now only DMs possible
    if targets != [] and not pretend:
        for target in targets:
            api.status_post(text.format(target=target),visibility="direct")
    else:
        print("Would have send the message to the users:")
        print(", ".join([t['username'] for t in targets]))

def main():
    typer.run(message)

if __name__ == "__main__":
    main()
