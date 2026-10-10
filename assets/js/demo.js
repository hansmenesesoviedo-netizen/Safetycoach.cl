/* Demo SafetyCoach Digital (empresa ficticia). Los datos se guardan solo en este navegador. */
(function () {
  'use strict';
  var KEY = 'sc-demo-registros';

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
  function save(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* modo privado: solo en memoria */ } memory = list; }
  var memory = load();
  function now() { return new Date().toLocaleString('es-CL', { dateStyle: 'short', timeStyle: 'short' }); }
  function add(rec) { var l = memory.slice(); rec.fecha = now(); l.unshift(rec); save(l); renderReg(); }
  function esc(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

  // ---------- Pestañas ----------
  var tabs = document.querySelectorAll('.demo-tabs [role="tab"]');
  function show(t) {
    tabs.forEach(function (b) { b.setAttribute('aria-selected', String(b.dataset.t === t)); });
    document.querySelectorAll('.demo-pane').forEach(function (p) { p.hidden = p.id !== 't-' + t; });
    if (t !== 'reg') sizeCanvases();
  }
  tabs.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.t); }); });

  // ---------- Firma ----------
  var sigs = {};
  function setupSig(id) {
    var c = document.getElementById(id), ctx = c.getContext('2d'), drawing = false, dirty = false;
    function pos(e) { var r = c.getBoundingClientRect(); return [(e.clientX - r.left) * c.width / r.width, (e.clientY - r.top) * c.height / r.height]; }
    c.addEventListener('pointerdown', function (e) { drawing = true; dirty = true; c.setPointerCapture(e.pointerId); var p = pos(e); ctx.beginPath(); ctx.moveTo(p[0], p[1]); });
    c.addEventListener('pointermove', function (e) { if (!drawing) return; var p = pos(e); ctx.lineTo(p[0], p[1]); ctx.stroke(); });
    ['pointerup', 'pointercancel'].forEach(function (ev) { c.addEventListener(ev, function () { drawing = false; }); });
    sigs[id] = {
      canvas: c,
      style: function () { ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.strokeStyle = '#0B1F3A'; },
      clear: function () { ctx.clearRect(0, 0, c.width, c.height); dirty = false; },
      signed: function () { return dirty; },
      data: function () { return c.toDataURL('image/png'); }
    };
    sigs[id].style();
  }
  function sizeCanvases() { Object.keys(sigs).forEach(function (k) { sigs[k].style(); }); }
  setupSig('sig-irl'); setupSig('sig-cap');
  document.querySelectorAll('.sig-clear').forEach(function (b) { b.addEventListener('click', function () { sigs[b.dataset.c].clear(); }); });

  // ---------- IRL ----------
  var mods = document.querySelectorAll('#irl-mods details'), read = new Set();
  mods.forEach(function (d, i) { d.addEventListener('toggle', function () { if (d.open) { read.add(i); d.classList.add('seen'); document.getElementById('irl-read').textContent = read.size; } }); });
  document.getElementById('irl-send').addEventListener('click', function () {
    var msg = document.getElementById('irl-msg'), nombre = document.getElementById('irl-nombre').value.trim();
    if (!nombre) { msg.textContent = 'Ingresa un nombre.'; return; }
    if (read.size < mods.length) { msg.textContent = 'Revisa los ' + mods.length + ' módulos antes de firmar.'; return; }
    if (!sigs['sig-irl'].signed()) { msg.textContent = 'Falta tu firma.'; return; }
    add({ tipo: 'Inducción IRL', nombre: nombre, detalle: document.getElementById('irl-cargo').value + ' · 6/6 módulos', ok: true, firma: sigs['sig-irl'].data() });
    msg.textContent = '✓ Inducción firmada y registrada.'; sigs['sig-irl'].clear();
  });

  // ---------- Cápsula ----------
  var slides = document.querySelectorAll('.slide'), si = 0;
  function go(n) {
    si = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (s, i) { s.classList.toggle('on', i === si); });
    if (si === slides.length - 1) document.getElementById('quiz').hidden = false;
  }
  document.getElementById('sl-prev').addEventListener('click', function () { go(si - 1); });
  document.getElementById('sl-next').addEventListener('click', function () { go(si + 1); });
  document.getElementById('cap-send').addEventListener('click', function () {
    var msg = document.getElementById('cap-msg'), a = document.querySelector('input[name=qa]:checked'), b = document.querySelector('input[name=qb]:checked');
    if (!a || !b) { msg.textContent = 'Responde las 2 preguntas.'; return; }
    if (!sigs['sig-cap'].signed()) { msg.textContent = 'Falta tu firma.'; return; }
    var nota = (+a.value) + (+b.value);
    add({ tipo: 'Cápsula: manejo manual de carga', nombre: document.getElementById('cap-nombre').value.trim() || 'Sin nombre', detalle: 'Evaluación ' + nota + '/2', ok: nota === 2, firma: sigs['sig-cap'].data() });
    msg.textContent = nota === 2 ? '✓ Aprobada y firmada.' : 'Registrada. Respuestas incorrectas: repasa la cápsula.';
    sigs['sig-cap'].clear();
  });

  // ---------- Inspección pre-uso ----------
  var CHECKS = {
    transpaleta: ['Batería cargada y conector en buen estado', 'Frenos y bocina funcionan', 'Horquillas sin deformaciones', 'Ruedas sin daños', 'Botón de parada de emergencia operativo'],
    rebanadora: ['Guarda protectora instalada', 'Hoja afilada y sin fisuras', 'Cable y enchufe en buen estado', 'Superficie limpia y sanitizada', 'Guante anticorte disponible'],
    horno: ['Sin olor a gas', 'Mangueras y válvulas sin daños', 'Encendido y apagado normal', 'Puerta y sellos en buen estado', 'Guantes térmicos disponibles']
  };
  var eq = document.getElementById('ins-eq'), list = document.getElementById('ins-list'), geo = '';
  function renderChecks() {
    list.innerHTML = CHECKS[eq.value].map(function (t, i) {
      return '<div class="ins-row"><span>' + esc(t) + '</span><label><input type="radio" name="c' + i + '" value="1"> Sí</label><label><input type="radio" name="c' + i + '" value="0"> No</label></div>';
    }).join('');
    document.getElementById('ins-res').hidden = true;
  }
  eq.addEventListener('change', renderChecks); renderChecks();
  document.getElementById('ins-geo').addEventListener('click', function () {
    var t = document.getElementById('ins-geo-t');
    if (!navigator.geolocation) { t.textContent = 'Tu navegador no permite ubicación.'; return; }
    t.textContent = 'Obteniendo ubicación…';
    navigator.geolocation.getCurrentPosition(function (p) {
      geo = p.coords.latitude.toFixed(5) + ', ' + p.coords.longitude.toFixed(5); t.textContent = '✓ ' + geo;
    }, function () { t.textContent = 'Ubicación no autorizada (es opcional).'; }, { timeout: 8000 });
  });
  document.getElementById('ins-send').addEventListener('click', function () {
    var n = CHECKS[eq.value].length, fails = [], res = document.getElementById('ins-res');
    for (var i = 0; i < n; i++) {
      var c = list.querySelector('input[name=c' + i + ']:checked');
      if (!c) { res.hidden = false; res.className = 'ins-res'; res.textContent = 'Responde los ' + n + ' puntos.'; return; }
      if (c.value === '0') fails.push(CHECKS[eq.value][i]);
    }
    var ok = !fails.length, name = eq.options[eq.selectedIndex].text;
    add({ tipo: 'Inspección pre-uso', nombre: document.getElementById('ins-nombre').value.trim() || 'Sin nombre', detalle: name + (ok ? ' · Apto' : ' · No apto: ' + fails.join(', ')), ok: ok, geo: geo });
    res.hidden = false;
    res.className = 'ins-res ' + (ok ? 'ok' : 'stop');
    res.innerHTML = ok ? '<b>✓ Equipo apto.</b> Puedes operar.' : '<b>✋ No operar.</b> Se avisó a tu supervisor: ' + esc(fails.join(', ')) + '.';
  });

  // ---------- Registros ----------
  function renderReg() {
    var l = memory, box = document.getElementById('reg-list');
    document.getElementById('reg-n').textContent = l.length;
    box.innerHTML = l.length ? l.map(function (r) {
      return '<article class="reg ' + (r.ok ? 'ok' : 'stop') + '"><div><b>' + esc(r.tipo) + '</b><span>' + esc(r.nombre) + ' · ' + esc(r.fecha) + '</span><small>' + esc(r.detalle) + (r.geo ? ' · 📍 ' + esc(r.geo) : '') + '</small></div>' +
        (r.firma ? '<img src="' + r.firma + '" alt="Firma">' : '') + '</article>';
    }).join('') : '<p class="demo-sub">Aún no hay registros. Completa una inducción, una cápsula o una inspección.</p>';
  }
  document.getElementById('reg-clear').addEventListener('click', function () { save([]); renderReg(); });
  renderReg();
})();
