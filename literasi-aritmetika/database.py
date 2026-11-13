"""
Penyimpanan data siswa & skor.

- Default  : SQLite lokal (file data.db) -> langsung jalan tanpa setting apa pun.
- Opsional : Supabase (hosting gratis). Isi environment variable
             SUPABASE_URL dan SUPABASE_KEY, maka data otomatis disimpan ke Supabase.
"""
import json
import os
import sqlite3
import urllib.request
from datetime import datetime, timezone

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")


def _now():
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------- Supabase
def _sb(method, path, body=None):
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation,resolution=merge-duplicates",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        txt = r.read().decode()
        return json.loads(txt) if txt else []


# ---------------------------------------------------------------- SQLite
def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    if USE_SUPABASE:
        return
    with _conn() as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS siswa(
                kode TEXT PRIMARY KEY, nama TEXT, kelas TEXT, dibuat TEXT)"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS skor(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kode TEXT, jenis TEXT, skor REAL, maks REAL,
                detail TEXT, waktu TEXT)"""
        )


def simpan_siswa(kode, nama, kelas):
    data = {"kode": kode, "nama": nama, "kelas": kelas, "dibuat": _now()}
    if USE_SUPABASE:
        _sb("POST", "siswa?on_conflict=kode", data)
        return data
    with _conn() as c:
        lama = c.execute("SELECT * FROM siswa WHERE kode=?", (kode,)).fetchone()
        if lama:
            if nama:
                c.execute("UPDATE siswa SET nama=?, kelas=? WHERE kode=?", (nama, kelas, kode))
            return dict(c.execute("SELECT * FROM siswa WHERE kode=?", (kode,)).fetchone())
        c.execute("INSERT INTO siswa VALUES(?,?,?,?)", (kode, nama, kelas, data["dibuat"]))
    return data


def simpan_skor(kode, jenis, skor, maks, detail):
    data = {"kode": kode, "jenis": jenis, "skor": skor, "maks": maks,
            "detail": json.dumps(detail), "waktu": _now()}
    if USE_SUPABASE:
        _sb("POST", "skor", data)
        return data
    with _conn() as c:
        c.execute(
            "INSERT INTO skor(kode,jenis,skor,maks,detail,waktu) VALUES(?,?,?,?,?,?)",
            (kode, jenis, skor, maks, data["detail"], data["waktu"]),
        )
    return data


def ambil_progres(kode):
    if USE_SUPABASE:
        rows = _sb("GET", f"skor?kode=eq.{urllib.request.quote(kode)}&order=waktu.desc")
    else:
        with _conn() as c:
            rows = [dict(r) for r in c.execute(
                "SELECT * FROM skor WHERE kode=? ORDER BY waktu DESC", (kode,))]
    for r in rows:
        try:
            r["detail"] = json.loads(r.get("detail") or "{}")
        except (TypeError, ValueError):
            pass
    return rows
