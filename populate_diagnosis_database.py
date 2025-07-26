"""
Script to populate the database with mock diagnosis data.
Run this script to insert all mock cases, tests, medicines, diagnoses, and treatments.
"""

import asyncio
import logging
from database import connect_to_mongo, close_mongo_connection, db
from mock_diagnosis_data import (
    MOCK_CASES,
    MOCK_TESTS,
    MOCK_MEDICINES,
    MOCK_DIAGNOSES,
    MOCK_TREATMENTS,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def populate_diagnosis_collections():
    """Populate all diagnosis-related collections with mock data."""

    try:
        # Connect to database
        await connect_to_mongo()
        logger.info("Connected to database")

        # Get collections
        cases_collection = db.cdss.cases
        tests_collection = db.cdss.tests
        medicines_collection = db.cdss.medicines
        diagnoses_collection = db.cdss.diagnoses
        treatments_collection = db.cdss.treatments

        # Clear existing data (optional - remove if you want to keep existing data)
        logger.info("Clearing existing diagnosis data...")
        await cases_collection.delete_many({})
        await tests_collection.delete_many({})
        await medicines_collection.delete_many({})
        await diagnoses_collection.delete_many({})
        await treatments_collection.delete_many({})

        # Insert Cases
        logger.info(f"Inserting {len(MOCK_CASES)} cases...")
        cases_data = [case.dict() for case in MOCK_CASES]
        if cases_data:
            await cases_collection.insert_many(cases_data)
        logger.info("Cases inserted successfully")

        # Insert Tests
        logger.info(f"Inserting {len(MOCK_TESTS)} tests...")
        tests_data = [test.dict() for test in MOCK_TESTS]
        if tests_data:
            await tests_collection.insert_many(tests_data)
        logger.info("Tests inserted successfully")

        # Insert Medicines
        logger.info(f"Inserting {len(MOCK_MEDICINES)} medicines...")
        medicines_data = [medicine.dict() for medicine in MOCK_MEDICINES]
        if medicines_data:
            await medicines_collection.insert_many(medicines_data)
        logger.info("Medicines inserted successfully")

        # Insert Diagnoses
        logger.info(f"Inserting {len(MOCK_DIAGNOSES)} diagnoses...")
        diagnoses_data = [diagnosis.dict() for diagnosis in MOCK_DIAGNOSES]
        if diagnoses_data:
            await diagnoses_collection.insert_many(diagnoses_data)
        logger.info("Diagnoses inserted successfully")

        # Insert Treatments
        logger.info(f"Inserting {len(MOCK_TREATMENTS)} treatments...")
        treatments_data = [treatment.dict() for treatment in MOCK_TREATMENTS]
        if treatments_data:
            await treatments_collection.insert_many(treatments_data)
        logger.info("Treatments inserted successfully")

        # Verify data insertion
        cases_count = await cases_collection.count_documents({})
        tests_count = await tests_collection.count_documents({})
        medicines_count = await medicines_collection.count_documents({})
        diagnoses_count = await diagnoses_collection.count_documents({})
        treatments_count = await treatments_collection.count_documents({})

        logger.info("=== Data Population Summary ===")
        logger.info(f"Cases: {cases_count}")
        logger.info(f"Tests: {tests_count}")
        logger.info(f"Medicines: {medicines_count}")
        logger.info(f"Diagnoses: {diagnoses_count}")
        logger.info(f"Treatments: {treatments_count}")
        logger.info("=== Population Complete ===")

        # Show sample patient data
        logger.info("\n=== Sample Patient Data ===")
        sample_cases = await cases_collection.find({"patient_id": "PT0001"}).to_list(
            length=5
        )
        for case in sample_cases:
            logger.info(
                f"Patient PT0001 - Case: {case['case_number'][:8]}... Status: {case['status']}"
            )

    except Exception as e:
        logger.error(f"Error populating database: {e}")
        raise

    finally:
        # Close database connection
        await close_mongo_connection()
        logger.info("Database connection closed")


async def populate_specific_patient(patient_id: str):
    """Populate data for a specific patient only."""

    try:
        await connect_to_mongo()
        logger.info(f"Populating data for patient: {patient_id}")

        # Filter data for specific patient
        patient_cases = [case for case in MOCK_CASES if case.patient_id == patient_id]
        patient_tests = [test for test in MOCK_TESTS if test.patient_id == patient_id]
        patient_medicines = [
            medicine for medicine in MOCK_MEDICINES if medicine.patient_id == patient_id
        ]
        patient_diagnoses = [
            diagnosis
            for diagnosis in MOCK_DIAGNOSES
            if diagnosis.patient_id == patient_id
        ]
        patient_treatments = [
            treatment
            for treatment in MOCK_TREATMENTS
            if treatment.patient_id == patient_id
        ]

        # Get collections
        cases_collection = db.cdss.cases
        tests_collection = db.cdss.tests
        medicines_collection = db.cdss.medicines
        diagnoses_collection = db.cdss.diagnoses
        treatments_collection = db.cdss.treatments

        # Insert patient data
        if patient_cases:
            await cases_collection.insert_many([case.dict() for case in patient_cases])
        if patient_tests:
            await tests_collection.insert_many([test.dict() for test in patient_tests])
        if patient_medicines:
            await medicines_collection.insert_many(
                [medicine.dict() for medicine in patient_medicines]
            )
        if patient_diagnoses:
            await diagnoses_collection.insert_many(
                [diagnosis.dict() for diagnosis in patient_diagnoses]
            )
        if patient_treatments:
            await treatments_collection.insert_many(
                [treatment.dict() for treatment in patient_treatments]
            )

        logger.info(f"Successfully populated data for {patient_id}")
        logger.info(f"- Cases: {len(patient_cases)}")
        logger.info(f"- Tests: {len(patient_tests)}")
        logger.info(f"- Medicines: {len(patient_medicines)}")
        logger.info(f"- Diagnoses: {len(patient_diagnoses)}")
        logger.info(f"- Treatments: {len(patient_treatments)}")

    except Exception as e:
        logger.error(f"Error populating data for {patient_id}: {e}")
        raise

    finally:
        await close_mongo_connection()


if __name__ == "__main__":
    # Run the population script
    asyncio.run(populate_diagnosis_collections())
