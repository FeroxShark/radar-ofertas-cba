import argparse
import os

from telegram import Update
from telegram.ext import Application, CommandHandler

from bot.bot import run as run_bot, start
from logic.payment import create_app
from logic.self_check import run as self_check_run

BOT_TOKEN = os.environ.get("TG_TOKEN", "")


def build_bot() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    return app

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('--token')


def main() -> None:
    args = parser.parse_args()
    if args.command == 'bot':
        if not args.token:
            raise SystemExit('token required')
        run_bot(args.token)
    elif args.command == 'self_check':
        self_check_run()
    elif args.command == 'payment':
        app = create_app()
        app.run()
    else:
        raise SystemExit('unknown command')


if __name__ == '__main__':
    main()
