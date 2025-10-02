from datetime import datetime
from typing import Dict, Any
from zoneinfo import ZoneInfo

# Importa tu helper de miles
from tools.dotstring import add_dots_to_number

def preprocess_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ajusta campos del payload:
    - Reemplaza \n por <br> en Description
    - Formatea Kilometers con puntos de miles (si existe)
    """
    d = dict(data)  # copia superficial

    desc = d.get("Description")
    if isinstance(desc, str):
        d["Description"] = desc.replace("\n", "<br>")

    kms = d.get("Kilometers")
    if kms is not None:
        try:
            # por si llega como string
            kms_int = int(str(kms).replace(".", "").replace(",", ""))
            d["Kilometers"] = add_dots_to_number(kms_int)
        except Exception:
            # si no se puede convertir, lo dejamos como vino
            pass

    return d

def add_print_timestamp(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agrega el timestamp de impresión (YYYY-mm-dd HH:MM:SS).
    """
    d = dict(data)
    local_tz = ZoneInfo("America/Guayaquil")
    d["PrintTimestamp"] = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
    return d

def sample_data(request) -> Dict[str, Any]:
    """
    Datos de muestra para /preview (incluye logo por HTTP).
    """
    # import local para evitar dependencias cruzadas
    from tools.image_rendering_tools import image_path_for_preview

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
        "ImagePath": image_path_for_preview(request),
        "SpareList": [
            {"Code": "OIL-15W40", "Description": "Aceite 15W-40", "Quantity": 20},
            {"Code": "FLT-001", "Description": "Filtro de aceite", "Quantity": 1},
            {"Code": "FLT-002", "Description": "Filtro de aire", "Quantity": 1},
        ],
        "PrintTimestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
