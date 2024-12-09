from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from io import BytesIO
import os

app = FastAPI()

template_path = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(template_path))

@app.post("/generate-pdf/")
async def generate_pdf(request: Request):
    # Leer datos dinámicos enviados en el cuerpo del request
    data = await request.json()
    template_data = data.get("data", {})  # Datos para la plantilla

    # Cargar la plantilla example.html
    template = env.get_template("example.review.html")
    template_data["description"] = template_data["description"].replace("\n", "<br>")
    html_content = template.render(template_data)  # Renderiza la plantilla con los datos
    
    # Generar el PDF usando WeasyPrint
    pdf_stream = BytesIO()
    HTML(string=html_content).write_pdf(pdf_stream)
    pdf_stream.seek(0)  # Reinicia el puntero del stream para lectura
    
    # Devolver el PDF como una respuesta HTTP
    return StreamingResponse(pdf_stream, media_type="application/pdf", headers={
        "Content-Disposition": "inline; filename=generated.pdf"
    })

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)