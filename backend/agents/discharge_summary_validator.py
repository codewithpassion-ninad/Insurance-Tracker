# agents/discharge_summary_validator.py
import re
from agents.data_extractor import extract_text_from_pdf, extract_text_from_image


MANDATORY_DS_FIELDS = [
    "patient_name",
    "patient_id",
    "hospital_name",
    "admission_date",
    "discharge_date",
    "doctor",
    "diagnosis",
    "total_amount"
]


def ocr_discharge_summary(document_path):
    """Runs OCR using the main extractor."""
    if str(document_path).lower().endswith(".pdf"):
        return extract_text_from_pdf(document_path)
    else:
        return extract_text_from_image(document_path)


def parse_discharge_summary(text):
    """Extract required fields from OCR text."""

    def extract(pattern):
        m = re.search(pattern, text, re.IGNORECASE)
        return m.group(1).strip() if m else None

    return {
        "patient_name": extract(r"Name[:\-\s]+([A-Za-z ]+)"),
        "patient_id": extract(r"Patient\s*ID[:\- ]+([A-Za-z0-9]+)"),
        "hospital_name": extract(r"Hospital\s*Name[:\- ]+([A-Za-z0-9 ]]+)"),
        "admission_date": extract(r"Admission\s*Date[:\- ]+([0-9\/\-]+)"),
        "discharge_date": extract(r"Discharge\s*Date[:\- ]+([0-9\/\-]+)"),
        "doctor": extract(r"Doctor[:\- ]+([A-Za-z .]+)"),
        "diagnosis": extract(r"Primary\s*Diagnosis[:\- ]+([A-Za-z0-9 ,]+)"),
        "total_amount": extract(r"Total\s*Amount[:\- ]+([0-9,]+)")
    }


def validate_discharge_summary(document_path):
    """
    Full validation with OCR inside.
    Returns fraud/legitimate + reason + extracted fields + raw OCR text.
    """
    raw_text = ocr_discharge_summary(document_path)
    fields = parse_discharge_summary(raw_text)

    missing = [f for f, v in fields.items() if v is None]

    if missing:
        return {
            "type": "discharge_summary_validation",
            "status": "fraud",
            "reason": f"Missing mandatory fields: {', '.join(missing)}",
            "fields": fields,
            "raw_text": raw_text
        }

    return {
        "type": "discharge_summary_validation",
        "status": "legitimate",
        "reason": "All mandatory fields present",
        "fields": fields,
        "raw_text": raw_text
    }
