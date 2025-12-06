import re
from agents.data_extractor import extract_text_from_pdf, extract_text_from_image
from agents.neo4j_helper import Neo4jClient


MANDATORY_FIELDS = [
    "invoice_no",
    "patient_name",
    "patient_id",
    "date",
    "doctor_name",
    "total_amount"
]


def ocr_bill(document_path):
    """Runs OCR using the central extractor functions."""
    if str(document_path).lower().endswith(".pdf"):
        return extract_text_from_pdf(document_path)
    else:
        return extract_text_from_image(document_path)


def parse_bill_text(text: str):
    """Extract key bill fields from OCR text."""

    def extract(pattern):
        m = re.search(pattern, text, re.IGNORECASE)
        return m.group(1).strip() if m else None

    return {
        "invoice_no": extract(r"Invoice\s*No[:\- ]+([A-Za-z0-9\-\/]+)"),
        "patient_name": extract(r"Patient\s*Name[:\- ]+([A-Za-z ]+)"),
        "patient_id": extract(r"Patient\s*ID[:\- ]+([A-Za-z0-9]+)"),
        "date": extract(r"Date[:\- ]+([0-9\/\-]+)"),
        "doctor_name": extract(r"Doctor[:\- ]+([A-Za-z .]+)"),
        "total_amount": extract(r"Total\s*Amount[:\- ]+([0-9,]+)")
    }


def validate_bill(document_path, neo4j_uri, neo4j_user, neo4j_password):
    """
    Full OCR + Neo4j validation pipeline.
    """

    # Step 1: OCR
    raw_text = ocr_bill(document_path)

    # Step 2: Extract fields
    fields = parse_bill_text(raw_text)

    # Step 3: Check missing fields
    missing = [f for f, v in fields.items() if v is None]

    # Initialize Neo4j client
    neo = Neo4jClient(neo4j_uri, neo4j_user, neo4j_password)

    neo_compare = {}
    mismatch_fields = []

    # Step 4: Neo4j checks only if patient_id is available
    if fields.get("patient_id"):

        # Fetch Patient
        patient_record = neo.get_patient(fields["patient_id"])
        if not patient_record:
            mismatch_fields.append("patient_id")
            neo_compare["patient_match"] = False
        else:
            name_match = (
                fields["patient_name"].lower() == patient_record["name"].lower()
            )
            neo_compare["patient_match"] = name_match
            if not name_match:
                mismatch_fields.append("patient_name")

        # Fetch Doctor
        if fields.get("doctor_name"):
            doctor_record = neo.get_doctor(fields["doctor_name"])
            doctor_exists = doctor_record is not None
            neo_compare["doctor_match"] = doctor_exists
            if not doctor_exists:
                mismatch_fields.append("doctor_name")

        # Fetch billing amount
        amount_record = neo.get_bill_amount(fields["patient_id"])
        if amount_record:
            db_amount = str(amount_record["amount"]).replace(",", "")
            extracted_amount = fields["total_amount"].replace(",", "")
            amount_match = (db_amount == extracted_amount)
            neo_compare["amount_match"] = amount_match

            if not amount_match:
                mismatch_fields.append("total_amount")

    # Final decision logic
    is_fraud = (len(missing) > 0) or (len(mismatch_fields) > 0)

    return {
        "type": "bill_validation",
        "status": "fraud" if is_fraud else "legitimate",
        "reason": {
            "missing_fields": missing,
            "mismatched_fields": mismatch_fields,
        },
        "fields_extracted": fields,
        "neo4j_comparison": neo_compare,
        "raw_text": raw_text
    }
