import argparse

import config


def cmd_scrape() -> None:
    from scraper import RETAILERS
    from logic.store import save_products

    db = config.get_db()
    total = 0
    for name, module in RETAILERS.items():
        products = module.scrape()
        total += save_products(db, products, retailer=name)
    print(f"Guardados {total} productos")


def cmd_rank() -> None:
    from logic.rank import generate_top20

    db = config.get_db()
    top = generate_top20(db, config.DEALS_DIR)
    print(f"Generado top con {len(top)} ofertas en {config.DEALS_DIR}")


def cmd_bot(token: str | None) -> None:
    from bot.bot import run as run_bot

    token = token or config.TELEGRAM_TOKEN
    if not token:
        raise SystemExit("token required (--token o TELEGRAM_TOKEN)")
    run_bot(token)


def cmd_payment() -> None:
    from logic.payment import create_app

    create_app().run()


def cmd_self_check() -> None:
    from logic.self_check import run as self_check_run

    self_check_run()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Radar Ofertas CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("scrape", help="Scrapea retailers y guarda precios")
    sub.add_parser("rank", help="Genera el top de ofertas del día")
    bot_p = sub.add_parser("bot", help="Corre el bot de Telegram (polling)")
    bot_p.add_argument("--token")
    sub.add_parser("payment", help="Levanta el servidor de webhooks de pago")
    sub.add_parser("self_check", help="Chequea salud de los scrapers")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "scrape":
        cmd_scrape()
    elif args.command == "rank":
        cmd_rank()
    elif args.command == "bot":
        cmd_bot(args.token)
    elif args.command == "payment":
        cmd_payment()
    elif args.command == "self_check":
        cmd_self_check()


if __name__ == "__main__":
    main()
