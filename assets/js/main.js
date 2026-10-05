/* SafetyCoach — interacción mínima, sin dependencias. */
(function () {
  'use strict';

  // ---------- Medición de conversiones (GTM / GA4 leen window.dataLayer) ----------
  window.dataLayer = window.dataLayer || [];
  function track(event, data) {
    window.dataLayer.push(Object.assign({ event: event }, data || {}));
  }

  // Origen del lead: UTM + página de entrada, se guarda en campos ocultos "origen".
  var params = new URLSearchParams(location.search);
  var origen = ['utm_source', 'utm_medium', 'utm_campaign']
    .map(function (k) { return params.get(k) ? k + '=' + params.get(k) : null; })
    .filter(Boolean).join('&') || (document.referrer ? 'ref=' + document.referrer : 'directo');
  document.querySelectorAll('input[name="origen"]').forEach(function (i) { i.value = origen; });

  // ---------- Año del footer ----------
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // ---------- Menú móvil ----------
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      menu.classList.toggle('open', !open);
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        toggle.setAttribute('aria-expanded', 'false');
        menu.classList.remove('open');
      }
    });
  }

  // ---------- CTA que preseleccionan la necesidad en el formulario ----------
  var needSelect = document.getElementById('necesidad');
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-need], [data-cta], [data-wa]');
    if (!el) return;
    if (el.dataset.need && needSelect) needSelect.value = el.dataset.need;
    if (el.dataset.cta) track('cta_click', { cta: el.dataset.cta });
    if (el.dataset.wa) track('whatsapp_click', { ubicacion: el.dataset.wa });
  });

  // ---------- Escala de cultura preventiva ----------
  var levels = [
    ['Nadie se ocupa realmente de la seguridad; se conoce poco la accidentabilidad y la normativa.',
     'Diagnóstico inicial: saber qué te exige la ley y qué te está costando no gestionarlo.'],
    ['Se actúa después del accidente o de la fiscalización.',
     'Diagnóstico y prioridades claras: qué hacer primero para dejar de apagar incendios.'],
    ['Se cumplen procedimientos y normas, pero la prevención depende del prevencionista.',
     'Implementación DS 44 con involucramiento de jefaturas: que el sistema no dependa de una sola persona.'],
    ['Se anticipan los riesgos y los líderes participan activamente.',
     'Coaching de liderazgo, metas e indicadores para sostener y medir el avance.'],
    ['La seguridad es un valor compartido: cada persona se cuida y cuida a otros.',
     'Consolidar la cultura: coaching ejecutivo, reconocimiento y bienestar organizacional.']
  ];
  var tabs = document.querySelectorAll('.mat-tabs button');
  var desc = document.querySelector('.mat-desc');
  var next = document.querySelector('.mat-next span');
  tabs.forEach(function (b) {
    b.addEventListener('click', function () {
      tabs.forEach(function (t) { t.setAttribute('aria-selected', 'false'); });
      b.setAttribute('aria-selected', 'true');
      var l = levels[+b.dataset.level];
      desc.textContent = l[0];
      next.textContent = l[1];
      track('cultura_nivel', { nivel: b.textContent });
    });
  });

  // ---------- Recursos (lead magnets) ----------
  var modal = document.getElementById('res-modal');
  if (modal && modal.showModal) {
    document.querySelectorAll('[data-resource]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        modal.querySelector('input[name="recurso"]').value = btn.dataset.resource;
        modal.querySelector('#res-title').textContent = btn.dataset.resource;
        modal.showModal();
      });
    });
    modal.addEventListener('click', function (e) {
      if (e.target === modal || e.target.closest('[data-close]')) modal.close();
    });
  } else {
    // Navegadores sin <dialog>: llevar al formulario principal.
    document.querySelectorAll('[data-resource]').forEach(function (btn) {
      btn.addEventListener('click', function () { location.hash = 'contacto'; });
    });
  }

  // ---------- Formularios: validación + envío ----------
  // Por defecto el formulario se envía de forma nativa (Netlify Forms lo captura).
  // Para usar otro servicio (Formspree, CRM, Make/Zapier), define data-endpoint="https://..." en el <form>:
  // se enviará por fetch como JSON y luego redirige a /gracias.html.
  document.querySelectorAll('.lead-form').forEach(function (form) {
    var msg = form.querySelector('.form-msg');
    form.addEventListener('submit', function (e) {
      var firstInvalid = null;
      form.querySelectorAll('[required]').forEach(function (f) {
        var ok = f.type === 'checkbox' ? f.checked : f.checkValidity() && f.value.trim() !== '';
        f.classList.toggle('invalid', !ok);
        f.setAttribute('aria-invalid', String(!ok));
        if (!ok && !firstInvalid) firstInvalid = f;
      });
      if (firstInvalid) {
        e.preventDefault();
        msg.textContent = 'Revisa los campos marcados para poder enviar tu solicitud.';
        firstInvalid.focus();
        return;
      }
      msg.textContent = '';
      var eventName = form.name === 'recursos' ? 'lead_magnet_submit' : 'form_submit';
      var data = Object.fromEntries(new FormData(form).entries());
      track(eventName, { necesidad: data.necesidad || data.recurso || '', trabajadores: data.trabajadores || '' });

      var endpoint = form.dataset.endpoint;
      if (!endpoint) return; // envío nativo
      e.preventDefault();
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        location.href = form.getAttribute('action') || '/gracias.html';
      }).catch(function () {
        msg.textContent = 'No pudimos enviar el formulario. Escríbeme directo a hans@safetycoach.cl o por WhatsApp.';
      });
    });
  });
})();
