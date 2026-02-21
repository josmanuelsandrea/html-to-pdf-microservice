from datetime import datetime
from typing import Dict, Any
from zoneinfo import ZoneInfo

# Importa tu helper de miles
from tools.dotstring import add_dots_to_number, format_currency

def preprocess_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ajusta campos del payload:
    - Reemplaza \n por <br> en Description
    - Formatea Kilometers con puntos de miles (si existe)
    - Formatea LaborCost, PartsCost, TotalCost como moneda
    - Formatea UnitPrice y Subtotal de cada item en SpareList
    """
    d = dict(data)  # copia superficial

    desc = d.get("Description")
    if isinstance(desc, str):
        d["Description"] = desc.replace("\n", "<br>")

    kms = d.get("Kilometers")
    if kms is not None:
        try:
            kms_int = int(str(kms).replace(".", "").replace(",", ""))
            d["Kilometers"] = add_dots_to_number(kms_int)
        except Exception:
            pass

    for cost_field in ("LaborCost", "PartsCost", "TotalCost"):
        if d.get(cost_field) is not None:
            d[cost_field] = format_currency(d[cost_field])

    spare_list = d.get("SpareList")
    if isinstance(spare_list, list):
        formatted_spares = []
        for item in spare_list:
            item = dict(item)
            for price_field in ("UnitPrice", "Subtotal"):
                if item.get(price_field) is not None:
                    item[price_field] = format_currency(item[price_field])
            formatted_spares.append(item)
        d["SpareList"] = formatted_spares

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
            {"Code": "OIL-15W40", "Description": "Aceite 15W-40",   "Quantity": 20, "UnitPrice": "12.50",  "Subtotal": "250.00"},
            {"Code": "FLT-001",   "Description": "Filtro de aceite", "Quantity": 1,  "UnitPrice": "35.00",  "Subtotal": "35.00"},
            {"Code": "FLT-002",   "Description": "Filtro de aire",   "Quantity": 1,  "UnitPrice": "28.00",  "Subtotal": "28.00"},
        ],
        "LaborCost": "150.00",
        "PartsCost": "313.00",
        "TotalCost": "463.00",
        "PrintTimestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
