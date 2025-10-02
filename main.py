# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
# from starlette.datastructures import URL  # ❌ ya no se usa
from weasyprint import HTML as WHTML
from jinja2 import Environment, FileSystemLoader
from io import BytesIO
from tools.dotstring import add_dots_to_number
import os
from datetime import datetime

app = FastAPI()

# --- Jinja env ---
template_path = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(template_path))
this_folder = os.path.dirname(os.path.abspath(__file__))

# --- /static para imágenes/CSS ---
media_dir = os.path.join(this_folder, "media")
app.mount("/static", StaticFiles(directory=media_dir), name="static")

def _sample_data(request: Request):
    """Data you can tweak while previewing."""
    return {
        "WorkOrderId": 1234,
        "Date": "2025-10-02",
        "Customer": "EMAC",
        "Guarantee": True,
        "Plate": "ABC-123",
        "Model": "Scania K310",
        "Chassis": "YS2K4X20001234567",
        "Kilometers": add_dots_to_number(23500),
        "Description": "Cambio de aceite y filtros.<br>Revisión de frenos.",
        # ✅ usar url_for
        "ImagePath": str(request.url_for("static", path="scania.png")),
        "SpareList": [
            {"Code": "OIL-15W40", "Description": "Aceite 15W-40", "Quantity": 20},
            {"Code": "FLT-001", "Description": "Filtro de aceite", "Quantity": 1},
            {"Code": "FLT-002", "Description": "Filtro de aire", "Quantity": 1},
        ],
        "PrintTimestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

@app.get("/preview", response_class=HTMLResponse)
async def preview_html(request: Request):
    template = env.get_template("example.review.html")
    data = _sample_data(request)
    return template.render(data)

@app.post("/preview", response_class=HTMLResponse)
async def preview_html_with_data(request: Request):
    template = env.get_template("example.review.html")
    payload = await request.json()
    data = payload.get("Data", {})
    if "Description" in data:
        data["Description"] = data["Description"].replace("\n", "<br>")
    if "Kilometers" in data:
        data["Kilometers"] = add_dots_to_number(data["Kilometers"])
    # ✅ usar url_for
    data["ImagePath"] = str(request.url_for("static", path="scania.png"))
    return template.render(data)

@app.post("/generate-pdf/")
async def generate_pdf(request: Request):
    data = await request.json()
    template_data = data.get("Data", {})
    template = env.get_template("example.review.html")

    if "Description" in template_data:
        template_data["Description"] = template_data["Description"].replace("\n", "<br>")
    if "Kilometers" in template_data:
        template_data["Kilometers"] = add_dots_to_number(template_data["Kilometers"])

    # ✅ usar url_for
    template_data["ImagePath"] = str(request.url_for("static", path="scania.png"))
    
    # Add print timestamp
    template_data["PrintTimestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = template.render(template_data)

    pdf_stream = BytesIO()
    # ✅ asegurar base_url como str
    WHTML(string=html_content, base_url=str(request.base_url)).write_pdf(pdf_stream)
    pdf_stream.seek(0)
    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=generated.pdf"},
    )

# Run with: uvicorn main:app --reload
