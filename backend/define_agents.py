# # # define_agents.py
# from agents.safety_agent import safety_check_agent
# from agents.data_extractor import extract_text_from_pdf, extract_text_from_image
# from agents.structured_renderer import render_structured_claim
# from agents.employee_validation import is_valid_employee
# from agents.policy_agent import policy_check
# from agents.hospital_validation import check_hospital
# from agents.medical_doc_agent import validate_medical_doc
# from agents.fraud_cql_agent import fraud_cql_agent
# from agents.amount_validation import amount_check
# from agents.disease_and_treatment import disease_treatment_check
# from agents.bill_validator import validate_bill
# from agents.discharge_summary_validator import validate_discharge_summary
# from agents.final_summary_agent import aggregate_results
# import pandas as pd

# # class AgentWrapper:
# #     def __init__(self, llm):
# #         self.llm = llm

# #     def run_full_investigation(self, claim_row: dict, document_paths: dict, policy_text: str, employee_db_csv: str):
# #         # 1. Safety
# #         if not safety_check_agent(self.llm, str(claim_row)):
# #             return {"error": "unsafe_input"}

# #         results = []

# #         # 2. Extract docs
# #         extracted_texts = {}
# #         for k, p in document_paths.items():
# #             if k in ["bill", "discharge_summary"]:
# #                 # BILL VALIDATION
# #                 bill_result = validate_bill(
# #                     document_paths["bill"],
# #                     neo4j_uri="bolt://localhost:7687",
# #                     neo4j_user="neo4j",
# #                     neo4j_password="admin@123"
# #                 )
# #                 results.append(bill_result)

# #                 continue
# #             if p.lower().endswith(".pdf"):
# #                 extracted_texts[k] = extract_text_from_pdf(p)
# #             else:
# #                 extracted_texts[k] = extract_text_from_image(p)

# #         # 3. Structured render
# #         structured = render_structured_claim(claim_row)
# #         results.append({"structured_ok": True})

# #         # 4. Employee validation
# #         emp = is_valid_employee(structured.get("patient_id") or structured.get("employee_id"))
# #         results.append(emp)

# #         df = pd.read_csv("/data/health_claims_dataset_no_employer.csv")
# #         subset = df[["policy_plan", "employee_id"]]
# #         employee_id = structured.get("patient_id") or structured.get("employee_id")

# #         # fetch all matching rows
# #         emp_rows = subset[subset["employee_id"] == employee_id]

# #         # if employee exists
# #         if emp_rows.empty:
# #             policy_plan = None
# #         else:
# #             # pick unique policy plan (should be one)
# #             policy_plan = emp_rows["policy_plan"].unique()[0]

# #         claim = policy_plan

# #         # 5. Hospital validation
# #         hosp = check_hospital(structured.get("hospital"))
# #         results.append(hosp)

# #         # 6. Medical docs validation
# #         # medv = validate_medical_doc(self.llm, extracted_texts.get("medical_report",""), ["diagnosis","discharge_date","doctor"])
# #         # results.append(medv)

# #         # schema_info = 
# #         cql_agt = fraud_cql_agent(self.llm, 
# #                 fraud_scenario="Multiple claims submitted from same doctor for same patient within 24 hours",
# #                 schema_info={"tables": ["claims", "patients", "doctors"],
# #                              "relationships": "claims.patient_id -> patients.id; claims.doctor_id -> doctors.id"})
# #         results.append(cql_agt)

# #         # 7. Policy check
# #         policy_kb = open("kb.txt").read()
# #         pol = policy_check(self.llm, policy_kb, claim)
# #         results.append(pol)

# #         # 8. Amount check
# #         amt = amount_check(structured.get("claim_amount"), claim)  # example policy limit
# #         results.append(amt)



# #         # 9. Disease/Treatment
# #         # dt = disease_treatment_check(self.llm, diagnosis=structured.get("diagnosis",""), treatment=structured.get("treatment",""))
# #         # results.append(dt)

# #         # Final aggregation
# #         summary = aggregate_results(results)
# #         return {"structured": structured, "agent_results": results, "summary": summary, "extracted_texts": extracted_texts}


# class AgentWrapper:
#     def __init__(self, llm):
#         self.llm = llm

#     def run_full_investigation(self, claim_row: dict, document_paths: dict, policy_text: str, employee_db_csv: str):

#         # 1. Safety
#         if not safety_check_agent(self.llm, str(claim_row)):
#             return {"error": "unsafe_input"}

#         results = []

#         extracted_texts = {}

#         # -------------------------
#         # 2. Extract OCR for non-bill and non-discharge docs
#         # -------------------------
#         for k, p in document_paths.items():
#             if k not in ["bill", "discharge_summary"]:
#                 if p.lower().endswith(".pdf"):
#                     extracted_texts[k] = extract_text_from_pdf(p)
#                 else:
#                     extracted_texts[k] = extract_text_from_image(p)

#         # -------------------------
#         # 3. Validate BILL (OCR inside)
#         # -------------------------
#         if "bill" in document_paths:
#             bill_result = validate_bill(
#                 document_paths["bill"],
#                 neo4j_uri="bolt://localhost:7687",
#                 neo4j_user="neo4j",
#                 neo4j_password="admin@123"
#             )
#             results.append(bill_result)

#         # -------------------------
#         # 4. Validate DISCHARGE SUMMARY
#         # -------------------------
#         if "discharge_summary" in document_paths:
#             discharge_result = validate_discharge_summary(
#                 document_paths["discharge_summary"],
#                 neo4j_uri="bolt://localhost:7687",
#                 neo4j_user="neo4j",
#                 neo4j_password="admin@123"
#             )
#             results.append(discharge_result)

#         # -------------------------
#         # 5. Structured claim extraction
#         # -------------------------
#         structured = render_structured_claim(claim_row)
#         results.append({"structured_ok": True})

#         # 6. Employee validation
#         emp = is_valid_employee(structured.get("patient_id") or structured.get("employee_id"))
#         results.append(emp)

#         # 7. Policy lookup from CSV
#         df = pd.read_csv("/data/health_claims_dataset_no_employer.csv")
#         subset = df[["policy_plan", "employee_id"]]
#         employee_id = structured.get("patient_id") or structured.get("employee_id")

#         emp_rows = subset[subset["employee_id"] == employee_id]
#         policy_plan = None if emp_rows.empty else emp_rows["policy_plan"].unique()[0]
#         claim = policy_plan

#         # 8. Hospital validation
#         hosp = check_hospital(structured.get("hospital"))
#         results.append(hosp)

#         # 9. Fraud pattern (CQL)
#         cql_agt = fraud_cql_agent(
#             self.llm,
#             fraud_scenario="Multiple claims submitted from same doctor for same patient within 24 hours",
#             schema_info={
#                 "tables": ["claims", "patients", "doctors"],
#                 "relationships": "claims.patient_id -> patients.id; claims.doctor_id -> doctors.id"
#             }
#         )
#         results.append(cql_agt)

#         # 10. Policy eligibility
#         policy_kb = open("kb.txt").read()
#         pol = policy_check(self.llm, policy_kb, claim)
#         results.append(pol)

#         # 11. Amount check
#         amt = amount_check(structured.get("claim_amount"), claim)
#         results.append(amt)

#         # Final aggregation
#         summary = aggregate_results(results)

#         return {
#             "structured": structured,
#             "agent_results": results,
#             "summary": summary,
#             "extracted_texts": extracted_texts
#         }


import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import shap
from sklearn.preprocessing import LabelEncoder

# Import your existing agents
from agents.safety_agent import safety_check_agent
from agents.data_extractor import extract_text_from_pdf, extract_text_from_image
from agents.structured_renderer import render_structured_claim
from agents.employee_validation import is_valid_employee
from agents.policy_agent import policy_check
from agents.hospital_validation import check_hospital
from agents.medical_doc_agent import validate_medical_doc
from agents.fraud_cql_agent import fraud_cql_agent
from agents.amount_validation import amount_check
from agents.disease_and_treatment import disease_treatment_check
from agents.bill_validator import validate_bill
from agents.discharge_summary_validator import validate_discharge_summary
from agents.final_summary_agent import aggregate_results

class AgentWrapper:
    def __init__(self, llm, model_path="xgb_claims_model.pkl"):
        self.llm = llm
        features = ["claim_amount", "previous_claim_count", "previous_risk_flags", "billing_total", "hospital_freq", "doctor_freq",
                    "speciality_le", "claim_date_month", "claim_date_day", "claim_date_weekday",
                    "claim_date_year", "reported_injury_month", "reported_injury_year",
                    "days_between"
                    ]
        self.features = features
        
        # Load trained XGBoost model
        self.model = joblib.load(model_path)
        self.explainer = shap.TreeExplainer(self.model)
    
    def _ml_predict(self, structured_claim):
        import xgboost as xgb
        import shap
        import numpy as np

        # Ensure all required features exist
        missing_features = [f for f in self.features if f not in structured_claim]
        if missing_features:
            # Return a safe response without running the model
            return None, None, None, f"ML model skipped: missing features {missing_features}"

        # Prepare input
        df_row = pd.DataFrame([structured_claim])[self.features]
        d = xgb.DMatrix(df_row)

        # Predict
        probs = self.model.predict(d)[0]
        pred_class = int(np.argmax(probs))

        # SHAP explainability
        shap_values = self.explainer.shap_values(df_row)  # binary classification
        top_features = sorted(
            zip(self.features, shap_values[0]),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:3]

        # Human explanation using LLM
        explanation = self.llm(f"Explain these feature importances in simple terms: {top_features}")

        return pred_class, probs, top_features, explanation


    def _explain_to_human(self, shap_dict, pred_class, pred_prob):
        """Generate human-readable explanation using LLM."""
        explanation_prompt = f"""
        The model predicted risk class {pred_class} with probability {pred_prob:.2f}.
        The top contributing features are:
        {shap_dict}
        Explain in simple words for a non-technical user why this claim is high-risk or low-risk.
        """
        explanation = self.llm(explanation_prompt)
        return explanation

    def run_full_investigation(self, document_paths: dict):
        # -------------------------
        # 1. Safety check
        # -------------------------
        # if not safety_check_agent(self.llm, str(claim_row)):
        #     return {"error": "unsafe_input"}

        results = {}
        extracted_texts = {}
        print("Documents present in paths: ", document_paths)

        # -------------------------
        # 2. Extract OCR text
        # -------------------------
        for k, p in document_paths.items():
            if k not in ["bill", "discharge_summary"]:
                if p.lower().endswith(".pdf"):
                    extracted_texts[k] = extract_text_from_pdf(p)
                else:
                    extracted_texts[k] = extract_text_from_image(p)


        print("Extracted text from the documents: ", extracted_texts)
        # -------------------------
        # 3. Validate BILL & DISCHARGE SUMMARY
        # -------------------------
        # if "bill" in document_paths:
        #     results["bill"] = validate_bill(document_paths["bill"])
        # if "discharge_summary" in document_paths:
        #     results["discharge_summary"] = validate_discharge_summary(document_paths["discharge_summary"])

        bill_result = results.get("bill", "Not provided")
        discharge_result = results.get("discharge_summary", "Not provided")

        print(
            "Extracted text from the bills and discharge summary:",
            bill_result,
            discharge_result
        )
        # -------------------------
        # 4. Structured claim extraction
        # -------------------------
        structured = render_structured_claim(extracted_texts)
        results["structured_ok"] = True

        print("Structured Output: ", structured)

        # -------------------------
        # 5. Employee validation
        # -------------------------
        results["employee"] = is_valid_employee(structured.get("patient_id") or structured.get("employee_id"))
        print("Employee validation: ", results["employee"])

        # -------------------------
        # 6. Policy & hospital validation
        # -------------------------
        df = pd.read_csv("C://Users//GenAIMUMOLYAUSR32//Documents//Insurance Tracker//backend//data//health_claims_dataset_no_employer.csv")
        employee_id = structured.get("patient_id") or structured.get("employee_id")
        emp_rows = df[df["employee_id"] == employee_id]
        policy_plan = None if emp_rows.empty else emp_rows["policy_plan"].unique()[0]
        policy_kb = open("kb.txt").read()
        results["policy"] = policy_check(self.llm, policy_kb, policy_plan)
        results["hospital"] = check_hospital(structured.get("hospital"))

        print("Results fetched from policy checker and hospital validation: ", results["policy"], " ", results["hospital"])

        # -------------------------
        # 7. Fraud CQL check & amount check
        # -------------------------
        # results["fraud_cql"] = fraud_cql_agent(self.llm)
        results["amount_check"] = amount_check(structured.get("claim_amount"), policy_plan)

        print("Amount greater than or less than check: ", results["amount_check"])

        # -------------------------
        # 8. Disease / treatment validation
        # -------------------------
        results["disease_treatment"] = disease_treatment_check(self.llm, structured.get("diagnosis",""), structured.get("treatment",""))
        print("Disease treatment check: ", results["disease_treatment"])

        # -------------------------
        # 9. ML-based risk prediction + SHAP explainability
        # -------------------------

        # ML prediction
        pred_class, probs, shap_explanations, human_explanation = self._ml_predict(structured)

        if pred_class is None:
            results["ml_model_warning"] = human_explanation
        else:
            results["ml_prediction"] = {
                "pred_class": pred_class,
                "probabilities": probs.tolist(),
                "top_features": shap_explanations,
                "explanation": human_explanation
            }
        summary = aggregate_results(results)

        return {
        "structured": structured,
        "agent_results": results,
        "summary": summary,
        "extracted_texts": extracted_texts
        }

