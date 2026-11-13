# ARITMA — Belajar Barisan & Deret Aritmetika

Aplikasi web (bisa di-install di HP Android) untuk siswa SMP belajar **Barisan dan Deret
Aritmetika**, dirancang dengan prinsip **Cognitive Load Theory** dari hasil wawancara siswa (S01),
dengan tujuan meningkatkan **Mathematical Literacy**.

- **Backend:** Python + Flask (`app.py`)
- **Frontend:** JavaScript + three.js (ilustrasi 3D), folder `static/`
- **Database:** SQLite (otomatis, lokal) atau Supabase (opsional, gratis)
- **Login:** kode siswa (contoh `S01`)
- **Bahasa:** Indonesia

## Fitur

| Fitur | Dasar dari wawancara |
|---|---|
| Halaman awal + login kode siswa | Etika: identitas siswa memakai kode |
| Materi 5 kartu singkat, contoh dibuka langkah demi langkah | DS03 (tidak bertele-tele), GL03, EL04 |
| Warna: hitam = penjelasan, **merah = rumus**, **biru = pengerjaan** | EL03 |
| Kartu khusus "Uₙ atau Sₙ?" | IL01, IL05, DS02 |
| Lab 3D (three.js): kolom kubus = suku barisan | Membayangkan pola secara visual |
| Kalkulator otomatis + langkah pengerjaan | DS01 |
| Latihan mudah → sulit; pilih rumus dulu, baru hitung; pembahasan bertahap | IL04, IL05, GL02 |
| Soal variasi acak | EL02, GL05 |
| Tes Literasi Matematika (4 indikator, skor per tahap, maks 24) | Kisi-kisi Mathematical Literacy |
| Penanda kuning pada informasi penting soal cerita | EL05 |
| Progres skor per siswa | Evaluasi |

## Cara menjalankan di laptop (VS Code)

1. Install **Python 3.10+** (centang *Add Python to PATH* saat install).
2. Buka folder `literasi-aritmetika` di VS Code → **Terminal → New Terminal**.
3. Jalankan:

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
python app.py
```

4. Muncul link **http://127.0.0.1:5000** → Ctrl+klik untuk membuka.

> Node.js/npm **tidak wajib**: three.js dimuat langsung dari CDN.

## Membuka di HP Android

**Cara cepat (satu Wi-Fi):** cari IP laptop dengan perintah `ipconfig` (lihat *IPv4 Address*,
misal `192.168.1.7`), lalu buka `http://192.168.1.7:5000` di Chrome HP. Jika tidak bisa, izinkan
Python di Windows Firewall.

**Link online (untuk presentasi):** deploy gratis ke [Render](https://render.com):
1. Upload proyek ke GitHub (lihat di bawah).
2. Render → *New → Web Service* → pilih repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Selesai → dapat link `https://nama-app.onrender.com`.

**Jadi "aplikasi" di HP:** buka link di Chrome Android → menu ⋮ → **Tambahkan ke layar utama /
Install aplikasi**. Ikon ARITMA muncul seperti aplikasi biasa.

## Upload ke GitHub

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Aplikasi ARITMA"
```

Lalu buat repository baru di github.com, dan ikuti perintah `git remote add origin ...` dan
`git push -u origin main` yang ditampilkan GitHub. Bagikan link repo ke dosen.

## Supabase (opsional)

Tanpa Supabase, data tersimpan di `data.db` (SQLite). Di Render, file ini bisa hilang saat server
restart, jadi untuk data permanen pakai Supabase:

1. Buat proyek di supabase.com → **SQL Editor** → jalankan isi `supabase.sql`.
2. Ambil *Project URL* dan *anon key* (Settings → API).
3. Isi environment variable `SUPABASE_URL` dan `SUPABASE_KEY` (di Render: *Environment*).

## Struktur folder

```
literasi-aritmetika/
├── app.py            # server Flask + API
├── content.py        # materi, latihan, soal literasi, kalkulator
├── database.py       # SQLite / Supabase
├── requirements.txt
├── supabase.sql
├── docs/kisi-kisi-soal.md
└── static/
    ├── index.html
    ├── css/style.css
    ├── js/app.js       # logika tampilan
    ├── js/scene3d.js   # ilustrasi 3D three.js
    ├── manifest.json, sw.js, icon.svg   # agar bisa di-install di Android
```

## API singkat

| Method | URL | Fungsi |
|---|---|---|
| POST | `/api/login` | `{kode, nama, kelas}` |
| GET | `/api/materi` | daftar kartu materi |
| GET | `/api/latihan` · `/api/latihan/acak` | soal latihan / soal variasi |
| POST | `/api/hitung` | `{a, b, n}` → Uₙ, Sₙ + langkah |
| GET | `/api/literasi` | soal tes (tanpa kunci) |
| POST | `/api/literasi/nilai` | `{kode, jawaban}` → skor per tahap |
| POST | `/api/skor` · GET `/api/progres/<kode>` | simpan & lihat skor |
