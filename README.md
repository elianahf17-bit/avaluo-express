# Avalúo Express

Landing de temporada para **Avalúo Express**: avalúo de propiedades por **₡45.000** en lugar de ₡85.000, con la oferta vigente **hasta el 4 de diciembre**. Los interesados reservan un cupo por día y quedan registrados como *leads*. Un servidor MCP permite consultar la campaña desde Claude.

> **Aviso:** este es un **trabajo académico**. Todos los datos (propiedades, leads, cupos, precios y la campaña en sí) son **ficticios** y no representan un servicio real.

## Estructura

```
avaluo-express/
├── landing/              # Landing + API (FastAPI)
│   ├── main.py           # Endpoints: cupos, leads, resumen
│   ├── static/           # index.html, propiedades.json e imágenes SVG
│   ├── gen_images.py     # Genera las imágenes de ejemplo
│   ├── requirements.txt
│   └── Procfile
├── mcp_server/           # Servidor MCP (FastMCP)
│   ├── server.py         # Herramientas que consultan la API de la landing
│   ├── requirements.txt
│   └── Procfile
└── .env.example          # Nombres de las variables de entorno
```

- **landing**: sirve la página (`/`) y la API: `GET /api/cupos`, `POST /api/leads`, y los protegidos con clave `GET /api/leads` y `GET /api/resumen`. Guarda los leads en una base SQLite local.
- **mcp_server**: expone herramientas MCP que llaman a la API de la landing enviando la clave en el encabezado `X-API-Key`.

## Herramientas del MCP

| Herramienta | Descripción |
|---|---|
| `cupos_por_dia` | Cupos totales y libres de cada día de la campaña Avalúo Express. |
| `listar_leads` | Últimos leads (nombre, WhatsApp, tipo de bien, provincia, día reservado). Parámetro `limite`, 20 por defecto. |
| `resumen_campana` | Resumen: leads, cupos libres y desglose por tipo de bien y provincia. |

## Variables de entorno

Solo se documentan los nombres; nunca se suben valores reales (`.env` está en `.gitignore`). Ver `.env.example`.

| Variable | Usada en | Para qué sirve |
|---|---|---|
| `API_KEY` | landing y mcp_server | Clave que protege los endpoints de leads y resumen. Debe ser la misma en ambos servicios. |
| `LANDING_URL` | mcp_server | URL pública de la landing desplegada. |

## Despliegue en Railway

Se despliegan **dos servicios** desde el mismo repositorio:

1. **Landing**: crear un servicio con *Root Directory* `landing`. Railway instala `requirements.txt` y ejecuta el `Procfile` (`uvicorn main:app --host 0.0.0.0 --port $PORT`). Definir `API_KEY` en *Variables*.
2. **MCP server**: crear otro servicio con *Root Directory* `mcp_server` (el `Procfile` ejecuta `web: python server.py`, que levanta el MCP por HTTP en `0.0.0.0:$PORT`). Definir `API_KEY` (igual que en la landing) y `LANDING_URL` (la URL pública del servicio anterior).

## Ejecución local (opcional)

```powershell
# Landing
cd landing
pip install -r requirements.txt
$env:API_KEY="tu-clave"
uvicorn main:app --reload

# MCP server (en otra terminal)
cd mcp_server
pip install -r requirements.txt
$env:API_KEY="tu-clave"
$env:LANDING_URL="http://localhost:8000"
python server.py
```
