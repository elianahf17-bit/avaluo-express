import os
import httpx
from fastmcp import FastMCP

LANDING_URL = os.environ["LANDING_URL"].rstrip("/")  # URL de la landing en Railway
API_KEY = os.environ["API_KEY"]                      # misma clave que la landing

mcp = FastMCP("Avaluo Express")

def _get(path: str):
    r = httpx.get(f"{LANDING_URL}{path}", headers={"X-API-Key": API_KEY}, timeout=15)
    r.raise_for_status()
    return r.json()

@mcp.tool
def cupos_por_dia() -> list:
    """Cupos totales y libres de cada día de la campaña Avalúo Express."""
    return _get("/api/cupos")

@mcp.tool
def listar_leads(limite: int = 20) -> list:
    """Últimos leads (nombre, WhatsApp, tipo de bien, provincia, día reservado)."""
    return _get("/api/leads")[:limite]

@mcp.tool
def resumen_campana() -> dict:
    """Resumen: leads, cupos libres y desglose por tipo de bien y provincia."""
    return _get("/api/resumen")

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
