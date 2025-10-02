from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from weasyprint import HTML as WHTML
from jinja2 import Environment, FileSystemLoader
from io import BytesIO
import os

# Helpers
from tools.image_rendering_tools import image_path_for_preview, image_path_for_pdf
from tools.data import preprocess_payload, sample_data, add_print_timestamp

app = FastAPI()

# Rutas base
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(THIS_FOLDER, "templates")
MEDIA_DIR = os.path.join(THIS_FOLDER, "media")

# Jinja
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Static para preview en navegador
app.mount("/static", StaticFiles(directory=MEDIA_DIR), name="static")


@app.get("/preview", response_class=HTMLResponse)
async def preview_html(request: Request):
    """Renderiza la plantilla como HTML para previsualizar en el navegador."""
    template = env.get_template("example.review.html")
    data = sample_data(request)  # datos de muestra con logo por HTTP
    return template.render(data)


@app.post("/preview", response_class=HTMLResponse)
async def preview_html_with_data(request: Request):
    """Permite mandar JSON con Data para ver el HTML renderizado en el navegador."""
    template = env.get_template("example.review.html")
    payload = await request.json()
    data = payload.get("Data", {}) or {}

    # normaliza campos, salto de línea, km, etc.
    data = preprocess_payload(data)

    # logo por HTTP (navegador)
    data["ImagePath"] = image_path_for_preview(request)

    # timestamp (opcional para preview también)
    data = add_print_timestamp(data)

    return template.render(data)


@app.post("/generate-pdf/")
async def generate_pdf(request: Request):
    """Genera el PDF con WeasyPrint."""
    payload = await request.json()
    template_data = payload.get("Data", {}) or {}

    # normaliza campos (saltos de línea, km con puntos, etc.)
    template_data = preprocess_payload(template_data)

    # timestamp de impresión
    template_data = add_print_timestamp(template_data)

    # logo por filesystem (más robusto para PDF)
    template_data["ImagePath"] = image_path_for_pdf(base_folder=THIS_FOLDER)

    # render HTML
    template = env.get_template("example.review.html")
    html_content = template.render(template_data)

    # PDF
    pdf_stream = BytesIO()
    # base_url a la carpeta del proyecto para permitir recursos relativos si los usas
    WHTML(string=html_content, base_url=THIS_FOLDER).write_pdf(pdf_stream)
    pdf_stream.seek(0)

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=generated.pdf"},
    )

# Run: uvicorn main:app --reload
