# agents/neo4j_helper.py
from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    # Fetch patient details
    def get_patient(self, patient_id):
        query = """
        MATCH (p:Patient {patient_id: $patient_id})
        RETURN p.patient_id AS id, p.name AS name
        """
        with self.driver.session() as session:
            result = session.run(query, patient_id=patient_id).data()
        return result[0] if result else None

    # Fetch doctor details
    def get_doctor(self, doctor_name):
        query = """
        MATCH (d:Doctor {name: $name})
        RETURN d.name AS name
        """
        with self.driver.session() as session:
            result = session.run(query, name=doctor_name).data()
        return result[0] if result else None

    # Fetch billing amount from DB
    def get_bill_amount(self, patient_id):
        query = """
        MATCH (:Patient {patient_id: $patient_id})-[:HAS_BILL]->(b:Bill)
        RETURN b.total_amount AS amount
        """
        with self.driver.session() as session:
            result = session.run(query, patient_id=patient_id).data()
        return result[0] if result else None
