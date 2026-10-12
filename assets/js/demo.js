/* Demo SafetyCoach Digital (empresa ficticia). Los datos se guardan solo en este navegador.
   Cada registro se entrega en el mismo formato de hoja que usan los clientes de SafetyCoach. */
(function () {
  'use strict';
  var KEY = 'sc-demo-registros-v3';
  var CO = 'Alimentos Demo SpA', RUT = '76.000.000-0', CO_UP = 'ALIMENTOS DEMO SPA';
  var RELATOR = 'Encargado de Prevención · SafetyCoach';

  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || null; } catch (e) { return null; } }
  function save(list) { memory = list; try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* modo privado */ } }
  var memory = load();
  function esc(t) { var d = document.createElement('div'); d.textContent = t == null ? '' : String(t); return d.innerHTML; }
  function $(id) { return document.getElementById(id); }
  function day(iso) { return iso.slice(0, 10); }
  function fmt(iso) { return new Date(iso).toLocaleString('es-CL', { dateStyle: 'short', timeStyle: 'short' }); }
  function rnd(n) { return Math.floor(Math.random() * Math.pow(10, n)).toString().padStart(n, '0'); }
  function folio(pre) { return 'AD-' + pre + '-' + new Date().getFullYear() + '-' + rnd(4); }

  function sha256(text) {
    function fallback() {
      var h = 2166136261;
      for (var i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
      return (h.toString(16) + '0'.repeat(56)).slice(0, 64);
    }
    if (window.crypto && crypto.subtle && window.TextEncoder) {
      return crypto.subtle.digest('SHA-256', new TextEncoder().encode(text)).then(function (buf) {
        return Array.prototype.map.call(new Uint8Array(buf), function (b) { return b.toString(16).padStart(2, '0'); }).join('');
      }).catch(fallback);
    }
    return Promise.resolve(fallback());
  }
  function stamp(rec) {
    rec.fecha = rec.fecha || new Date().toISOString();
    return sha256(JSON.stringify(rec)).then(function (h) { rec.hash = h; return rec; });
  }
  function add(rec) { return stamp(rec).then(function (r) { save([r].concat(memory || [])); renderReg(); return r; }); }

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
    function pos(e) { var r = c.getBoundingClientRect(); return [(e.clientX - r.left) * c.width / r.width, (e.clientY - r.top) * c.height / r.height]; }
    c.addEventListener('pointerdown', function (e) { drawing = true; dirty = true; c.setPointerCapture(e.pointerId); ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.strokeStyle = '#111'; var p = pos(e); ctx.beginPath(); ctx.moveTo(p[0], p[1]); });
    c.addEventListener('pointermove', function (e) { if (!drawing) return; var p = pos(e); ctx.lineTo(p[0], p[1]); ctx.stroke(); });
    ['pointerup', 'pointercancel'].forEach(function (ev) { c.addEventListener(ev, function () { drawing = false; }); });
    sigs[id] = { clear: function () { ctx.clearRect(0, 0, c.width, c.height); dirty = false; }, signed: function () { return dirty; }, data: function () { return c.toDataURL('image/png'); } };
  }
  ['sig-irl', 'sig-cap', 'sig-epp', 'sig-ins'].forEach(setupSig);
  document.querySelectorAll('.sig-clear').forEach(function (b) { b.addEventListener('click', function () { sigs[b.dataset.c].clear(); }); });
  // Firma de ejemplo para los registros precargados.
  function sampleSig() {
    var c = document.createElement('canvas'); c.width = 600; c.height = 160; var x = c.getContext('2d');
    x.lineWidth = 3; x.lineCap = 'round'; x.strokeStyle = '#111'; x.beginPath();
    x.moveTo(60, 110); x.bezierCurveTo(120, 20, 170, 150, 230, 70); x.bezierCurveTo(260, 30, 300, 120, 340, 80); x.lineTo(420, 60); x.moveTo(180, 120); x.lineTo(470, 95);
    x.stroke(); return c.toDataURL('image/png');
  }

  // ---------- Datos de los formatos ----------
  var PTS = ['PTS: Uso seguro de cuchillos y elementos de corte', 'PTS: Uso seguro de cocina y gas', 'PTS: Uso de rebanadora industrial', 'Procedimiento de gestión de incidentes y accidentes', 'Plan de emergencia y evacuación', 'Protocolo de prevención de acoso laboral, sexual y violencia en el trabajo (Ley Karin)', 'HDS: Desengrasante industrial', 'HDS: Cloro 5%'];
  var IRL = ['M01 — Bienvenida, empresa y marco legal', 'M02 — Lugar de trabajo y matriz de riesgos', 'M03 — Cortes y uso seguro de cuchillos', 'M04 — Quemaduras y cocción segura', 'M05 — Caídas, orden y limpieza', 'M06 — Ergonomía y manejo manual de carga', 'M07 — Productos químicos, HDS y SGA', 'M08 — Emergencias: gas, incendio y evacuación', 'M09 — Riesgo psicosocial y Ley Karin', 'M10 — Accidentes, incidentes y alertas de peligro'];
  function ingresoSheets(p, firma) {
    var base = [['Nombre completo', p.nombre], ['N° Carnet identidad', p.rut], ['Cargo', p.cargo], ['Centro de trabajo', 'Planta Santiago']];
    var rel = ['Modalidad', 'Capacitación en línea · equivale a 2 horas'], rl = ['Relator', RELATOR];
    return [
      { fmt: 'fc', tipo: 'Documento de ingreso', code: 'AD-RE-RIOHS', titulo: 'Entrega y Recepción del Reglamento Interno', norma: 'Art.156° CT · DS44 Art.56', folio: folio('RIOHS'), nombre: p.nombre,
        kv: base.concat([['Fecha de entrega', 'hoy']]), firma: firma, relator: false,
        decl: 'Declaro haber recibido en forma gratuita una copia del <b>REGLAMENTO INTERNO DE ORDEN, HIGIENE Y SEGURIDAD (RIOHS)</b> de la Empresa <b>' + CO_UP + '</b>, de acuerdo con lo establecido en el artículo 156° inciso 2 del Código del Trabajo y el artículo 56 del Decreto Supremo N°44/2024. Asumo mi responsabilidad de dar lectura a su contenido y dar cumplimiento a las obligaciones, prohibiciones y normas de orden, higiene y seguridad que en él están escritas.' },
      { fmt: 'fc', tipo: 'Documento de ingreso', code: 'AD-RE-PTS', titulo: 'Registro de Capacitación y Entrega de Procedimientos', norma: 'DS44 Art.15 num.3-4 · DS43 SGA · Ley 16.744', folio: folio('PTS'), nombre: p.nombre,
        kv: [['Trabajador/a', p.nombre], ['RUT', p.rut], ['Centro de trabajo', 'Planta Santiago'], ['Fecha', 'hoy'], rel, rl], list: { t: 'Procedimientos, protocolos y HDS entregados', items: PTS }, firma: firma, relator: true,
        decl: 'Declaro haber recibido y comprendido la información entregada. Se me ha informado sobre los riesgos, medidas de prevención y métodos de trabajo seguro. He recibido los documentos indicados, conforme al D.S. N°44/2024 Art.15.' },
      { fmt: 'fc', tipo: 'Documento de ingreso', code: 'AD-RE-IRL', titulo: 'Registro de Información de Riesgos Laborales (IRL)', norma: 'DS44 Art.15 · Derecho a Saber · Ley 16.744', folio: folio('IRL'), nombre: p.nombre,
        kv: [['Tipo de inducción', 'Trabajador/a nuevo/a'], ['Nombre completo', p.nombre], ['N° Carnet identidad', p.rut], ['Cargo', p.cargo], ['Centro de trabajo', 'Planta Santiago'], ['Fecha', 'hoy'], rel, rl],
        list: { t: 'Módulos IRL completados y aprobados', items: IRL.concat(['PTS y plan de emergencia entregados', 'RIOHS + protocolo Ley Karin entregados']) }, firma: firma, relator: true,
        decl: 'Declaro haber completado el proceso de integración y formación IRL de <b>' + CO_UP + '</b> (RUT ' + RUT + '). Cada módulo fue impartido en lenguaje comprensible. Ninguna actividad fue realizada fuera de mi horario laboral. Declaro conocer el protocolo de emergencias, el procedimiento de reporte de incidentes y el canal de denuncia. Se conservará por mínimo 5 años.' }
    ];
  }

  // ---------- 1. Documentos de ingreso ----------
  var docs = document.querySelectorAll('#irl-mods details'), read = new Set();
  docs.forEach(function (d, i) { d.addEventListener('toggle', function () { if (d.open) { read.add(i); d.classList.add('seen'); $('irl-read').textContent = read.size; } }); });
  $('irl-send').addEventListener('click', function () {
    var msg = $('irl-msg'), nombre = $('irl-nombre').value.trim();
    if (!nombre) { msg.textContent = 'Ingresa un nombre.'; return; }
    if (read.size < docs.length) { msg.textContent = 'Abre y lee los ' + docs.length + ' documentos antes de firmar.'; return; }
    if (!sigs['sig-irl'].signed()) { msg.textContent = 'Falta tu firma.'; return; }
    var sh = ingresoSheets({ nombre: nombre, rut: $('irl-rut').value, cargo: $('irl-cargo').value }, sigs['sig-irl'].data()), chain = Promise.resolve();
    sh.reverse().forEach(function (r) { r.detalle = r.titulo; r.ok = true; chain = chain.then(function () { return add(r); }); });
    chain.then(function () { msg.textContent = '✓ 3 registros firmados. Míralos en Registros o en la carpeta de abajo.'; sigs['sig-irl'].clear(); });
  });

  // ---------- 2. Cápsula interactiva ----------
  var MIN_SEG = 30, t0 = null, attempts = 1, sesIni = null;
  function secs() { return t0 ? Math.round((Date.now() - t0) / 1000) : 0; }
  function startTimer() {
    if (t0) return; t0 = Date.now(); sesIni = new Date().toISOString();
    setInterval(function () { var s = secs(); $('cap-timer').textContent = '⏱ ' + s + ' s' + (s < MIN_SEG ? ' · mínimo ' + MIN_SEG + ' s' : ' ✓'); }, 1000);
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
    var nota = ans.reduce(function (s, a) { return s + (+a.value); }, 0);
    if (nota < 3) {
      msg.textContent = 'Obtuviste ' + nota + ' de 4. Repasa y vuelve a intentarlo.';
      attempts++; $('cap-try').textContent = attempts;
      document.querySelectorAll('.quiz input[type=radio]').forEach(function (r) { r.checked = false; });
      return;
    }
    if (secs() < MIN_SEG) { msg.textContent = 'Tiempo mínimo de la cápsula: faltan ' + (MIN_SEG - secs()) + ' s.'; return; }
    if (!sigs['sig-cap'].signed()) { msg.textContent = 'Falta tu firma.'; return; }
    var nombre = $('cap-nombre').value.trim() || 'Sin nombre', fin = new Date().toISOString();
    add({ fmt: 'fc', tipo: 'Cápsula', code: 'AD-RE-CAP-M03', titulo: 'Registro de Capacitación — Cápsula M03 · Prevención de cortes', norma: 'DS44 Art.15-16 · Ley 16.744', folio: folio('CAP'), nombre: nombre,
      kv: [['Trabajador/a', nombre], ['Módulo', 'M03 — Prevención de cortes · versión 1'], ['Inicio de sesión', fmt(sesIni)], ['Término de sesión', fmt(fin)], ['Duración', secs() + ' s'],
        ['Tiempo mínimo pedagógico', 'Cumple (' + MIN_SEG + ' s)'], ['Evaluación', nota + ' de 4 (' + (nota * 25) + '%) · Aprobada'], ['Intentos', String(attempts)], ['Modalidad', 'Cápsula interactiva en línea'], ['Relator', RELATOR]],
      list: { t: 'Actividades completadas', items: ['Video y contenido del módulo', 'Identificación de 3 conductas inseguras (3 de 3)', 'Escenario de decisión: respuesta correcta', 'Evaluación final aprobada'] },
      firma: sigs['sig-cap'].data(), relator: true, ok: true, detalle: 'Aprobada ' + nota + '/4 · intento ' + attempts + ' · ' + secs() + ' s',
      decl: 'Declaro haber realizado personalmente esta cápsula de capacitación, dentro de mi horario laboral, y haber comprendido su contenido. Me comprometo a aplicar las medidas preventivas aprendidas en mi trabajo diario.' })
      .then(function (r) { msg.textContent = '✓ Aprobada y firmada · folio ' + r.folio; sigs['sig-cap'].clear(); });
  });

  // ---------- 3. Entrega de EPP ----------
  var EPP = [
    ['Calzado de seguridad antideslizante sin cordones', 'NCh461 · DS594 Art.53', '42'],
    ['Guantes anticorte nivel 3 o superior', 'NCh1261', 'M'],
    ['Guantes térmicos / anticontacto calor', 'NCh1261', 'M'],
    ['Antiparras de seguridad', 'DS594 Art.53', ''],
    ['Protector auditivo tipo fono', 'DS594 Art.53', ''],
    ['Delantal impermeable', 'DS594 Art.53', 'L']
  ];
  $('epp-list').innerHTML = EPP.map(function (e, i) {
    return '<div class="epp-row"><label class="chk"><input type="checkbox" data-i="' + i + '"' + (i < 4 ? ' checked' : '') + '> <span>' + esc(e[0]) + ' <small>' + esc(e[1]) + '</small></span></label>' +
      (e[2] ? '<input class="epp-talla" data-i="' + i + '" value="' + esc(e[2]) + '" aria-label="Talla">' : '<span class="epp-na">—</span>') +
      '<input class="epp-cant" type="number" min="1" value="1" data-i="' + i + '" aria-label="Cantidad"></div>';
  }).join('');
  $('epp-send').addEventListener('click', function () {
    var msg = $('epp-msg'), nombre = $('epp-nombre').value.trim(), rows = [];
    document.querySelectorAll('#epp-list input[type=checkbox]:checked').forEach(function (c) {
      var i = c.dataset.i, t = document.querySelector('.epp-talla[data-i="' + i + '"]'), q = document.querySelector('.epp-cant[data-i="' + i + '"]');
      rows.push([EPP[i][0], EPP[i][1], t ? t.value : '—', q.value || '1']);
    });
    if (!nombre) { msg.textContent = 'Ingresa el nombre del trabajador.'; return; }
    if (!rows.length) { msg.textContent = 'Marca al menos un elemento.'; return; }
    if (!sigs['sig-epp'].signed()) { msg.textContent = 'Falta la firma del trabajador.'; return; }
    add({ fmt: 'fc', tipo: 'Entrega de EPP', code: 'AD-RE-EPP', titulo: 'Registro de Entrega de Elementos de Protección Personal', norma: 'DS594 Art.53 · NCh461 · NCh1261', folio: folio('EPP'), nombre: nombre,
      kv: [['Trabajador/a', nombre], ['Cargo', $('epp-cargo').value], ['Centro de trabajo', 'Planta Santiago'], ['Motivo de la entrega', $('epp-motivo').value], ['Fecha', 'hoy']],
      table: { t: 'Elementos de protección personal entregados', head: ['Elemento', 'Norma', 'Talla', 'Cant.'], rows: rows },
      firma: sigs['sig-epp'].data(), relator: false, ok: true, detalle: rows.length + ' elementos · ' + $('epp-motivo').value,
      decl: 'Declaro haber recibido en forma gratuita los EPP detallados, en buen estado y en la talla indicada. Me comprometo a usarlos durante toda la jornada y a reportar cualquier deterioro, conforme al DS594 Art.53 y el RIOHS vigente.' })
      .then(function (r) { msg.textContent = '✓ Entrega registrada · folio ' + r.folio; sigs['sig-epp'].clear(); });
  });

  // ---------- 4. Inspección de máquina (formato PROSEMEH) ----------
  var MAQ = {
    esmeril: { n: 'Esmeril Angular', code: 'AD-INS-ESANG', serie: '6', area: 'Taller de mantención', hab: 'Maestro de mantención', riesgos: 'Proyección de partículas · corte · contacto eléctrico · incendio por chispas',
      op: [['Disco sin grietas, deformación ni desgaste excesivo', 1], ['Disco compatible (diámetro y velocidad máxima ≥ velocidad máquina)', 1], ['Protector de disco instalado y orientado hacia el operador', 1], ['Material sujeto firmemente antes de operar', 1], ['Protector facial completo en uso (no solo antiparras)', 1], ['Protección auditiva en uso', 0], ['Guantes de seguridad en uso', 0], ['Ropa ajustada — sin mangas sueltas ni elementos colgantes', 0], ['Sin personal en área de proyección de chispas', 1], ['Sin inflamables almacenados cerca del área', 1]],
      mant: [['Herramienta desenchufada antes de intervenir (bloqueo de energía)', 1], ['Cambio de disco con la llave adecuada', 0], ['Cable, enchufe y carcasa sin daños', 1], ['Protector reinstalado y ajustado tras la mantención', 1]],
      limp: [['Herramienta desenchufada antes de limpiar', 1], ['Rejillas de ventilación limpias, sin polvo metálico', 0]] },
    sierra: { n: 'Mesa Sierra (sierra de banco)', code: 'AD-INS-MSIER', serie: '2', area: 'Taller de mantención', hab: 'Maestro de mantención', riesgos: 'Corte o amputación · proyección de partículas · contacto eléctrico',
      op: [['Resguardo superior del disco instalado y sin intervenir', 1], ['Cuchillo divisor alineado con el disco', 1], ['Parada de emergencia operativa, visible y accesible', 1], ['Disco sin dientes faltantes ni fisuras', 1], ['Empujador disponible para cortes angostos', 0], ['Tablero de comandos identificado en español', 0], ['Antiparras y protector auditivo en uso', 0], ['Operador habilitado para esta máquina', 1]],
      mant: [['Bloqueo LOTO aplicado: candado y tarjeta personal', 1], ['Energía residual disipada y estado cero verificado', 1], ['Herramientas adecuadas y en buen estado', 0]],
      limp: [['Máquina detenida y desenergizada antes de limpiar', 1], ['Viruta retirada con escobilla o aspiradora, nunca con la mano', 0], ['Área libre de residuos y derrames', 0]] },
    rebanadora: { n: 'Rebanadora Industrial', code: 'AD-INS-REBAN', serie: '1', area: 'Cocina', hab: 'Ayudante de cocina habilitado', riesgos: 'Corte o amputación · contacto eléctrico',
      op: [['Guarda de la hoja instalada', 1], ['Carro portaalimentos y empujador funcionan', 1], ['Hoja sin fisuras ni desgaste irregular', 0], ['Cable y enchufe sin daños', 0], ['Guante anticorte disponible y en uso', 1], ['Operador habilitado para esta máquina', 1]],
      mant: [['Desenchufada antes de intervenir', 1], ['Afilado solo por personal autorizado', 0]],
      limp: [['Desenchufada y perilla en cero antes de limpiar', 1], ['Guante anticorte en uso durante la limpieza', 1], ['Limpieza desde el centro hacia afuera de la hoja', 0]] }
  };
  var KIND = { op: 'OPERACIÓN', mant: 'MANTENCIÓN', limp: 'LIMPIEZA' };
  var eq = $('ins-eq'), list = $('ins-list'), kind = 'op', geo = '';
  eq.innerHTML = Object.keys(MAQ).map(function (k) { return '<option value="' + k + '">' + esc(MAQ[k].n + ' · ' + MAQ[k].area) + '</option>'; }).join('');
  function renderChecks() {
    var m = MAQ[eq.value];
    $('ins-serie-n').textContent = m.serie; $('ins-serie').checked = false;
    list.innerHTML = '<p class="ins-risk"><b>Riesgos críticos (matriz):</b> ' + esc(m.riesgos) + '</p>' +
      m[kind].map(function (it) {
        return '<div class="ins-row"><span>' + esc(it[0]) + (it[1] ? ' <em class="stop-b">STOP</em>' : '') + '</span>' +
          '<div class="cnc"><button type="button" data-v="C">C</button><button type="button" data-v="NC">NC</button><button type="button" data-v="NA">N/A</button></div>' +
          '<div class="nc-box" hidden><input placeholder="Hallazgo" class="nc-h"><input placeholder="Acción correctiva" class="nc-a"><input placeholder="Plazo (ej.: Inmediato, 7 días)" class="nc-p"></div></div>';
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
    navigator.geolocation.getCurrentPosition(function (p) { geo = p.coords.latitude.toFixed(5) + ', ' + p.coords.longitude.toFixed(5); t.textContent = '✓ ' + geo; },
      function () { t.textContent = 'Ubicación no autorizada (es opcional).'; }, { timeout: 8000 });
  });
  function inspRecord(key, k, nombre, marks, firma) {
    var m = MAQ[key], secs = {}, c = 0, nc = 0, na = 0, stop = [];
    ['op', 'mant', 'limp'].forEach(function (s) {
      if (s !== k) { secs[s] = null; na += m[s].length; return; }
      secs[s] = m[s].map(function (it, i) {
        var v = marks[i];
        if (v.v === 'Conforme') c++; else if (v.v === 'N/A') na++; else { nc++; if (it[1]) stop.push(it[0]); }
        return [i + 1, it[0], v.v, v.h || '', v.a || '', v.p || ''];
      });
    });
    return { fmt: 'f7', tipo: 'Inspección de máquina', code: m.code, titulo: 'REGISTRO DE INSPECCIÓN — ' + m.n, norma: 'PROSEMEH — DS44', folio: folio('INS'), nombre: nombre,
      maq: m.n, serie: m.serie, hab: m.hab, actividad: KIND[k], secs: secs, lens: { op: m.op.length, mant: m.mant.length, limp: m.limp.length },
      resumen: { total: m.op.length + m.mant.length + m.limp.length, c: c, nc: nc, na: na }, stop: stop, ok: !stop.length, firma: firma, geo: geo,
      detalle: m.n + ' · ' + KIND[k] + ' · ' + (stop.length ? 'NO AUTORIZADA' : 'Autorizada') + (nc ? ' · ' + nc + ' hallazgo(s)' : '') };
  }
  $('ins-send').addEventListener('click', function () {
    var res = $('ins-res'), rows = list.querySelectorAll('.ins-row'), marks = [];
    function err(t) { res.hidden = false; res.className = 'ins-res'; res.textContent = t; }
    if (!$('ins-serie').checked) return err('Confirma que el N° de serie coincide con la máquina.');
    for (var i = 0; i < rows.length; i++) {
      var v = rows[i].dataset.v;
      if (!v) return err('Marca los ' + rows.length + ' ítems (C, NC o N/A).');
      var mk = { v: v === 'C' ? 'Conforme' : v === 'NA' ? 'N/A' : 'No conf.' };
      if (v === 'NC') {
        mk.h = rows[i].querySelector('.nc-h').value.trim(); mk.a = rows[i].querySelector('.nc-a').value.trim(); mk.p = rows[i].querySelector('.nc-p').value.trim();
        if (!mk.h || !mk.a || !mk.p) return err('Completa hallazgo, acción correctiva y plazo en cada No conforme.');
      }
      marks.push(mk);
    }
    if (!sigs['sig-ins'].signed()) return err('Falta la firma del inspector u operador.');
    add(inspRecord(eq.value, kind, $('ins-nombre').value.trim() || 'Sin nombre', marks, sigs['sig-ins'].data())).then(function (r) {
      res.hidden = false; res.className = 'ins-res ' + (r.ok ? 'ok' : 'stop');
      res.innerHTML = r.ok ? '<b>✓ Autorizado a operar la máquina.</b> ' + (r.resumen.nc ? r.resumen.nc + ' hallazgo(s) con acción y plazo. ' : '') + 'Folio ' + esc(r.folio) + '.'
        : '<b>✋ STOP: no operar.</b> Etiqueta la máquina "Fuera de servicio", desenergízala y avisa a tu supervisor y a Prevención. Motivo: ' + esc(r.stop.join(', ')) + '.';
      sigs['sig-ins'].clear();
    });
  });

  // ---------- Hojas: mismo formato que el entregable real ----------
  function logo() { return '<div class="sh-logo">TU LOGO</div>'; }
  function sheetFC(r) {
    var d = day(r.fecha), kv = r.kv.map(function (x) { return '<tr><th>' + esc(x[0]) + '</th><td>' + esc(x[1] === 'hoy' ? d : x[1]) + '</td></tr>'; }).join('');
    var list = r.list ? '<h4>' + esc(r.list.t) + '</h4><ul class="sh-list">' + r.list.items.map(function (i) { return '<li>✓ ' + esc(i) + '</li>'; }).join('') + '</ul>' : '';
    var tbl = r.table ? '<h4>' + esc(r.table.t) + '</h4><table class="sh-t"><thead><tr>' + r.table.head.map(function (h) { return '<th>' + esc(h) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      r.table.rows.map(function (row) { return '<tr>' + row.map(function (c) { return '<td>' + esc(c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table>' : '';
    return '<article class="sheet fc"><header class="fc-h">' + logo() + '<div class="fc-t"><h3>' + esc(r.titulo) + '</h3><p>' + esc(CO) + ' · RUT ' + RUT + ' · ' + esc(r.norma) + '</p></div>' +
      '<div class="fc-r"><b>' + esc(r.code) + '</b><span>v1.1 · Folio: ' + esc(r.folio) + '</span><span>' + d + '</span></div></header>' +
      '<table class="sh-kv">' + kv + '</table>' + list + tbl + '<div class="sh-decl">' + r.decl + '</div>' +
      '<div class="sh-sign"><div><img src="' + r.firma + '" alt="Firma"><span>Firma Persona Trabajadora</span></div><div>' + (r.relator ? '<i class="sh-line"></i><span>' + RELATOR + '</span>' : '<i class="sh-line"></i>') + '</div></div>' +
      '<p class="sh-val">Firma validada · ' + esc(r.fecha) + ' · hash ' + esc(r.hash.slice(0, 16)) + '…</p>' +
      '<footer class="sh-f"><span>' + esc(r.norma) + '</span><span>' + esc(r.code) + ' · ' + d + '</span></footer>' + (r.ejemplo ? '<span class="sh-demo">Ejemplo</span>' : '') + '</article>';
  }
  function sheetF7(r) {
    var d = day(r.fecha);
    function sec(k) {
      var t = '<h4 class="f7-s">' + KIND[k] + ' — ' + esc(r.maq) + '</h4>';
      if (!r.secs[k]) return t + '<p class="f7-na">N/A — no se realizó esta actividad en este registro (' + r.lens[k] + ' ítems).</p>';
      return t + '<table class="f7-t"><thead><tr><th>#</th><th>Ítem</th><th>Estado</th><th>Hallazgo</th><th>Acción correctiva</th><th>Plazo</th></tr></thead><tbody>' +
        r.secs[k].map(function (x) { return '<tr><td>' + x[0] + '</td><td>' + esc(x[1]) + '</td><td class="st ' + (x[2] === 'Conforme' ? 'c' : x[2] === 'N/A' ? 'na' : 'nc') + '">' + esc(x[2]) + '</td><td>' + esc(x[3]) + '</td><td>' + esc(x[4]) + '</td><td>' + esc(x[5]) + '</td></tr>'; }).join('') + '</tbody></table>';
    }
    return '<article class="sheet f7"><header class="f7-h">' + logo() + '<div><h3>' + esc(r.titulo) + '</h3><p>' + esc(CO) + ' · RUT ' + RUT + ' | Código: ' + esc(r.code) + ' · ' + esc(r.norma) + '</p></div></header>' +
      '<div class="f7-box"><div><span>Máquina / equipo</span><b>' + esc(r.maq) + '</b></div><div><span>N° de serie / máquina</span><b>' + esc(r.serie) + '</b></div><div><span>Nombre y apellido</span><b>' + esc(r.nombre) + '</b></div><div><span>Fecha</span><b>' + d + '</b></div></div>' +
      '<p class="f7-meta"><b>Código:</b> ' + esc(r.code) + ' &nbsp; <b>Operador habitual:</b> ' + esc(r.hab) + ' &nbsp; <b>Actividad realizada:</b> ' + esc(r.actividad) + (r.geo ? ' &nbsp; <b>Ubicación:</b> ' + esc(r.geo) : '') + '</p>' +
      sec('op') + sec('mant') + sec('limp') +
      '<h4 class="f7-s">Resumen</h4><p class="f7-sum">Total ítems: ' + r.resumen.total + ' &nbsp; Conformes: ' + r.resumen.c + ' &nbsp; No conformes: ' + r.resumen.nc + ' &nbsp; N/A: ' + r.resumen.na + '</p>' +
      '<div class="sh-decl"><b>Declaración del trabajador:</b> Declaro que estoy utilizando la máquina o herramienta en conocimiento del procedimiento de trabajo seguro, con todos mis elementos de protección personal, que la máquina o herramienta cuenta con todas sus protecciones y dispositivos de seguridad, y que conozco los criterios de detención inmediata de este registro. <b>(Aceptada)</b></div>' +
      '<p class="f7-fl">Firma inspector/operador:</p><div class="f7-sig"><img src="' + r.firma + '" alt="Firma"></div>' +
      '<p class="f7-ok ' + (r.ok ? 'si' : 'no') + '">' + (r.ok ? '✓ AUTORIZADO A OPERAR LA MÁQUINA' : '✋ NO AUTORIZADO — MÁQUINA FUERA DE SERVICIO (criterio STOP: ' + esc(r.stop.join(', ')) + ')') + '</p>' +
      '<footer class="sh-f"><span>' + esc(r.code) + ' · ' + esc(r.norma) + ' · Encargado de Prevención · Generado ' + fmt(r.fecha) + '</span><span>Folio ' + esc(r.folio) + ' · hash ' + esc(r.hash.slice(0, 12)) + '…</span></footer>' + (r.ejemplo ? '<span class="sh-demo">Ejemplo</span>' : '') + '</article>';
  }
  function sheet(r) { return r.fmt === 'f7' ? sheetF7(r) : sheetFC(r); }
  function showSheets(recs, scroll) {
    $('sheets').innerHTML = recs.map(sheet).join('');
    if (scroll) $('carpeta').scrollIntoView({ behavior: 'smooth' });
  }

  // ---------- 5. Registros e indicadores ----------
  function renderReg() {
    var l = memory || [], box = $('reg-list');
    $('reg-n').textContent = l.length;
    var ins = l.filter(function (r) { return r.fmt === 'f7'; });
    var hall = ins.reduce(function (s, r) { return s + r.resumen.nc; }, 0);
    var k = [
      [l.filter(function (r) { return r.tipo === 'Documento de ingreso'; }).length, 'registros de ingreso'],
      [l.filter(function (r) { return r.tipo === 'Cápsula'; }).length, 'cápsulas aprobadas'],
      [l.filter(function (r) { return r.tipo === 'Entrega de EPP'; }).length, 'entregas de EPP'],
      [ins.length ? Math.round(100 * ins.filter(function (r) { return r.ok; }).length / ins.length) + '%' : '—', 'máquinas autorizadas'],
      [hall, 'hallazgos con acción y plazo']
    ];
    $('kpis').innerHTML = k.map(function (x) { return '<div><b>' + x[0] + '</b><span>' + x[1] + '</span></div>'; }).join('');
    box.innerHTML = l.length ? l.map(function (r, i) {
      return '<article class="reg ' + (r.ok ? 'ok' : 'stop') + '"><div><b>' + esc(r.code) + (r.ejemplo ? ' <em class="ej">Ejemplo</em>' : '') + '</b><span>' + esc(r.nombre) + ' · ' + esc(fmt(r.fecha)) + '</span><small>' + esc(r.detalle) + '</small><small class="reg-h">Folio ' + esc(r.folio) + ' · hash ' + esc(r.hash.slice(0, 12)) + '…</small><button type="button" class="reg-ver" data-i="' + i + '">Ver hoja ↓</button></div>' +
        (r.firma ? '<img src="' + r.firma + '" alt="Firma">' : '') + '</article>';
    }).join('') : '<p class="demo-sub">Aún no hay registros.</p>';
    showSheets(l.slice(0, 2), false);
  }
  $('reg-list').addEventListener('click', function (e) { var b = e.target.closest('.reg-ver'); if (b) showSheets([memory[+b.dataset.i]], true); });
  $('sheets-all').addEventListener('click', function () { showSheets(memory || [], true); });
  $('sheets-print').addEventListener('click', function () { window.print(); });
  $('reg-clear').addEventListener('click', function () { save([]); renderReg(); });

  // ---------- Ejemplos precargados: un par de hojas para ver el entregable de inmediato ----------
  if (memory === null) {
    memory = [];
    var firma = sampleSig(), ayer = new Date(Date.now() - 86400000).toISOString();
    var ej1 = ingresoSheets({ nombre: 'Camila Rojas (ficticia)', rut: '11.111.111-1', cargo: 'Ayudante de cocina' }, firma)[0];
    ej1.fecha = ayer; ej1.ejemplo = true; ej1.ok = true; ej1.detalle = ej1.titulo;
    var marks = MAQ.esmeril.op.map(function (it, i) { return i === 6 ? { v: 'No conf.', h: 'No usa guantes', a: 'Se le solicita usar guantes', p: 'Inmediato' } : { v: 'Conforme' }; });
    var ej2 = inspRecord('esmeril', 'op', 'Pedro Soto (ficticio)', marks, firma);
    ej2.fecha = ayer; ej2.ejemplo = true;
    Promise.all([stamp(ej2), stamp(ej1)]).then(function (r) { save(r); renderReg(); });
  } else {
    renderReg();
  }
})();
