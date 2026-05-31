import argparse

import config


def cmd_scrape() -> None:
    """Scrapea todos los retailers y agrega los precios al historial local."""
    from scraper import scrape_all
    from logic.store import append_prices

    saved = append_prices(scrape_all(), config.PRICES_FILE)
    print(f"Guardados {saved} productos en {config.PRICES_FILE}")


def cmd_build() -> None:
    """Genera la página web con el top de ofertas a partir del historial."""
    from logic.store import load_prices
    from logic.rank import generate_deals
    from web.render import render_page

    deals = generate_deals(load_prices(config.PRICES_FILE))
    out = render_page(deals, config.WEB_DIR / "index.html")
    print(f"Generadas {len(deals)} ofertas en {out}")


def cmd_demo() -> None:
    """Carga datos de muestra y genera la web (sin scrapear nada real)."""
    import json

    from logic.sample import sample_products

    config.PRICES_FILE.parent.mkdir(parents=True, exist_ok=True)
    records = [p.model_dump(mode="json") for p in sample_products()]
    config.PRICES_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2))
    cmd_build()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Radar Ofertas CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("scrape", help="Scrapea retailers y guarda precios")
    sub.add_parser("build", help="Genera la web con el top de ofertas")
    sub.add_parser("demo", help="Genera la web con datos de muestra")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "scrape":
        cmd_scrape()
    elif args.command == "build":
        cmd_build()
    elif args.command == "demo":
        cmd_demo()


if __name__ == "__main__":
    main()
