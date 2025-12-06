# agents/structured_renderer.py
from typing import Dict, Any

def render_structured_claim(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clean and normalize fields:
    - dates -> ISO
    - amounts -> float
    - missing -> None
    """
    import dateutil.parser as dp

    out = {}
    
    normalized = {str(k).lower(): v for k, v in extracted_fields.items()}

    for k, v in normalized.items():
        if v is None or (isinstance(v, str) and v.strip() == ""):
            out[k] = None
            continue
        if "date" in k or "discharge" in k:
            try:
                out[k] = dp.parse(v).date().isoformat()
            except Exception:
                out[k] = v
        elif "amount" in k or "total" in k or "billing" in k:
            try:
                out[k] = float(str(v).replace(",", "").replace("₹","").strip())
            except:
                out[k] = None
        else:
            out[k] = v
    return out
