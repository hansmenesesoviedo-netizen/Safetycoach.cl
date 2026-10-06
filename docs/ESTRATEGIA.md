# SafetyCoach — Estrategia del sitio (bosquejo v1)

## 1. Propuesta de valor

**SafetyCoach es tu área externa de prevención: diagnostica, implementa y acompaña hasta que la seguridad funcione en las personas, no solo en los documentos.**

- Para: gerentes, dueños, RR.HH., operaciones y prevencionistas de pymes, contratistas y empresas con varios centros de trabajo.
- Problema: cumplen en papel (o no cumplen) y la prevención depende de una persona sobrecargada.
- Diferencia: experiencia técnica de más de 20 años más herramientas de coaching para líderes y equipos.
- Modelo comercial: Diagnóstico → Implementación → Acompañamiento mensual → Fidelización.

### Alternativas de frase central (elegida: la 1)
1. **“No te entrego solamente un documento. Te acompaño hasta que la prevención funcione.”** (Elegida: habla del cliente, promete un resultado y vende acompañamiento recurrente.)
2. “No trabajo para que tu empresa tenga más documentos. Trabajo para que la prevención realmente funcione.”
3. “Menos carpetas, más prevención que se nota en terreno.”
4. “Cumplir es el piso. Gestionar es lo que evita el próximo accidente.”
5. “La seguridad se firma en papel, pero se construye en las personas.”

## 2. Arquitectura y navegación

**Fase 1 (este bosquejo):** una página principal larga (one-page) con anclas. Contiene todas las secciones y permite validar el mensaje y empezar a captar contactos de inmediato.

**Fase 2:** separar cada sección en su propia URL (mejor SEO):

```
/                         Home
/sobre-safetycoach/       Hans Meneses + método
/ds-44/                   Diagnóstico e implementación DS 44
/servicios/               Especialidades (y subpáginas por protocolo)
  /servicios/protocolos-minsal/
  /servicios/tmert/  /servicios/prexor/  /servicios/mmc/ ...
/coaching-de-seguridad/   Sesiones de política, metas, líderes
/riesgos-psicosociales/   CEAL-SM y planes de intervención
/bienestar/               SafetyCoach Bienestar
/pymes/                   Landing "Tu prevención externa"
/contratistas/            Landing contratistas
/experiencia/             Casos y testimonios
/recursos/                Biblioteca / Academia (blog + descargables)
/contacto/
```

Landings SEO locales para después: `/prevencion-de-riesgos-santiago/`, `/prevencion-de-riesgos-la-serena/`, `/asesoria-ds-44/`, `/prevencionista-externo/`.

Menú principal: DS 44 · Servicios · Coaching · Psicosocial · Bienestar · Sobre Hans · Recursos · [Solicitar diagnóstico].

## 3. Sistema visual

- **Colores (del logo):** azul marino `#0B1F3A` (autoridad), verde `#3BA54A` (acción/CTA), celeste faro `#2FA8E0`, amarillo luz `#F5CD30` (acentos, nunca en textos largos), petróleo `#0F4C5C` (sección psicosocial).
- **Tipografía:** Manrope (títulos) + Inter (texto).
- **Símbolo:** el faro, que guía sin empujar. Es la metáfora del coach y sirve también para cursos, comunidad y certificaciones.
- **Reglas:** mucho blanco, pocas imágenes y de calidad, nada de fotos de stock con casco, sin exceso de íconos.
- **Fotografía:** pendiente sesión de fotos de Hans (retrato, terreno real, facilitando un taller).

## 4. CTA y conversión

| CTA | Dónde | Lleva a |
|---|---|---|
| Solicitar diagnóstico | Header, hero, formulario | Formulario (#contacto) |
| Hablar con Hans | Hero | WhatsApp con mensaje |
| Solicitar diagnóstico DS 44 | Sección DS 44 | Formulario con “Diagnóstico DS 44” preseleccionado |
| Quiero evaluar mi empresa | Planes | Formulario con “Prevención externa” |
| Quiero conversar sobre la prevención de mi empresa | Pymes | Formulario |
| Necesito implementar protocolos | Servicios | Formulario con “Protocolos MINSAL” |
| Quiero fortalecer mi cultura preventiva | Coaching | Formulario con “Bienestar/cultura” |
| Agendar una conversación | Sobre Hans | Formulario |
| Descargar recurso | Biblioteca | Modal de captura (nombre, empresa, correo, WhatsApp) |

Cada CTA **preselecciona la necesidad** en el formulario, así el lead llega ya clasificado.

**Formulario calificador:** tamaño (trabajadores, centros), si tiene prevencionista y qué necesita. Con eso se pueden priorizar los contactos:
- A (llamar hoy): 26+ trabajadores, o sin prevencionista, o fiscalización o accidente.
- B (48 h): diagnóstico DS 44 o protocolos.
- C (nutrir): solo recurso descargable.

**Medición:** `main.js` envía a `dataLayer` los eventos `cta_click`, `whatsapp_click`, `form_submit`, `lead_magnet_submit`, `cultura_nivel`, y `gracias.html` envía `lead_thanks` (la conversión principal en GA4).

## 5. Estructura SEO

- `title` y `description` con: prevención de riesgos, DS 44, protocolos MINSAL, Chile.
- H1 único (pregunta del hero). H2 por sección con palabras clave naturales: “DS 44”, “protocolos MINSAL”, “riesgos psicosociales”, “prevencionista externo” (pymes), “empresas contratistas”.
- Schema.org: `ProfessionalService` + `Person` + `WebSite`. En fase 2: `Service` por página, `FAQPage` y `Article` en el blog.
- Open Graph con imagen propia (`og-safetycoach.jpg`).
- `sitemap.xml`, `robots.txt`, URL canónica.

| Palabra clave | Página destino (fase 2) |
|---|---|
| implementación DS 44, diagnóstico DS 44, asesoría DS44 empresas | /ds-44/ |
| prevención de riesgos Chile, asesoría prevención de riesgos | / |
| prevencionista externo, prevención de riesgos para empresas | /pymes/ |
| protocolos MINSAL, implementación protocolos MINSAL | /servicios/protocolos-minsal/ |
| riesgo psicosocial, CEAL-SM | /riesgos-psicosociales/ |
| prevención de riesgos Santiago / La Serena | landings locales |
| seguridad laboral, asesor en prevención de riesgos | blog + home |

## 6. Contenidos que debes aportar

- [ ] **[FOTOGRAFÍA DE HANS]**: 3 a 6 fotos profesionales (retrato, terreno, facilitando).
- [ ] **[LINK LINKEDIN]**
- [ ] Confirmar **WhatsApp** (+56 9 3230 4800) y correo (hans@safetycoach.cl), tomados de tu firma.
- [ ] Confirmar la **redacción exacta de títulos** (institución y nombre del título) y si quieres mostrar logos de las certificaciones.
- [ ] Confirmar cifras para el hero: “+20 años”. Tu presentación menciona “+300 pymes asesoradas” y “+100 empresas”: solo los publico si los confirmas.
- [ ] 2 o 3 **[TESTIMONIO REAL]** con nombre, cargo y empresa (con autorización).
- [ ] **[LOGO CLIENTE]** que tengas autorización para mostrar.
- [ ] 1 o 2 **[CASO DE ÉXITO]**: situación → qué hiciste → resultado (puede ser anónimo).
- [ ] Zonas de atención presencial (¿Santiago? ¿La Serena? ¿Coquimbo?).
- [ ] ¿Mostrar precios “desde”? (Recomendación: no en la web; sí después del diagnóstico).
- [ ] Contenido de los 7 recursos descargables (PDF).
- [ ] Nombres definitivos de los programas de Bienestar.
- [ ] Logo vectorial (SVG/AI/PDF). El actual (643 px) sirve para la web, pero el vectorial asegura nitidez en todo tamaño.
- [ ] **Derechos de las fotos:** las fotos de personas (coaching, reunión, diagnóstico, muro, ejecutivo con flechas, figura 3D) y la ilustración de la ampolleta vienen de tus presentaciones y parecen de bancos de imágenes. Confirma que tienes licencia para usarlas en la web, o reemplázalas por fotos propias o compradas (por ejemplo, en Shutterstock, Adobe Stock, o gratuitas de Unsplash/Pexels).
- [ ] Fotos propias en terreno y en talleres: son más creíbles que cualquier foto de banco y reemplazarían a las actuales.

## 7. Recomendaciones de conversión

1. Responder en menos de 2 horas hábiles: el primer prevencionista que responde suele quedarse con la conversación.
2. Ofrecer una “Conversación de diagnóstico de 30 minutos” agendable (Calendly o Google Calendar) en `gracias.html`.
3. Publicar cuanto antes los 2 o 3 testimonios: es el elemento que más falta hoy.
4. Hacer primero el Checklist DS 44 y usarlo en LinkedIn como gancho.
5. Crear el perfil de Google Business (ficha local) con el mismo nombre, teléfono y web.
6. Escribir un artículo al mes sobre preguntas reales de clientes (“¿Qué me fiscalizan del DS 44?”).
