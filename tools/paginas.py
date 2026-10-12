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
        "close": '¿Vas a seguir cumpliendo en papel o vas a gestionar de verdad?',
        "questions": ['¿Tu matriz de riesgos la conoce el supervisor que está en terreno, o solo quien la hizo?', '¿Tu programa preventivo tiene responsables con nombre y plazos que se cumplen?', 'Si mañana un fiscalizador le pregunta a un trabajador por sus riesgos, ¿qué respondería?'],
        "punch": 'Un sistema que solo existe en papel no evita ningún accidente.',
        "title": "Diagnóstico e implementación DS 44 | SafetyCoach",
        "desc": "Asesoría para cumplir el DS 44 en Chile: diagnóstico de brechas, matriz de riesgos, programa preventivo, capacitación y preparación para fiscalización. Hans Meneses, SafetyCoach.",
        "eyebrow": "DS 44 · Gestión preventiva",
        "h1": "Tienes la carpeta del DS 44. ¿Y tu gente sabe lo que dice?",
        "lead": "El DS 44 no se cumple con documentos: se cumple gestionando. Te digo qué te exige según tu tamaño y rubro, qué te falta, y lo implementamos con tus líderes y tu equipo, con evidencia lista para cualquier fiscalización.",
        "img": "terreno-bodega.webp",
        "need": "Diagnóstico DS 44",
        "cta": "Quiero saber dónde estoy · desde $99.000",
        "blocks": [
            ("¿Qué es el DS 44?", "<p>Es el reglamento sobre gestión preventiva de los riesgos laborales, vigente desde febrero de 2025, que reemplazó a los antiguos DS 40 y DS 54. Pone el foco en que la empresa <b>gestione</b> sus riesgos de forma continua, no solo en tener documentos.</p>"),
            ("Lo que normalmente se revisa", "<ul class='checks'><li>Política de seguridad y salud en el trabajo</li><li>Matriz de identificación de peligros y evaluación de riesgos</li><li>Programa de trabajo preventivo con responsables y plazos</li><li>Información de riesgos y capacitación a los trabajadores</li><li>Plan de emergencias</li><li>Organización preventiva: comité paritario, encargado o departamento según tamaño</li><li>Investigación de accidentes y seguimiento de medidas</li></ul>"),
            ("Cómo lo hacemos funcionar", "<ol class='steps'><li><b>Diagnóstico</b> de brechas con visita y revisión de evidencias.</li><li><b>Hoja de ruta</b> priorizada: qué hacer primero y qué puede esperar.</li><li><b>Implementación</b> con tus jefaturas y trabajadores. Los documentos son el resultado, no el objetivo.</li><li><b>Registros digitales</b> de inducciones, capacitaciones e inspecciones.</li><li><b>Seguimiento</b> con indicadores y simulación de fiscalización.</li></ol>"),
        ],
        "faq": [
            ("¿El DS 44 aplica a mi empresa?", "Aplica a las empresas y entidades empleadoras en Chile. Lo que cambia según el número de trabajadores y el rubro es cómo se organiza la prevención (comité paritario, departamento de prevención, etc.). En el diagnóstico revisamos exactamente qué te corresponde."),
            ("¿Cuánto demora el diagnóstico?", "Normalmente entre 1 y 2 semanas, según el tamaño y la cantidad de centros de trabajo. El diagnóstico en una sola vista parte desde $99.000 + IVA, con garantía: si no te muestra al menos 3 brechas que no marcaste en tu encuesta inicial, no lo pagas."),
            ("Ya tengo prevencionista, ¿me sirve?", "Sí. Un prevencionista solo no puede estar en todas partes. Lo apoyo para ordenar el sistema, priorizar y dejar evidencia digital, sin reemplazarlo."),
        ],
        "testi": None,
    },
    {
        "slug": "ley-karin",
        "close": '¿Vas a esperar la primera denuncia para ordenar tu casa?',
        "questions": ['¿Tus trabajadores saben cómo y dónde denunciar, sin miedo?', 'Si hoy llega una denuncia, ¿sabes qué hacer en las primeras 24 horas?', '¿Puedes demostrar, con firma y fecha, que capacitaste a todo tu equipo?'],
        "punch": 'Decir que son una familia no basta. La familia se cuida, y lo demuestra.',
        "title": "Ley Karin para empresas: protocolo, denuncias e investigación | SafetyCoach",
        "desc": "Implementación de la Ley Karin (Ley 21.643) en tu empresa: protocolo de prevención, canal de denuncias, investigación, medidas de resguardo y registros digitales.",
        "eyebrow": "Ley Karin · Ley 21.643",
        "h1": "Ley Karin: la denuncia va a llegar. ¿Tu empresa está preparada?",
        "lead": "Una denuncia mal gestionada se transforma en un problema legal y en un quiebre del clima que cuesta años reparar. Te acompaño a tener el protocolo, el procedimiento y los registros en orden, y a actuar con criterio cuando llega el momento.",
        "img": "taller-riesgos-2.webp",
        "need": "Ley Karin",
        "cta": "Quiero mi Ley Karin en orden",
        "blocks": [
            ("¿Qué exige la Ley Karin?", "<p>La Ley 21.643, vigente desde agosto de 2024, obliga a los empleadores a prevenir, investigar y sancionar el acoso laboral, el acoso sexual y la violencia en el trabajo. Entre otras cosas, pide un <b>protocolo de prevención</b>, un <b>procedimiento de investigación</b> y <b>medidas de resguardo</b> para las personas involucradas.</p>"),
            ("Lo que implementamos contigo", "<ul class='checks'><li>Protocolo de prevención basado en la evaluación de riesgos psicosociales</li><li>Actualización del reglamento interno</li><li>Canal y procedimiento de denuncia claros</li><li>Apoyo en la investigación y en las medidas de resguardo</li><li>Cápsulas de capacitación con videos y firma digital del trabajador</li><li>Seguimiento y registros listos ante la Dirección del Trabajo</li></ul>"),
            ("¿Ya recibiste una denuncia?", "<p>No improvises. Lo primero es actuar dentro de los plazos y resguardar a las personas. Escríbeme hoy: te oriento sobre los pasos y los registros que debes dejar.</p>"),
        ],
        "faq": [
            ("¿Toda empresa debe tener protocolo Ley Karin?", "Sí, la ley aplica a todos los empleadores. El alcance del protocolo y del procedimiento se ajusta al tamaño y la realidad de cada empresa."),
            ("¿Cómo demuestro que capacité a mis trabajadores?", "Con cápsulas digitales que registran quién las vio, su evaluación y su firma. Queda evidencia con fecha y hora."),
            ("¿Pueden investigar una denuncia por nosotros?", "Te acompaño en el proceso y en las medidas de resguardo. Revisamos en cada caso cuál es la mejor forma de llevar la investigación según lo que establece la ley."),
        ],
        "testi": None,
    },
    {
        "slug": "fiscalizaciones",
        "close": '¿Prefieres prepararte ahora o explicar después por qué no lo hiciste?',
        "questions": ['Si hoy entra un fiscalizador, ¿cuánto te demoras en evidenciar tus registros de prevención? Conmigo: tu carpeta digital, y listo.', '¿Las observaciones de la última fiscalización están corregidas, o solo pagaste la multa?', 'Si ocurre un accidente grave, ¿tu equipo sabe qué hacer en la primera hora?'],
        "punch": 'He estado del otro lado de la mesa. Sé lo que miran y cómo prepararte.',
        "title": "Fiscalizaciones, accidentes graves y trámites SEREMI | SafetyCoach",
        "desc": "Apoyo ante fiscalizaciones de la Dirección del Trabajo y SEREMI de Salud, accidentes graves, programas de asistencia al cumplimiento (PAC), autorizaciones sanitarias y calificación industrial.",
        "eyebrow": "Fiscalizaciones y trámites",
        "h1": "La fiscalización no avisa. ¿Tu empresa está lista hoy?",
        "lead": "Un accidente grave, una visita de la Inspección del Trabajo o de la SEREMI de Salud, una multa o un permiso sanitario pendiente. Cuando llega la autoridad no estás solo: te acompaño a responder con orden, corregir lo que corresponde y demostrar que tu empresa gestiona.",
        "img": "fiscalizacion-dt.webp",
        "need": "Auditoría/fiscalización",
        "cta": "Tengo una fiscalización o un accidente grave",
        "blocks": [
            ("Inspección del Trabajo", "<ul class='checks'><li>Fiscalizaciones tras accidentes del trabajo graves</li><li>Antecedentes, medidas correctivas y seguimiento de lo observado</li><li>Programas de asistencia al cumplimiento (PAC) para corregir en vez de solo pagar la multa</li></ul>"),
            ("SEREMI de Salud", "<ul class='checks'><li>Fiscalizaciones y verificaciones</li><li>Nuevas autorizaciones sanitarias y actualizaciones</li><li>Calificación industrial y ambiental</li><li>Implementación de protocolos MINSAL (TMERT, MMC, PREXOR, riesgos psicosociales y otros), desde $299.000 + IVA por protocolo, según guía y cronograma real, sin estresar a tu organización</li></ul>"),
            ("Ante un accidente grave", "<p>Las primeras horas son clave: suspender la faena, notificar a la autoridad y resguardar la información. Contáctame de inmediato y te oriento en los pasos.</p>"),
        ],
        "faq": [
            ("¿Qué hago si me cursaron una multa?", "No la pagues sin antes revisar tus opciones. Según el tamaño de tu empresa, puedes acogerte a un Programa de Asistencia al Cumplimiento (PAC) y reemplazar la multa, hasta evitarla al 100%. Revisamos lo observado, corregimos y ordenamos la evidencia."),
            ("¿Me ayudan a abrir un local con autorización sanitaria?", "Sí. Te acompaño en los requisitos y trámites ante la SEREMI de Salud para nuevas autorizaciones o actualizaciones."),
            ("¿SafetyCoach trabaja para la autoridad?", "No. SafetyCoach es una asesoría independiente que acompaña a las empresas en sus gestiones ante estos organismos."),
        ],
        "testi": None,
    },
    {
        "slug": "pymes",
        "close": '¿Hasta cuándo vas a improvisar con lo más importante que tienes: tu gente?',
        "questions": ['¿Tienes reglamento interno, matriz de riesgos y programa preventivo al día?', '¿Cuántas horas al mes le dedicas tú a la seguridad? ¿Y cuántas deberías?', 'Si mañana se accidenta alguien de tu equipo, ¿cuánto le cuesta a tu negocio?'],
        "punch": 'Ser pyme no te hace menos responsable. Te hace más vulnerable.',
        "title": "Prevencionista externo para pymes | SafetyCoach",
        "desc": "Prevención de riesgos para pymes que no tienen departamento de prevención: diagnóstico, reglamento interno, matriz de riesgos, protocolos, trámites y visitas mensuales.",
        "eyebrow": "Pymes · Prevención externa",
        "h1": "¿Sabes lo que te exige la ley? ¿Seguro?",
        "lead": "Deja de botar plata en multas y parches: mejor inviértela y protégete. No tienes tiempo ni un experto en casa. No es excusa: tu coach y prevencionista externo, sin contratar un departamento. Te digo qué es urgente según tu tamaño y rubro, y lo hacemos juntos, cada semana.",
        "img": "terreno-cocina.webp",
        "need": "Plan Pyme anual",
        "cta": "Quiero uno de los 5 cupos",
        "blocks": [
            ("Promoción: Plan Pyme Anual", "<div class='pp-mini'><p class='pp-price'><span class='pp-desde'>desde</span><span class='pp-cur'>$</span>549.000<small>+ IVA / mes</small></p><p>Pymes de hasta 50 trabajadores en Santiago · contrato anual con pago mensual. Incluye <b>visita semanal en terreno de hasta 3 horas</b> (AM o PM según disponibilidad), <b>asesoría virtual entre visitas</b>, <b>implementación de protocolos MINSAL</b> y <b>coaching mensual a la gerencia</b>.</p><p class='pp-per'><b>Solo 5 cupos.</b> Cuando se llenan, se cierra la promoción.</p></div>"),
            ("Lo que incluye", "<ul class='checks'><li>Diagnóstico y plan priorizado</li><li>Reglamento interno, matriz de riesgos y programa preventivo</li><li>Implementación de los protocolos MINSAL que te correspondan, con cronograma real</li><li>Inducciones y capacitaciones con firma digital</li><li>Apoyo en trámites ante la SEREMI y la Dirección del Trabajo</li><li>Visitas y seguimiento mensual</li></ul>"),
            ("Por qué funciona para una pyme", "<p>Pagas solo lo que necesitas, sin sueldos fijos. Tienes a alguien con más de 20 años de experiencia, que conoció más de 300 pymes por dentro desde una mutualidad, conoce tu operación y responde cuando lo necesitas.</p>"),
        ],
        "faq": [
            ("¿Cuánto cuesta?", "Para pymes de hasta 50 trabajadores, el Plan Pyme Anual parte desde $549.000 + IVA al mes, con visita semanal en Santiago y asesoría virtual (solo 5 cupos). Si tienes más trabajadores o centros, lo ajustamos en el diagnóstico."),
            ("Tengo muy pocos trabajadores, ¿igual debo cumplir?", "Sí, hay obligaciones que aplican a todas las empresas. Lo que cambia es la forma y la cantidad de exigencias. Te digo exactamente cuáles te corresponden."),
        ],
        "testi": None,
    },
    {
        "slug": "sistemas-de-gestion",
        "close": '¿Vas a seguir mirando cómo otros ganan los contratos que podrían ser tuyos?',
        "questions": ['¿Cuántas licitaciones has perdido por tu tasa de accidentes o por no tener un sistema de gestión, sin saberlo?', '¿Tu prevención funcionaría igual si tu prevencionista se va mañana?', '¿Sabes que para optar a la rebaja de tu tasa tu sistema de gestión debe llevar un año completo funcionando antes de la evaluación?'],
        "punch": 'La certificación no es el trofeo. Es la prueba de que tu sistema funciona.',
        "title": "Implementación de sistemas de gestión y certificación PEC / GPS | SafetyCoach",
        "desc": "Implementa tu sistema de gestión de seguridad y salud en el trabajo y certifícate en el programa de tu organismo administrador (Mutual de Seguridad, ACHS, IST, ISL). Desde el nivel básico.",
        "eyebrow": "Sistemas de gestión · Certificaciones",
        "h1": "Tus clientes ya piden un sistema de gestión. ¿Tú lo tienes?",
        "lead": "Un sistema de gestión ordena tu prevención, te abre la puerta a clientes y licitaciones exigentes y es la base para certificarte con tu organismo administrador. Partimos por el nivel básico y no nos detenemos ahí.",
        "img": "taller-riesgos-3.webp",
        "need": "Sistema de gestión",
        "cta": "Quiero certificar mi empresa",
        "blocks": [
            ("Certificaciones que puedes lograr", "<div class='seals'><img src='../assets/img/sello-pec-mutual.webp' alt='Sello PEC Empresa Estándar, Mutual de Seguridad' width='200' height='265' loading='lazy'><img src='../assets/img/sello-gps-achs.webp' alt='Certificado de nivel de desarrollo preventivo GPS, ACHS' width='564' height='222' loading='lazy'></div><p>Cada organismo administrador tiene su propio programa y niveles. Por ejemplo, el <b>PEC</b> de Mutual de Seguridad (con niveles como <b>Empresa Estándar</b>) o el <b>GPS</b> de ACHS, que certifica tu nivel de desarrollo preventivo. IST e ISL también tienen sus programas. <b>Partimos por el nivel básico</b> y avanzamos.</p><p class='note'>Las certificaciones las otorga tu organismo administrador. SafetyCoach te acompaña a cumplir sus requisitos; las imágenes son referenciales.</p>"),
            ("Cómo lo implementamos", "<ol class='steps'><li><b>Diagnóstico</b> frente a los requisitos del programa de tu mutualidad.</li><li><b>Plan de implementación</b> con responsables y plazos realistas.</li><li><b>Documentos y registros</b>, en formato digital y trazable.</li><li><b>Auditoría interna</b> para llegar preparados.</li><li><b>Postulación</b> y acompañamiento en la auditoría del organismo.</li><li><b>Mantención</b> y paso al siguiente nivel.</li></ol>"),
            ("Por qué te conviene", "<ul class='checks'><li>Muchos clientes y licitaciones exigen un sistema de gestión de seguridad</li><li>Ordena el cumplimiento del DS 44 en un solo sistema</li><li>Mejores indicadores y menos accidentes</li><li><b>Es requisito para optar a la rebaja de tu tasa:</b> en la evaluación de los años impares debes estar al día en tus cotizaciones y tener un sistema de gestión funcionando durante todo el año previo, con política firmada, diagnóstico de riesgos y programa de trabajo. Empieza ya: haremos todo lo posible para que tu empresa sea candidata a la rebaja.</li><li>Es la base para instalar una cultura preventiva</li></ul>"),
        ],
        "faq": [
            ("¿Qué nivel me conviene?", "Parte por el nivel básico del programa de tu organismo administrador. Es alcanzable, ordena lo esencial y te deja listo para el siguiente nivel."),
            ("¿SafetyCoach entrega la certificación?", "No. La certificación la otorga tu organismo administrador (Mutual de Seguridad, ACHS, IST o ISL) después de su auditoría. Yo te acompaño a cumplir los requisitos y a llegar preparado."),
            ("¿Cuánto demora?", "Depende de tu tamaño y de tu punto de partida. En el diagnóstico estimamos el plazo con un plan concreto."),
            ("¿Qué tiene que ver el sistema de gestión con mi tasa de cotización?", "Para optar a la rebaja en la evaluación de los años impares debes estar al día en tus cotizaciones y tener un sistema de gestión de seguridad y salud en el trabajo funcionando durante todo el año previo a la evaluación. Debe incluir al menos una política firmada por el representante legal, un diagnóstico de riesgos y requisitos legales, y un programa de trabajo con responsables y plazos, y se acredita ante tu organismo administrador. Empieza ya: haremos todo lo posible para que tu empresa sea candidata a la rebaja."),
        ],
        "testi": None,
    },
    {
        "slug": "contratistas",
        "close": '¿Vas a seguir perdiendo contratos por algo que se puede resolver?',
        "questions": ['¿Sabes cuál es tu tasa de accidentes y cómo la ve tu mandante cuando evalúa proveedores?', '¿Tu documentación y tus acreditaciones están al día hoy, no la próxima semana?', '¿Tus trabajadores nuevos entran a faena con su inducción firmada?'],
        "punch": 'Deja de rezar antes de cada auditoría.',
        "title": "Cumplimiento de contratistas y programa para mandantes | SafetyCoach",
        "desc": "Apoyo a empresas contratistas para cumplir los estándares de su mandante, y programa para mandantes: requisitos unificados, inducciones digitales y control de cumplimiento por contratista.",
        "eyebrow": "Contratistas y mandantes",
        "h1": "Tu mandante no te pregunta si cumples. Te pide que lo demuestres.",
        "lead": "No seas huevón: ¿no tienes sistema? Pa' fuera. ¿Demandas o enfermedades profesionales? Pa' fuera. La empresa principal responde contigo de forma solidaria o subsidiaria y tiene tolerancia cero: tus números importan, pero su reputación importa más. Y en cada licitación aparece el Chacal de la Trompeta. Al contratista le exigen demostrar que trabaja seguro. Al mandante le cuesta controlar a decenas de contratistas. Trabajo con ambos lados para que el cumplimiento sea simple, digital y verificable, y deje de ser un dolor de cabeza antes de cada auditoría.",
        "img": "trabajo-altura.webp",
        "need": "Programa contratistas",
        "cta": "Toma tu programa · desde $549.000/mes",
        "blocks": [
            ("Por si no lo sabías", "<div class='lic-inline'><p><b>Tú miras tus costos. Tu mandante no mira solo tu precio.</b> Para elegirte también revisa si estás limpio: sin accidentes, sin denuncias, sin multas. Las políticas de compra y licitación evalúan tu accidentabilidad, y hay competidores que hacen lo mismo que tú, o peor, pero llegan sin accidentes a cuestas. Y se quedan con el contrato.</p><p><i>Te lo digo porque estuve ahí, del otro lado de la mesa.</i></p></div>"),
            ("Si eres contratista: programa desde $549.000 + IVA al mes", "<ul class='checks'><li>Revisión de los requisitos de tu mandante</li><li>Matrices, procedimientos y protocolos de tu faena</li><li>Documentación y acreditaciones al día</li><li>Inducciones y permisos de trabajo digitales</li><li>Preparación para las auditorías del mandante</li></ul>"),
            ("Si eres mandante: programa para contratistas", "<ul class='checks'><li>Un estándar común de seguridad para todos tus contratistas</li><li>Inducción digital con firma antes de entrar a tus instalaciones</li><li>Inspecciones y permisos por QR</li><li>Reporte de cumplimiento por contratista, en línea</li><li>Acompañamiento a los contratistas que más lo necesitan</li></ul>"),
        ],
        "faq": [
            ("¿El programa sirve si tengo contratistas pequeños?", "Sí. Está pensado para que hasta el contratista más pequeño pueda cumplir con herramientas simples desde el celular."),
            ("¿Quién paga el programa?", "Si eres contratista, tu programa parte desde $549.000 + IVA al mes. Si eres mandante, se puede estructurar de distintas formas: lo financia el mandante, cada contratista o un modelo mixto. Lo definimos juntos."),
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
        v = re.sub(r'href="(ds-44|ley-karin|fiscalizaciones|pymes|contratistas|sistemas-de-gestion|autodiagnostico|liderazgo|demo|mi-historia)/"', rf'href="{prefix}\1/"', v)
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
    qs = "".join(f"<li>{q}</li>" for q in p["questions"])
    espejo = f'          <article class="svc-block svc-espejo"><h2>Antes de seguir, responde con honestidad</h2><ol>{qs}</ol><p>Si dudaste en alguna, no tienes un problema de suerte. Tienes una oportunidad de hacerlo mejor.</p></article>\n'
    blocks = espejo + "\n".join(f'          <article class="svc-block"><h2>{t}</h2>{b}</article>' for t, b in p["blocks"])
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
        <p class="hero-punch">{p['punch']}</p>
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
            <h3>¿Te atreves a mirarte al espejo?</h3>
            <p>12 preguntas simples para dueños y RR.HH. En 3 minutos sabrás qué tan preparada está tu empresa. Gratis.</p>
            <a class="btn btn-secondary" href="../autodiagnostico/" data-cta="svc_autodiag_{p['slug']}">Hacer autodiagnóstico</a>
          </div>
        </aside>
      </div>
    </section>
    <section class="section alt">
      <div class="wrap narrow">
        <h2 class="h-center">Lo que te estás preguntando</h2>
{faq}
        <p class="svc-close">{p['close']}</p>
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
              <div class="gate-extra full" hidden>
                <p class="gate-extra-t">Opcional: con estos datos ajusto aún más tu evaluación</p>
                <div class="fgrid">
                  <label>N.º de trabajadores<select name="trabajadores"><option value="">Selecciona</option><option>1 a 10</option><option>11 a 25</option><option>26 a 49</option><option>50 a 99</option><option>100 a 499</option><option>500 o más</option></select></label>
                  <label>Sucursales o centros de trabajo<select name="centros"><option value="">Selecciona</option><option>1</option><option>2 a 5</option><option>6 a 20</option><option>Más de 20</option></select></label>
                  <label>Accidentes del trabajo el último año<select name="accidentes"><option value="">Selecciona</option><option>0</option><option>1 a 2</option><option>3 a 5</option><option>6 a 10</option><option>Más de 10</option><option>No lo sé</option></select></label>
                  <label>¿Sabes tu tasa de cotización actual o cuánto pagas a tu mutualidad por el seguro de accidentes?<select name="seguro_conoce"><option value="">Selecciona</option><option>Sí</option><option>No lo sé</option></select></label>
                  <label class="full seguro-monto" hidden>Tasa de cotización adicional o monto mensual aproximado<input name="seguro_monto" placeholder="Ej.: 0,68 % o $450.000 al mes"></label>
                  <p class="full gate-help">Te lo pregunto solo para saber si estás pagando más de lo que deberías y ayudarte a reducir ese monto. ¿Sabías que en los años impares se evalúa tu tasa? Para optar a la rebaja debes estar al día en tus cotizaciones y haber mantenido un sistema de gestión durante todo el año anterior a la evaluación.</p>
                </div>
              </div>
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


VITRINA = r"""        <section class="vitrina" id="vitrina" aria-labelledby="vit-t">
          <div class="vit-copy">
            <p class="eyebrow">Pruébalo ahora · dentro del celular</p>
            <h2 id="vit-t">Cápsulas digitales con <span>firma digital</span> y diploma</h2>
            <p>Así lo vive tu trabajador: elige la cápsula, mira el video, responde, completa sus datos, firma con el dedo y recibe su <b>diploma con código QR</b> de verificación. Todo queda registrado para tu empresa.</p>
            <ol class="vit-steps"><li>Elige una opción en la carátula</li><li>Presiona el video</li><li>Responde 3 preguntas</li><li>Completa tus datos y firma</li><li>Descarga tu diploma con QR</li></ol>
            <p class="vit-note">Ejemplo activo: cápsula Ley Karin. Empresa y datos ficticios; tu versión lleva tu logo, tus riesgos y tus videos.</p>
          </div>
          <div class="frame-wrap">
          <div class="scenes" role="group" aria-label="Escenario"><span>Escenario:</span><button type="button" data-scene="cocina" aria-pressed="true">Cocina</button><button type="button" data-scene="bodega" aria-pressed="false">Bodega</button><button type="button" data-scene="fabrica" aria-pressed="false">Fábrica</button></div>
          <div class="frame" id="frame" data-scene="cocina">
            <img class="frame-img" id="frame-img" src="../assets/img/frame-cocina.webp" alt="Mano sosteniendo un celular en una cocina industrial" width="590" height="870" fetchpriority="high">
            <div class="frame-screen"><div class="app" id="app">

              <!-- Carátula: multi opciones -->
              <div class="scr on" data-scr="home">
                <div class="app-top"><span class="logo-ph">TU LOGO</span><div><b>Tu empresa</b><small>Programa de prevención digital</small></div><img class="sc-corner dark" src="../assets/img/logo-safetycoach.png" alt="SafetyCoach" width="643" height="285"></div>
                <p class="app-k">● DS 44 · Programa digital</p>
                <h3 class="app-h">¿Qué quieres <em>probar?</em></h3>
                <div class="opt-grid">
                  <button type="button" class="opt live" data-go="cover"><span class="opt-i">🎬</span><b>Cápsula con video</b><small>Ley Karin · diploma con QR</small><em>Prueba ahora</em></button>
                  <button type="button" class="opt" data-soon="irl"><span class="opt-i">✍️</span><b>Registro IRL</b><small>Ingreso con firma digital</small></button>
                  <button type="button" class="opt" data-soon="epp"><span class="opt-i">🦺</span><b>Entrega de EPP</b><small>Talla, norma y firma</small></button>
                  <button type="button" class="opt" data-soon="ins"><span class="opt-i">🔧</span><b>Inspección MEHM</b><small>Operación · STOP</small></button>
                </div>
                <p class="app-toast" id="app-toast" hidden></p>
              </div>

              <!-- Portada de la cápsula -->
              <div class="scr" data-scr="cover">
                <div class="app-bar"><button type="button" class="app-back" data-go="home">‹</button><span>CÁPSULA LK-01 · 1/4</span><span class="app-pct">0%</span></div>
                <div class="cover-hero">
                  <p class="app-k">● Ley 21.643 · Ley Karin</p>
                  <span class="pro">★ CÁPSULA PRO</span>
                  <h3 class="app-h big">Comunícate<br>con <em>respeto</em></h3>
                  <i class="rule"></i>
                  <p class="app-p">Qué es el acoso laboral, cómo prevenirlo y dónde denunciar. Video, preguntas y diploma.</p>
                  <div class="stats"><div><b>1</b><span>Video</span></div><div><b>3</b><span>Preguntas</span></div><div><b>5'</b><span>Duración</span></div><div><b>60%</b><span>Mínimo aprobación</span></div></div>
                  <button type="button" class="app-cta" data-go="video">Comenzar módulo →</button>
                </div>
              </div>

              <!-- Video -->
              <div class="scr" data-scr="video">
                <div class="app-bar"><button type="button" class="app-back" data-go="cover">‹</button><span>S2 · VIDEO</span><span class="app-pct">25%</span></div>
                <h4 class="app-sec">Módulo — Ley Karin</h4>
                <div class="vid" id="vid" data-id="w9JTHkaXcSE">
                  <button type="button" class="vid-play" id="vid-play" aria-label="Reproducir video"><img src="https://i.ytimg.com/vi/w9JTHkaXcSE/hqdefault.jpg" alt="" loading="lazy"><span>▶</span></button>
                </div>
                <p class="vid-cap">Ley 21.643 (Ley Karin) — Comunícate con respeto · <a href="https://youtu.be/w9JTHkaXcSE" target="_blank" rel="noopener">Ver en YouTube ↗</a></p>
                <p class="app-p small" id="vid-msg">Presiona el video para comenzar.</p>
                <button type="button" class="app-cta" id="vid-next" disabled>Continuar →</button>
              </div>

              <!-- Preguntas -->
              <div class="scr" data-scr="quiz">
                <div class="app-bar"><button type="button" class="app-back" data-go="video">‹</button><span>S3 · EVALUACIÓN</span><span class="app-pct">50%</span></div>
                <h4 class="app-sec">Responde (mínimo 60%)</h4>
                <div class="aq" data-q="1"><p>1. Burlas reiteradas a un compañero, ¿pueden ser acoso laboral?</p><button type="button" data-v="1">Sí</button><button type="button" data-v="0">No, es solo humor</button></div>
                <div class="aq" data-q="2"><p>2. Si presencias una situación de acoso, debes…</p><button type="button" data-v="0">No meterte</button><button type="button" data-v="1">Informarlo por el canal de denuncia</button></div>
                <div class="aq" data-q="3"><p>3. ¿La Ley Karin aplica también a la violencia de clientes o terceros?</p><button type="button" data-v="1">Sí</button><button type="button" data-v="0">No</button></div>
                <p class="app-p small" id="quiz-msg"></p>
                <button type="button" class="app-cta" id="quiz-next">Ver resultado →</button>
              </div>

              <!-- Datos y firma -->
              <div class="scr" data-scr="datos">
                <div class="app-bar"><button type="button" class="app-back" data-go="quiz">‹</button><span>S4 · TUS DATOS</span><span class="app-pct">75%</span></div>
                <h4 class="app-sec">Completa tus datos y firma</h4>
                <form class="app-form" id="app-form" novalidate>
                  <label>Nombre completo<input name="nombre" required autocomplete="name"></label>
                  <label>RUT<input name="rut" required placeholder="12.345.678-9"></label>
                  <div class="two"><label>Cargo<input name="cargo" required autocomplete="organization-title"></label><label>Empresa<input name="empresa" required autocomplete="organization"></label></div>
                  <label>Correo (te enviamos el diploma)<input type="email" name="correo" required autocomplete="email"></label>
                  <div class="app-sig"><canvas id="sig-app" width="600" height="180"></canvas><button type="button" id="sig-app-clear">Borrar</button><span>Firma con el dedo</span></div>
                  <label class="app-chk"><input type="checkbox" name="consentimiento" required> Acepto que SafetyCoach me contacte por esta demo.</label>
                  <p class="app-p small" id="form-msg"></p>
                  <button type="submit" class="app-cta">Firmar y obtener diploma →</button>
                </form>
              </div>

              <!-- Diploma -->
              <div class="scr" data-scr="diploma">
                <div class="app-bar"><button type="button" class="app-back" data-go="home">⌂</button><span>DIPLOMA · 100%</span><span class="app-pct ok">✓</span></div>
                <div class="dip-wrap"><div id="dip-mini"></div></div>
                <div class="dip-btns"><button type="button" class="app-cta" id="dip-open">Descargar diploma (PDF)</button><button type="button" class="app-ghost" data-go="home">Volver a la carátula</button></div>
              </div>

            </div></div>
            <button type="button" class="frame-full" id="frame-full">⤢ Ver en grande</button>
          </div>
          </div>
        </section>
        <div class="dip-print" id="dip-print" hidden></div>

"""


def render_demo(shell):
    return """<!doctype html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Demo SafetyCoach Digital: ingreso, cápsulas, EPP e inspecciones | SafetyCoach</title>
  <meta name="description" content="Prueba la demo de SafetyCoach Digital con una empresa ficticia: documentos de ingreso con firma, cápsula interactiva con evaluación, entrega de EPP e inspección de máquinas con criterios STOP.">
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
            <h1>Demo Pyme SpA</h1>
            <p class="lead">Pyme de 45 trabajadores con cocina y taller de mantención. Así se ve, desde el celular del trabajador, lo que en tu empresa hoy está en papel: firmado, con folio y listo para cualquier fiscalización.</p>
          </div>
          <p class="demo-warn">Esta es una demostración. Los datos que ingreses se guardan solo en este navegador y no se envían a nadie.</p>
        </div>

""" + VITRINA + gate_form("Demo digital", "Para ver la demo, cuéntame de tu empresa", "Así te muestro lo que más sirve a tu operación. Toma 1 minuto.", "Ver la demo") + """
        <div id="tool" hidden>
        <div class="demo-tabs" role="tablist">
          <button role="tab" aria-selected="true" data-t="irl">1 · Ingreso: RIOHS + IRL</button>
          <button role="tab" aria-selected="false" data-t="cap">2 · Cápsula interactiva</button>
          <button role="tab" aria-selected="false" data-t="epp">3 · Entrega de EPP</button>
          <button role="tab" aria-selected="false" data-t="ins">4 · Inspección de máquina</button>
          <button role="tab" aria-selected="false" data-t="reg">5 · Registros <span id="reg-n">0</span></button>
        </div>

        <div class="phone">
          <div class="phone-co"><span class="logo-ph">TU LOGO</span><p>Demo Pyme SpA<small>RUT 76.000.000-0 · empresa ficticia</small></p><img class="sc-corner" src="../assets/img/logo-safetycoach.png" alt="SafetyCoach" width="643" height="285"></div>

          <!-- 1. Ingreso -->
          <div class="demo-pane" id="t-irl">
            <h2>Documentos de ingreso</h2>
            <p class="demo-sub">El trabajador abre cada documento, lo lee y firma una sola vez. Cada documento queda con su propio registro, folio y código de verificación.</p>
            <label>Nombre (ficticio)<input id="irl-nombre" value="Camila Rojas"></label>
            <label>RUT (ficticio)<input id="irl-rut" value="11.111.111-1"></label>
            <label>Cargo<select id="irl-cargo"><option>Ayudante de cocina</option><option>Operaria de envasado</option><option>Maestro de mantención</option><option>Bodeguero</option></select></label>
            <div class="mods docs" id="irl-mods">
              <details data-k="riohs"><summary>Reglamento Interno (RIOHS) <small>Art. 156 CT · DS 44 Art. 56</small></summary><p>Declaro haber recibido en forma gratuita una copia del Reglamento Interno de Orden, Higiene y Seguridad, y asumo la responsabilidad de leerlo y cumplir sus obligaciones, prohibiciones y normas.</p></details>
              <details data-k="irl"><summary>Información de riesgos laborales (IRL) <small>DS 44</small></summary><p><b>Tus riesgos:</b> caídas por pisos húmedos, cortes con cuchillos y rebanadoras, quemaduras con hornos y vapor, manejo manual de carga y atrapamiento en máquinas. <b>Medidas:</b> calzado antideslizante, guante anticorte, guantes térmicos, máximo 25 kg por persona y nunca intervenir una máquina en movimiento.</p></details>
              <details data-k="pts"><summary>Procedimiento de trabajo seguro (PTS) <small>Cuchillos y rebanadora</small></summary><p>Corta siempre alejando el filo del cuerpo, transporta el cuchillo con la punta hacia abajo y nunca lo dejes en agua jabonosa. Antes de limpiar la rebanadora: desenchúfala, deja la perilla en cero y usa guante anticorte.</p></details>
              <details data-k="emer"><summary>Plan de emergencias <small>Vías de evacuación y punto de encuentro</small></summary><p>Ante una alarma, detén tu trabajo, corta el gas si es seguro hacerlo y evacúa sin correr por la vía señalizada hasta el punto de encuentro del estacionamiento.</p></details>
            </div>
            <p class="demo-prog"><span id="irl-read">0</span> de 4 documentos leídos</p>
            <p class="decl">Declaro haber recibido, leído y comprendido los documentos anteriores, sus riesgos, medidas preventivas y métodos de trabajo correctos.</p>
            <div class="sig"><canvas id="sig-irl" width="600" height="160"></canvas><button type="button" class="sig-clear" data-c="sig-irl">Borrar</button><span>Firma aquí con el dedo</span></div>
            <button class="btn btn-primary full" id="irl-send">Firmar y enviar</button>
            <p class="demo-msg" id="irl-msg"></p>
          </div>

          <!-- 2. Cápsula interactiva -->
          <div class="demo-pane" id="t-cap" hidden>
            <h2>Cápsula M03 · Prevención de cortes</h2>
            <p class="demo-sub">Interactiva, con tiempo mínimo, evaluación, intentos y firma. <span class="cap-timer" id="cap-timer">⏱ 0 s</span></p>
            <div class="cap-steps"><span class="on">1</span><span>2</span><span>3</span><span>4</span><span>✓</span></div>
            <div class="slide on" data-s="0"><div class="video-ph" role="img" aria-label="Espacio para video"><span>▶</span><small>Espacio para el video de tu cápsula · 1 a 2 min</small></div><b>1 · ¿Por qué importa?</b><p>Los cortes son de los accidentes más frecuentes en cocinas y plantas de alimentos. Casi todos se evitan con tres hábitos. Vamos a encontrarlos.</p></div>
            <div class="slide" data-s="1"><b>2 · Toca las 3 conductas inseguras</b>
              <div class="tap-grid" id="tap-grid">
                <button type="button" data-bad="1">Cortar en dirección al cuerpo</button>
                <button type="button" data-bad="0">Usar guante anticorte</button>
                <button type="button" data-bad="1">Dejar el cuchillo dentro del lavaplatos con agua jabonosa</button>
                <button type="button" data-bad="0">Llevar el cuchillo con la punta hacia abajo, pegado al cuerpo</button>
                <button type="button" data-bad="1">Sacar la guarda de la rebanadora para limpiar más rápido</button>
                <button type="button" data-bad="0">Desenchufar la rebanadora antes de limpiarla</button>
              </div>
              <p class="tap-msg" id="tap-msg">Encontradas: 0 de 3</p></div>
            <div class="slide" data-s="2"><b>3 · ¿Qué harías?</b><p>Estás picando y el cuchillo se te resbala de la tabla.</p>
              <div class="tap-grid one" id="sc-grid">
                <button type="button" data-ok="0">Intento atraparlo antes de que caiga</button>
                <button type="button" data-ok="1">Lo dejo caer y me aparto</button>
              </div><p class="tap-msg" id="sc-msg"></p></div>
            <div class="slide" data-s="3"><b>4 · Regla de oro</b><p>Filo lejos del cuerpo, cuchillo a la vista y máquina desenergizada antes de meter las manos. <b>Si no hay guarda, no se opera.</b></p></div>
            <div class="slide-nav"><button type="button" class="btn btn-ghost btn-sm" id="sl-prev">‹ Anterior</button><button type="button" class="btn btn-ghost btn-sm" id="sl-next">Siguiente ›</button></div>
            <div class="quiz" id="quiz" hidden>
              <p class="quiz-t">Evaluación · aprobación con 3 de 4 · intento <span id="cap-try">1</span></p>
              <fieldset><legend>1. ¿Hacia dónde debe ir el filo al cortar?</legend>
                <label><input type="radio" name="q1" value="1"> Alejado del cuerpo</label><label><input type="radio" name="q1" value="0"> Hacia el cuerpo, para tener más control</label></fieldset>
              <fieldset><legend>2. Si un cuchillo se cae, debes…</legend>
                <label><input type="radio" name="q2" value="0"> Atraparlo en el aire</label><label><input type="radio" name="q2" value="1"> Dejarlo caer y apartarte</label></fieldset>
              <fieldset><legend>3. Antes de limpiar la rebanadora…</legend>
                <label><input type="radio" name="q3" value="1"> La desenchufo, perilla en cero y guante anticorte</label><label><input type="radio" name="q3" value="0"> La apago y limpio con cuidado</label></fieldset>
              <fieldset><legend>4. ¿Se puede operar la rebanadora sin guarda?</legend>
                <label><input type="radio" name="q4" value="0"> Sí, con cuidado</label><label><input type="radio" name="q4" value="1"> No, nunca</label></fieldset>
              <label class="q-name">Nombre (ficticio)<input id="cap-nombre" value="Camila Rojas"></label>
              <p class="decl">Declaro haber realizado personalmente esta capacitación y comprendido su contenido.</p>
              <div class="sig"><canvas id="sig-cap" width="600" height="160"></canvas><button type="button" class="sig-clear" data-c="sig-cap">Borrar</button><span>Firma aquí con el dedo</span></div>
              <button class="btn btn-primary full" id="cap-send">Enviar evaluación y firma</button>
              <p class="demo-msg" id="cap-msg"></p>
            </div>
          </div>

          <!-- 3. Entrega de EPP -->
          <div class="demo-pane" id="t-epp" hidden>
            <h2>Entrega de EPP</h2>
            <p class="demo-sub">Registro de entrega con firma: qué se entregó, talla, cantidad, motivo y certificación. <small>Ley 16.744 Art. 68 · DS 594 Art. 53</small></p>
            <label>Trabajador (ficticio)<input id="epp-nombre" value="Pedro Soto"></label>
            <label>Cargo<select id="epp-cargo"><option>Maestro de mantención</option><option>Ayudante de cocina</option><option>Bodeguero</option></select></label>
            <label>Motivo de la entrega<select id="epp-motivo"><option>Ingreso</option><option>Reposición por desgaste</option><option>Reposición por pérdida o daño</option><option>Cambio de talla</option></select></label>
            <div class="epp-list" id="epp-list"></div>
            <p class="decl">Declaro haber recibido gratuitamente los elementos de protección personal indicados, en buen estado, y haber sido instruido en su uso, cuidado y reposición. Me comprometo a usarlos durante toda la tarea.</p>
            <div class="sig"><canvas id="sig-epp" width="600" height="160"></canvas><button type="button" class="sig-clear" data-c="sig-epp">Borrar</button><span>Firma aquí con el dedo</span></div>
            <button class="btn btn-primary full" id="epp-send">Registrar entrega</button>
            <p class="demo-msg" id="epp-msg"></p>
          </div>

          <!-- 4. Inspección de máquina -->
          <div class="demo-pane" id="t-ins" hidden>
            <h2>Inspección de máquina</h2>
            <p class="demo-sub">Lista de verificación construida desde la matriz de riesgos. Los ítems <span class="stop-b">STOP</span> detienen la máquina. <small>Res. Ex. 341 ISP (PROSEMEH) · DS 44</small></p>
            <label>Máquina (en terreno, se escanea el QR)<select id="ins-eq"></select></label>
            <div class="ins-type" role="tablist" id="ins-type">
              <button type="button" data-k="op" aria-selected="true">Operación (preuso)</button>
              <button type="button" data-k="mant" aria-selected="false">Mantención</button>
              <button type="button" data-k="limp" aria-selected="false">Limpieza</button>
            </div>
            <label>Inspector (ficticio)<input id="ins-nombre" value="Pedro Soto"></label>
            <label class="chk"><input type="checkbox" id="ins-serie"> <span>El N° de serie <b id="ins-serie-n"></b> coincide con la máquina</span></label>
            <div id="ins-list" class="ins-list"></div>
            <button type="button" class="btn btn-ghost btn-sm" id="ins-geo">📍 Agregar ubicación (opcional)</button> <small id="ins-geo-t"></small>
            <div class="sig"><canvas id="sig-ins" width="600" height="160"></canvas><button type="button" class="sig-clear" data-c="sig-ins">Borrar</button><span>Firma del inspector</span></div>
            <button class="btn btn-primary full" id="ins-send">Registrar inspección</button>
            <div class="ins-res" id="ins-res" hidden></div>
          </div>

          <!-- 5. Registros -->
          <div class="demo-pane" id="t-reg" hidden>
            <h2>Registros e indicadores</h2>
            <p class="demo-sub">Lo que ve la gerencia o el prevencionista, en línea. Toca <b>Ver hoja</b> para ver el registro tal como se entrega.</p>
            <div class="kpis" id="kpis"></div>
            <div id="reg-list" class="reg-list"></div>
            <button type="button" class="btn btn-ghost btn-sm" id="reg-clear">Borrar datos de la demo</button>
          </div>
        </div>

        <section class="sheets-wrap" id="carpeta" aria-labelledby="carpeta-t">
          <div class="sheets-head">
            <div><p class="eyebrow">El entregable</p><h2 id="carpeta-t">Tu carpeta digital: así queda cada registro</h2><p class="demo-sub">Mismo formato que entregamos a nuestros clientes: código, versión, folio, firma validada y huella digital. Con tu logo. Lista para imprimir o guardar en PDF.</p></div>
            <div class="sheets-btns"><button type="button" class="btn btn-ghost btn-sm" id="sheets-all">Ver carpeta completa</button><button type="button" class="btn btn-primary btn-sm" id="sheets-print">Imprimir / guardar PDF</button></div>
          </div>
          <div class="sheets" id="sheets"></div>
        </section>
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
  <script src="../assets/js/vendor/qrcode.js" defer></script>
  <script src="../assets/js/vitrina.js" defer></script>
  <script src="../assets/js/demo.js" defer></script>
</body>
</html>
"""

HISTORIA = """
        <section class="story-ch"><h2>El héroe sin capa</h2>
          <p>Soy Hans Meneses, prevencionista, coach y consultor en prevención de riesgos, liderazgo y cultura preventiva, con más de 20 años de experiencia.</p>
          <p>Durante mucho tiempo me vi como un héroe sin capa. Mi pega era proteger vidas, anticiparme a los peligros y lograr que cada persona volviera sana a su casa. Lo hacía con convicción y con una exigencia brutal.</p>
          <p>Hasta que descubrí una verdad incómoda: <b>podía cuidar a todos y, al mismo tiempo, dejar de cuidar lo esencial de mi propia vida.</b> Penca, pero real.</p>
        </section>
        <section class="story-ch with-img"><div><h2>BASF: la prevención tenía que ir más allá</h2>
          <p>En BASF enfrenté el desafío que marcó mi carrera: avanzar hacia el cero accidentes. Y aprendí que no basta con procedimientos, capacitaciones ni carpetas. Si los líderes no se involucran y los hábitos no cambian, el papel no protege a nadie.</p>
          <p>Hicimos cosas concretas: <b>tolerancia cero frente a riesgos críticos, rondas inspectivas, evidencias visuales, seguimiento riguroso y planes de acción con pocas prioridades, pero bien definidas.</b> La seguridad entró en las decisiones de todos los niveles, desde quien ejecutaba la tarea hasta la gerencia y la dirección corporativa.</p>
          <p class="story-hit">Resultado: más de tres años sin accidentes. Rompimos el récord del tablero: cuatro dígitos.</p>
          <p>Esa experiencia es parte de mi sello: con prioridades claras, liderazgo, controles y seguimiento constante, los resultados se sostienen.</p></div>
          <figure><img src="../assets/img/planta-aislapol.webp" alt="Hans Meneses junto al tablero de días sin accidentes en Aislapol, grupo BASF" width="1195" height="896" loading="lazy" style="object-position:70% 50%"><figcaption>El tablero que llegó a cuatro dígitos.</figcaption></figure>
        </section>
        <section class="story-ch"><h2>Mutual de Seguridad: el otro lado de la mesa</h2>
          <p>Después llegué a una mutualidad como asesor, director de cuenta y consultor de riesgos. Conocí más de 300 pymes por dentro, conversé con sus dueños y gerencias y vi cómo se evalúa a una empresa cuando las cosas salen mal.</p>
          <p>Pero mientras aprendía a proteger a otros, me quedaba la lección más personal de todas.</p>
        </section>
        <section class="story-ch dark"><h2>El quiebre</h2>
          <p>Durante años puse casi toda mi energía en trabajar, responder y proveer. Sin darme cuenta, el trabajo se comió espacios que necesitaban mi presencia, mi tiempo y mi atención.</p>
          <p>Después llegó un despido masivo, el quiebre de mi matrimonio y relaciones que me obligaron a mirarme de verdad. No fue solo un problema laboral o personal: fue el derrumbe de mi forma de entender la vida y mi identidad.</p>
          <p class="story-hit">Dejé de preguntarme quién tenía la culpa y empecé a preguntarme qué tenía que reconocer y transformar en mí.</p>
        </section>
        <section class="story-ch"><h2>La noche más oscura del alma</h2>
          <p>Decidí hacer un proceso de transformación profundo, con la misma determinación con la que enfrentaba los desafíos de seguridad. Coaching, exploración emocional, respiración consciente, meditación, PNL y otras prácticas de bienestar. Revisé mis patrones, mis relaciones, mis creencias y mis decisiones.</p>
          <p>No fue mágico ni de un día para otro. Hubo que mirar lo incómodo, asumir mi parte y dejar de esconderme detrás del trabajo y de los logros. Cambiar no es negar lo vivido ni cargar con toda la culpa: es reconocer lo que te corresponde, aprender y decidir qué vas a hacer distinto.</p>
          <p>Ahí la imagen del ave fénix se volvió real. No se trataba de volver a ser el mismo. Se trataba de renacer con más conciencia.</p>
        </section>
        <section class="story-ch"><h2>De mi proceso al servicio</h2>
          <p>Lo que aprendí despertó las ganas de acompañar a otros. Empecé a guiar procesos de bienestar y transformación personal, con las herramientas que estudié y practiqué. Conocí historias muy duras y aprendí que cada persona es distinta y que no hay una técnica que lo resuelva todo.</p>
          <p class="story-note">No atribuyo a mis herramientas la curación de enfermedades ni prometo resultados que no se pueden garantizar. Acompaño procesos de autoconocimiento y bienestar, y respeto siempre la necesidad de atención médica o psicológica cuando corresponde.</p>
        </section>
        <section class="story-ch"><h2>SafetyCoach renace</h2>
          <p>Hoy llevo todo esto a una nueva etapa de SafetyCoach. Conservo la base de dos décadas: prevención de riesgos, gestión, experiencia con empresas y la convicción de que los resultados salen de acciones concretas y sostenidas. Y le sumo una mirada más profunda sobre las personas, el liderazgo, la comunicación y los factores humanos.</p>
          <p>No basta con diseñar un buen sistema. Hay que lograr que funcione en la realidad, que los responsables se involucren y que las medidas se mantengan. <b>No vendo soluciones mágicas.</b> La prevención no cambia de la noche a la mañana: requiere método, compromiso, seguimiento y mejora continua.</p>
        </section>
        <section class="story-ch"><h2>Yo Puedo Sanarme</h2>
          <p>En paralelo, a través de Yo Puedo Sanarme desarrollo mi faceta de coach de bienestar: acompaño procesos de autoconocimiento, exploración emocional y transformación personal. SafetyCoach trabaja con empresas; Yo Puedo Sanarme, con personas. Los dos nacen del mismo propósito.</p>
        </section>
        <section class="story-ch phoenix"><h2>El ave fénix</h2>
          <p>No reniego del profesional que fui, ni de mis errores, mis logros o lo que me trajo hasta aquí. Lo integro todo. Ya no quiero ser el héroe sin capa que protege a todos mientras se olvida de sí mismo.</p>
          <p class="story-hit">Soy Hans Meneses. No comienzo desde cero: renazco con todo lo aprendido.</p>
          <p class="story-claim">SafetyCoach: experiencia que protege, liderazgo que transforma y prevención que se sostiene.</p>
        </section>
"""

PUENTE = """
        <section class="bridge">
          <p class="eyebrow">Para tu empresa</p>
          <h2>La prevención también se construye en las relaciones humanas</h2>
          <p>Los conflictos, la mala comunicación y los roles poco claros desgastan el clima y a los equipos. Si no los abordas a tiempo, terminan en licencias, denuncias o gente que se va.</p>
          <div class="bridge-grid">
            <article><b>Ley Karin y prevención del acoso y la violencia</b><p>Difusión, formación, liderazgo y medidas organizacionales, respetando los procedimientos legales.</p></article>
            <article><b>Gestión de conflictos</b><p>Herramientas para reconocer tensiones, facilitar conversaciones y resolver desacuerdos.</p></article>
            <article><b>Conoce tu arquetipo y el de tu equipo</b><p>Autoconocimiento y estilos de comunicación. Herramienta de exploración, no diagnóstico psicológico.</p></article>
            <article><b>Comunicación y liderazgo preventivo</b><p>Expectativas claras, retroalimentación y relaciones laborales más sanas.</p></article>
            <article><b>Bienestar y factores psicosociales</b><p>Acciones complementarias para entornos saludables y medidas preventivas.</p></article>
          </div>
          <p class="story-note">Estas actividades complementan, pero no reemplazan, la evaluación de riesgos psicosociales, las medidas organizacionales exigibles ni los procedimientos formales que establece la normativa.</p>
        </section>
"""


def render_historia(shell):
    return """<!doctype html>
<html lang="es-CL">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mi historia: del héroe sin capa al ave fénix | Hans Meneses · SafetyCoach</title>
  <meta name="description" content="La historia de Hans Meneses: más de 20 años en prevención de riesgos, más de tres años sin accidentes en BASF, el quiebre personal y el renacimiento de SafetyCoach.">
  <link rel="canonical" href="https://www.safetycoach.cl/mi-historia/">
  <meta name="theme-color" content="#0B1F3A">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="Mi historia: del héroe sin capa al ave fénix · Hans Meneses">
  <meta property="og:image" content="https://www.safetycoach.cl/assets/img/og-safetycoach.jpg">
  """ + shell['head_links'] + """
</head>
<body>
  <a class="skip" href="#contenido">Saltar al contenido</a>
  """ + shell['svg'] + shell['header'] + """
  <main id="contenido">
    <section class="story-hero">
      <div class="wrap story-hero-in">
        <div>
          <p class="crumbs"><a href="../index.html">Inicio</a> › Mi historia</p>
          <p class="eyebrow">Mi historia</p>
          <h1>Del héroe sin capa al <span>ave fénix</span></h1>
          <p class="lead">Durante años protegí a otros. Hasta que la vida me enseñó que también tenía que aprender a cuidarme.</p>
        </div>
        <img src="../assets/img/hans-retrato.webp" alt="Hans Meneses, fundador de SafetyCoach" width="800" height="1000">
      </div>
    </section>
    <div class="wrap narrow story">""" + HISTORIA + PUENTE + """
      <div class="story-cta">
        <h2>¿Hacemos match?</h2>
        <p>Yo elijo con quién trabajo. Si tú también eliges hacerlo distinto, conversemos.</p>
        <div class="cta-row center"><a class="btn btn-primary btn-lg" href="../index.html#contacto" data-cta="historia_contacto">Conversemos</a><a class="btn btn-ghost btn-lg" href="../autodiagnostico/" data-cta="historia_autodiag">Hacer el autodiagnóstico</a></div>
      </div>
    </div>
  </main>
  """ + shell['footer'] + shell['wa'] + """
  <script src="../assets/js/main.js" defer></script>
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
    out = ROOT / "mi-historia" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render_historia(shell), encoding="utf-8")
    print("ok", out.relative_to(ROOT))
    out = ROOT / "autodiagnostico" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render_autodiag(shell), encoding="utf-8")
    print("ok", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
