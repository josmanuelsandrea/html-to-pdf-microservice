import os
from fastapi import Request

def image_path_for_preview(request: Request) -> str:
    """
    Devuelve la URL HTTP para usar el logo en el navegador (preview).
    Requiere que hayas montado /static con name="static".
    """
    return str(request.url_for("static", path="scania.png"))

def image_path_for_pdf(base_folder: str) -> str:
    """
    Devuelve una ruta file:/// absoluta (Windows-friendly) para WeasyPrint.
    Esto evita problemas de red/cors cuando genera PDF.
    """
    logo_path = os.path.join(base_folder, "media", "scania.png")
    # Normaliza a forward slashes para WeasyPrint en Windows
    return "file:///" + logo_path.replace("\\", "/")