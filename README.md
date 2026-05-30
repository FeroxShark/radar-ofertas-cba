# Radar de Ofertas CBA

Radar de precios de supermercados que **scrapea ofertas y las muestra en una
página web** que abrís cuando querés. Sin notificaciones, sin cuentas, sin
servicios externos: los precios se guardan en un JSON local y la salida es un
`index.html` autocontenido que se puede abrir desde cualquier celular.

## Desarrollo

```bash
make dev    # instala dependencias
make test   # flake8 + pytest
```

## Uso

```bash
python main.py scrape   # scrapea los retailers y guarda precios en data/prices.json
python main.py build    # genera web/index.html con el top de ofertas
python main.py demo      # genera web/index.html con datos de muestra (sin scrapear)
```

Abrí `web/index.html` en el navegador (computadora o celular). La página
permite buscar productos, filtrar por tienda y ordenar por mayor ahorro o
menor precio.

## Cómo funciona

1. **Scrapers** (`scraper/`): cada tienda define su regex y URL; toda la lógica
   común vive en `scraper/base.py`. `scrape_all()` corre todas.
2. **Historial** (`logic/store.py`): los productos se acumulan en
   `data/prices.json`.
3. **Ranking** (`logic/rank.py`): compara cada precio contra el promedio
   histórico del producto y calcula el % de ahorro; devuelve el top.
4. **Web** (`web/render.py`): renderiza un HTML estático y autocontenido con
   las ofertas embebidas (no necesita servidor ni conexión a una API).

> Nota: las URLs de los scrapers (`*.example.com`) son de ejemplo. Para datos
> reales hay que cablear las URLs y selectores de cada tienda. Mientras tanto,
> `python main.py demo` muestra la web con datos de muestra.

## Configuración (opcional)

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DATA_DIR` | Carpeta del historial de precios | `data/` |
| `WEB_DIR` | Carpeta de salida de la web | `web/` |
| `PRICE_WINDOW_DAYS` | Ventana de precios para el ranking | `30` |
| `TOP_N` | Cantidad de ofertas en el top | `20` |
