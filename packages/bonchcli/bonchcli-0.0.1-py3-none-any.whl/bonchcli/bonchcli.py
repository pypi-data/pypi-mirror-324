#!/usr/bin/env python
import asyncio
import argparse
from getpass import getpass

from bonchapi import BonchAPI
from bonchapi.bonchapi import AuthError

from .get_token_from_browser import Brow
from .config_manager import cm, Config
from . import formatting


def input_auth_data():
    mail = input("Your mail> ")
    password = getpass("Your password> ")
    config = Config(mail, password)
    cm.write_config(config)


async def main():
    if not cm.is_config_exists():
        cm.create_config_file()
        if not cm.check_validity_config():
            input_auth_data()
        config = cm.read_config()
    else:
        config = cm.read_config()

    parser = argparse.ArgumentParser(
                        prog="bonchcli",
                        description='What the program does',
                        epilog='Text at the bottom of help')

    parser.add_argument('week_offset', nargs="?", type=int, default=0)
    args = parser.parse_args()

    api = BonchAPI()

    await api.login(config.mail, config.password)

    api.cookies = {}

    def write_brow_token():
        browser = Brow(config)
        token = browser.get_token()
        setattr(api, "cookies", {}) 
        with open("/tmp/bonch-token", "w") as file:
            file.write(token)
        api.cookies["miden"] = token

    def read_token_from_cache():
        with open("/tmp/bonch-token", "r") as file:
            token = file.readline()
            api.cookies["miden"] = token

    write_brow_token()

    try:
        read_token_from_cache()
    except FileNotFoundError:
        write_brow_token()

    try:
        rsp = await api.get_timetable(week_offset=args.week_offset)
    except AuthError:
        write_brow_token()

    
    rsp = await api.get_timetable(week_offset=args.week_offset)
    
    formatting.render_timetable(rsp)

def sync_main():
    """This func need for build pipx applicaion as entry point"""

    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
