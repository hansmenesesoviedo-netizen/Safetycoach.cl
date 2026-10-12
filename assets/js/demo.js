/* Demo SafetyCoach Digital (empresa ficticia). Los datos se guardan solo en este navegador. */
(function () {
  'use strict';
  var KEY = 'sc-demo-registros-v2';
  var CO = 'Alimentos Demo SpA';

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
  function save(list) { memory = list; try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* modo privado: solo en memoria */ } }
  var memory = load();
  function esc(t) { var d = document.createElement('div'); d.textContent = t == null ? '' : String(t); return d.innerHTML; }
  function $(id) { return document.getElementById(id); }
  function nowISO() { return new Date().toISOString(); }
  function fmt(iso) { return new Date(iso).toLocaleString('es-CL', { dateStyle: 'short', timeStyle: 'medium' }); }
  function rnd(n) { return Math.floor(Math.random() * Math.pow(10, n)).toString().padStart(n, '0'); }
  function folio(pre) { return pre + '-' + new Date().getFullYear() + '-' + rnd(4); }
  function verif() { return 'SC-' + Math.random().toString(16).slice(2, 8).toUpperCase(); }

  // Huella SHA-256 del registro (con respaldo simple si el navegador no la permite).
  function sha256(text) {
    if (window.crypto && crypto.subtle && window.TextEncoder) {
      return crypto.subtle.digest('SHA-256', new TextEncoder().encode(text)).then(function (buf) {
        return Array.prototype.map.call(new Uint8Array(buf), function (b) { return b.toString(16).padStart(2, '0'); }).join('');
      }).catch(fallback);
    }
    return Promise.resolve(fallback());
    function fallback() {
      var h = 2166136261;
      for (var i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
      return (h.toString(16) + '0'.repeat(56)).slice(0, 64);
    }
  }
  function add(rec) {
    rec.empresa = CO; rec.fecha = rec.fecha || nowISO(); rec.verificacion = verif();
    var base = JSON.stringify(rec);
    return sha256(base).then(function (h) { rec.hash = h; save([rec].concat(memory)); renderReg(); return rec; });
  }

  // ---------- Pestañas ----------
  var tabs = document.querySelectorAll('.demo-tabs [role="tab"]');
  function show(t) {
    tabs.forEach(function (b) { b.setAttribute('aria-selected', String(b.dataset.t === t)); });
    document.querySelectorAll('.demo-pane').forEach(function (p) { p.hidden = p.id !== 't-' + t; });
    if (t === 'cap') startTimer();
  }
  tabs.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.t); }); });

  // ---------- Firma ----------
  var sigs = {};
  function setupSig(id) {
    var c = $(id); if (!c) return;
    var ctx = c.getContext('2d'), drawing = false, dirty = false;
    function style() { ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.strokeStyle = '#0B1F3A'; }
    function pos(e) { var r = c.getBoundingClientRect(); return [(e.clientX - r.left) * c.width / r.width, (e.clientY - r.top) * c.height / r.height]; }
    c.addEventListener('pointerdown', function (e) { drawing = true; dirty = true; c.setPointerCapture(e.pointerId); style(); var p = pos(e); ctx.beginPath(); ctx.moveTo(p[0], p[1]); });
    c.addEventListener('pointermove', function (e) { if (!drawing) return; var p = pos(e); ctx.lineTo(p[0], p[1]); ctx.stroke(); });
    ['pointerup', 'pointercancel'].forEach(function (ev) { c.addEventListener(ev, function () { drawing = false; }); });
    sigs[id] = {
      clear: function () { ctx.clearRect(0, 0, c.width, c.height); dirty = false; },
      signed: function () { return dirty; },
      data: function () { return c.toDataURL('image/png'); }
    };
  }
  ['sig-irl', 'sig-cap', 'sig-epp', 'sig-ins'].forEach(setupSig);
  document.querySelectorAll('.sig-clear').forEach(function (b) { b.addEventListener('click', function () { sigs[b.dataset.c].clear(); }); });

  // ---------- 1. Documentos de ingreso ----------
  var docs = document.querySelectorAll('#irl-mods details'), read = new Set();
  docs.forEach(function (d, i) { d.addEventListener('toggle', function () { if (d.open) { read.add(i); d.classList.add('seen'); $('irl-read').textContent = read.size; } }); });
  $('irl-send').addEventListener('click', function () {
    var msg = $('irl-msg'), nombre = $('irl-nombre').value.trim();
    if (!nombre) { msg.textContent = 'Ingresa un nombre.'; return; }
    if (read.size < docs.length) { msg.textContent = 'Abre y lee los ' + docs.length + ' documentos antes de firmar.'; return; }
    if (!sigs['sig-irl'].signed()) { msg.textContent = 'Falta tu firma.'; return; }
    var f = folio('AD-ING'), firma = sigs['sig-irl'].data(), chain = Promise.resolve();
    docs.forEach(function (d) {
      chain = chain.then(function () {
        return add({ tipo: 'Documento de ingreso', codigo: d.dataset.code, documento: d.dataset.name, norma: d.dataset.ref, folio: f,
          nombre: nombre, rut: $('irl-rut').value, cargo: $('irl-cargo').value, ok: true, firma: firma, detalle: d.dataset.name });
      });
    });
    chain.then(function () { msg.textContent = '✓ ' + docs.length + ' documentos firmados · folio ' + f; sigs['sig-irl'].clear(); });
  });

  // ---------- 2. Cápsula interactiva ----------
  var MIN_SEG = 30, t0 = null, timerId = null, attempts = 1;
  function secs() { return t0 ? Math.round((Date.now() - t0) / 1000) : 0; }
  function startTimer() {
    if (t0) return; t0 = Date.now();
    timerId = setInterval(function () { var s = secs(); $('cap-timer').textContent = '⏱ ' + s + ' s' + (s < MIN_SEG ? ' · mínimo ' + MIN_SEG + ' s' : ' ✓'); }, 1000);
  }
  var slides = document.querySelectorAll('.slide'), steps = document.querySelectorAll('.cap-steps span'), si = 0, found = 0, scOk = false;
  function canLeave(i) {
    if (i === 1 && found < 3) { $('tap-msg').textContent = 'Encuentra las 3 conductas inseguras para continuar.'; return false; }
    if (i === 2 && !scOk) { $('sc-msg').textContent = 'Elige la respuesta correcta para continuar.'; return false; }
    return true;
  }
  function go(n) {
    if (n > si && !canLeave(si)) return;
    si = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (s, i) { s.classList.toggle('on', i === si); });
    steps.forEach(function (s, i) { s.classList.toggle('on', i <= si); });
    if (si === slides.length - 1) { $('quiz').hidden = false; steps[steps.length - 1].classList.add('on'); }
  }
  $('sl-prev').addEventListener('click', function () { go(si - 1); });
  $('sl-next').addEventListener('click', function () { go(si + 1); });
  document.querySelectorAll('#tap-grid button').forEach(function (b) {
    b.addEventListener('click', function () {
      if (b.classList.contains('hit') || b.classList.contains('miss')) return;
      if (b.dataset.bad === '1') { b.classList.add('hit'); found++; $('tap-msg').textContent = found < 3 ? '¡Bien! Encontradas: ' + found + ' de 3' : '✓ Las encontraste todas. Sigue.'; }
      else { b.classList.add('miss'); $('tap-msg').textContent = 'Esa es una conducta segura. Busca las inseguras.'; }
    });
  });
  document.querySelectorAll('#sc-grid button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('#sc-grid button').forEach(function (x) { x.classList.remove('hit', 'miss'); });
      if (b.dataset.ok === '1') { b.classList.add('hit'); scOk = true; $('sc-msg').textContent = '✓ Correcto: un cuchillo que cae no se ataja.'; }
      else { b.classList.add('miss'); $('sc-msg').textContent = 'Riesgo de corte grave. Inténtalo otra vez.'; }
    });
  });
  $('cap-send').addEventListener('click', function () {
    var msg = $('cap-msg'), ans = [1, 2, 3, 4].map(function (i) { return document.querySelector('input[name=q' + i + ']:checked'); });
    if (ans.some(function (a) { return !a; })) { msg.textContent = 'Responde las 4 preguntas.'; return; }
    if (secs() < MIN_SEG) { msg.textContent = 'Tiempo mínimo de la cápsula: faltan ' + (MIN_SEG - secs()) + ' s.'; return; }
    var nota = ans.reduce(function (s, a) { return s + (+a.value); }, 0);
    if (nota < 3) {
      msg.textContent = 'Obtuviste ' + nota + ' de 4. Repasa y vuelve a intentarlo.';
      attempts++; $('cap-try').textContent = attempts;
      document.querySelectorAll('.quiz input[type=radio]').forEach(function (r) { r.checked = false; });
      return;
    }
    if (!sigs['sig-cap'].signed()) { msg.textContent = 'Falta tu firma.'; return; }
    add({ tipo: 'Cápsula', codigo: 'AD-CAP-M03', documento: 'Cápsula M03 · Prevención de cortes', norma: 'DS 44 · Capacitación', folio: folio('AD-CAP'),
      nombre: $('cap-nombre').value.trim() || 'Sin nombre', ok: true, firma: sigs['sig-cap'].data(),
      detalle: 'Aprobada ' + nota + '/4 · intento ' + attempts + ' · ' + secs() + ' s',
      campos: { 'Puntaje': nota + ' de 4', 'Resultado': 'Aprobada', 'Intentos': attempts, 'Duración de la sesión': secs() + ' s', 'Tiempo mínimo pedagógico': 'Cumple (' + MIN_SEG + ' s)', 'Actividades interactivas': '3 de 3 conductas inseguras identificadas · escenario correcto' } })
      .then(function (r) { msg.textContent = '✓ Aprobada y firmada · código ' + r.verificacion; sigs['sig-cap'].clear(); });
  });

  // ---------- 3. Entrega de EPP ----------
  var EPP = [
    ['Zapatos de seguridad antideslizantes', 'Talla', '42', 'Certificado ISP'],
    ['Guante anticorte nivel 5', 'Talla', 'M', 'EN 388'],
    ['Guantes térmicos', 'Talla', 'M', 'EN 407'],
    ['Lentes de seguridad', '', '', 'Certificado ISP'],
    ['Protector auditivo tipo fono', '', '', 'Certificado ISP'],
    ['Delantal impermeable', 'Talla', 'L', '—']
  ];
  $('epp-list').innerHTML = EPP.map(function (e, i) {
    return '<div class="epp-row"><label class="chk"><input type="checkbox" data-i="' + i + '"' + (i < 3 ? ' checked' : '') + '> <span>' + esc(e[0]) + ' <small>' + esc(e[3]) + '</small></span></label>' +
      (e[1] ? '<input class="epp-talla" data-i="' + i + '" value="' + esc(e[2]) + '" aria-label="Talla">' : '<span></span>') +
      '<input class="epp-cant" type="number" min="1" value="1" data-i="' + i + '" aria-label="Cantidad"></div>';
  }).join('');
  $('epp-send').addEventListener('click', function () {
    var msg = $('epp-msg'), nombre = $('epp-nombre').value.trim(), items = [];
    document.querySelectorAll('#epp-list input[type=checkbox]:checked').forEach(function (c) {
      var i = c.dataset.i, t = document.querySelector('.epp-talla[data-i="' + i + '"]'), q = document.querySelector('.epp-cant[data-i="' + i + '"]');
      items.push(EPP[i][0] + (t ? ' (talla ' + t.value + ')' : '') + ' × ' + (q.value || 1) + ' · ' + EPP[i][3]);
    });
    if (!nombre) { msg.textContent = 'Ingresa el nombre del trabajador.'; return; }
    if (!items.length) { msg.textContent = 'Marca al menos un elemento.'; return; }
    if (!sigs['sig-epp'].signed()) { msg.textContent = 'Falta la firma del trabajador.'; return; }
    add({ tipo: 'Entrega de EPP', codigo: 'AD-RE-EPP', documento: 'Registro de entrega de elementos de protección personal', norma: 'Ley 16.744 Art. 68 · DS 594 Art. 53', folio: folio('AD-EPP'),
      nombre: nombre, cargo: $('epp-cargo').value, ok: true, firma: sigs['sig-epp'].data(),
      detalle: items.length + ' elementos · ' + $('epp-motivo').value,
      campos: { 'Motivo': $('epp-motivo').value, 'Elementos entregados': items.join('\n'), 'Instrucción de uso': 'Sí, al momento de la entrega' } })
      .then(function (r) { msg.textContent = '✓ Entrega registrada · folio ' + r.folio; sigs['sig-epp'].clear(); });
  });

  // ---------- 4. Inspección de máquina (operación · mantención · limpieza, con criterios STOP) ----------
  var LOTO = [['Planificar la tarea y avisar a los afectados', 1], ['Apagar la máquina con su control normal', 1], ['Aislar la energía (desconectar del tablero o enchufe)', 1], ['Bloquear con candado y tarjeta personal', 1], ['Disipar energía residual', 1], ['Verificar estado cero: intentar encender sin resultado', 1]];
  var MAQ = {
    sierra: { n: 'Sierra de banco SB-01 · Taller de mantención', serie: 'SB-2024-0117', riesgos: 'Corte o amputación · proyección de partículas · contacto eléctrico',
      op: [['Resguardo superior del disco instalado y sin intervenir', 1], ['Cuchillo divisor alineado con el disco', 1], ['Parada de emergencia operativa, visible y accesible', 1], ['Disco sin dientes faltantes ni fisuras', 1], ['Empujador disponible para cortes angostos', 0], ['Cable, enchufe y tablero sin daños, comandos en español', 0], ['Lentes de seguridad y protector auditivo en uso', 0], ['Operador habilitado para esta máquina', 1]],
      mant: [['Herramientas adecuadas y en buen estado', 0]], limp: [['Máquina detenida y desenergizada antes de limpiar', 1], ['Viruta retirada con escobilla o aspiradora, nunca con la mano', 0], ['Área libre de residuos y derrames', 0]] },
    esmeril: { n: 'Esmeril angular EA-02 · Taller de mantención', serie: 'EA-2023-0042', riesgos: 'Proyección de partículas · corte · contacto eléctrico · incendio por chispas',
      op: [['Guarda del disco instalada', 1], ['Disco compatible con las RPM y sin daños', 1], ['Mango lateral instalado', 0], ['Cable y enchufe sin daños', 1], ['Careta facial, lentes y guantes en uso', 1], ['Área sin materiales combustibles cerca', 0], ['Operador habilitado para esta máquina', 1]],
      mant: [['Cambio de disco con la llave correcta', 0]], limp: [['Esmeril desenchufado antes de limpiar', 1], ['Rejillas de ventilación limpias', 0]] },
    rebanadora: { n: 'Rebanadora industrial RB-01 · Cocina', serie: 'RB-2022-0310', riesgos: 'Corte o amputación · contacto eléctrico',
      op: [['Guarda de la hoja instalada', 1], ['Carro portaalimentos y empujador funcionan', 1], ['Hoja sin fisuras ni desgaste irregular', 0], ['Cable y enchufe sin daños', 0], ['Guante anticorte disponible', 1], ['Operador habilitado para esta máquina', 1]],
      mant: [['Afilado solo por personal autorizado', 0]], limp: [['Desenchufada y perilla en cero antes de limpiar', 1], ['Guante anticorte en uso durante la limpieza', 1], ['Limpieza desde el centro hacia afuera de la hoja', 0]] }
  };
  var eq = $('ins-eq'), list = $('ins-list'), kind = 'op', geo = '';
  eq.innerHTML = Object.keys(MAQ).map(function (k) { return '<option value="' + k + '">' + esc(MAQ[k].n) + '</option>'; }).join('');
  function items() { var m = MAQ[eq.value]; return kind === 'mant' ? LOTO.concat(m.mant) : m[kind]; }
  function renderChecks() {
    var m = MAQ[eq.value];
    $('ins-serie-n').textContent = m.serie; $('ins-serie').checked = false;
    list.innerHTML = '<p class="ins-risk"><b>Riesgos críticos (matriz):</b> ' + esc(m.riesgos) + '</p>' +
      (kind === 'mant' ? '<p class="ins-loto">Bloqueo de energías (LOTO): las 6 etapas son obligatorias antes de intervenir.</p>' : '') +
      items().map(function (it, i) {
        return '<div class="ins-row" data-i="' + i + '"><span>' + esc(it[0]) + (it[1] ? ' <em class="stop-b">STOP</em>' : '') + '</span>' +
          '<div class="cnc"><button type="button" data-v="C">C</button><button type="button" data-v="NC">NC</button><button type="button" data-v="NA">N/A</button></div>' +
          '<div class="nc-box" hidden><input placeholder="Hallazgo" class="nc-h"><input placeholder="Acción correctiva" class="nc-a"><input type="date" class="nc-p" aria-label="Plazo"></div></div>';
      }).join('');
    $('ins-res').hidden = true;
  }
  list.addEventListener('click', function (e) {
    var b = e.target.closest('.cnc button'); if (!b) return;
    var row = b.closest('.ins-row');
    row.querySelectorAll('.cnc button').forEach(function (x) { x.classList.toggle('on', x === b); });
    row.dataset.v = b.dataset.v;
    row.querySelector('.nc-box').hidden = b.dataset.v !== 'NC';
  });
  eq.addEventListener('change', renderChecks);
  document.querySelectorAll('#ins-type button').forEach(function (b) {
    b.addEventListener('click', function () {
      kind = b.dataset.k;
      document.querySelectorAll('#ins-type button').forEach(function (x) { x.setAttribute('aria-selected', String(x === b)); });
      renderChecks();
    });
  });
  renderChecks();
  $('ins-geo').addEventListener('click', function () {
    var t = $('ins-geo-t');
    if (!navigator.geolocation) { t.textContent = 'Tu navegador no permite ubicación.'; return; }
    t.textContent = 'Obteniendo ubicación…';
    navigator.geolocation.getCurrentPosition(function (p) {
      geo = p.coords.latitude.toFixed(5) + ', ' + p.coords.longitude.toFixed(5); t.textContent = '✓ ' + geo;
    }, function () { t.textContent = 'Ubicación no autorizada (es opcional).'; }, { timeout: 8000 });
  });
  $('ins-send').addEventListener('click', function () {
    var res = $('ins-res'), m = MAQ[eq.value], its = items(), rows = list.querySelectorAll('.ins-row'), stop = [], nc = [], c = 0;
    function err(t) { res.hidden = false; res.className = 'ins-res'; res.textContent = t; }
    if (!$('ins-serie').checked) return err('Confirma que el N° de serie coincide con la máquina.');
    for (var i = 0; i < rows.length; i++) {
      var v = rows[i].dataset.v;
      if (!v) return err('Marca los ' + rows.length + ' ítems (C, NC o N/A).');
      if (v === 'C') c++;
      if (v === 'NC') {
        var h = rows[i].querySelector('.nc-h').value.trim(), a = rows[i].querySelector('.nc-a').value.trim(), p = rows[i].querySelector('.nc-p').value;
        if (!h || !a || !p) return err('Completa hallazgo, acción correctiva y plazo en cada No conforme.');
        nc.push(its[i][0] + ': ' + h + ' → ' + a + ' (plazo ' + p + ')');
        if (its[i][1]) stop.push(its[i][0]);
      }
    }
    if (!sigs['sig-ins'].signed()) return err('Falta la firma del inspector.');
    var ok = !stop.length, tipo = { op: 'Operación (preuso)', mant: 'Mantención', limp: 'Limpieza' }[kind];
    var estado = stop.length ? 'FUERA DE SERVICIO' : (nc.length ? 'Apta con hallazgos' : 'Apta');
    add({ tipo: 'Inspección de máquina', codigo: 'AD-INS-' + eq.value.toUpperCase(), documento: m.n + ' · ' + tipo, norma: 'Res. Ex. 341 ISP (PROSEMEH) · DS 44', folio: folio('AD-INS'),
      nombre: $('ins-nombre').value.trim() || 'Sin nombre', ok: ok, firma: sigs['sig-ins'].data(), geo: geo,
      detalle: m.n.split(' · ')[0] + ' · ' + tipo + ' · ' + estado,
      campos: { 'N° de serie': m.serie + ' (verificado)', 'Tipo de inspección': tipo, 'Resultado': estado, 'Conformes': c + ' de ' + rows.length, 'Hallazgos': nc.length ? nc.join('\n') : 'Sin hallazgos', 'Criterio STOP': stop.length ? stop.join(', ') : 'No aplica' } })
      .then(function (r) {
        res.hidden = false;
        res.className = 'ins-res ' + (stop.length ? 'stop' : 'ok');
        res.innerHTML = stop.length
          ? '<b>✋ STOP: máquina fuera de servicio.</b> Etiquétala, desenergízala y avisa a tu supervisor y a Prevención. Motivo: ' + esc(stop.join(', ')) + '. Folio ' + esc(r.folio) + '.'
          : '<b>✓ ' + esc(estado) + '.</b> ' + (nc.length ? nc.length + ' hallazgo(s) con acción y plazo. ' : '') + 'Folio ' + esc(r.folio) + '.';
        sigs['sig-ins'].clear();
      });
  });

  // ---------- 5. Registros, indicadores y comprobante ----------
  function renderReg() {
    var l = memory, box = $('reg-list');
    $('reg-n').textContent = l.length;
    var ins = l.filter(function (r) { return r.tipo === 'Inspección de máquina'; });
    var hall = ins.reduce(function (s, r) { return s + (r.campos && r.campos['Hallazgos'] !== 'Sin hallazgos' ? r.campos['Hallazgos'].split('\n').length : 0); }, 0);
    var k = [
      [l.filter(function (r) { return r.tipo === 'Documento de ingreso'; }).length, 'documentos de ingreso firmados'],
      [l.filter(function (r) { return r.tipo === 'Cápsula'; }).length, 'cápsulas aprobadas'],
      [l.filter(function (r) { return r.tipo === 'Entrega de EPP'; }).length, 'entregas de EPP'],
      [ins.length ? Math.round(100 * ins.filter(function (r) { return r.ok; }).length / ins.length) + '%' : '—', 'máquinas aptas'],
      [hall, 'hallazgos con acción y plazo']
    ];
    $('kpis').innerHTML = k.map(function (x) { return '<div><b>' + x[0] + '</b><span>' + x[1] + '</span></div>'; }).join('');
    box.innerHTML = l.length ? l.map(function (r, i) {
      return '<article class="reg ' + (r.ok ? 'ok' : 'stop') + '"><div><b>' + esc(r.tipo) + ' · ' + esc(r.codigo) + '</b><span>' + esc(r.nombre) + ' · ' + esc(fmt(r.fecha)) + '</span><small>' + esc(r.detalle) + (r.geo ? ' · 📍 ' + esc(r.geo) : '') + '</small><small class="reg-h">Folio ' + esc(r.folio) + ' · ' + esc(r.verificacion) + ' · hash ' + esc(r.hash.slice(0, 12)) + '…</small><button type="button" class="reg-ver" data-i="' + i + '">Ver comprobante</button></div>' +
        (r.firma ? '<img src="' + r.firma + '" alt="Firma">' : '') + '</article>';
    }).join('') : '<p class="demo-sub">Aún no hay registros. Firma los documentos de ingreso, aprueba la cápsula, registra una entrega de EPP o inspecciona una máquina.</p>';
  }
  $('reg-list').addEventListener('click', function (e) {
    var b = e.target.closest('.reg-ver'); if (!b) return;
    var r = memory[+b.dataset.i], rows = [['Empresa', r.empresa], ['Documento', r.documento], ['Código', r.codigo], ['Normativa', r.norma], ['Folio', r.folio], ['Nombre', r.nombre]];
    if (r.rut) rows.push(['RUT', r.rut]);
    if (r.cargo) rows.push(['Cargo', r.cargo]);
    Object.keys(r.campos || {}).forEach(function (k) { rows.push([k, r.campos[k]]); });
    if (r.geo) rows.push(['Ubicación', r.geo]);
    rows.push(['Fecha y hora', fmt(r.fecha)]);
    $('comp-in').innerHTML = '<p class="comp-k">Comprobante · demo</p><h3>' + esc(r.documento) + '</h3><dl>' +
      rows.map(function (x) { return '<dt>' + esc(x[0]) + '</dt><dd>' + esc(x[1]).replace(/\n/g, '<br>') + '</dd>'; }).join('') + '</dl>' +
      (r.firma ? '<img class="comp-sig" src="' + r.firma + '" alt="Firma">' : '') +
      '<p class="comp-v">Firma validada · ' + esc(r.fecha) + '<br>Código de verificación ' + esc(r.verificacion) + '<br>SHA-256 ' + esc(r.hash) + '</p>';
    var d = $('comp'); if (d.showModal) d.showModal(); else d.setAttribute('open', '');
  });
  $('comp-close').addEventListener('click', function () { var d = $('comp'); if (d.close) d.close(); else d.removeAttribute('open'); });
  $('comp-print').addEventListener('click', function () { window.print(); });
  $('reg-clear').addEventListener('click', function () { save([]); renderReg(); });
  renderReg();
})();
