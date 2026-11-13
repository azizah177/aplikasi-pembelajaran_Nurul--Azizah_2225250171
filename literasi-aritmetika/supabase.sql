-- Jalankan di Supabase -> SQL Editor
create table if not exists siswa (
  kode   text primary key,
  nama   text,
  kelas  text,
  dibuat timestamptz default now()
);

create table if not exists skor (
  id     bigint generated always as identity primary key,
  kode   text references siswa(kode),
  jenis  text,
  skor   real,
  maks   real,
  detail text,
  waktu  timestamptz default now()
);

-- Izinkan akses dengan anon key (untuk prototipe tugas kuliah)
alter table siswa enable row level security;
alter table skor  enable row level security;
create policy "akses siswa" on siswa for all using (true) with check (true);
create policy "akses skor"  on skor  for all using (true) with check (true);
