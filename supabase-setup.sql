-- ARITMA / Kak Zizah - salin SEMUA isi file ini ke Supabase -> SQL Editor -> Run
create table if not exists siswa (
  kode   text primary key,
  nama   text,
  kelas  text,
  dibuat timestamptz default now()
);

create table if not exists skor (
  id     bigint generated always as identity primary key,
  kode   text,
  jenis  text,
  skor   real,
  maks   real,
  detail text,
  waktu  timestamptz default now()
);

alter table siswa enable row level security;
alter table skor  enable row level security;

-- Aplikasi boleh membaca, menambah, dan memperbarui data siswa; tidak boleh menghapus.
drop policy if exists "baca siswa" on siswa;
drop policy if exists "tambah siswa" on siswa;
drop policy if exists "ubah siswa" on siswa;
create policy "baca siswa"   on siswa for select using (true);
create policy "tambah siswa" on siswa for insert with check (true);
create policy "ubah siswa"   on siswa for update using (true) with check (true);

-- Skor hanya boleh dibaca dan ditambah.
drop policy if exists "baca skor" on skor;
drop policy if exists "tambah skor" on skor;
create policy "baca skor"   on skor for select using (true);
create policy "tambah skor" on skor for insert with check (true);
