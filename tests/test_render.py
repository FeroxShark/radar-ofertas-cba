from logic.sample import sample_products
from logic.rank import generate_deals
from web.render import render_page


def test_render_page_writes_self_contained_html(tmp_path):
    records = [p.model_dump(mode="json") for p in sample_products()]
    deals = generate_deals(records)
    out = render_page(deals, tmp_path / "index.html")

    html = out.read_text(encoding="utf-8")
    assert html.startswith("<!DOCTYPE html>")
    assert "Radar de Ofertas" in html
    assert "const DEALS = [" in html
    # Los datos quedan embebidos: no hay fetch externo.
    assert "fetch(" not in html
