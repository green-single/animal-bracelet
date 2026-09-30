/* 3D 小鹿模型（Three.js r128，程序化建模，Ori2 发光风格）
   挂载到 #deer3dBox；暴露 window.Deer3D = { spin(), leap(), idle(), isReady }
   加载失败时 isReady=false（调用方降级到 2D 图片动画） */
(function(){
  if (typeof THREE === 'undefined') return; // three.min.js 未加载则直接跳过
  var deerScene, deerCamera, deerRenderer, deerGroup, deerBox;
  var deerAnim = null, spinProg = 0, leapProg = 0, t = 0, clock;
  var ready = false;

  function init() {
    deerBox = document.getElementById('deer3dBox');
    if (!deerBox || deerBox.dataset.init) return;
    deerBox.dataset.init = '1';

    deerScene = new THREE.Scene();
    deerCamera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    deerCamera.position.set(0, 1.1, 5.4);
    deerCamera.lookAt(0, 0.75, 0);

    var bw = deerBox.clientWidth || 150;
    var bh = deerBox.clientHeight || 150;
    deerBox.style.width = bw + 'px'; deerBox.style.height = bh + 'px';
    deerRenderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    deerRenderer.setSize(bw, bh);
    deerRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    deerBox.appendChild(deerRenderer.domElement);

    // 灯光：暖主光 + 冷补光
    deerScene.add(new THREE.HemisphereLight(0xffe9c8, 0x8a9cff, 0.9));
    var key = new THREE.DirectionalLight(0xffd9a0, 1.0); key.position.set(3, 5, 4); deerScene.add(key);
    var fill = new THREE.PointLight(0x9ab0ff, 0.6, 12); fill.position.set(-3, 2, -2); deerScene.add(fill);

    deerGroup = new THREE.Group();
    function mat(color, emissive, emInt) {
      return new THREE.MeshStandardMaterial({ color: color, roughness: .55, metalness: .1, emissive: emissive || 0x000000, emissiveIntensity: emInt || 0 });
    }
    var bodyMat = mat(0xd9c9a8, 0x6b4a2a, .12);
    var darkMat = mat(0x8a6f4e, 0x3a2a18, .15);
    var antlerMat = mat(0xd9b98a, 0x8a6a35, .35);

    // 身体
    var body = new THREE.Mesh(new THREE.SphereGeometry(0.62, 24, 18), bodyMat);
    body.scale.set(1.32, 0.9, 0.82); body.position.y = 0.95; deerGroup.add(body);

    // 腿
    function leg(x, z) {
      var l = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.1, 0.6, 10), darkMat);
      l.position.set(x, 0.3, z); return l;
    }
    deerGroup.add(leg(-0.32, 0.24)); deerGroup.add(leg(0.32, 0.24));
    deerGroup.add(leg(-0.3, -0.26)); deerGroup.add(leg(0.3, -0.26));

    // 脖子
    var neck = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.17, 0.52, 12), bodyMat);
    neck.position.set(0.55, 1.16, 0); neck.rotation.z = -0.6; deerGroup.add(neck);

    // 头
    var head = new THREE.Mesh(new THREE.SphereGeometry(0.2, 18, 14), bodyMat);
    head.position.set(0.9, 1.52, 0); head.scale.set(0.9, 0.82, 0.78); deerGroup.add(head);

    // 口鼻
    var snout = new THREE.Mesh(new THREE.SphereGeometry(0.09, 12, 10), darkMat);
    snout.position.set(1.1, 1.46, 0); snout.scale.set(1, 0.8, 0.8); deerGroup.add(snout);

    // 耳朵
    function ear(x) {
      var e = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.2, 10), bodyMat);
      e.position.set(x, 1.74, 0); e.rotation.z = x > 0 ? 0.25 : -0.25; return e;
    }
    deerGroup.add(ear(0.86)); deerGroup.add(ear(1.1));

    // 鹿角
    function antler(x) {
      var g = new THREE.Group();
      var main = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.04, 0.34, 8), antlerMat); main.position.y = 0.17;
      var br = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.03, 0.18, 8), antlerMat); br.position.set(0.07, 0.33, 0); br.rotation.z = -0.5;
      g.add(main); g.add(br); g.position.set(x, 1.6, 0); return g;
    }
    deerGroup.add(antler(-0.06)); deerGroup.add(antler(0.06));

    // 尾巴
    var tail = new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8), bodyMat);
    tail.position.set(-0.72, 1.15, 0); deerGroup.add(tail);

    // 萤火虫光点
    for (var i = 0; i < 24; i++) {
      var p = new THREE.Mesh(new THREE.SphereGeometry(0.02 + Math.random()*0.03, 6, 6),
        new THREE.MeshBasicMaterial({ color: 0xffe9a8, transparent: true, opacity: .85 }));
      var a = Math.random() * Math.PI * 2;
      var r = 0.9 + Math.random() * 1.6;
      p.position.set(Math.cos(a)*r, 0.4 + Math.random()*1.8, Math.sin(a)*r);
      deerScene.add(p);
    }

    deerScene.add(deerGroup);
    clock = new THREE.Clock();
    ready = true;
    animate();
  }

  function animate() {
    requestAnimationFrame(animate);
    var dt = clock.getDelta(); t += dt;
    if (deerAnim === 'spin') {
      deerGroup.rotation.y += dt * 3.4;
      deerGroup.position.y = 0.15 + Math.sin(deerGroup.rotation.y) * 0.12;
      if (deerGroup.rotation.y >= Math.PI*2) { deerGroup.rotation.y = 0; deerAnim = null; }
    } else if (deerAnim === 'leap') {
      leapProg += dt * 1.6;
      if (leapProg >= 1) { leapProg = 0; deerGroup.position.y = 0; deerGroup.rotation.x = 0; deerAnim = null; }
      else {
        deerGroup.position.y = Math.sin(leapProg * Math.PI) * 1.2;
        deerGroup.rotation.x = Math.sin(leapProg * Math.PI) * -0.25;
      }
    } else {
      deerGroup.position.y = Math.sin(t * 2.4) * 0.035;
      deerGroup.scale.y = 1 + Math.sin(t * 2.4) * 0.012;
    }
    if (deerRenderer && deerCamera) deerRenderer.render(deerScene, deerCamera);
  }

  window.Deer3D = {
    get isReady() { return ready; },
    spin: function(){ if (!ready) return; deerAnim = 'spin'; deerGroup.rotation.y = 0; },
    leap: function(){ if (!ready) return; deerAnim = 'leap'; leapProg = 0; },
    idle: function(){ if (!ready) return; deerAnim = null; leapProg = 0; },
    state: function(){ return { ready: ready, anim: deerAnim, rotY: deerGroup ? deerGroup.rotation.y : 0, posY: deerGroup ? deerGroup.position.y : 0 }; }
  };

  // 容器可见时初始化（moon 主题显示时）：MutationObserver + 兜底轮询
  function tryInit() {
    if (ready || !document.body) { setTimeout(tryInit, 300); return; }
    if (!deerBox) deerBox = document.getElementById('deer3dBox');
    var v = document.body.getAttribute('data-theme');
    if (v === 'moon' && deerBox && (deerBox.offsetParent || getComputedStyle(deerBox).display !== 'none')) {
      try { init(); } catch(e) { if (window.console) console.warn('deer3d init:', e && e.message); }
      return;
    }
    setTimeout(tryInit, 500);
  }
  var mo = null;
  try {
    mo = new MutationObserver(function(){
      var v = document.body ? document.body.getAttribute('data-theme') : null;
      if (v === 'moon' && !ready) tryInit();
    });
    mo.observe(document.body, { attributes: true, attributeFilter: ['data-theme'] });
  } catch(e) {}
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tryInit);
  } else {
    tryInit();
  }
})();
