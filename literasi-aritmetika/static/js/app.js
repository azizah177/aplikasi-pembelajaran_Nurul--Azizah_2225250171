// ARITMA — logika tampilan (JavaScript murni + modul three.js)
import { buatScene } from "./scene3d.js";

const $ = (s) => document.querySelector(s);
const esc = (t) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const rp = (x) => Number(x).toLocaleString("id-ID");

const JUDUL = {
  login: "ARITMA", home: "Beranda", materi: "Materi", lab: "Lab 3D",
  kalkulator: "Kalkulator", latihan: "Latihan Soal", literasi: "Tes Literasi", progres: "Progres",
};

const state = {
  siswa: null, materi: [], mIdx: 0, mStep: 0,
  latihan: [], lIdx: 0, lHasil: [], literasi: [], tIdx: 0, jawabLit: {},
  labMode: "Un",
};

// ------------------------------------------------------------ util
async function api(url, data) {
  const opt = data ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) } : {};
  const r = await fetch(url, opt);
  const j = await r.json();
  if (!r.ok) throw new Error(j.error || "Terjadi kesalahan");
  return j;
}
function toast(msg) {
  const t = $("#toast");
  t.textContent = msg; t.classList.remove("hidden");
  clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.add("hidden"), 2200);
}
function parseAngka(s) {
  if (s == null) return null;
  s = String(s).toLowerCase().replace(/rp/g, "").replace(/\s/g, "");
  if (!s) return null;
  if (s.includes(".") && s.includes(",")) s = s.replace(/\./g, "").replace(",", ".");
  else if (s.includes(",")) s = s.replace(",", ".");
  else if ((s.match(/\./g) || []).length > 1 || /^-?\d{1,3}\.\d{3}$/.test(s)) s = s.replace(/\./g, "");
  const v = Number(s);
  return Number.isFinite(v) ? v : null;
}
// Menandai angka dalam soal cerita (membantu menemukan informasi penting)
const tandaiAngka = (t) => esc(t).replace(/(Rp)?\d[\d.,]*/g, (m) => `<mark>${m}</mark>`);
function tandaiFrasa(t, frasa = []) {
  let h = esc(t);
  frasa.forEach((f) => { h = h.split(esc(f)).join(`<mark>${esc(f)}</mark>`); });
  return h;
}
function dots(el, n, aktif, status = []) {
  el.innerHTML = Array.from({ length: n }, (_, i) =>
    `<i class="${status[i] === true ? "ok" : status[i] === false ? "no" : i === aktif ? "on" : ""}"></i>`).join("");
}
const simpan = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} };
const muat = (k) => { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } };

// ------------------------------------------------------------ navigasi (hash -> tombol back Android bekerja)
function tampil(view) {
  if (!state.siswa && view !== "login") view = "login";
  document.querySelectorAll(".view").forEach((v) => v.classList.add("hidden"));
  $("#v-" + view).classList.remove("hidden");
  $("#judul").textContent = JUDUL[view] || "ARITMA";
  $("#btnBack").classList.toggle("hidden", view === "login" || view === "home");
  window.scrollTo(0, 0);
  const init = { home: renderHome, materi: renderMateri, lab: renderLab, latihan: mulaiLatihan,
                 literasi: mulaiLiterasi, progres: renderProgres };
  init[view]?.();
}
const go = (v) => { location.hash = v; };
window.addEventListener("hashchange", () => tampil(location.hash.slice(1) || "home"));
$("#btnBack").onclick = () => go("home");
document.querySelectorAll("[data-go]").forEach((b) => (b.onclick = () => go(b.dataset.go)));

// ------------------------------------------------------------ login
$("#formLogin").onsubmit = async (e) => {
  e.preventDefault();
  $("#loginErr").textContent = "";
  try {
    const { siswa } = await api("/api/login", { kode: $("#inKode").value, nama: $("#inNama").value, kelas: $("#inKelas").value });
    state.siswa = siswa; simpan("siswa", siswa);
    go("home");
    if (location.hash === "#home") tampil("home");
  } catch (err) { $("#loginErr").textContent = err.message; }
};
$("#btnLogout").onclick = () => {
  state.siswa = null; try { localStorage.removeItem("siswa"); } catch {}
  $("#userBadge").classList.add("hidden");
  go("login");
};
function renderHome() {
  const s = state.siswa;
  $("#hello").textContent = `Halo, ${s.nama || s.kode}! Mau belajar apa hari ini?`;
  $("#userBadge").textContent = s.kode; $("#userBadge").classList.remove("hidden");
}

// ------------------------------------------------------------ materi (satu kartu, langkah dibuka bertahap)
async function renderMateri() {
  if (!state.materi.length) state.materi = await api("/api/materi");
  const m = state.materi[state.mIdx];
  dots($("#materiDots"), state.materi.length, state.mIdx);
  const langkah = m.contoh.langkah.slice(0, state.mStep).map((l) => `<li>${esc(l)}</li>`).join("");
  const habis = state.mStep >= m.contoh.langkah.length;
  $("#materiCard").innerHTML = `
    <div class="ikon">${m.ikon}</div>
    <h2>${esc(m.judul)}</h2>
    <p class="c-text">${esc(m.penjelasan)}</p>
    <div class="rumus-box">${esc(m.rumus)}</div>
    <div class="contoh">
      <b>Contoh:</b> <span class="soal">${tandaiAngka(m.contoh.soal)}</span>
      <ol class="steps">${langkah}</ol>
      ${habis ? "" : `<button class="btn full" id="btnStep">👉 Lihat langkah ${state.mStep + 1} dari ${m.contoh.langkah.length}</button>`}
    </div>
    <div class="ingat">💡 ${esc(m.ingat)}</div>
    ${[2, 3].includes(m.id) ? `<p><button class="btn full" id="btnKe3d">🧊 Lihat di Lab 3D</button></p>` : ""}`;
  $("#btnStep")?.addEventListener("click", () => { state.mStep++; renderMateri(); });
  $("#btnKe3d")?.addEventListener("click", () => { state.labMode = m.id === 2 ? "Un" : "Sn"; go("lab"); });
  $("#mPrev").disabled = state.mIdx === 0;
  $("#mNext").textContent = state.mIdx === state.materi.length - 1 ? "Ke Latihan ✏️" : "Berikutnya ›";
}
$("#mPrev").onclick = () => { if (state.mIdx > 0) { state.mIdx--; state.mStep = 0; renderMateri(); } };
$("#mNext").onclick = () => {
  if (state.mIdx < state.materi.length - 1) { state.mIdx++; state.mStep = 0; renderMateri(); }
  else go("latihan");
};

// ------------------------------------------------------------ Lab 3D
let lab = null;
function renderLab() {
  if (!lab) lab = buatScene($("#lab3d"));
  const a = +$("#sA").value, b = +$("#sB").value, n = +$("#sN").value;
  $("#vA").textContent = a; $("#vB").textContent = b; $("#vN").textContent = n;
  const { nilai } = lab.update(a, b, n, state.labMode);
  const un = a + (n - 1) * b, sn = (n * (2 * a + (n - 1) * b)) / 2;
  $("#modeUn").classList.toggle("primary", state.labMode === "Un");
  $("#modeSn").classList.toggle("primary", state.labMode === "Sn");
  $("#labInfo").innerHTML = state.labMode === "Un"
    ? `Kolom <b class="c-rumus">merah</b> = suku ke-${n} saja.<br><span class="c-rumus">U${n} = a + (n − 1)b</span> = <span class="c-kerja">${a} + ${n - 1}×${b} = <b>${un}</b></span>`
    : `Semua kolom <b class="c-kerja">biru</b> dijumlahkan.<br><span class="c-rumus">S${n} = n/2 × (2a + (n − 1)b)</span> = <span class="c-kerja">${nilai.join(" + ")} = <b>${sn}</b></span>`;
}
["#sA", "#sB", "#sN"].forEach((s) => ($(s).oninput = renderLab));
$("#modeUn").onclick = () => { state.labMode = "Un"; renderLab(); };
$("#modeSn").onclick = () => { state.labMode = "Sn"; renderLab(); };

// ------------------------------------------------------------ kalkulator otomatis + langkah (Python)
$("#formHitung").onsubmit = async (e) => {
  e.preventDefault();
  try {
    const h = await api("/api/hitung", { a: $("#kA").value, b: $("#kB").value, n: $("#kN").value });
    const daftar = (arr) => arr.map((l, i) => i === 0 ? `<div class="rumus-box">${esc(l)}</div>` : `<li>${esc(l)}</li>`).join("");
    $("#hasilHitung").innerHTML = `
      <div class="card"><b>Barisan:</b> <span class="c-kerja">${h.barisan.map(rp).join(", ")}${h.barisan.length < +$("#kN").value ? ", …" : ""}</span></div>
      <div class="card"><h3>🎯 Suku ke-n (satu nilai)</h3>${daftar(h.langkah_un).replace(/(<li>.*)/s, '<ol class="steps">$1</ol>')}</div>
      <div class="card"><h3>➕ Jumlah n suku (total)</h3>${daftar(h.langkah_sn).replace(/(<li>.*)/s, '<ol class="steps">$1</ol>')}</div>
      <div class="ingat">💡 Ditanya "suku ke-…"? pakai Uₙ. Ditanya "jumlah/total"? pakai Sₙ.</div>`;
  } catch (err) { toast(err.message); }
};

// ------------------------------------------------------------ latihan: pilih rumus dulu, lalu hitung
async function mulaiLatihan() {
  if (!state.latihan.length) state.latihan = await api("/api/latihan");
  if (state.lIdx >= state.latihan.length) return ringkasLatihan();
  renderSoal();
}
const NAMA_RUMUS = { b: "Beda (b)", Un: "Suku ke-n (Uₙ)", Sn: "Jumlah n suku (Sₙ)" };
function renderSoal() {
  const s = state.latihan[state.lIdx];
  const ss = { rumusOk: false, coba: 0, selesai: false, langkah: 0 };
  dots($("#latDots"), state.latihan.length, state.lIdx, state.lHasil);
  const card = $("#latCard");
  card.innerHTML = `
    <span class="level">${esc(s.level)}</span> <small class="info">Soal ${state.lIdx + 1}/${state.latihan.length}</small>
    <p class="soal">${tandaiAngka(s.soal)}</p>
    <details><summary>Bantu aku: Diketahui &amp; Ditanya</summary>
      <p class="c-kerja">Diketahui: ${s.diketahui.map(esc).join(", ")}<br>Ditanya: ${esc(s.ditanya)}</p></details>
    <p><b>Langkah 1.</b> Rumus apa yang kamu pakai?</p>
    <div class="chips" id="chipRumus">${Object.entries(NAMA_RUMUS).map(([k, v]) => `<button class="chip" data-r="${k}">${v}</button>`).join("")}</div>
    <div id="fbRumus"></div>
    <div id="tahapHitung" class="hidden">
      <p><b>Langkah 2.</b> Hitung jawabannya ${s.satuan ? `(${esc(s.satuan)})` : ""}</p>
      <div class="row"><input id="inJawab" inputmode="decimal" placeholder="Jawabanmu"><button class="btn primary" id="btnCek" style="flex:0 0 90px">Cek</button></div>
      <div id="fbJawab"></div>
    </div>
    <div id="pembahasan"></div>
    <div id="lanjut"></div>`;

  card.querySelectorAll("#chipRumus .chip").forEach((c) => (c.onclick = () => {
    if (ss.rumusOk) return;
    const benar = c.dataset.r === s.rumus;
    c.classList.add(benar ? "ok" : "no");
    $("#fbRumus").innerHTML = benar
      ? `<div class="feedback ok">Tepat! Pakai ${NAMA_RUMUS[s.rumus]}.</div>`
      : `<div class="feedback tip">Coba lagi. Lihat kata tanyanya: "${esc(s.ditanya)}". ${s.rumus === "Sn" ? "Ada kata jumlah/total → dijumlahkan." : s.rumus === "Un" ? "Ada kata \"ke-…\" → satu nilai saja." : "Yang dicari selisih dua suku berurutan."}</div>`;
    if (benar) { ss.rumusOk = true; $("#tahapHitung").classList.remove("hidden"); $("#inJawab").focus(); }
  }));

  const tampilPembahasan = () => {
    const sudah = s.langkah.slice(0, ss.langkah).map((l) => `<li>${esc(l)}</li>`).join("");
    $("#pembahasan").innerHTML = `<b>Pembahasan:</b><ol class="steps">${sudah}</ol>` +
      (ss.langkah < s.langkah.length ? `<button class="btn full" id="btnLangkah">👉 Langkah berikutnya</button>` : "");
    $("#btnLangkah")?.addEventListener("click", () => { ss.langkah++; tampilPembahasan(); });
  };
  const akhiri = (benar) => {
    ss.selesai = true;
    state.lHasil[state.lIdx] = benar;
    dots($("#latDots"), state.latihan.length, state.lIdx, state.lHasil);
    $("#lanjut").innerHTML = `<button class="btn primary full" id="btnLanjut">${state.lIdx < state.latihan.length - 1 ? "Soal berikutnya ›" : "Lihat hasil"}</button>`;
    $("#btnLanjut").onclick = () => { state.lIdx++; mulaiLatihan(); };
  };

  $("#btnCek").onclick = () => {
    if (ss.selesai) return;
    const v = parseAngka($("#inJawab").value);
    if (v === null) return toast("Isi jawaban dengan angka ya");
    ss.coba++;
    if (Math.abs(v - s.jawaban) < 1e-6) {
      $("#fbJawab").innerHTML = `<div class="feedback ok">✔ Benar! ${rp(s.jawaban)} ${esc(s.satuan)}</div>`;
      ss.langkah = s.langkah.length; tampilPembahasan();
      akhiri(ss.coba === 1);
    } else if (ss.coba < 2) {
      $("#fbJawab").innerHTML = `<div class="feedback no">Belum tepat. Cek lagi perhitunganmu, lalu coba sekali lagi.</div>`;
    } else {
      $("#fbJawab").innerHTML = `<div class="feedback no">Jawaban yang benar: ${rp(s.jawaban)} ${esc(s.satuan)}. Yuk lihat langkahnya 👇</div>`;
      ss.langkah = 1; tampilPembahasan();
      akhiri(false);
    }
  };
  $("#inJawab").onkeydown = (e) => { if (e.key === "Enter") $("#btnCek").click(); };
}
async function ringkasLatihan() {
  const benar = state.lHasil.filter(Boolean).length, total = state.latihan.length;
  dots($("#latDots"), total, -1, state.lHasil);
  $("#latCard").innerHTML = `
    <h2>Hasil Latihan</h2>
    <div class="skor-besar">${benar}/${total}</div>
    <p class="info" style="text-align:center">benar pada percobaan pertama</p>
    <button class="btn primary full" id="btnAcak">🎲 Coba soal variasi</button><p></p>
    <button class="btn full" id="btnUlang">↻ Ulangi latihan</button>`;
  $("#btnUlang").onclick = () => { state.lIdx = 0; state.lHasil = []; state.latihan = []; ringkasLatihan.tersimpan = false; mulaiLatihan(); };
  $("#btnAcak").onclick = async () => {
    state.latihan.push(await api("/api/latihan/acak"));
    renderSoal();
  };
  if (!ringkasLatihan.tersimpan) {
    ringkasLatihan.tersimpan = true;
    api("/api/skor", { kode: state.siswa.kode, jenis: "latihan", skor: benar, maks: total }).catch(() => {});
  }
}

// ------------------------------------------------------------ tes literasi matematika (skor per tahap)
async function mulaiLiterasi() {
  if (!state.literasi.length) state.literasi = await api("/api/literasi");
  renderLiterasi();
}
function renderLiterasi() {
  const L = state.literasi, s = L[state.tIdx];
  const jaw = (state.jawabLit[s.id] ||= []);
  dots($("#litDots"), L.length, state.tIdx);
  $("#litCard").innerHTML = `
    <div class="indikator">Soal ${state.tIdx + 1}/${L.length} · ${esc(s.indikator)}</div>
    <h2>${esc(s.judul)}</h2>
    <p class="soal">${tandaiFrasa(s.soal, s.penting)}</p>
    <div class="ingat">💡 Bagian <mark>berwarna kuning</mark> adalah informasi penting. Kerjakan per tahap.</div>
    ${s.tahap.map((t, i) => `
      <div class="tahap"><b>${esc(t.teks)}</b> <small class="info">(skor ${t.skor})</small>
      ${t.tipe === "angka"
        ? `<input data-i="${i}" class="inLit" inputmode="decimal" value="${esc(jaw[i] ?? "")}" placeholder="Tulis angka">`
        : t.opsi.map((o, k) => `<button class="btn opsi ${String(jaw[i]) === String(k) ? "primary" : ""}" data-i="${i}" data-k="${k}">${esc(o)}</button>`).join("")}
      </div>`).join("")}
    <p></p>
    <div class="row">
      <button class="btn" id="tPrev" ${state.tIdx === 0 ? "disabled" : ""}>‹ Sebelumnya</button>
      <button class="btn primary" id="tNext">${state.tIdx === L.length - 1 ? "Kumpulkan ✔" : "Berikutnya ›"}</button>
    </div>`;
  document.querySelectorAll(".inLit").forEach((el) => (el.oninput = () => { jaw[+el.dataset.i] = el.value; }));
  document.querySelectorAll(".opsi").forEach((el) => (el.onclick = () => { jaw[+el.dataset.i] = el.dataset.k; renderLiterasi(); }));
  $("#tPrev").onclick = () => { state.tIdx--; renderLiterasi(); };
  $("#tNext").onclick = () => {
    if (state.tIdx < L.length - 1) { state.tIdx++; renderLiterasi(); return; }
    const kosong = L.reduce((n, q) => n + q.tahap.filter((_, i) => !(state.jawabLit[q.id] || [])[i]).length, 0);
    if (kosong && !confirm(`Masih ada ${kosong} tahap kosong. Tetap kumpulkan?`)) return;
    kumpulkanLiterasi();
  };
}
async function kumpulkanLiterasi() {
  const h = await api("/api/literasi/nilai", { kode: state.siswa.kode, jawaban: state.jawabLit });
  dots($("#litDots"), 0, 0);
  $("#litCard").innerHTML = `
    <h2>Hasil Tes Literasi Matematika</h2>
    <div class="skor-besar">${h.total}/${h.maks}</div>
    ${h.per_soal.map((p) => `
      <div class="tahap">
        <b>${esc(p.indikator)}</b> — ${p.skor}/${p.maks}
        <div class="bar"><div style="width:${(p.skor / p.maks) * 100}%"></div></div>
        <small>${p.tahap.map((t, i) => `Tahap ${i + 1}: ${t.benar ? "✔" : "✘"}`).join(" · ")}</small>
        <details><summary>Lihat pembahasan</summary><ol class="steps">${p.pembahasan.map((l) => `<li>${esc(l)}</li>`).join("")}</ol></details>
      </div>`).join("")}
    <p></p>
    <button class="btn primary full" id="tUlang">↻ Kerjakan ulang</button>`;
  $("#tUlang").onclick = () => { state.jawabLit = {}; state.tIdx = 0; renderLiterasi(); };
}

// ------------------------------------------------------------ progres
async function renderProgres() {
  const rows = await api("/api/progres/" + encodeURIComponent(state.siswa.kode));
  $("#progresList").innerHTML = rows.length
    ? `<div class="card"><table class="tbl"><tr><th>Waktu</th><th>Jenis</th><th>Skor</th></tr>
        ${rows.map((r) => `<tr><td>${new Date(r.waktu).toLocaleString("id-ID", { dateStyle: "short", timeStyle: "short" })}</td>
        <td>${esc(r.jenis)}</td><td><b>${r.skor}/${r.maks}</b></td></tr>`).join("")}</table></div>`
    : `<div class="card">Belum ada skor. Coba kerjakan Latihan atau Tes Literasi dulu ya!</div>`;
}

// ------------------------------------------------------------ mulai
const hero = buatScene($("#hero3d"), { autoRotate: true, interaktif: false });
hero.update(1, 1, 6, "Sn");
state.siswa = muat("siswa");
tampil(location.hash.slice(1) || (state.siswa ? "home" : "login"));
if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
