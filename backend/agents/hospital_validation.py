# agents/hospital_validation.py
BLACKLIST = set(["Fake Hospital Pvt Ltd", "Blacklisted Clinic"])

def check_hospital(hospital_name: str) -> dict:
    if hospital_name in BLACKLIST:
        return {"valid": False, "reason": "blacklisted"}
    # In real system: check license / registry
    return {"valid": True}
