"""Genera una página web estática y autocontenida con el top de ofertas."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from logic.rank import Deal

_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0b0f17">
<title>Radar de Ofertas</title>
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #0b0f17; color: #e8edf5; -webkit-font-smoothing: antialiased;
  }}
  header {{
    position: sticky; top: 0; z-index: 5; padding: 16px 16px 12px;
    background: rgba(11,15,23,.92); backdrop-filter: blur(8px);
    border-bottom: 1px solid #1d2533;
  }}
  h1 {{ font-size: 20px; margin: 0 0 2px; letter-spacing: .3px; }}
  .sub {{ font-size: 12px; color: #7d8aa0; margin-bottom: 12px; }}
  .controls {{ display: flex; gap: 8px; }}
  #q {{
    flex: 1; padding: 11px 14px; border-radius: 12px; border: 1px solid #243047;
    background: #121826; color: #e8edf5; font-size: 15px; outline: none;
  }}
  #q:focus {{ border-color: #3b82f6; }}
  #sort {{
    padding: 0 12px; border-radius: 12px; border: 1px solid #243047;
    background: #121826; color: #e8edf5; font-size: 14px;
  }}
  .chips {{ display: flex; gap: 8px; overflow-x: auto; padding: 12px 16px 4px; }}
  .chip {{
    flex: 0 0 auto; padding: 7px 14px; border-radius: 999px; font-size: 13px;
    border: 1px solid #243047; background: #121826; color: #aab6c9; cursor: pointer;
  }}
  .chip.active {{ background: #1d4ed8; border-color: #1d4ed8; color: #fff; }}
  main {{ padding: 8px 16px 40px; display: grid; gap: 12px; max-width: 720px; margin: 0 auto; }}
  .card {{
    background: #121826; border: 1px solid #1d2533; border-radius: 16px;
    padding: 14px 16px; display: flex; align-items: center; gap: 14px;
  }}
  .save {{
    flex: 0 0 auto; width: 62px; height: 62px; border-radius: 14px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    font-weight: 700; background: #0e2a1a; color: #4ade80; border: 1px solid #1f5135;
  }}
  .save small {{ font-size: 10px; font-weight: 600; opacity: .8; }}
  .save.low {{ background: #2a230e; color: #fbbf24; border-color: #51421f; }}
  .info {{ flex: 1; min-width: 0; }}
  .name {{ font-size: 15px; font-weight: 600; margin: 0 0 3px; }}
  .meta {{ font-size: 12px; color: #7d8aa0; display: flex; gap: 8px; flex-wrap: wrap; }}
  .badge {{ background: #1b2233; color: #9fb0c9; padding: 2px 8px; border-radius: 6px; }}
  .price {{ font-size: 17px; font-weight: 700; margin-top: 5px; }}
  .price small {{ font-size: 12px; font-weight: 500; color: #7d8aa0; }}
  .go {{
    flex: 0 0 auto; text-decoration: none; color: #93c5fd; font-size: 13px;
    border: 1px solid #243047; padding: 8px 12px; border-radius: 10px;
  }}
  .empty {{ text-align: center; color: #7d8aa0; padding: 48px 0; }}
  footer {{ text-align: center; color: #4b5568; font-size: 11px; padding: 0 16px 32px; }}
</style>
</head>
<body>
<header>
  <h1>🛒 Radar de Ofertas</h1>
  <div class="sub">Actualizado: {updated} · {count} ofertas</div>
  <div class="controls">
    <input id="q" type="search" placeholder="Buscar producto…" autocomplete="off">
    <select id="sort">
      <option value="savings">Mayor ahorro</option>
      <option value="price">Menor precio</option>
    </select>
  </div>
</header>
<div class="chips" id="chips"></div>
<main id="list"></main>
<footer>Datos de muestra · Radar Ofertas CBA</footer>
<script>
const DEALS = {data};
let store = "Todas", sort = "savings", q = "";

const fmt = n => "$" + n.toLocaleString("es-AR", {{maximumFractionDigits: 0}});
const stores = ["Todas", ...[...new Set(DEALS.map(d => d.store).filter(Boolean))]];

const chips = document.getElementById("chips");
stores.forEach(s => {{
  const b = document.createElement("button");
  b.className = "chip" + (s === store ? " active" : "");
  b.textContent = s;
  b.onclick = () => {{ store = s; [...chips.children].forEach(c => c.classList.toggle("active", c.textContent === s)); render(); }};
  chips.appendChild(b);
}});

document.getElementById("q").oninput = e => {{ q = e.target.value.toLowerCase(); render(); }};
document.getElementById("sort").onchange = e => {{ sort = e.target.value; render(); }};

function render() {{
  let rows = DEALS.filter(d =>
    (store === "Todas" || d.store === store) &&
    (!q || d.name.toLowerCase().includes(q) || (d.brand||"").toLowerCase().includes(q))
  );
  rows.sort((a, b) => sort === "price" ? a.price_ars - b.price_ars : b.savings_pct - a.savings_pct);
  const list = document.getElementById("list");
  if (!rows.length) {{ list.innerHTML = '<div class="empty">Sin resultados</div>'; return; }}
  list.innerHTML = rows.map(d => {{
    const s = Math.round(d.savings_pct);
    const unit = d.size_ml ? `<small> · ${{fmt(d.price_unit*1000)}}/L</small>` : "";
    return `<div class="card">
      <div class="save ${{s < 15 ? 'low' : ''}}">${{s}}%<small>OFF</small></div>
      <div class="info">
        <p class="name">${{d.name}}</p>
        <div class="meta">${{d.store ? `<span class="badge">${{d.store}}</span>`:""}}${{d.brand?`<span>${{d.brand}}</span>`:""}}</div>
        <div class="price">${{fmt(d.price_ars)}}${{unit}}</div>
      </div>
      <a class="go" href="${{d.url}}" target="_blank" rel="noopener">Ver</a>
    </div>`;
  }}).join("");
}}
render();
</script>
</body>
</html>
"""


def render_page(deals: list[Deal], output: Path) -> Path:
    """Escribe una página HTML autocontenida con las ofertas embebidas."""
    data = json.dumps([d.model_dump(mode="json") for d in deals], ensure_ascii=False)
    html = _TEMPLATE.format(
        updated=datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC"),
        count=len(deals),
        data=data,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return output
