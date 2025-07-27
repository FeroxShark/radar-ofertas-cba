import argparse

from bot.bot import run as run_bot
from logic.payment import create_app
from logic.self_check import run as self_check_run

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
