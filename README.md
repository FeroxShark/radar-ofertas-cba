# Radar de Ofertas CBA

Radar de precios de supermercados que **scrapea ofertas reales y las muestra en
una página web** que abrís cuando querés. Sin notificaciones, sin cuentas, sin
base de datos: los precios se guardan en un JSON local y la salida es un
`index.html` autocontenido que se abre desde cualquier celular.

Las tiendas soportadas (Carrefour y Día) corren sobre **VTEX**, que expone una
API pública de catálogo. De ahí salen el precio actual y el **precio de lista**,
así que el % de descuento es real (no estimado).

## Desarrollo

```bash
make dev    # instala dependencias
make test   # flake8 + pytest
```

## Uso

```bash
python main.py scrape   # scrapea Carrefour y Día (datos REALES) -> data/prices.json
python main.py build    # genera web/index.html con las mejores ofertas
python main.py demo     # genera la web con datos de muestra (sin red)
```

Después abrí `web/index.html` en el navegador. La página permite buscar
productos, filtrar por tienda y ordenar por mayor descuento o menor precio.

> **Nota sobre la red:** `scrape` necesita salida a internet hacia los sitios de
> las tiendas. Corré `python main.py scrape` desde tu máquina (o un servidor con
> red abierta). En entornos con allowlist de red no va a poder conectarse.

## Cómo funciona

1. **Tiendas** (`scraper/__init__.py`): registro de hosts VTEX + canasta de
   términos a buscar (`DEFAULT_TERMS`).
2. **Cliente VTEX** (`scraper/vtex.py`): consulta la API de catálogo y extrae
   precio, precio de lista, marca y link de cada producto disponible.
3. **Historial** (`logic/store.py`): los productos se guardan en
   `data/prices.json`.
4. **Ranking** (`logic/rank.py`): calcula el descuento real (precio vs precio de
   lista) y devuelve las mejores ofertas.
5. **Web** (`web/render.py`): renderiza un HTML estático y autocontenido con las
   ofertas embebidas (no necesita servidor ni API).

## Agregar / cambiar tiendas y productos

- Tiendas: editá `STORES` en `scraper/__init__.py` (cualquier tienda VTEX anda
  con su host base).
- Productos a buscar: editá `DEFAULT_TERMS` en el mismo archivo.

## Configuración (opcional)

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DATA_DIR` | Carpeta del historial de precios | `data/` |
| `WEB_DIR` | Carpeta de salida de la web | `web/` |
| `PRICE_WINDOW_DAYS` | Ventana de tiempo para considerar precios | `30` |
| `TOP_N` | Cantidad de ofertas en el top | `20` |
