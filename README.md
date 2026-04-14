# Polymarket Cortex

Repositorio base para explorar Polymarket, consumir mercado público, guardar snapshots en SQLite y construir una primera capa de features y scoring.

## Requisitos

- Python 3.10+
- Windows PowerShell o terminal equivalente
- Acceso a Internet para consultar los endpoints públicos de Polymarket

## Instalación

1. Crear y activar el entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Revisar o crear el archivo `.env` con la configuración base:

```env
POLY_GAMMA_HOST=https://gamma-api.polymarket.com
POLY_DATA_HOST=https://data-api.polymarket.com
POLY_CLOB_HOST=https://clob.polymarket.com
DATABASE_URL=sqlite:///data/trading.db
```

## Ejecución

### Consultas y consola base

```powershell
python -m apps.operator_console.find_markets
python -m apps.operator_console.get_market_by_slug
python -m apps.operator_console.check_clob_public
python -m apps.operator_console.show_last_snapshots
```

### Collector en vivo

```powershell
python -m services.market_data.collector
```

### Capa Cortex

```powershell
python -m services.strategy_engine.process_features
python -m apps.operator_console.show_feature_snapshots
python -m apps.operator_console.feature_summary
```

### Depuración WS

```powershell
python -m apps.operator_console.debug_ws_raw
python -m apps.operator_console.debug_ws_raw_to_file
python -m apps.operator_console.inspect_ws_raw_file
```

### Utilidades de cobertura y reset

```powershell
python -m apps.operator_console.check_size_coverage
python -m apps.operator_console.reset_feature_snapshots
python -m services.market_data.rest_snapshot
```

## Estructura del proyecto

- `apps/operator_console/` consola y utilidades de inspección
- `libs/polymarket_client/` cliente REST y WS de Polymarket
- `libs/storage/` capa SQLite
- `libs/cortex_core/` features, scoring y clasificación
- `services/market_data/` collector y helpers de datos
- `services/strategy_engine/` procesamiento histórico de features
- `data/` base de datos, raw dumps y artefactos locales

## Qué se hizo por día

### Día 1

- Se montó el proyecto base.
- Se creó el entorno virtual y la instalación de dependencias.
- Se añadió el archivo `.env` con hosts públicos y la base SQLite.
- Se implementó un cliente REST mínimo para Polymarket.
- Se crearon scripts para listar mercados, resolver mercados por slug y comprobar endpoints públicos.

### Día 2

- Se añadió soporte para WebSocket público de mercado.
- Se implementó suscripción por `clobTokenIds`.
- Se creó el collector con persistencia en SQLite.
- Se implementó un parser tolerante para snapshots de libro.
- Se creó una consola para ver snapshots recientes.
- Se añadió un debugger WS crudo y soporte de keepalive `PING`.

### Día 3

- Se añadió la primera capa de Cortex.
- Se creó la tabla `feature_snapshots`.
- Se implementaron `phi_features`, `kappa_scoring` y `lambda_validation`.
- Se creó el procesador histórico de snapshots.
- Se añadieron consolas para ver clasificaciones y resúmenes agregados.
- El sistema quedó clasificando snapshots en `NO_TRADE`, `WATCH` e `INTERESTING`.

### Día 3.5

- Se endureció el parser para aceptar más variantes de payload.
- Se añadió un dumper de mensajes raw del WS a `data/raw/ws/`.
- Se añadió un inspector de raw guardados.
- Se creó un snapshot REST opcional para complementar el libro.
- Se añadieron utilidades para medir cobertura de tamaños y vaciar features antes de reprocesar.

## Estado actual

- El market collector arranca y guarda snapshots.
- La capa Cortex procesa snapshots históricos y genera clasificaciones.
- Los tamaños de libro (`bid_size` y `ask_size`) todavía pueden faltar en algunos caminos, así que la clasificación actual se apoya sobre todo en `spread` y `midpoint`.
- El flujo está listo para seguir refinando la microestructura antes de pasar a ejecución operativa.

## Notas

- El mercado usado para las pruebas ha sido `btc-updown-5m-1776181500`.
- Las utilidades de depuración raw están pensadas para revisar la forma real de los mensajes WS antes de endurecer más el parser.