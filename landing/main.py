import os, re, hmac, sqlite3, datetime as dt
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.getenv("DB_PATH", os.path.join(BASE, "leads.db"))
API_KEY = os.getenv("API_KEY")  # clave que usa el MCP (variable de entorno)
CUPOS_DIA = 2
TIPOS = {"Terreno", "Finca", "Casa", "Local", "Ganado", "Vehículo"}
PROVINCIAS = {"San José", "Alajuela", "Cartago", "Heredia", "Guanacaste", "Puntarenas", "Limón"}

def _dias():
    d, fin, out = dt.date(2026, 11, 23), dt.date(2026, 12, 4), []
    while d <= fin:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out
DIAS = _dias()

def conn():
    c = sqlite3.connect(DB, isolation_level=None)
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, whatsapp TEXT,
        tipo TEXT, provincia TEXT, dia TEXT, creado TEXT)""")
    return c

class Lead(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    whatsapp: str = Field(min_length=8, max_length=20)
    tipo: str
    provincia: str
    dia: str

def requiere_clave(key):
    if not API_KEY:
        raise HTTPException(503, "API_KEY no configurada")
    if not key or not hmac.compare_digest(key, API_KEY):
        raise HTTPException(401, "Clave inválida")

app = FastAPI(title="Avalúo Express")
app.mount("/static", StaticFiles(directory=os.path.join(BASE, "static")), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join(BASE, "static", "index.html"))

def _cupos(c):
    usados = {r["dia"]: r["n"] for r in c.execute("SELECT dia, COUNT(*) n FROM leads GROUP BY dia")}
    return [{"dia": d, "total": CUPOS_DIA, "libres": CUPOS_DIA - usados.get(d, 0)} for d in DIAS]

@app.get("/api/cupos")
def cupos():
    return _cupos(conn())

@app.post("/api/leads", status_code=201)
def crear_lead(l: Lead):
    if not re.fullmatch(r"\+?[\d\s\-]{8,20}", l.whatsapp):
        raise HTTPException(422, "WhatsApp inválido")
    if l.tipo not in TIPOS or l.provincia not in PROVINCIAS or l.dia not in DIAS:
        raise HTTPException(422, "Datos inválidos")
    c = conn()
    c.execute("BEGIN IMMEDIATE")
    try:
        usados = c.execute("SELECT COUNT(*) FROM leads WHERE dia=?", (l.dia,)).fetchone()[0]
        if usados >= CUPOS_DIA:
            c.execute("ROLLBACK")
            raise HTTPException(409, "Ese día ya no tiene cupos. Elige otro.")
        c.execute("INSERT INTO leads(nombre,whatsapp,tipo,provincia,dia,creado) VALUES(?,?,?,?,?,?)",
                  (l.nombre.strip(), l.whatsapp.strip(), l.tipo, l.provincia, l.dia,
                   dt.datetime.now().isoformat(timespec="seconds")))
        c.execute("COMMIT")
    except HTTPException:
        raise
    except Exception:
        c.execute("ROLLBACK")
        raise
    return {"ok": True}

@app.get("/api/leads")
def listar(x_api_key: str = Header(None)):
    requiere_clave(x_api_key)
    return [dict(r) for r in conn().execute("SELECT * FROM leads ORDER BY id DESC")]

@app.get("/api/resumen")
def resumen(x_api_key: str = Header(None)):
    requiere_clave(x_api_key)
    c = conn()
    cu = _cupos(c)
    total = sum(x["total"] for x in cu)
    libres = sum(x["libres"] for x in cu)
    def agrupa(col):
        return {r[0]: r[1] for r in c.execute(f"SELECT {col}, COUNT(*) FROM leads GROUP BY {col}")}
    return {"leads": total - libres, "cupos_totales": total, "cupos_libres": libres,
            "por_tipo": agrupa("tipo"), "por_provincia": agrupa("provincia")}
