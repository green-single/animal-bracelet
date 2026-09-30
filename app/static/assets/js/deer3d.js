/* 3D 小鹿 v2：原 2D 插画 → 3D 立体视差卡片
   方案：保留 role_deer.png 插画形象，用多层厚度卡片 + 双层视差 + Ori2 发光，
   转圈时能看到立体厚度与前后层次，跳跃/呼吸保留。
   挂载到 #deer3dBox；暴露 window.Deer3D = { spin(), leap(), idle(), isReady }
   贴图加载失败时 isReady=false（调用方降级到 2D 图片动画） */
(function(){
  if (typeof THREE === 'undefined') return; // three.min.js 未加载则直接跳过
  var deerScene, deerCamera, deerRenderer, deerGroup, deerBox;
  var deerAnim = null, leapProg = 0, t = 0, clock;
  var ready = false, started = false;

  function init() {
    deerBox = document.getElementById('deer3dBox');
    if (!deerBox || deerBox.dataset.init) return;
    deerBox.dataset.init = '1';

    var bw = deerBox.clientWidth || 150;
    var bh = deerBox.clientHeight || 150;
    deerBox.style.width = bw + 'px'; deerBox.style.height = bh + 'px';

    deerScene = new THREE.Scene();
    deerCamera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
    deerCamera.position.set(0, 0.1, 6.0);
    deerCamera.lookAt(0, 0, 0);

    deerRenderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    deerRenderer.setSize(bw, bh);
    deerRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    deerBox.appendChild(deerRenderer.domElement);

    // 灯光：暖主光 + 冷补光（保留 Ori2 氛围）
    deerScene.add(new THREE.HemisphereLight(0xffe9c8, 0x8a9cff, 1.0));
    var key = new THREE.DirectionalLight(0xffd9a0, 1.1); key.position.set(3, 5, 4); deerScene.add(key);
    var fill = new THREE.PointLight(0x9ab0ff, 0.6, 12); fill.position.set(-3, 2, -2); deerScene.add(fill);

    deerGroup = new THREE.Group();

    // ===== 加载原插画作为贴图 =====
    var loader = new THREE.TextureLoader();
    loader.crossOrigin = 'anonymous';
    loader.load('/static/assets/img/role_deer.png', function(tex){
      tex.anisotropy = Math.min(4, deerRenderer.capabilities ? deerRenderer.capabilities.getMaxAnisotropy() : 2);
      tex.minFilter = THREE.LinearFilter;
      buildDeer(tex);
    }, undefined, function(){
      // 贴图加载失败 → 降级 2D（isReady 保持 false）
      if (window.console) console.warn('deer3d: 贴图加载失败，降级 2D');
      ready = false;
    });
  }

  function buildDeer(tex) {
    var W = 1.55, H = 1.55; // 方形插画（原图 720x720）

    // 正面主卡：原插画
    var mainMat = new THREE.MeshBasicMaterial({
      map: tex, transparent: true, alphaTest: 0.06,
      depthWrite: false, side: THREE.DoubleSide
    });
    var main = new THREE.Mesh(new THREE.PlaneGeometry(W, H), mainMat);
    deerGroup.add(main);

    // 厚度层：z 方向叠 7 层（形成立体纸雕厚度，转圈可见）
    var layerMat = new THREE.MeshBasicMaterial({
      map: tex, transparent: true, alphaTest: 0.06,
      depthWrite: false, side: THREE.DoubleSide
    });
    var N = 7, depth = 0.34;
    for (var i = 1; i < N; i++) {
      var z = (i / (N - 1) - 0.5) * depth;
      var layer = new THREE.Mesh(new THREE.PlaneGeometry(W, H), layerMat);
      layer.position.z = z;
      deerGroup.add(layer);
    }

    // 背面补光层：半透明暖光，让背面也有层次
    var backMat = new THREE.MeshBasicMaterial({
      color: 0xffe9c8, transparent: true, opacity: 0.28,
      side: THREE.DoubleSide, depthWrite: false
    });
    var back = new THREE.Mesh(new THREE.PlaneGeometry(W * 1.02, H * 1.02), backMat);
    back.position.z = -depth / 2 - 0.02;
    deerGroup.add(back);

    // 轮廓光晕：略大的淡金发光面（Ori2 风格，很淡）
    var glowMat = new THREE.MeshBasicMaterial({
      color: 0xffd9a0, transparent: true, opacity: 0.14,
      side: THREE.DoubleSide, depthWrite: false
    });
    var glow = new THREE.Mesh(new THREE.PlaneGeometry(W * 1.14, H * 1.14), glowMat);
    glow.position.z = -depth / 2 - 0.04;
    deerGroup.add(glow);

    // 萤火虫光点（漂浮，增强月光氛围）
    for (var i = 0; i < 18; i++) {
      var p = new THREE.Mesh(new THREE.SphereGeometry(0.022 + Math.random()*0.03, 6, 6),
        new THREE.MeshBasicMaterial({ color: 0xffe9a8, transparent: true, opacity: .8 }));
      var a = Math.random() * Math.PI * 2;
      var r = 0.95 + Math.random() * 1.5;
      p.position.set(Math.cos(a)*r, -0.6 + Math.random()*1.6, Math.sin(a)*r);
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
      // 绕 Y 轴立体旋转：正/背面都是插画，侧面可见厚度层
      deerGroup.rotation.y += dt * 3.2;
      deerGroup.position.y = Math.sin(deerGroup.rotation.y) * 0.1;
      if (deerGroup.rotation.y >= Math.PI*2) { deerGroup.rotation.y = 0; deerAnim = null; }
    } else if (deerAnim === 'leap') {
      leapProg += dt * 1.6;
      if (leapProg >= 1) { leapProg = 0; deerGroup.position.y = 0; deerGroup.rotation.x = 0; deerAnim = null; }
      else {
        deerGroup.position.y = Math.sin(leapProg * Math.PI) * 1.1;
        deerGroup.rotation.x = Math.sin(leapProg * Math.PI) * -0.18;
      }
    } else {
      // 待机：呼吸浮动 + 极轻微俯仰（有生命感）
      deerGroup.position.y = Math.sin(t * 2.2) * 0.05;
      deerGroup.rotation.z = Math.sin(t * 1.3) * 0.03;
      deerGroup.scale.y = 1 + Math.sin(t * 2.2) * 0.015;
      deerGroup.scale.x = 1 - Math.sin(t * 2.2) * 0.01;
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

  // 容器可见时初始化：MutationObserver + 兜底轮询
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
