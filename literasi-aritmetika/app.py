"""
ARITMA — Aplikasi belajar Barisan & Deret Aritmetika untuk siswa SMP.
Backend : Python (Flask)  |  Frontend : JavaScript + three.js (folder static/)

Jalankan:
    pip install -r requirements.txt
    python app.py
Lalu buka http://127.0.0.1:5000  (atau http://<IP-laptop>:5000 dari HP Android di Wi-Fi yang sama)
"""
import os
import re

from flask import Flask, jsonify, request, send_from_directory

import database as db
from content import LATIHAN, LITERASI, MATERI, hitung, soal_acak

app = Flask(__name__, static_folder="static", static_url_path="")
db.init_db()


def parse_angka(teks):
    """Ubah input siswa jadi angka. Menerima '1.350.000', 'Rp 1.350.000', '0,5', '-3'."""
    if teks is None:
        return None
    s = str(teks).lower().replace("rp", "").replace(" ", "").strip()
    if not s:
        return None
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif s.count(".") > 1 or re.fullmatch(r"-?\d{1,3}\.\d{3}", s):
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def kode_valid(kode):
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{2,20}", kode or ""))


# ------------------------------------------------------------------ Halaman
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ------------------------------------------------------------------ API
@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    kode = (data.get("kode") or "").strip().upper()
    if not kode_valid(kode):
        return jsonify(error="Kode siswa 2–20 huruf/angka, contoh: S01"), 400
    siswa = db.simpan_siswa(kode, (data.get("nama") or "").strip()[:60],
                            (data.get("kelas") or "").strip()[:10])
    return jsonify(siswa=siswa)


@app.get("/api/materi")
def materi():
    return jsonify(MATERI)


@app.get("/api/latihan")
def latihan():
    return jsonify(LATIHAN)


@app.get("/api/latihan/acak")
def latihan_acak():
    return jsonify(soal_acak())


@app.post("/api/hitung")
def api_hitung():
    data = request.get_json(silent=True) or {}
    a, b, n = parse_angka(data.get("a")), parse_angka(data.get("b")), parse_angka(data.get("n"))
    if a is None or b is None or n is None or n < 1 or n != int(n) or n > 10000:
        return jsonify(error="Isi a dan b dengan angka, n bilangan bulat 1–10000."), 400
    a = int(a) if a.is_integer() else a
    b = int(b) if b.is_integer() else b
    return jsonify(hitung(a, b, int(n)))


@app.get("/api/literasi")
def literasi():
    """Soal tes tanpa kunci jawaban."""
    hasil = []
    for s in LITERASI:
        s2 = {k: v for k, v in s.items() if k != "pembahasan"}
        s2["tahap"] = [{k: v for k, v in t.items() if k != "kunci"} for t in s["tahap"]]
        hasil.append(s2)
    return jsonify(hasil)


@app.post("/api/literasi/nilai")
def nilai_literasi():
    """Penskoran per tahap (skor parsial tetap diberikan)."""
    data = request.get_json(silent=True) or {}
    jawaban = data.get("jawaban") or {}          # {"1": ["1", "190000", ...], ...}
    per_soal, total, maks = [], 0, 0
    for s in LITERASI:
        jaw = jawaban.get(str(s["id"])) or []
        rinci, skor = [], 0
        for i, t in enumerate(s["tahap"]):
            j = jaw[i] if i < len(jaw) else None
            if t["tipe"] == "angka":
                v = parse_angka(j)
                benar = v is not None and abs(v - t["kunci"]) < 1e-6
            else:
                benar = str(j) == str(t["kunci"])
            dapat = t["skor"] if benar else 0
            skor += dapat
            rinci.append({"benar": benar, "skor": dapat, "maks": t["skor"]})
        m = sum(t["skor"] for t in s["tahap"])
        total, maks = total + skor, maks + m
        per_soal.append({"id": s["id"], "indikator": s["indikator"], "skor": skor, "maks": m,
                         "tahap": rinci, "pembahasan": s["pembahasan"]})
    kode = (data.get("kode") or "").strip().upper()
    if kode_valid(kode):
        db.simpan_skor(kode, "literasi", total, maks,
                       {p["indikator"]: p["skor"] for p in per_soal})
    return jsonify(total=total, maks=maks, per_soal=per_soal)


@app.post("/api/skor")
def simpan_skor():
    data = request.get_json(silent=True) or {}
    kode = (data.get("kode") or "").strip().upper()
    if not kode_valid(kode):
        return jsonify(error="kode tidak valid"), 400
    db.simpan_skor(kode, str(data.get("jenis", "latihan"))[:20],
                   float(data.get("skor", 0)), float(data.get("maks", 0)), data.get("detail") or {})
    return jsonify(ok=True)


@app.get("/api/progres/<kode>")
def progres(kode):
    if not kode_valid(kode):
        return jsonify(error="kode tidak valid"), 400
    return jsonify(db.ambil_progres(kode.upper()))


@app.get("/api/health")
def health():
    return jsonify(status="ok", database="supabase" if db.USE_SUPABASE else "sqlite")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("\n  ARITMA berjalan!")
    print(f"  Buka di laptop : http://127.0.0.1:{port}")
    print(f"  Buka di HP     : http://<IP-laptop>:{port}  (HP & laptop satu Wi-Fi)\n")
    app.run(host="0.0.0.0", port=port, debug=True)
