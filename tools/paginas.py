#!/usr/bin/env python3
"""Genera las páginas de servicio (ds-44/, ley-karin/, ...) reutilizando el
encabezado, pie y estilos de index.html.

Uso:  python3 tools/paginas.py
Edita el contenido en PAGES y vuelve a ejecutar. No edites a mano los
index.html de las carpetas: se sobrescriben.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.safetycoach.cl"
WA = ("https://wa.me/56932304800?text=Hola%20Hans%2C%20llegu%C3%A9%20a%20SafetyCoach%20"
      "y%20quisiera%20conversar%20sobre%20las%20necesidades%20de%20prevenci%C3%B3n%20de%20mi%20empresa.")

PAGES = [
    {
        "slug": "ds-44",
        "title": "Diagnóstico e implementación DS 44 | SafetyCoach",
        "desc": "Asesoría para cumplir el DS 44 en Chile: diagnóstico de brechas, matriz de riesgos, programa preventivo, capacitación y preparación para fiscalización. Hans Meneses, SafetyCoach.",
        "eyebrow": "DS 44 · Gestión preventiva",
        "h1": "DS 44: cumple, demuéstralo y deja de depender de una carpeta",
        "lead": "El DS 44 cambió la forma en que las empresas en Chile deben gestionar la prevención. Te ayudo a saber qué te exige según tu tamaño y rubro, qué te falta y cómo implementarlo con tu equipo, con evidencia lista para cualquier fiscalización.",
        "img": "terreno-bodega.webp",
        "need": "Diagnóstico DS 44",
        "cta": "Solicitar diagnóstico DS 44",
        "blocks": [
            ("¿Qué es el DS 44?", "<p>Es el reglamento sobre gestión preventiva de los riesgos laborales, vigente desde febrero de 2025, que reemplazó a los antiguos DS 40 y DS 54. Pone el foco en que la empresa <b>gestione</b> sus riesgos de forma continua, no solo en tener documentos.</p>"),
            ("Lo que normalmente se revisa", "<ul class='checks'><li>Política de seguridad y salud en el trabajo</li><li>Matriz de identificación de peligros y evaluación de riesgos</li><li>Programa de trabajo preventivo con responsables y plazos</li><li>Información de riesgos y capacitación a los trabajadores</li><li>Plan de emergencias</li><li>Organización preventiva: comité paritario, encargado o departamento según tamaño</li><li>Investigación de accidentes y seguimiento de medidas</li></ul>"),
            ("Cómo lo trabajamos", "<ol class='steps'><li><b>Diagnóstico</b> de brechas con visita y revisión de evidencias.</li><li><b>Hoja de ruta</b> priorizada: qué hacer primero y qué puede esperar.</li><li><b>Implementación</b> con tus jefaturas y trabajadores, no solo documentos.</li><li><b>Registros digitales</b> de inducciones, capacitaciones e inspecciones.</li><li><b>Seguimiento</b> con indicadores y simulación de fiscalización.</li></ol>"),
        ],
        "faq": [
            ("¿El DS 44 aplica a mi empresa?", "Aplica a las empresas y entidades empleadoras en Chile. Lo que cambia según el número de trabajadores y el rubro es cómo se organiza la prevención (comité paritario, departamento de prevención, etc.). En el diagnóstico revisamos exactamente qué te corresponde."),
            ("¿Cuánto demora el diagnóstico?", "Normalmente entre 1 y 2 semanas, según el tamaño y la cantidad de centros de trabajo. Tiene un valor fijo que acordamos antes de empezar."),
            ("Ya tengo prevencionista, ¿me sirve?", "Sí. Apoyo a tu prevencionista para ordenar el sistema, priorizar y dejar evidencia digital, sin reemplazarlo."),
        ],
        "testi": ("Nuestra empresa creció y me dieron más responsabilidades. Hans me ayudó a implementar el DS 44 y los protocolos.", "Patricio Abarca · Experto en Prevención, Alex Stewart International"),
    },
    {
        "slug": "ley-karin",
        "title": "Ley Karin para empresas: protocolo, denuncias e investigación | SafetyCoach",
        "desc": "Implementación de la Ley Karin (Ley 21.643) en tu empresa: protocolo de prevención, canal de denuncias, investigación, medidas de resguardo y registros digitales.",
        "eyebrow": "Ley Karin · Ley 21.643",
        "h1": "Ley Karin: prevenir, responder bien y dejar todo respaldado",
        "lead": "Una denuncia mal gestionada puede convertirse en un problema legal y en un quiebre del clima laboral. Te acompaño a tener el protocolo, el procedimiento y los registros en orden, y a actuar con criterio cuando llega una denuncia.",
        "img": "taller-riesgos-2.webp",
        "need": "Ley Karin",
        "cta": "Necesito apoyo con Ley Karin",
        "blocks": [
            ("¿Qué exige la Ley Karin?", "<p>La Ley 21.643, vigente desde agosto de 2024, obliga a los empleadores a prevenir, investigar y sancionar el acoso laboral, el acoso sexual y la violencia en el trabajo. Entre otras cosas, pide un <b>protocolo de prevención</b>, un <b>procedimiento de investigación</b> y <b>medidas de resguardo</b> para las personas involucradas.</p>"),
            ("Lo que implementamos contigo", "<ul class='checks'><li>Protocolo de prevención basado en la evaluación de riesgos psicosociales</li><li>Actualización del reglamento interno</li><li>Canal y procedimiento de denuncia claros</li><li>Apoyo en la investigación y en las medidas de resguardo</li><li>Cápsulas de capacitación con videos y firma digital del trabajador</li><li>Seguimiento y registros listos ante la Dirección del Trabajo</li></ul>"),
            ("Si ya recibiste una denuncia", "<p>Lo primero es actuar dentro de los plazos y resguardar a las personas. Conversemos de inmediato: te oriento sobre los pasos y los registros que debes dejar.</p>"),
        ],
        "faq": [
            ("¿Toda empresa debe tener protocolo Ley Karin?", "Sí, la ley aplica a todos los empleadores. El alcance del protocolo y del procedimiento se ajusta al tamaño y la realidad de cada empresa."),
            ("¿Cómo demuestro que capacité a mis trabajadores?", "Con cápsulas digitales que registran quién las vio, su evaluación y su firma. Queda evidencia con fecha y hora."),
            ("¿Pueden investigar una denuncia por nosotros?", "Te acompaño en el proceso y en las medidas de resguardo. Revisamos en cada caso cuál es la mejor forma de llevar la investigación según lo que establece la ley."),
        ],
        "testi": ("Tenemos más de 20 casinos concesionados con exigencias distintas. Con Hans y sus sistemas digitales sabemos cómo estamos, en tiempo real, y cumplimos a nuestros clientes.", "Cecilia Gallardo · Encargada de Gestión de Personas, Food Chef"),
    },
    {
        "slug": "fiscalizaciones",
        "title": "Fiscalizaciones, accidentes graves y trámites SEREMI | SafetyCoach",
        "desc": "Apoyo ante fiscalizaciones de la Dirección del Trabajo y SEREMI de Salud, accidentes graves, programas de asistencia al cumplimiento (PAC), autorizaciones sanitarias y calificación industrial.",
        "eyebrow": "Fiscalizaciones y trámites",
        "h1": "Cuando llega la autoridad, no estás solo",
        "lead": "Un accidente grave, una visita de la Inspección del Trabajo o de la SEREMI de Salud, una multa o un permiso sanitario pendiente. Te acompaño a responder con orden, corregir lo que corresponde y dejar evidencia de que tu empresa gestiona.",
        "img": "fiscalizacion-dt.webp",
        "need": "Auditoría/fiscalización",
        "cta": "Tengo una fiscalización o un accidente grave",
        "blocks": [
            ("Inspección del Trabajo", "<ul class='checks'><li>Fiscalizaciones tras accidentes del trabajo graves</li><li>Antecedentes, medidas correctivas y seguimiento de lo observado</li><li>Programas de asistencia al cumplimiento (PAC) para corregir en vez de solo pagar la multa</li></ul>"),
            ("SEREMI de Salud", "<ul class='checks'><li>Fiscalizaciones y verificaciones</li><li>Nuevas autorizaciones sanitarias y actualizaciones</li><li>Calificación industrial y ambiental</li><li>Protocolos MINSAL: TMERT, MMC, PREXOR, riesgos psicosociales y otros</li></ul>"),
            ("Ante un accidente grave", "<p>Las primeras horas son clave: suspender la faena, notificar a la autoridad y resguardar la información. Contáctame de inmediato y te oriento en los pasos.</p>"),
        ],
        "faq": [
            ("¿Qué hago si me cursaron una multa?", "Revisamos lo observado, corregimos y ordenamos la evidencia. Según el caso, existen alternativas para corregir la infracción y reducir el impacto de la multa."),
            ("¿Me ayudan a abrir un local con autorización sanitaria?", "Sí. Te acompaño en los requisitos y trámites ante la SEREMI de Salud para nuevas autorizaciones o actualizaciones."),
            ("¿SafetyCoach trabaja para la autoridad?", "No. SafetyCoach es una asesoría independiente que acompaña a las empresas en sus gestiones ante estos organismos."),
        ],
        "testi": ("Junto a SafetyCoach logramos nuestro sueño: abrir nuestro restaurante en Pirque, Onde Skinners, con todos los permisos y autorizaciones sanitarias de la SEREMI.", "Alex Skinner · Restaurante Onde Skinners, Pirque"),
    },
    {
        "slug": "pymes",
        "title": "Prevencionista externo para pymes | SafetyCoach",
        "desc": "Prevención de riesgos para pymes que no tienen departamento de prevención: diagnóstico, reglamento interno, matriz de riesgos, protocolos, trámites y visitas mensuales.",
        "eyebrow": "Pymes · Prevención externa",
        "h1": "Tu prevencionista externo, sin contratar un departamento",
        "lead": "Sabes que tienes que cumplir, pero no tienes tiempo ni un experto en casa. Te digo qué es urgente según tu tamaño y rubro, y lo hacemos juntos, con un plan mensual a tu medida.",
        "img": "terreno-cocina.webp",
        "need": "Prevención externa",
        "cta": "Quiero conversar sobre mi pyme",
        "blocks": [
            ("Lo que incluye", "<ul class='checks'><li>Diagnóstico y plan priorizado</li><li>Reglamento interno, matriz de riesgos y programa preventivo</li><li>Protocolos MINSAL que te correspondan</li><li>Inducciones y capacitaciones con firma digital</li><li>Apoyo en trámites ante la SEREMI y la Dirección del Trabajo</li><li>Visitas y seguimiento mensual</li></ul>"),
            ("Por qué funciona para una pyme", "<p>Pagas solo lo que necesitas, sin sueldos fijos. Tienes a alguien con más de 20 años de experiencia que conoce tu operación y responde cuando lo necesitas.</p>"),
        ],
        "faq": [
            ("¿Cuánto cuesta?", "Depende del número de trabajadores, centros de trabajo y nivel de apoyo. Después de una primera conversación te propongo un plan con alcance y valor cerrados."),
            ("Tengo muy pocos trabajadores, ¿igual debo cumplir?", "Sí, hay obligaciones que aplican a todas las empresas. Lo que cambia es la forma y la cantidad de exigencias. Te digo exactamente cuáles te corresponden."),
        ],
        "testi": ("Junto a SafetyCoach logramos nuestro sueño: abrir nuestro restaurante en Pirque, Onde Skinners, con todos los permisos y autorizaciones sanitarias de la SEREMI.", "Alex Skinner · Restaurante Onde Skinners, Pirque"),
    },
    {
        "slug": "contratistas",
        "title": "Cumplimiento de contratistas y programa para mandantes | SafetyCoach",
        "desc": "Apoyo a empresas contratistas para cumplir los estándares de su mandante, y programa para mandantes: requisitos unificados, inducciones digitales y control de cumplimiento por contratista.",
        "eyebrow": "Contratistas y mandantes",
        "h1": "Contratistas que cumplen y mandantes que lo pueden ver",
        "lead": "Al contratista le exigen demostrar que trabaja seguro. Al mandante le cuesta controlar a decenas de contratistas. Trabajo con ambos lados para que el cumplimiento sea simple, digital y verificable.",
        "img": "trabajo-altura.webp",
        "need": "Auditoría/fiscalización",
        "cta": "Conversemos sobre contratistas",
        "blocks": [
            ("Si eres contratista", "<ul class='checks'><li>Revisión de los requisitos de tu mandante</li><li>Matrices, procedimientos y protocolos de tu faena</li><li>Documentación y acreditaciones al día</li><li>Inducciones y permisos de trabajo digitales</li><li>Preparación para las auditorías del mandante</li></ul>"),
            ("Si eres mandante: programa para contratistas", "<ul class='checks'><li>Un estándar común de seguridad para todos tus contratistas</li><li>Inducción digital con firma antes de entrar a tus instalaciones</li><li>Inspecciones y permisos por QR</li><li>Reporte de cumplimiento por contratista, en línea</li><li>Acompañamiento a los contratistas que más lo necesitan</li></ul>"),
        ],
        "faq": [
            ("¿El programa sirve si tengo contratistas pequeños?", "Sí. Está pensado para que hasta el contratista más pequeño pueda cumplir con herramientas simples desde el celular."),
            ("¿Quién paga el programa?", "Se puede estructurar de distintas formas: lo financia el mandante, cada contratista o un modelo mixto. Lo definimos juntos."),
        ],
        "testi": None,
    },
]


def page_shell(index_html, prefix="../"):
    """Extrae y adapta encabezado, pie, WhatsApp y SVG de marca de index.html."""
    def grab(start, end):
        i = index_html.index(start)
        j = index_html.index(end, i) + len(end)
        return index_html[i:j]
    parts = {
        "head_links": grab('<link rel="icon"', 'styles.css">'),
        "svg": grab('<svg width="0"', "</svg>"),
        "header": grab('<header class="site-header"', "</header>"),
        "footer": grab('<footer class="site-footer"', "</footer>"),
        "wa": grab('<a class="wa-float"', "</a>"),
    }
    for k, v in parts.items():
        v = re.sub(r'(href|src)="assets/', rf'\1="{prefix}assets/', v)
        v = re.sub(r'href="#(?!faro)', f'href="{prefix}index.html#', v)
        v = v.replace('href="index.html"', f'href="{prefix}index.html"')
        v = re.sub(r'href="(ds-44|ley-karin|fiscalizaciones|pymes|contratistas|autodiagnostico)/"', rf'href="{prefix}\1/"', v)
        parts[k] = v
    return parts


def render(p, shell):
    url = f"{SITE}/{p['slug']}/"
    contact = f"../index.html?necesidad={html.escape(p['need']).replace(' ', '%20')}#contacto"
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "description": p["desc"],
              "url": url, "areaServed": {"@type": "Country", "name": "Chile"},
              "provider": {"@type": "ProfessionalService", "name": "SafetyCoach", "url": SITE + "/"}}
    blocks = "\n".join(f'          <article class="svc-block"><h2>{t}</h2>{b}</article>' for t, b in p["blocks"])
    faq = "\n".join(f"        <details><summary>{q}</summary><p>{a}</p></details>" for q, a in p["faq"])
    testi = ""
    if p["testi"]:
        testi = f'<blockquote class="aud-quote">“{p["testi"][0]}”<cite>{p["testi"][1]}</cite></blockquote>'
    return f"""<!doctype html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['title']}</title>
  <meta name="description" content="{p['desc']}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0B1F3A">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta property="og:site_name" content="SafetyCoach">
  <meta property="og:title" content="{p['title']}">
  <meta property="og:description" content="{p['desc']}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og-safetycoach.jpg">
  <meta name="twitter:card" content="summary_large_image">
  {shell['head_links']}
  <script type="application/ld+json">{json.dumps(svc_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
  <a class="skip" href="#contenido">Saltar al contenido</a>
  {shell['svg']}
  {shell['header']}
  <main id="contenido">
    <section class="hero bg-photo svc-hero">
      <div class="bg-photo-img" aria-hidden="true"><img src="../assets/img/{p['img']}" alt="" fetchpriority="high"></div>
      <div class="wrap">
        <p class="crumbs"><a href="../index.html">Inicio</a> › {p['eyebrow']}</p>
        <p class="eyebrow">{p['eyebrow']}</p>
        <h1>{p['h1']}</h1>
        <p class="lead">{p['lead']}</p>
        <div class="cta-row">
          <a class="btn btn-primary btn-lg" href="{contact}" data-cta="svc_{p['slug']}">{p['cta']}</a>
          <a class="btn btn-ghost btn-lg" href="{WA}" target="_blank" rel="noopener" data-wa="svc_{p['slug']}">Hablar con Hans</a>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="wrap svc-layout">
        <div class="svc-blocks">
{blocks}
        </div>
        <aside class="svc-side">
          {testi}
          <div class="svc-diag">
            <h3>¿No sabes por dónde empezar?</h3>
            <p>Responde 10 preguntas y descubre en 3 minutos qué tan preparada está tu empresa.</p>
            <a class="btn btn-secondary" href="../autodiagnostico/" data-cta="svc_autodiag_{p['slug']}">Hacer autodiagnóstico</a>
          </div>
        </aside>
      </div>
    </section>
    <section class="section alt">
      <div class="wrap narrow">
        <h2 class="h-center">Preguntas frecuentes</h2>
{faq}
        <div class="cta-row center">
          <a class="btn btn-primary btn-lg" href="{contact}" data-cta="svc_final_{p['slug']}">{p['cta']}</a>
        </div>
        <p class="note center">La implementación se realiza considerando la normativa chilena vigente. Los requisitos específicos se verifican según tipo de empresa, actividad y número de trabajadores.</p>
      </div>
    </section>
  </main>
  {shell['footer']}
  {shell['wa']}
  <script src="../assets/js/main.js" defer></script>
</body>
</html>
"""


QUESTIONS = [
    "¿Tienes una política de seguridad firmada por la gerencia y conocida por los trabajadores?",
    "¿Tienes una matriz de riesgos actualizada en el último año?",
    "¿Tienes un programa de trabajo preventivo con responsables y plazos?",
    "¿Todos tus trabajadores recibieron inducción de riesgos con registro firmado?",
    "¿Tu reglamento interno está actualizado, incluida la Ley Karin?",
    "¿Tienes protocolo y procedimiento de Ley Karin implementados?",
    "¿Aplicaste los protocolos MINSAL que te corresponden (CEAL-SM, TMERT, MMC, PREXOR u otros)?",
    "¿Tienes plan de emergencias y realizaste simulacros este año?",
    "¿Investigas los accidentes e incidentes y haces seguimiento de las medidas?",
    "¿Podrías mostrar hoy todas tus evidencias si llega una fiscalización?",
]


def render_autodiag(shell):
    url = f"{SITE}/autodiagnostico/"
    qs = "\n".join(
        f"""          <fieldset class="q"><legend><span>{i+1}</span>{q}</legend>
            <label><input type="radio" name="q{i}" value="2" required> Sí</label>
            <label><input type="radio" name="q{i}" value="1"> En parte</label>
            <label><input type="radio" name="q{i}" value="0"> No</label>
          </fieldset>""" for i, q in enumerate(QUESTIONS))
    return f"""<!doctype html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Autodiagnóstico de prevención y DS 44 gratis | SafetyCoach</title>
  <meta name="description" content="Responde 10 preguntas y descubre en 3 minutos qué tan preparada está tu empresa para el DS 44, la Ley Karin y una fiscalización. Resultado inmediato y gratuito.">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0B1F3A">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta property="og:title" content="¿Qué tan preparada está tu empresa? Autodiagnóstico SafetyCoach">
  <meta property="og:description" content="10 preguntas, 3 minutos, resultado inmediato.">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og-safetycoach.jpg">
  {shell['head_links']}
</head>
<body>
  <a class="skip" href="#contenido">Saltar al contenido</a>
  {shell['svg']}
  {shell['header']}
  <main id="contenido">
    <section class="section diag">
      <div class="wrap narrow">
        <p class="crumbs"><a href="../index.html">Inicio</a> › Autodiagnóstico</p>
        <p class="eyebrow">Gratis · 3 minutos</p>
        <h1>¿Qué tan preparada está tu empresa?</h1>
        <p class="lead">Responde con honestidad. Al final verás tu nivel y las brechas que conviene atender primero frente al DS 44, la Ley Karin y una fiscalización.</p>
        <form id="diag-form" class="diag-form" novalidate>
{qs}
          <button class="btn btn-primary btn-lg" type="submit">Ver mi resultado</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>

        <div id="diag-result" class="diag-result" hidden>
          <p class="eyebrow">Tu resultado</p>
          <div class="diag-score"><strong id="r-score">0</strong><span>/ 20</span></div>
          <h2 id="r-level">Nivel</h2>
          <p id="r-text"></p>
          <h3>Lo que conviene atender primero</h3>
          <ul id="r-gaps" class="aud-pain"></ul>
          <div class="diag-next">
            <h3>Recibe tu resultado y una conversación de 30 minutos sin costo</h3>
            <form class="lead-form compact" name="autodiagnostico" method="POST" action="../gracias.html" data-netlify="true" netlify-honeypot="empresa_web" novalidate>
              <input type="hidden" name="form-name" value="autodiagnostico">
              <input type="hidden" name="puntaje" value="">
              <input type="hidden" name="nivel" value="">
              <input type="hidden" name="brechas" value="">
              <input type="hidden" name="origen" value="">
              <p class="hp"><label>No completar <input name="empresa_web" tabindex="-1" autocomplete="off"></label></p>
              <div class="fgrid">
                <label>Nombre<input name="nombre" required autocomplete="name"></label>
                <label>Empresa<input name="empresa" required autocomplete="organization"></label>
                <label>Cargo<input name="cargo" autocomplete="organization-title"></label>
                <label>N.º de trabajadores
                  <select name="trabajadores" required><option value="">Selecciona</option><option>1 a 10</option><option>11 a 25</option><option>26 a 49</option><option>50 a 99</option><option>100 a 499</option><option>500 o más</option></select>
                </label>
                <label>Correo<input type="email" name="correo" required autocomplete="email"></label>
                <label>Teléfono / WhatsApp<input type="tel" name="telefono" required autocomplete="tel" placeholder="+56 9 ..."></label>
                <label class="full consent"><input type="checkbox" name="consentimiento" value="Sí" required> Acepto que SafetyCoach use estos datos para contactarme.</label>
              </div>
              <button class="btn btn-primary btn-lg full" type="submit">Quiero conversar sobre mi resultado</button>
              <p class="form-msg" role="status" aria-live="polite"></p>
            </form>
          </div>
          <p class="note">Este autodiagnóstico es orientativo y no reemplaza una revisión de la normativa aplicable a tu empresa.</p>
        </div>
      </div>
    </section>
  </main>
  {shell['footer']}
  {shell['wa']}
  <script src="../assets/js/main.js" defer></script>
  <script>
  (function () {{
    var GAPS = {json.dumps(["Política de seguridad", "Matriz de riesgos actualizada", "Programa de trabajo preventivo", "Inducción de riesgos con registro firmado", "Reglamento interno actualizado", "Protocolo y procedimiento Ley Karin", "Protocolos MINSAL", "Plan de emergencias y simulacros", "Investigación de accidentes y seguimiento", "Evidencias listas para fiscalización"], ensure_ascii=False)};
    var LEVELS = [
      [8, 'Crítico', 'Tu empresa está muy expuesta ante un accidente o una fiscalización. Conviene actuar de inmediato con un diagnóstico y un plan priorizado.'],
      [14, 'En riesgo', 'Tienes avances, pero hay brechas importantes que podrían traducirse en multas o accidentes. Es el momento de ordenar y priorizar.'],
      [18, 'En camino', 'Vas bien. Ajustando algunas brechas y dejando todo en evidencia digital, estarás preparado para cualquier fiscalización.'],
      [20, 'Preparado', 'Excelente base. El siguiente paso es sostenerlo con indicadores y llevar la seguridad a la cultura de tu equipo.']
    ];
    var form = document.getElementById('diag-form');
    form.addEventListener('submit', function (e) {{
      e.preventDefault();
      var score = 0, gaps = [], missing = 0;
      for (var i = 0; i < GAPS.length; i++) {{
        var c = form.querySelector('input[name="q' + i + '"]:checked');
        if (!c) {{ missing++; continue; }}
        score += +c.value;
        if (c.value !== '2') gaps.push(GAPS[i] + (c.value === '1' ? ' (en parte)' : ''));
      }}
      if (missing) {{ form.querySelector('.form-msg').textContent = 'Responde las ' + missing + ' preguntas pendientes para ver tu resultado.'; return; }}
      var lv = LEVELS.filter(function (l) {{ return score <= l[0]; }})[0];
      document.getElementById('r-score').textContent = score;
      document.getElementById('r-level').textContent = 'Nivel: ' + lv[1];
      document.getElementById('r-text').textContent = lv[2];
      document.getElementById('r-gaps').innerHTML = gaps.length ? gaps.map(function (g) {{ return '<li>' + g + '</li>'; }}).join('') : '<li>No detectamos brechas en estas preguntas.</li>';
      var lf = document.querySelector('form[name="autodiagnostico"]');
      lf.puntaje.value = score; lf.nivel.value = lv[1]; lf.brechas.value = gaps.join('; ');
      var res = document.getElementById('diag-result');
      res.hidden = false; form.hidden = true;
      res.scrollIntoView({{ behavior: 'smooth' }});
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({{ event: 'autodiagnostico_resultado', puntaje: score, nivel: lv[1] }});
    }});
  }})();
  </script>
</body>
</html>
"""


def main():
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    shell = page_shell(index_html)
    for p in PAGES:
        out = ROOT / p["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(render(p, shell), encoding="utf-8")
        print("ok", out.relative_to(ROOT))
    out = ROOT / "autodiagnostico" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render_autodiag(shell), encoding="utf-8")
    print("ok", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
