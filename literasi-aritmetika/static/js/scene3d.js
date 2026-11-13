// Ilustrasi 3D (three.js): setiap suku barisan = satu kolom kubus.
// Tinggi kolom ke-i = Uᵢ. Mode "Un" menyorot satu kolom, mode "Sn" menyorot semua kolom.
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const WARNA = { biasa: 0x93c5fd, un: 0xdc2626, sn: 0x1d4ed8, minus: 0xd1d5db };

function labelSprite(teks, warna = "#111827") {
  const c = document.createElement("canvas");
  c.width = 256; c.height = 128;
  const g = c.getContext("2d");
  g.font = "bold 64px system-ui, sans-serif";
  g.textAlign = "center"; g.textBaseline = "middle";
  g.fillStyle = "rgba(255,255,255,.85)";
  g.beginPath(); g.roundRect(28, 20, 200, 88, 24); g.fill();
  g.fillStyle = warna; g.fillText(teks, 128, 66);
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthTest: false }));
  s.scale.set(1.6, 0.8, 1);
  return s;
}

export function buatScene(container, { autoRotate = false, interaktif = true } = {}) {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 500);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  scene.add(new THREE.AmbientLight(0xffffff, 0.75));
  const sun = new THREE.DirectionalLight(0xffffff, 1.1);
  sun.position.set(8, 20, 12);
  scene.add(sun);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.enabled = interaktif;
  controls.autoRotate = autoRotate;
  controls.autoRotateSpeed = 1.5;

  const grup = new THREE.Group();
  scene.add(grup);
  const geo = new THREE.BoxGeometry(0.9, 0.9, 0.9);

  function bersihkan() {
    grup.children.forEach((o) => {
      if (o.material?.map) o.material.map.dispose();
      if (o.material) o.material.dispose();
    });
    grup.clear();
  }

  function update(a, b, n, mode = "Un") {
    bersihkan();
    const nilai = Array.from({ length: n }, (_, i) => a + i * b);
    const total = nilai.reduce((s, v) => s + Math.max(0, v), 0) || 1;
    const lebar = n * 1.2;

    nilai.forEach((v, i) => {
      const tinggi = Math.max(0, Math.round(v));
      const x = i * 1.2 - lebar / 2 + 0.6;
      let warna = WARNA.biasa;
      if (mode === "Un" && i === n - 1) warna = WARNA.un;
      if (mode === "Sn") warna = WARNA.sn;
      if (tinggi === 0) warna = WARNA.minus;
      const mat = new THREE.MeshStandardMaterial({ color: warna, roughness: 0.5 });
      const inst = new THREE.InstancedMesh(geo, mat, Math.max(1, tinggi));
      const m = new THREE.Matrix4();
      for (let k = 0; k < Math.max(1, tinggi); k++) {
        m.makeTranslation(x, tinggi === 0 ? -0.45 : k + 0.45, 0);
        inst.setMatrixAt(k, m);
      }
      if (tinggi === 0) inst.scale.set(1, 0.1, 1);
      grup.add(inst);
      const lbl = labelSprite(String(v), mode === "Un" && i === n - 1 ? "#dc2626" : "#1d4ed8");
      lbl.position.set(x, Math.max(1, tinggi) + 0.9, 0);
      grup.add(lbl);
      const idx = labelSprite("U" + (i + 1), "#6b7280");
      idx.scale.set(1.2, 0.6, 1);
      idx.position.set(x, -0.6, 0.9);
      grup.add(idx);
    });

    const maxH = Math.max(...nilai, 1);
    controls.target.set(0, maxH / 2, 0);
    const jarak = Math.max(lebar, maxH) * 1.3 + 4;
    camera.position.set(jarak * 0.35, maxH / 2 + jarak * 0.35, jarak);
    controls.update();
    return { nilai, total };
  }

  function ukur() {
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    renderer.domElement.style.width = "100%";
    renderer.domElement.style.height = "100%";
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(ukur).observe(container);
  ukur();

  (function loop() {
    requestAnimationFrame(loop);
    if (!container.offsetParent) return; // hemat baterai saat tidak tampil
    controls.update();
    renderer.render(scene, camera);
  })();

  return { update };
}
