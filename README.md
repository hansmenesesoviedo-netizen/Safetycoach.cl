# SafetyCoach — sitio web

Sitio de **SafetyCoach · Hans Meneses**: prevención de riesgos, DS 44, protocolos MINSAL, riesgo psicosocial, coaching de seguridad y bienestar laboral.

Estado: **bosquejo v1** (página principal completa y funcional). La estrategia, la arquitectura y los contenidos pendientes están en [`docs/ESTRATEGIA.md`](docs/ESTRATEGIA.md).

## Estructura

```
index.html              Página principal (todas las secciones)
gracias.html            Página de agradecimiento (conversión)
404.html                Página no encontrada
robots.txt, sitemap.xml SEO técnico
netlify.toml            Configuración de publicación (Netlify)
assets/
  css/styles.css        Sistema visual y responsive
  js/main.js            Menú, formularios, recursos, eventos de medición
  img/                  Logo, favicon, imagen para redes (OG)
docs/ESTRATEGIA.md      Propuesta de valor, SEO, CTA y contenidos pendientes
```

HTML, CSS y JS puros: sin compilación ni dependencias.

## Ver en tu computador

**Lo más simple:** descomprime la carpeta y haz doble clic en `index.html`. Se abre en tu navegador con todas las imágenes.

**Con servidor local (para probar como en internet):**

```bash
npx http-server -p 8080
# abrir http://localhost:8080
```

(O con Python: `python3 -m http.server 8080`.)

## Publicar

**Opción recomendada: Netlify (gratis)**
1. Crea una cuenta en netlify.com y elige “Import from Git”. Selecciona este repositorio.
2. No hace falta configurar nada: Netlify lee `netlify.toml`.
3. Los formularios funcionan automáticamente (Netlify Forms) y llegan a tu correo. Actívalo en *Site settings → Forms → Notifications*.
4. Conecta el dominio `safetycoach.cl` en *Domain settings* y apunta el DNS de NIC Chile a Netlify.

**Alternativa: otro hosting (cPanel, Vercel, GitHub Pages)**
Sube los archivos tal cual. Para los formularios crea una cuenta en Formspree (u otro servicio, o tu CRM) y agrega el atributo `data-endpoint="https://formspree.io/f/XXXX"` a cada `<form class="lead-form">`.

## Medición

Pega tu etiqueta de Google Tag Manager en `<head>` (hay un comentario marcando el lugar). Eventos disponibles en `dataLayer`: `cta_click`, `whatsapp_click`, `form_submit`, `lead_magnet_submit`, `cultura_nivel`, `lead_thanks`, `lead_magnet_thanks`.

## Placeholders a reemplazar

Busca en `index.html`: `[TESTIMONIO REAL]` y `[CASO DE ÉXITO]`. Los comentarios `<!-- Confirmar ... -->` marcan datos que debes verificar.
