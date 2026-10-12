/* Vitrina SafetyCoach: cápsula interactiva dentro del celular de la imagen publicitaria.
   Carátula → portada → video → preguntas → datos y firma → diploma con QR. */
(function () {
  'use strict';
  var app = document.getElementById('app');
  if (!app) return;
  function $(id) { return document.getElementById(id); }
  var fit = null;
  var SC_LOGO = (function () { try { return new URL('../img/logo-safetycoach.png', document.currentScript.src).href; } catch (e) { return '../assets/img/logo-safetycoach.png'; } })();
  function esc(t) { var d = document.createElement('div'); d.textContent = t == null ? '' : String(t); return d.innerHTML; }

  // ---------- Escenarios: cocina, bodega y fábrica (misma app, distinto fondo) ----------
  var SCENES = {
    cocina: { img: 'frame-cocina.webp', alt: 'Mano sosteniendo un celular en una cocina industrial', box: [23.05, 7.82, 53.9, 73.79] },
    bodega: { img: 'frame-bodega.webp', alt: 'Mano sosteniendo un celular en una bodega', box: [22.5, 13.56, 52.7, 68.4] },
    fabrica: { img: 'frame-fabrica.webp', alt: 'Mano sosteniendo un celular en un taller de fábrica', box: [22.5, 10.34, 53.2, 72.2] }
  };
  var frameImg = $('frame-img'), base = frameImg.getAttribute('src').replace(/frame-[a-z]+\.webp$/, '');
  function scene(name) {
    var s = SCENES[name]; if (!s) return;
    frameImg.src = base + s.img; frameImg.alt = s.alt;
    var b = s.box, scr = app.parentElement.style;
    scr.left = b[0] + '%'; scr.top = b[1] + '%'; scr.width = b[2] + '%'; scr.height = b[3] + '%';
    $('frame').dataset.scene = name;
    document.querySelectorAll('.scenes button').forEach(function (x) { x.setAttribute('aria-pressed', String(x.dataset.scene === name)); });
    if (typeof fit === 'function') setTimeout(fit, 0);
  }
  document.querySelectorAll('.scenes button').forEach(function (b) { b.addEventListener('click', function () { scene(b.dataset.scene); }); });
  Object.keys(SCENES).forEach(function (k) { var i = new Image(); i.src = base + SCENES[k].img; });

  // ---------- Navegación entre pantallas ----------
  function go(name) {
    app.querySelectorAll('.scr').forEach(function (s) { s.classList.toggle('on', s.dataset.scr === name); });
    app.scrollTop = 0;
    if (window.dataLayer) window.dataLayer.push({ event: 'vitrina_paso', paso: name });
  }
  app.addEventListener('click', function (e) {
    var b = e.target.closest('[data-go]'); if (b) { if (b.dataset.go === 'cover') scene('bodega'); go(b.dataset.go); return; }
    var s = e.target.closest('[data-soon]');
    if (s) {
      scene(s.dataset.soon === 'ins' ? 'fabrica' : s.dataset.soon === 'epp' ? 'bodega' : 'cocina');
      var t = $('app-toast'); t.hidden = false;
      t.innerHTML = 'Este ejemplo está en la <a href="#gate">demo completa</a>, más abajo. Aquí puedes probar la cápsula con video.';
    }
  });

  // ---------- Video (se carga solo al presionarlo) ----------
  var vid = $('vid'), t0 = 0, MIN = 15, timer = null;
  $('vid-play').addEventListener('click', function () {
    vid.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + vid.dataset.id + '?autoplay=1&rel=0&playsinline=1" title="Video Ley Karin" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
    t0 = Date.now();
    timer = setInterval(function () {
      var s = Math.round((Date.now() - t0) / 1000), left = MIN - s;
      if (left > 0) { $('vid-msg').textContent = 'Mira el video · podrás continuar en ' + left + ' s'; return; }
      clearInterval(timer); $('vid-msg').textContent = '✓ Video visto. Continúa con las preguntas.'; $('vid-next').disabled = false;
    }, 1000);
  });
  $('vid-next').addEventListener('click', function () { go('quiz'); });

  // ---------- Preguntas ----------
  var answers = {}, nota = 0;
  app.querySelectorAll('.aq button').forEach(function (b) {
    b.addEventListener('click', function () {
      var q = b.closest('.aq');
      q.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
      answers[q.dataset.q] = +b.dataset.v;
    });
  });
  $('quiz-next').addEventListener('click', function () {
    var msg = $('quiz-msg');
    if (Object.keys(answers).length < 3) { msg.textContent = 'Responde las 3 preguntas.'; return; }
    var ok = answers[1] + answers[2] + answers[3];
    nota = Math.round(ok / 3 * 100);
    app.querySelectorAll('.aq').forEach(function (q) {
      q.querySelectorAll('button').forEach(function (x) { x.classList.remove('good', 'bad'); if (x.classList.contains('on')) x.classList.add(+x.dataset.v ? 'good' : 'bad'); });
    });
    if (nota < 60) { msg.textContent = 'Nota ' + nota + '%. Necesitas 60%: revisa tus respuestas y vuelve a intentarlo.'; return; }
    msg.textContent = '';
    go('datos');
  });

  // ---------- Firma ----------
  var c = $('sig-app'), ctx = c.getContext('2d'), drawing = false, signed = false;
  function pos(e) { var r = c.getBoundingClientRect(); return [(e.clientX - r.left) * c.width / r.width, (e.clientY - r.top) * c.height / r.height]; }
  c.addEventListener('pointerdown', function (e) { drawing = true; signed = true; c.setPointerCapture(e.pointerId); ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.strokeStyle = '#111'; var p = pos(e); ctx.beginPath(); ctx.moveTo(p[0], p[1]); });
  c.addEventListener('pointermove', function (e) { if (!drawing) return; var p = pos(e); ctx.lineTo(p[0], p[1]); ctx.stroke(); });
  ['pointerup', 'pointercancel'].forEach(function (ev) { c.addEventListener(ev, function () { drawing = false; }); });
  $('sig-app-clear').addEventListener('click', function () { ctx.clearRect(0, 0, c.width, c.height); signed = false; });

  // ---------- Datos → registro → diploma ----------
  var diploma = null;
  $('app-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var f = e.target, msg = $('form-msg'), bad = null;
    f.querySelectorAll('[required]').forEach(function (i) {
      var ok = i.type === 'checkbox' ? i.checked : i.value.trim() !== '' && i.checkValidity();
      i.classList.toggle('invalid', !ok); if (!ok && !bad) bad = i;
    });
    if (bad) { msg.textContent = 'Completa los campos marcados.'; bad.focus(); return; }
    if (!signed) { msg.textContent = 'Falta tu firma.'; return; }
    var d = Object.fromEntries(new FormData(f).entries());
    var code = 'SC-RE-09-CAP-LK01-' + Math.floor(100000 + Math.random() * 900000);
    diploma = { nombre: d.nombre.trim(), rut: d.rut.trim(), cargo: d.cargo.trim(), empresa: d.empresa.trim(), nota: nota, code: code, firma: c.toDataURL('image/png'),
      fecha: new Date().toLocaleDateString('es-CL', { day: '2-digit', month: '2-digit', year: 'numeric' }).replace(/\//g, '-') };
    // Registro del interesado (Netlify Forms) y acceso directo a la demo completa.
    var lead = { 'form-name': 'registro-herramienta', herramienta: 'Vitrina: cápsula Ley Karin', nombre: d.nombre, cargo: d.cargo, empresa: d.empresa, correo: d.correo, consentimiento: 'Sí', origen: 'vitrina-demo' };
    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(lead).toString() }).catch(function () { /* vista local */ });
    try { sessionStorage.setItem('sc-lead', JSON.stringify({ correo: d.correo, empresa: d.empresa, nombre: d.nombre })); } catch (err) { /* sin almacenamiento */ }
    if (window.dataLayer) window.dataLayer.push({ event: 'vitrina_diploma', nota: nota });
    var g = $('gate'), tool = $('tool'); if (g) g.hidden = true; if (tool) tool.hidden = false;
    $('dip-mini').innerHTML = diplomaHTML(diploma);
    go('diploma');
  });

  function qrSVG(text) {
    if (typeof window.qrcode !== 'function') return '<div class="qr-fallback">QR</div>';
    var q = window.qrcode(0, 'M'); q.addData(text); q.make();
    return q.createSvgTag({ cellSize: 3, margin: 0, scalable: true });
  }
  function diplomaHTML(p) {
    var url = location.origin + location.pathname + '?verificar=' + encodeURIComponent(p.code);
    return '<article class="dip">' +
      '<header class="dip-h"><span class="dip-logo">TU LOGO</span><div><b>' + esc(p.empresa.toUpperCase()) + '</b><small>Programa de prevención · Organismo administrador</small></div><img class="dip-sc" src="' + SC_LOGO + '" alt="SafetyCoach"></header>' +
      '<i class="dip-rule"></i><h5>DIPLOMA DE CAPACITACIÓN</h5><p class="dip-s">Se certifica que</p>' +
      '<p class="dip-n">' + esc(p.nombre) + '</p><p class="dip-m">RUT ' + esc(p.rut) + ' · ' + esc(p.cargo) + ' · ' + esc(p.empresa) + '</p>' +
      '<p class="dip-s">Aprobó satisfactoriamente el módulo</p><p class="dip-mod">LK-01 — LEY KARIN: COMUNÍCATE CON RESPETO</p>' +
      '<p class="dip-c">Contenidos: acoso laboral, acoso sexual y violencia en el trabajo · conductas esperadas · canal de denuncia y medidas de resguardo · marco legal Ley 21.643, Ley 16.744, DS44.</p>' +
      '<p class="dip-ok">Nota evaluación: ' + p.nota + '% · Aprobado</p><p class="dip-f">Fecha: ' + esc(p.fecha) + '</p>' +
      '<div class="dip-sig"><div><img src="' + p.firma + '" alt="Firma"><span>' + esc(p.nombre) + '</span></div><div><i></i><span>Encargado de Prevención<br>SafetyCoach</span></div></div>' +
      '<footer class="dip-foot"><div><small>Código registro SC-RE-09 · Marco legal mínimo: Ley 21.643 · Ley 16.744 · DS44</small><small class="dip-code">' + esc(p.code) + '</small></div>' +
      '<a class="dip-qr" href="' + esc(url) + '" title="Verificar diploma">' + qrSVG(url) + '<small>Verificar</small></a></footer>' +
      '<span class="dip-wm" aria-hidden="true">DS44</span></article>';
  }
  $('dip-open').addEventListener('click', function () {
    if (!diploma) return;
    var box = $('dip-print'); box.innerHTML = diplomaHTML(diploma); box.hidden = false;
    document.body.classList.add('printing-dip');
    setTimeout(function () { window.print(); }, 150);
  });
  window.addEventListener('afterprint', function () { document.body.classList.remove('printing-dip'); $('dip-print').hidden = true; });

  // ---------- Escala: la app se diseña a 360 px y se ajusta a la pantalla del celular ----------
  var screen = app.parentElement;
  fit = function () {
    var w = screen.clientWidth, h = screen.clientHeight, k = w / 360;
    app.style.transform = 'scale(' + k + ')'; app.style.width = '360px'; app.style.height = (h / k) + 'px';
  };
  if (window.ResizeObserver) new ResizeObserver(fit).observe(screen); else window.addEventListener('resize', fit);
  fit();

  // ---------- Ver en grande ----------
  $('frame-full').addEventListener('click', function () {
    var on = document.body.classList.toggle('frame-zoom');
    this.textContent = on ? '✕ Cerrar' : '⤢ Ver en grande';
  });

  // ---------- Verificación por QR (demo) ----------
  var v = new URLSearchParams(location.search).get('verificar');
  if (v) {
    var t = $('app-toast'); t.hidden = false;
    t.innerHTML = '✓ Código <b>' + esc(v) + '</b>: en tu versión, aquí se muestra el diploma original con su firma validada.';
  }
})();
