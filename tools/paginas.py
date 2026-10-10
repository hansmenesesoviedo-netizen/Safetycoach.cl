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
        v = re.sub(r'href="(ds-44|ley-karin|fiscalizaciones|pymes|contratistas|autodiagnostico|liderazgo|demo)/"', rf'href="{prefix}\1/"', v)
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
            <p>12 preguntas simples para dueños y RR.HH. Descubre en 3 minutos qué tan preparada está tu empresa.</p>
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


RUBROS = ["Alimentación y casinos", "Industria / manufactura", "Construcción", "Comercio y retail",
          "Logística y transporte", "Agrícola", "Minería", "Servicios", "Salud", "Educación", "Otro"]


def gate_form(herramienta, titulo, texto, boton):
    """Registro previo: datos de contacto y de la empresa antes de entregar la herramienta."""
    rub = "".join(f"<option>{r}</option>" for r in RUBROS)
    return f"""        <div class="gate" id="gate">
          <h2>{titulo}</h2>
          <p>{texto}</p>
          <form class="lead-form gate-form" name="registro-herramienta" method="POST" action="../gracias.html" data-netlify="true" netlify-honeypot="empresa_web" data-gate="tool" novalidate>
            <input type="hidden" name="form-name" value="registro-herramienta">
            <input type="hidden" name="herramienta" value="{herramienta}">
            <input type="hidden" name="origen" value="">
            <p class="hp"><label>No completar <input name="empresa_web" tabindex="-1" autocomplete="off"></label></p>
            <div class="fgrid">
              <label>Nombre<input name="nombre" required autocomplete="name"></label>
              <label>Cargo<input name="cargo" required autocomplete="organization-title"></label>
              <label>Empresa<input name="empresa" required autocomplete="organization"></label>
              <label>Rubro<select name="rubro" required><option value="">Selecciona</option>{rub}</select></label>
              <label>Correo<input type="email" name="correo" required autocomplete="email"></label>
              <label>Teléfono / WhatsApp<input type="tel" name="telefono" required autocomplete="tel" placeholder="+56 9 ..."></label>
              <label>N.º de trabajadores<select name="trabajadores" required><option value="">Selecciona</option><option>1 a 10</option><option>11 a 25</option><option>26 a 49</option><option>50 a 99</option><option>100 a 499</option><option>500 o más</option></select></label>
              <label>Sucursales o centros de trabajo<select name="centros" required><option value="">Selecciona</option><option>1</option><option>2 a 5</option><option>6 a 20</option><option>Más de 20</option></select></label>
              <label>Accidentes del trabajo el último año<select name="accidentes" required><option value="">Selecciona</option><option>0</option><option>1 a 2</option><option>3 a 5</option><option>6 a 10</option><option>Más de 10</option><option>No lo sé</option></select></label>
              <label>¿Sabes cuánto pagas hoy por el seguro de accidentes (cotización adicional)?<select name="seguro_conoce" required><option value="">Selecciona</option><option>Sí</option><option>No lo sé</option></select></label>
              <label class="full">Si lo sabes: tasa de cotización adicional o monto mensual aproximado (opcional)<input name="seguro_monto" placeholder="Ej.: 0,68 % o $450.000 al mes"></label>
              <label class="full consent"><input type="checkbox" name="consentimiento" value="Sí" required> Acepto que SafetyCoach use estos datos para contactarme y preparar mi evaluación.</label>
            </div>
            <button class="btn btn-primary btn-lg full" type="submit">{boton}</button>
            <p class="form-msg" role="status" aria-live="polite"></p>
          </form>
          <p class="note">Tus datos son confidenciales y solo se usan para contactarte sobre tu evaluación.</p>
        </div>
"""


RESULT_FORM = """  <form name="resultado-herramienta" data-netlify="true" hidden>
    <input name="herramienta"><input name="correo"><input name="empresa"><input name="resultado"><textarea name="detalle"></textarea>
  </form>
"""

NEXT_STEP = """          <div class="diag-next">
            <h3>Siguiente paso: conversemos sobre tu resultado</h3>
            <p>Ya recibí tus datos y tu resultado. Antes de conversar te enviaré una breve entrevista para que la reunión vaya directo a lo importante.</p>
            <div class="cta-row">
              <a class="btn btn-primary" href="WAURL" target="_blank" rel="noopener" data-wa="resultado">Escribir a Hans por WhatsApp</a>
              <a class="btn btn-ghost" href="../index.html" data-cta="resultado_inicio">Volver al inicio</a>
            </div>
          </div>
""".replace("WAURL", "https://wa.me/56932304800?text=Hola%20Hans%2C%20complet%C3%A9%20una%20evaluaci%C3%B3n%20en%20SafetyCoach%20y%20quiero%20conversar%20sobre%20mi%20resultado.")


# Autodiagnóstico para dueños y RR.HH. Basado en lo esencial de la
# "Autoevaluación inicial de cumplimiento de aspectos legales" (Anexo 1,
# propuesta unificada de los organismos administradores de la Ley 16.744).
# (bloque, pregunta en lenguaje simple, brecha a mostrar si no se cumple)
QUESTIONS = [
    ("Tu organización", "¿Tienes Reglamento Interno de Orden, Higiene y Seguridad actualizado y cada trabajador firmó que lo recibió?", "Reglamento interno actualizado y entregado con firma"),
    ("Tu organización", "¿Tienes el protocolo de Ley Karin implementado y conocido por tu equipo?", "Protocolo Ley Karin"),
    ("Tu organización", "¿Tienes una política de seguridad, una matriz de riesgos y un programa de trabajo con responsables y plazos?", "Sistema de gestión DS 44: política, matriz de riesgos y programa de trabajo"),
    ("Tu organización", "Según tu tamaño, ¿funciona el Comité Paritario (más de 25 trabajadores) o eligieron un Delegado de Seguridad (10 a 25)?", "Comité Paritario o Delegado de Seguridad"),
    ("Tu organización", "¿Tú o la persona que designaste se capacitó en gestión de riesgos con tu mutualidad?", "Capacitación del representante legal en gestión de riesgos"),
    ("Tus personas", "Antes de empezar a trabajar, ¿cada persona recibe información de sus riesgos y de cómo trabajar seguro, con registro firmado?", "Información de riesgos al ingreso, con registro"),
    ("Tus personas", "¿Entregas los elementos de protección personal sin costo, con registro y enseñando a usarlos?", "Entrega y capacitación de elementos de protección personal"),
    ("Tu lugar de trabajo", "¿Baños, comedor, ventilación e iluminación están en buen estado y son suficientes para tu equipo?", "Condiciones sanitarias y ambientales básicas"),
    ("Tu lugar de trabajo", "¿Las máquinas y equipos tienen procedimiento de trabajo seguro y mantención al día?", "Procedimientos y mantención de máquinas y equipos"),
    ("Tu lugar de trabajo", "¿Tienes señalización, vías de evacuación, extintores mantenidos y un plan de emergencias que tu equipo conoce?", "Señalización, extintores y plan de emergencias"),
    ("Tu seguimiento", "¿Investigas cada accidente o incidente y llevas el registro de tu accidentabilidad?", "Investigación de accidentes y estadísticas"),
    ("Tu seguimiento", "Si mañana llega una fiscalización, ¿podrías mostrar todos estos registros en menos de una hora?", "Evidencias ordenadas y listas para fiscalización"),
]


def render_autodiag(shell):
    url = f"{SITE}/autodiagnostico/"
    rows, last = [], None
    for i, (blk, q, _) in enumerate(QUESTIONS):
        if blk != last:
            rows.append(f'          <h2 class="q-block">{blk}</h2>')
            last = blk
        rows.append(f"""          <fieldset class="q"><legend><span>{i+1}</span>{q}</legend>
            <label><input type="radio" name="q{i}" value="2" required> Sí</label>
            <label><input type="radio" name="q{i}" value="1"> En parte</label>
            <label><input type="radio" name="q{i}" value="0"> No</label>
            <label><input type="radio" name="q{i}" value="-1"> No sé</label>
          </fieldset>""")
    qs = "\n".join(rows)
    gaps_js = json.dumps([g for _, _, g in QUESTIONS], ensure_ascii=False)
    return f"""<!doctype html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Autodiagnóstico de prevención y DS 44 gratis | SafetyCoach</title>
  <meta name="description" content="12 preguntas simples para dueños y gerentes de personas: descubre en 3 minutos qué tan preparada está tu empresa para cumplir la ley y enfrentar una fiscalización.">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0B1F3A">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta property="og:title" content="¿Qué tan preparada está tu empresa? Autodiagnóstico SafetyCoach">
  <meta property="og:description" content="12 preguntas, 3 minutos, resultado inmediato.">
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
        <p class="lead">Para dueños, gerentes y encargados de personas. No necesitas saber de prevención: responde con honestidad y, si no sabes, marca «No sé». Al final verás tu nivel y lo que conviene atender primero.</p>
        <p class="note">Basado en lo esencial de la autoevaluación inicial de cumplimiento legal que usan los organismos administradores de la Ley 16.744.</p>
{gate_form("Autodiagnóstico legal", "Antes de empezar, cuéntame de tu empresa", "Así la evaluación queda acorde a tu realidad y puedo darte una lectura útil de tu resultado. Toma 1 minuto.", "Comenzar el autodiagnóstico")}
        <div id="tool" hidden>
        <form id="diag-form" class="diag-form" novalidate>
{qs}
          <button class="btn btn-primary btn-lg" type="submit">Ver mi resultado</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>

        <div id="diag-result" class="diag-result" hidden>
          <p class="eyebrow">Tu resultado</p>
          <div class="diag-score"><strong id="r-score">0</strong><span>% de cumplimiento</span></div>
          <h2 id="r-level">Nivel</h2>
          <p id="r-text"></p>
          <h3>Lo que conviene atender primero</h3>
          <ul id="r-gaps" class="aud-pain"></ul>
{NEXT_STEP}          <p class="note">Este autodiagnóstico es orientativo y no reemplaza una revisión de la normativa aplicable a tu empresa.</p>
        </div>
        </div>
      </div>
    </section>
  </main>
  {shell['footer']}
  {shell['wa']}
{RESULT_FORM}  <script src="../assets/js/main.js" defer></script>
  <script>
  (function () {{
    var GAPS = {gaps_js};
    var LEVELS = [
      [40, 'Crítico', 'Tu empresa está muy expuesta ante un accidente o una fiscalización. Conviene actuar de inmediato con un diagnóstico y un plan priorizado.'],
      [70, 'En riesgo', 'Tienes avances, pero hay brechas importantes que podrían traducirse en multas o accidentes. Es el momento de ordenar y priorizar.'],
      [90, 'En camino', 'Vas bien. Ajustando algunas brechas y dejando todo en evidencia digital, estarás preparado para cualquier fiscalización.'],
      [100, 'Preparado', 'Excelente base. El siguiente paso es sostenerlo con indicadores y llevar la seguridad a la cultura de tu equipo.']
    ];
    var form = document.getElementById('diag-form');
    form.addEventListener('submit', function (e) {{
      e.preventDefault();
      var score = 0, gaps = [], missing = 0;
      for (var i = 0; i < GAPS.length; i++) {{
        var c = form.querySelector('input[name="q' + i + '"]:checked');
        if (!c) {{ missing++; continue; }}
        score += Math.max(0, +c.value);
        if (c.value !== '2') gaps.push(GAPS[i] + (c.value === '1' ? ' (en parte)' : c.value === '-1' ? ' (no sabes si se cumple)' : ''));
      }}
      if (missing) {{ form.querySelector('.form-msg').textContent = 'Responde las ' + missing + ' preguntas pendientes para ver tu resultado.'; return; }}
      score = Math.round(score * 100 / (GAPS.length * 2));
      var lv = LEVELS.filter(function (l) {{ return score <= l[0]; }})[0];
      document.getElementById('r-score').textContent = score;
      document.getElementById('r-level').textContent = 'Nivel: ' + lv[1];
      document.getElementById('r-text').textContent = lv[2];
      document.getElementById('r-gaps').innerHTML = gaps.length ? gaps.map(function (g) {{ return '<li>' + g + '</li>'; }}).join('') : '<li>No detectamos brechas en estas preguntas.</li>';
      window.scSendResult && window.scSendResult('Autodiagnóstico legal', score + '% · ' + lv[1], gaps.join('; '));
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


# Autoevaluación de liderazgo en seguridad: 5 factores de éxito, escala 1 a 7.
FACTORS = [
    ("compromiso", "Fuerte compromiso del liderazgo", "#5B5BF0",
     ["La gerencia participa personalmente en seguridad (rondas, reuniones o inspecciones) al menos una vez al mes.",
      "La seguridad tiene recursos y tiempo, incluso cuando hay presión por producir."],
     "Agenda un liderazgo visible mínimo una vez al mes: una ronda en terreno y una conversación con el equipo."),
    ("tolerancia", "Tolerancia cero", "#3BA54A",
     ["No se acepta trabajar sin las medidas de control, aunque eso atrase la producción.",
      "Ante una falta grave se aplica siempre la misma regla, sin importar el cargo."],
     "Define 3 a 5 reglas de oro claras, con consecuencias conocidas, y aplícalas igual para todos."),
    ("comportamiento", "Cambio en comportamiento", "#F2B33D",
     ["Las jefaturas observan cómo se trabaja y conversan con las personas sobre cómo hacerlo seguro.",
      "Se reconoce a quienes reportan incidentes o proponen mejoras."],
     "Instala observaciones conductuales y reconoce públicamente los buenos reportes."),
    ("comunicacion", "Comunicación clara y retroalimentación", "#7E9AAE",
     ["Todos conocen las metas de seguridad y saben cómo vamos.",
      "Cuando alguien reporta un problema, recibe respuesta."],
     "Comparte un indicador simple cada mes y responde cada reporte, aunque sea para decir «lo estamos viendo»."),
    ("plan", "Desafiante plan de acción y fuerte seguimiento", "#2F8DE0",
     ["Existe un plan anual con metas, responsables y plazos para cada cargo.",
      "Cada mes se revisan los avances y se cierran las observaciones a tiempo."],
     "Arma un plan por cargo (gerencia, jefaturas, supervisores) y revísalo mes a mes con plazos de cierre."),
]


def render_liderazgo(shell):
    url = f"{SITE}/liderazgo/"
    items, n = [], 0
    for key, name, color, stmts, _ in FACTORS:
        items.append(f'          <h2 class="q-block" style="border-color:{color}">{name}</h2>')
        for st in stmts:
            opts = "".join(f'<label><input type="radio" name="l{n}" value="{v}"{" required" if v == 1 else ""}><span>{v}</span></label>' for v in range(1, 8))
            items.append(f'          <fieldset class="q q7" data-f="{key}"><legend><span>{n+1}</span>{st}</legend><div class="scale7">{opts}</div><div class="scale7-k"><small>Nunca</small><small>Siempre</small></div></fieldset>')
            n += 1
    qs = "\n".join(items)
    fjs = json.dumps([{"k": k, "n": nm, "c": c, "tip": tip} for k, nm, c, _, tip in FACTORS], ensure_ascii=False)
    return f"""<!doctype html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Autoevaluación de liderazgo en seguridad | SafetyCoach</title>
  <meta name="description" content="¿Tienes real tolerancia cero a los accidentes? Evalúa en 3 minutos el liderazgo en seguridad de tu organización en 5 factores de éxito, con escala de 1 a 7.">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0B1F3A">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_CL">
  <meta property="og:title" content="¿Tienes real tolerancia cero a los accidentes? Autoevaluación de liderazgo">
  <meta property="og:description" content="5 factores de éxito, escala de 1 a 7, resultado inmediato.">
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
        <p class="crumbs"><a href="../index.html">Inicio</a> › Liderazgo en seguridad</p>
        <p class="eyebrow">Para gerencias y jefaturas · 3 minutos</p>
        <h1>¿Tienes real tolerancia cero a los accidentes?</h1>
        <p class="lead">Los accidentes no bajan con más documentos: bajan cuando el liderazgo se involucra. Evalúa a tu organización en los 5 factores de éxito que uso en mis programas, de 1 (nunca) a 7 (siempre).</p>
{gate_form("Autoevaluación de liderazgo", "Antes de empezar, cuéntame de tu empresa", "Así puedo leer tu resultado en contexto: tu rubro, tu tamaño y tu accidentabilidad. Toma 1 minuto.", "Comenzar la autoevaluación")}
        <div id="tool" hidden>
        <form id="lid-form" class="diag-form" novalidate>
{qs}
          <button class="btn btn-primary btn-lg" type="submit">Ver mi resultado</button>
          <p class="form-msg" role="status" aria-live="polite"></p>
        </form>

        <div id="lid-result" class="diag-result" hidden>
          <p class="eyebrow">Tu resultado</p>
          <div class="lid-wheel">
            <div class="lid-core"><b>Factores de éxito</b><strong id="l-avg">0</strong></div>
            <div id="l-factors"></div>
          </div>
          <h2 id="l-level"></h2>
          <p id="l-text"></p>
          <h3>Tu factor más débil y por dónde partir</h3>
          <p id="l-tip" class="lid-tip"></p>
{NEXT_STEP}        </div>
        </div>
      </div>
    </section>
  </main>
  {shell['footer']}
  {shell['wa']}
{RESULT_FORM}  <script src="../assets/js/main.js" defer></script>
  <script>
  (function () {{
    var F = {fjs};
    var form = document.getElementById('lid-form');
    form.addEventListener('submit', function (e) {{
      e.preventDefault();
      var sets = form.querySelectorAll('fieldset.q7'), sums = {{}}, cnt = {{}}, missing = 0;
      sets.forEach(function (fs, i) {{
        var c = fs.querySelector('input:checked');
        if (!c) {{ missing++; return; }}
        var k = fs.dataset.f; sums[k] = (sums[k] || 0) + +c.value; cnt[k] = (cnt[k] || 0) + 1;
      }});
      if (missing) {{ form.querySelector('.form-msg').textContent = 'Responde las ' + missing + ' afirmaciones pendientes.'; return; }}
      var avgs = F.map(function (f) {{ return {{ f: f, v: Math.round(sums[f.k] / cnt[f.k] * 10) / 10 }}; }});
      var total = Math.round(avgs.reduce(function (a, b) {{ return a + b.v; }}, 0) / avgs.length * 10) / 10;
      var fmt = function (v) {{ return v.toFixed(1).replace('.', ','); }};
      document.getElementById('l-avg').textContent = fmt(total);
      document.getElementById('l-factors').innerHTML = avgs.map(function (a, i) {{
        return '<div class="lid-f lid-f' + i + '" style="background:' + a.f.c + '"><span>' + a.f.n + '</span><strong>' + fmt(a.v) + '</strong></div>';
      }}).join('');
      var lv = total >= 6 ? ['Liderazgo fuerte', 'Tu liderazgo sostiene la seguridad. El desafío es mantenerlo y llevarlo a cada supervisor y trabajador.']
             : total >= 5 ? ['Liderazgo en desarrollo', 'Hay compromiso, pero todavía depende de pocas personas. Con un plan por cargo y seguimiento mensual puedes dar el salto.']
             : ['Liderazgo débil', 'Hoy la seguridad está delegada o se activa solo cuando pasa algo. Es la principal causa de que los accidentes no bajen.'];
      var weak = avgs.slice().sort(function (a, b) {{ return a.v - b.v; }})[0];
      document.getElementById('l-level').textContent = lv[0] + ' (' + fmt(total) + ' de 7)';
      document.getElementById('l-text').textContent = lv[1];
      document.getElementById('l-tip').innerHTML = '<b>' + weak.f.n + ' (' + fmt(weak.v) + '):</b> ' + weak.f.tip;
      window.scSendResult && window.scSendResult('Autoevaluación de liderazgo', fmt(total) + ' de 7 · ' + lv[0], avgs.map(function (a) {{ return a.f.n + ' ' + fmt(a.v); }}).join('; '));
      var res = document.getElementById('lid-result'); res.hidden = false; form.hidden = true;
      res.scrollIntoView({{ behavior: 'smooth' }});
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({{ event: 'liderazgo_resultado', promedio: total }});
    }});
  }})();
  </script>
</body>
</html>
"""


def render_demo(shell):
    return """<!doctype html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Demo SafetyCoach Digital: IRL, cápsulas e inspecciones | SafetyCoach</title>
  <meta name="description" content="Prueba la demo de SafetyCoach Digital con una empresa ficticia: inducción IRL con firma digital, cápsula de capacitación con evaluación e inspección pre-uso de equipos.">
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#0B1F3A">
  """ + shell['head_links'] + """
</head>
<body class="demo-body">
  <a class="skip" href="#contenido">Saltar al contenido</a>
  """ + shell['svg'] + shell['header'] + """
  <main id="contenido">
    <section class="section demo">
      <div class="wrap">
        <p class="crumbs"><a href="../index.html">Inicio</a> › Demo SafetyCoach Digital</p>
        <div class="demo-head">
          <div>
            <p class="eyebrow">Demo · Empresa ficticia</p>
            <h1>Alimentos Demo SpA</h1>
            <p class="lead">Planta de alimentos con 60 trabajadores. Así se ve, desde el celular del trabajador, lo que en tu empresa hoy está en papel.</p>
          </div>
          <p class="demo-warn">Esta es una demostración. Los datos que ingreses se guardan solo en este navegador y no se envían a nadie.</p>
        </div>

""" + gate_form("Demo digital", "Para ver la demo, cuéntame de tu empresa", "Así te muestro lo que más sirve a tu operación. Toma 1 minuto.", "Ver la demo") + """
        <div id="tool" hidden>
        <div class="demo-tabs" role="tablist">
          <button role="tab" aria-selected="true" data-t="irl">1 · Inducción IRL</button>
          <button role="tab" aria-selected="false" data-t="cap">2 · Cápsula</button>
          <button role="tab" aria-selected="false" data-t="ins">3 · Inspección pre-uso</button>
          <button role="tab" aria-selected="false" data-t="reg">4 · Registros <span id="reg-n">0</span></button>
        </div>

        <div class="phone">
          <!-- IRL -->
          <div class="demo-pane" id="t-irl">
            <h2>Información de riesgos laborales (IRL)</h2>
            <p class="demo-sub">Antes de empezar a trabajar, revisa tus riesgos y firma.</p>
            <label>Nombre (ficticio)<input id="irl-nombre" value="Camila Rojas"></label>
            <label>Cargo<select id="irl-cargo"><option>Operaria de envasado</option><option>Bodeguero</option><option>Ayudante de cocina industrial</option></select></label>
            <div class="mods" id="irl-mods">
              <details><summary>Caídas al mismo nivel</summary><p>Pisos húmedos en zona de lavado. Usa calzado antideslizante y avisa de derrames de inmediato.</p></details>
              <details><summary>Cortes</summary><p>Cuchillos y rebanadoras. Usa guante anticorte y nunca retires la guarda de la máquina.</p></details>
              <details><summary>Manejo manual de carga</summary><p>Máximo 25 kg por persona. Dobla las rodillas, carga pegada al cuerpo y pide ayuda o usa transpaleta.</p></details>
              <details><summary>Atrapamiento en máquinas</summary><p>No intervengas una máquina en movimiento. Bloquea la energía antes de limpiar o mantener.</p></details>
              <details><summary>Quemaduras</summary><p>Hornos y vapor. Usa guantes térmicos y no abras equipos a presión.</p></details>
              <details><summary>Emergencias y evacuación</summary><p>Conoce tu vía de evacuación y el punto de encuentro. Ante una alarma, sal sin correr.</p></details>
            </div>
            <p class="demo-prog"><span id="irl-read">0</span> de 6 módulos revisados</p>
            <p class="decl">Declaro haber recibido y comprendido la información de los riesgos de mi trabajo, sus medidas preventivas y los métodos de trabajo correctos.</p>
            <div class="sig"><canvas id="sig-irl" width="600" height="160"></canvas><button type="button" class="sig-clear" data-c="sig-irl">Borrar</button><span>Firma aquí con el dedo</span></div>
            <button class="btn btn-primary full" id="irl-send">Firmar y enviar</button>
            <p class="demo-msg" id="irl-msg"></p>
          </div>

          <!-- Cápsula -->
          <div class="demo-pane" id="t-cap" hidden>
            <h2>Cápsula: manejo manual de carga</h2>
            <p class="demo-sub">3 láminas, 2 preguntas y tu firma. 2 minutos.</p>
            <div class="slides">
              <div class="slide on"><b>1/3 · ¿Por qué importa?</b><p>Las lesiones de espalda son una de las causas más comunes de licencias en bodegas y plantas de alimentos.</p></div>
              <div class="slide"><b>2/3 · La regla</b><p>Hasta 25 kg por persona. Sobre eso, usa ayuda mecánica (transpaleta) o carga entre dos.</p></div>
              <div class="slide"><b>3/3 · La técnica</b><p>Pies separados, rodillas dobladas, espalda recta y la carga pegada al cuerpo. No gires el tronco con peso.</p></div>
            </div>
            <div class="slide-nav"><button type="button" class="btn btn-ghost btn-sm" id="sl-prev">‹ Anterior</button><button type="button" class="btn btn-ghost btn-sm" id="sl-next">Siguiente ›</button></div>
            <div class="quiz" id="quiz" hidden>
              <fieldset><legend>¿Cuál es el peso máximo por persona?</legend>
                <label><input type="radio" name="qa" value="0"> 50 kg</label><label><input type="radio" name="qa" value="1"> 25 kg</label><label><input type="radio" name="qa" value="0"> No hay límite</label></fieldset>
              <fieldset><legend>Al levantar una caja debes…</legend>
                <label><input type="radio" name="qb" value="0"> Doblar la espalda</label><label><input type="radio" name="qb" value="1"> Doblar las rodillas y mantener la carga pegada</label></fieldset>
              <label>Nombre (ficticio)<input id="cap-nombre" value="Camila Rojas"></label>
              <div class="sig"><canvas id="sig-cap" width="600" height="160"></canvas><button type="button" class="sig-clear" data-c="sig-cap">Borrar</button><span>Firma aquí con el dedo</span></div>
              <button class="btn btn-primary full" id="cap-send">Enviar evaluación y firma</button>
              <p class="demo-msg" id="cap-msg"></p>
            </div>
          </div>

          <!-- Inspección -->
          <div class="demo-pane" id="t-ins" hidden>
            <h2>Inspección pre-uso</h2>
            <p class="demo-sub">En terreno, el trabajador llega aquí escaneando el código QR pegado en el equipo.</p>
            <label>Equipo<select id="ins-eq">
              <option value="transpaleta">Transpaleta eléctrica TP-02</option>
              <option value="rebanadora">Rebanadora industrial RB-01</option>
              <option value="horno">Horno a gas HG-03</option></select></label>
            <label>Operador (ficticio)<input id="ins-nombre" value="Pedro Soto"></label>
            <div id="ins-list" class="ins-list"></div>
            <button type="button" class="btn btn-ghost btn-sm" id="ins-geo">📍 Agregar ubicación (opcional)</button> <small id="ins-geo-t"></small>
            <button class="btn btn-primary full" id="ins-send">Registrar inspección</button>
            <div class="ins-res" id="ins-res" hidden></div>
          </div>

          <!-- Registros -->
          <div class="demo-pane" id="t-reg" hidden>
            <h2>Registros</h2>
            <p class="demo-sub">Lo que vería la gerencia o el prevencionista: cada registro con responsable, fecha, hora y firma.</p>
            <div id="reg-list" class="reg-list"></div>
            <button type="button" class="btn btn-ghost btn-sm" id="reg-clear">Borrar datos de la demo</button>
          </div>
        </div>

        </div>
        <div class="demo-cta">
          <div><h4>¿Lo quieres para tu empresa?</h4><p>Lo hacemos a la medida de tu operación: tus riesgos, tus equipos, tus cargos y tu logo.</p></div>
          <a class="btn btn-primary" href="../index.html?necesidad=Demo%20digital#contacto" data-cta="demo_contacto">Quiero mi versión</a>
        </div>
      </div>
    </section>
  </main>
  """ + shell['footer'] + shell['wa'] + RESULT_FORM + """
  <script src="../assets/js/main.js" defer></script>
  <script src="../assets/js/demo.js" defer></script>
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
    out = ROOT / "demo" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render_demo(shell), encoding="utf-8")
    print("ok", out.relative_to(ROOT))
    out = ROOT / "liderazgo" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render_liderazgo(shell), encoding="utf-8")
    print("ok", out.relative_to(ROOT))
    out = ROOT / "autodiagnostico" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render_autodiag(shell), encoding="utf-8")
    print("ok", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
