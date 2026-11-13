"""
Isi pembelajaran: Barisan dan Deret Aritmetika (SMP).

Prinsip Cognitive Load (dari hasil wawancara S01):
- Teks singkat, satu ide per kartu (DS03, EL04)
- Warna: hitam = penjelasan, MERAH = rumus, BIRU = pengerjaan (EL03)
- Contoh soal dibuka langkah demi langkah (GL03, IL02)
- Selalu pilih rumus dulu: Un atau Sn? (IL01, IL05, DS02)
- Soal cerita kehidupan sehari-hari + penanda Diketahui/Ditanya (EL05, GL01)
- Latihan mudah -> sulit dan variasi soal (IL04, GL05, EL02)
"""
import random

# ------------------------------------------------------------------ MATERI
MATERI = [
    {
        "id": 1,
        "judul": "Pola & Beda",
        "ikon": "🔢",
        "penjelasan": "Barisan aritmetika adalah urutan bilangan yang selalu bertambah "
                      "(atau berkurang) dengan angka yang SAMA. Angka itu disebut beda (b).",
        "rumus": "b = U₂ − U₁",
        "contoh": {
            "soal": "Barisan: 12, 14, 16, 18, … Berapa bedanya?",
            "langkah": [
                "Ambil dua suku berurutan: 14 dan 12.",
                "b = 14 − 12 = 2",
                "Cek: 16 − 14 = 2 ✔. Jadi beda = 2.",
            ],
        },
        "ingat": "Beda bisa negatif. Contoh 20, 17, 14 → b = −3.",
    },
    {
        "id": 2,
        "judul": "Suku ke-n (Uₙ)",
        "ikon": "🎯",
        "penjelasan": "Uₙ adalah SATU bilangan pada urutan ke-n. "
                      "Pakai Uₙ jika yang ditanya \"suku ke-…\", \"hari ke-…\", \"baris ke-…\".",
        "rumus": "Uₙ = a + (n − 1) × b",
        "contoh": {
            "soal": "Barisan 5, 8, 11, … Tentukan suku ke-10.",
            "langkah": [
                "Diketahui: a = 5, b = 8 − 5 = 3, n = 10.",
                "Ditanya: U₁₀ (satu suku) → pakai rumus Uₙ.",
                "U₁₀ = 5 + (10 − 1) × 3",
                "U₁₀ = 5 + 27 = 32",
            ],
        },
        "ingat": "a = suku pertama, b = beda, n = urutan suku.",
    },
    {
        "id": 3,
        "judul": "Jumlah n Suku (Sₙ)",
        "ikon": "➕",
        "penjelasan": "Deret aritmetika adalah PENJUMLAHAN suku-suku barisan. "
                      "Pakai Sₙ jika yang ditanya \"jumlah\", \"total\", \"seluruhnya\".",
        "rumus": "Sₙ = n/2 × (2a + (n − 1) × b)   atau   Sₙ = n/2 × (a + Uₙ)",
        "contoh": {
            "soal": "Hitung jumlah 10 suku pertama dari 5, 8, 11, …",
            "langkah": [
                "Diketahui: a = 5, b = 3, n = 10.",
                "Ditanya: jumlah (total) → pakai rumus Sₙ.",
                "S₁₀ = 10/2 × (2×5 + 9×3)",
                "S₁₀ = 5 × (10 + 27) = 5 × 37 = 185",
            ],
        },
        "ingat": "Sₙ selalu lebih besar dari Uₙ (jika suku-sukunya positif), karena Sₙ adalah total.",
    },
    {
        "id": 4,
        "judul": "Uₙ atau Sₙ?",
        "ikon": "🤔",
        "penjelasan": "Jangan tertukar! Baca kata kunci pada pertanyaan sebelum memilih rumus.",
        "rumus": "\"ke-…\" → Uₙ     |     \"jumlah / total\" → Sₙ",
        "contoh": {
            "soal": "Ani menabung Rp2.000 pada hari pertama, lalu naik Rp1.000 tiap hari. "
                    "(a) Berapa tabungan pada hari ke-7? (b) Berapa total tabungan 7 hari?",
            "langkah": [
                "(a) \"hari ke-7\" → satu nilai → Uₙ.",
                "U₇ = 2.000 + 6 × 1.000 = 8.000",
                "(b) \"total 7 hari\" → dijumlahkan → Sₙ.",
                "S₇ = 7/2 × (2.000 + 8.000) = 3,5 × 10.000 = 35.000",
            ],
        },
        "ingat": "Uₙ = satu kotak. Sₙ = semua kotak digabung.",
    },
    {
        "id": 5,
        "judul": "Strategi Soal Cerita",
        "ikon": "📖",
        "penjelasan": "Soal panjang? Pakai 5 langkah DITA-RS: Diketahui, Ditanya, "
                      "pilih Rumus, hitung (Selesaikan), lalu Simpulkan.",
        "rumus": "Diketahui → Ditanya → Rumus → Hitung → Simpulkan",
        "contoh": {
            "soal": "Gedung pertunjukan: baris pertama 15 kursi, tiap baris berikutnya bertambah "
                    "2 kursi. Ada 12 baris. Berapa kursi seluruhnya?",
            "langkah": [
                "Diketahui: a = 15, b = 2, n = 12.",
                "Ditanya: kursi SELURUHNYA → total.",
                "Rumus: Sₙ = n/2 × (2a + (n − 1)b).",
                "S₁₂ = 6 × (30 + 22) = 6 × 52 = 312",
                "Simpulkan: jumlah kursi seluruhnya 312 kursi.",
            ],
        },
        "ingat": "Garis bawahi angka & kata tanya. Abaikan informasi yang tidak dipakai.",
    },
]

# ------------------------------------------------------------------ LATIHAN (mudah -> sulit)
LATIHAN = [
    {"id": 1, "level": "Mudah", "soal": "Tentukan beda barisan 7, 11, 15, 19, …",
     "diketahui": ["U₁ = 7", "U₂ = 11"], "ditanya": "beda (b)", "rumus": "b",
     "jawaban": 4, "satuan": "",
     "langkah": ["b = U₂ − U₁", "b = 11 − 7 = 4"]},
    {"id": 2, "level": "Mudah", "soal": "Tentukan suku ke-8 dari barisan 3, 5, 7, …",
     "diketahui": ["a = 3", "b = 2", "n = 8"], "ditanya": "suku ke-8", "rumus": "Un",
     "jawaban": 17, "satuan": "",
     "langkah": ["U₈ = a + (n − 1)b", "U₈ = 3 + 7 × 2", "U₈ = 3 + 14 = 17"]},
    {"id": 3, "level": "Mudah", "soal": "Hitung jumlah 6 suku pertama dari 2, 4, 6, …",
     "diketahui": ["a = 2", "b = 2", "n = 6"], "ditanya": "jumlah 6 suku", "rumus": "Sn",
     "jawaban": 42, "satuan": "",
     "langkah": ["S₆ = n/2 × (2a + (n − 1)b)", "S₆ = 3 × (4 + 10)", "S₆ = 3 × 14 = 42"]},
    {"id": 4, "level": "Sedang",
     "soal": "Dina menabung Rp5.000 pada minggu pertama. Setiap minggu tabungannya naik Rp2.000. "
             "Berapa uang yang ditabung Dina pada minggu ke-10?",
     "diketahui": ["a = 5.000", "b = 2.000", "n = 10"], "ditanya": "tabungan minggu ke-10",
     "rumus": "Un", "jawaban": 23000, "satuan": "rupiah",
     "langkah": ["Kata kunci \"minggu ke-10\" → Uₙ", "U₁₀ = 5.000 + 9 × 2.000",
                 "U₁₀ = 5.000 + 18.000 = 23.000"]},
    {"id": 5, "level": "Sedang",
     "soal": "Sebuah aula memiliki 10 baris kursi. Baris pertama ada 12 kursi dan setiap baris "
             "berikutnya bertambah 3 kursi. Berapa jumlah kursi di aula itu?",
     "diketahui": ["a = 12", "b = 3", "n = 10"], "ditanya": "jumlah seluruh kursi",
     "rumus": "Sn", "jawaban": 255, "satuan": "kursi",
     "langkah": ["Kata kunci \"jumlah kursi\" → Sₙ", "S₁₀ = 5 × (2×12 + 9×3)",
                 "S₁₀ = 5 × (24 + 27) = 5 × 51 = 255"]},
    {"id": 6, "level": "Sedang",
     "soal": "Tumpukan kaleng di toko: lapisan paling atas 4 kaleng, lapisan di bawahnya selalu "
             "2 kaleng lebih banyak. Berapa kaleng pada lapisan ke-9 dari atas?",
     "diketahui": ["a = 4", "b = 2", "n = 9"], "ditanya": "kaleng lapisan ke-9",
     "rumus": "Un", "jawaban": 20, "satuan": "kaleng",
     "langkah": ["\"lapisan ke-9\" → Uₙ", "U₉ = 4 + 8 × 2 = 20"]},
    {"id": 7, "level": "Sulit",
     "soal": "Pak Budi memproduksi kerupuk. Hari pertama 40 bungkus, hari ke-2 45 bungkus, "
             "hari ke-3 50 bungkus, dan seterusnya. Berapa total bungkus selama 14 hari?",
     "diketahui": ["a = 40", "b = 5", "n = 14"], "ditanya": "total 14 hari",
     "rumus": "Sn", "jawaban": 1015, "satuan": "bungkus",
     "langkah": ["b = 45 − 40 = 5", "\"total\" → Sₙ", "S₁₄ = 7 × (2×40 + 13×5)",
                 "S₁₄ = 7 × (80 + 65) = 7 × 145 = 1.015"]},
    {"id": 8, "level": "Sulit",
     "soal": "Suku ke-3 suatu barisan aritmetika adalah 14 dan suku ke-7 adalah 30. "
             "Tentukan suku ke-20.",
     "diketahui": ["U₃ = 14 → a + 2b = 14", "U₇ = 30 → a + 6b = 30"], "ditanya": "suku ke-20",
     "rumus": "Un", "jawaban": 82, "satuan": "",
     "langkah": ["Kurangkan: (a + 6b) − (a + 2b) = 30 − 14", "4b = 16 → b = 4",
                 "a + 2×4 = 14 → a = 6", "U₂₀ = 6 + 19 × 4 = 6 + 76 = 82"]},
]

# ------------------------------------------------------------------ TES MATHEMATICAL LITERACY
# Mengikuti struktur kisi-kisi: 4 indikator, skor per tahap, maks 6 per soal (total 24).
LITERASI = [
    {
        "id": 1,
        "indikator": "Mathematical Reasoning",
        "deskripsi": "Membandingkan alternatif, memberi alasan, dan menentukan keputusan.",
        "judul": "Memilih Rencana Menabung",
        "soal": "Rina ingin menabung selama 10 minggu. Rencana A: minggu pertama Rp10.000, lalu "
                "setiap minggu naik Rp2.000. Rencana B: setiap minggu tetap Rp15.000. "
                "Rina ingin total tabungannya sebanyak mungkin. Rencana mana yang sebaiknya "
                "dipilih Rina? Jelaskan alasan matematismu.",
        "penting": ["10 minggu", "Rp10.000", "naik Rp2.000", "tetap Rp15.000", "total tabungan"],
        "tahap": [
            {"teks": "Tahap 1 — Yang harus dibandingkan adalah …", "tipe": "pilihan",
             "opsi": ["Tabungan minggu ke-10 saja", "TOTAL tabungan 10 minggu tiap rencana",
                      "Tabungan minggu pertama"], "kunci": 1, "skor": 1},
            {"teks": "Tahap 2a — Total tabungan Rencana A (S₁₀) = Rp …", "tipe": "angka",
             "kunci": 190000, "skor": 1},
            {"teks": "Tahap 2b — Total tabungan Rencana B = Rp …", "tipe": "angka",
             "kunci": 150000, "skor": 1},
            {"teks": "Tahap 3 — Selisih total A dan B = Rp …", "tipe": "angka",
             "kunci": 40000, "skor": 1},
            {"teks": "Tahap 4 — Keputusan: Rina sebaiknya memilih …", "tipe": "pilihan",
             "opsi": ["Rencana A", "Rencana B", "Sama saja"], "kunci": 0, "skor": 1},
            {"teks": "Tahap 5 — Alasan yang tepat:", "tipe": "pilihan",
             "opsi": ["Karena minggu pertama A lebih kecil",
                      "Karena total A lebih besar Rp40.000 walaupun awalnya lebih kecil",
                      "Karena B nilainya tetap sehingga lebih mudah"], "kunci": 1, "skor": 1},
        ],
        "pembahasan": [
            "Yang dibandingkan adalah TOTAL 10 minggu, bukan satu minggu.",
            "A: S₁₀ = 10/2 × (2×10.000 + 9×2.000) = 5 × 38.000 = Rp190.000",
            "B: 10 × 15.000 = Rp150.000",
            "Selisih: 190.000 − 150.000 = Rp40.000",
            "Pilih Rencana A, karena totalnya lebih besar walaupun minggu awalnya lebih kecil.",
        ],
    },
    {
        "id": 2,
        "indikator": "Formulating Situations Mathematically",
        "deskripsi": "Mengidentifikasi informasi relevan dan mengubah situasi menjadi model matematika.",
        "judul": "Kursi Gedung Pertunjukan",
        "soal": "Sebuah gedung pertunjukan memiliki 15 baris kursi. Baris pertama berisi 20 kursi "
                "dan setiap baris berikutnya bertambah 4 kursi. Gedung dicat ulang tahun 2020. "
                "Panitia sudah menjual 700 tiket. Apakah kursi di gedung cukup untuk semua "
                "penonton? Ubah situasi ini menjadi model matematika, lalu selesaikan.",
        "penting": ["15 baris", "20 kursi", "bertambah 4 kursi", "700 tiket"],
        "tahap": [
            {"teks": "Tahap 1 — Suku pertama (a) = …", "tipe": "angka", "kunci": 20, "skor": 1},
            {"teks": "Tahap 2 — Beda (b) = …", "tipe": "angka", "kunci": 4, "skor": 1},
            {"teks": "Tahap 3 — Banyak suku (n) = …", "tipe": "angka", "kunci": 15, "skor": 1},
            {"teks": "Tahap 4 — Model matematika yang tepat:", "tipe": "pilihan",
             "opsi": ["U₁₅ = 20 + 14 × 4", "S₁₅ = 15/2 × (2×20 + 14×4)", "700 ÷ 15"],
             "kunci": 1, "skor": 1},
            {"teks": "Tahap 5 — Jumlah seluruh kursi = …", "tipe": "angka", "kunci": 720, "skor": 1},
            {"teks": "Tahap 6 — Kesimpulan:", "tipe": "pilihan",
             "opsi": ["Tidak cukup, kurang 20 kursi", "Cukup, masih sisa 20 kursi",
                      "Cukup, sisa 76 kursi"], "kunci": 1, "skor": 1},
        ],
        "pembahasan": [
            "Informasi \"dicat tahun 2020\" tidak dipakai (informasi pengecoh).",
            "a = 20, b = 4, n = 15. Ditanya total kursi → Sₙ.",
            "S₁₅ = 15/2 × (40 + 56) = 15/2 × 96 = 720 kursi",
            "720 ≥ 700 → cukup, sisa 720 − 700 = 20 kursi.",
        ],
    },
    {
        "id": 3,
        "indikator": "Employing Mathematical Concepts, Facts, and Procedures",
        "deskripsi": "Memilih dan menggunakan konsep serta prosedur untuk memperoleh solusi.",
        "judul": "Produksi Kue",
        "soal": "Bu Sari membuat kue untuk dijual. Hari pertama ia membuat 30 kue, hari kedua 35 kue, "
                "hari ketiga 40 kue, dan seterusnya. Keuntungan setiap kue Rp1.500. Berapa kue yang "
                "dibuat pada hari ke-12, berapa total kue selama 12 hari, dan berapa total "
                "keuntungannya? Tunjukkan langkah perhitunganmu.",
        "penting": ["30 kue", "35 kue", "hari ke-12", "total kue selama 12 hari", "Rp1.500"],
        "tahap": [
            {"teks": "Tahap 1 — Beda (b) = …", "tipe": "angka", "kunci": 5, "skor": 1},
            {"teks": "Tahap 2 — Kue hari ke-12 (U₁₂) = …", "tipe": "angka", "kunci": 85, "skor": 2},
            {"teks": "Tahap 3 — Total kue 12 hari (S₁₂) = …", "tipe": "angka", "kunci": 690, "skor": 2},
            {"teks": "Tahap 4 — Total keuntungan = Rp …", "tipe": "angka", "kunci": 1035000, "skor": 1},
        ],
        "pembahasan": [
            "b = 35 − 30 = 5",
            "U₁₂ = 30 + 11 × 5 = 85 kue",
            "S₁₂ = 12/2 × (30 + 85) = 6 × 115 = 690 kue",
            "Keuntungan = 690 × 1.500 = Rp1.035.000",
        ],
    },
    {
        "id": 4,
        "indikator": "Interpreting, Applying, and Evaluating Mathematical Outcomes",
        "deskripsi": "Menafsirkan hasil dalam konteks, menilai kewajaran, dan mengambil keputusan.",
        "judul": "Menabung untuk Sepeda",
        "soal": "Doni menabung Rp50.000 pada bulan pertama, lalu setiap bulan tabungannya naik "
                "Rp25.000. Ia ingin membeli sepeda seharga Rp1.500.000. Temannya menghitung: "
                "50.000 + (n − 1) × 25.000 = 1.500.000, sehingga n = 59. Temannya menyimpulkan "
                "Doni harus menabung 59 bulan. Apakah kamu setuju? Tentukan berapa bulan "
                "sebenarnya Doni harus menabung dan jelaskan alasanmu.",
        "penting": ["Rp50.000", "naik Rp25.000", "Rp1.500.000", "n = 59"],
        "tahap": [
            {"teks": "Tahap 1 — Pendapatmu tentang cara teman Doni:", "tipe": "pilihan",
             "opsi": ["Setuju, rumusnya sudah benar",
                      "Tidak setuju, harga sepeda dibandingkan dengan TOTAL tabungan (Sₙ), bukan Uₙ",
                      "Tidak setuju, seharusnya dibagi 25.000"], "kunci": 1, "skor": 1},
            {"teks": "Tahap 2 — Total tabungan 9 bulan (S₉) = Rp …", "tipe": "angka",
             "kunci": 1350000, "skor": 1},
            {"teks": "Tahap 3 — Kekurangan uang setelah 9 bulan = Rp …", "tipe": "angka",
             "kunci": 150000, "skor": 1},
            {"teks": "Tahap 4 — Total tabungan 10 bulan (S₁₀) = Rp …", "tipe": "angka",
             "kunci": 1625000, "skor": 1},
            {"teks": "Tahap 5 — Doni minimal menabung … bulan", "tipe": "angka", "kunci": 10, "skor": 1},
            {"teks": "Tahap 6 — Sisa uang setelah membeli sepeda = Rp …", "tipe": "angka",
             "kunci": 125000, "skor": 1},
        ],
        "pembahasan": [
            "Teman Doni keliru: ia memakai Uₙ (tabungan satu bulan), padahal uang sepeda "
            "berasal dari TOTAL tabungan → Sₙ.",
            "S₉ = 9/2 × (100.000 + 8×25.000) = 4,5 × 300.000 = Rp1.350.000 (belum cukup)",
            "Kurang 1.500.000 − 1.350.000 = Rp150.000",
            "S₁₀ = 5 × (100.000 + 9×25.000) = 5 × 325.000 = Rp1.625.000 (cukup)",
            "Jadi cukup 10 bulan, sisa 1.625.000 − 1.500.000 = Rp125.000. Hasil 59 bulan tidak wajar.",
        ],
    },
]

# ------------------------------------------------------------------ Soal acak (variasi, GL05)
KONTEKS_ACAK = [
    ("Siti menabung Rp{a} pada hari pertama, lalu setiap hari bertambah Rp{b}.",
     "Berapa uang yang ditabung pada hari ke-{n}?", "Berapa total tabungan selama {n} hari?", "rupiah", 1000),
    ("Baris pertama sebuah stadion mini berisi {a} kursi, dan setiap baris berikutnya bertambah {b} kursi.",
     "Berapa kursi pada baris ke-{n}?", "Berapa jumlah kursi pada {n} baris pertama?", "kursi", 1),
    ("Andi berlatih push-up. Hari pertama {a} kali, setiap hari bertambah {b} kali.",
     "Berapa push-up pada hari ke-{n}?", "Berapa total push-up selama {n} hari?", "kali", 1),
    ("Sebuah pabrik memproduksi {a} botol pada minggu pertama dan naik {b} botol setiap minggu.",
     "Berapa produksi pada minggu ke-{n}?", "Berapa total produksi selama {n} minggu?", "botol", 1),
]


def rupiah(x):
    if isinstance(x, float) and not x.is_integer():
        return f"{x:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return f"{int(x):,}".replace(",", ".")


def soal_acak():
    teks, tanya_un, tanya_sn, satuan, skala = random.choice(KONTEKS_ACAK)
    a = random.randint(2, 20) * skala
    b = random.randint(1, 6) * skala
    n = random.randint(6, 20)
    jenis = random.choice(["Un", "Sn"])
    un = a + (n - 1) * b
    sn = n * (2 * a + (n - 1) * b) // 2
    f = dict(a=rupiah(a), b=rupiah(b), n=n)
    if jenis == "Un":
        langkah = [f"Kata kunci \"ke-{n}\" → Uₙ", f"U{n} = {rupiah(a)} + ({n} − 1) × {rupiah(b)}",
                   f"U{n} = {rupiah(a)} + {rupiah((n - 1) * b)} = {rupiah(un)}"]
        tanya, jawab = tanya_un, un
    else:
        langkah = [f"Kata kunci \"total/jumlah\" → Sₙ",
                   f"S{n} = {n}/2 × (2×{rupiah(a)} + {n - 1}×{rupiah(b)})",
                   f"S{n} = {n}/2 × {rupiah(2 * a + (n - 1) * b)} = {rupiah(sn)}"]
        tanya, jawab = tanya_sn, sn
    return {
        "id": f"acak-{random.randint(1000, 9999)}", "level": "Variasi",
        "soal": teks.format(**f) + " " + tanya.format(**f),
        "diketahui": [f"a = {rupiah(a)}", f"b = {rupiah(b)}", f"n = {n}"],
        "ditanya": tanya.format(**f), "rumus": jenis, "jawaban": jawab, "satuan": satuan,
        "langkah": langkah,
    }


# ------------------------------------------------------------------ Kalkulator otomatis + langkah (DS01)
def hitung(a, b, n):
    n = int(n)
    if n < 1:
        raise ValueError("n harus bilangan bulat positif")
    un = a + (n - 1) * b
    sn = n / 2 * (2 * a + (n - 1) * b)
    sn = int(sn) if float(sn).is_integer() else sn
    un = int(un) if float(un).is_integer() else un
    r = rupiah
    return {
        "un": un, "sn": sn,
        "barisan": [a + i * b for i in range(min(n, 12))],
        "langkah_un": [
            "Rumus: Uₙ = a + (n − 1) × b",
            f"U{n} = {r(a)} + ({n} − 1) × {r(b)}",
            f"U{n} = {r(a)} + {r((n - 1) * b)}",
            f"U{n} = {r(un)}",
        ],
        "langkah_sn": [
            "Rumus: Sₙ = n/2 × (2a + (n − 1) × b)",
            f"S{n} = {n}/2 × (2 × {r(a)} + ({n} − 1) × {r(b)})",
            f"S{n} = {n}/2 × ({r(2 * a)} + {r((n - 1) * b)})",
            f"S{n} = {n}/2 × {r(2 * a + (n - 1) * b)}",
            f"S{n} = {r(sn)}",
        ],
    }
