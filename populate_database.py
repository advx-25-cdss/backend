"""
Script to populate the local database with mock patient data.
Run this script to insert all 20 mock patients into the MongoDB database.
"""

import asyncio
import logging
from database import connect_to_mongo, close_mongo_connection, db
from services.ehr_service import (
    demographics_service, menstrual_service, obstetric_service, marital_service,
    history_present_illness_service, past_medical_history_service, family_history_service,
    medication_history_service, allergy_history_service, social_history_service,
    vital_signs_service
)
from mock_patient_data import MOCK_PATIENTS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def populate_database():
    """Populate the database with mock patient data."""
    try:
        # Connect to database
        await connect_to_mongo()
        logger.info("Connected to MongoDB")

        # Counters for tracking insertions
        counters = {
            'demographics': 0,
            'vital_signs': 0,
            'social_history': 0,
            'menstrual': 0,
            'obstetric': 0,
            'marital': 0,
            'past_medical_history': 0,
            'family_history': 0,
            'medication_history': 0,
            'allergy_history': 0,
            'history_present_illness': 0
        }

        # Process each patient
        for i, patient_data in enumerate(MOCK_PATIENTS, 1):
            patient_id = patient_data["demographics"].patient_id
            logger.info(f"Processing patient {i}/20: {patient_id}")

            # Insert demographics (always present)
            if "demographics" in patient_data:
                demo_dict = patient_data["demographics"].dict()
                await demographics_service.create(demo_dict)
                counters['demographics'] += 1
                logger.info(f"  ✓ Demographics inserted for {patient_id}")

            # Insert vital signs (always present)
            if "vital_signs" in patient_data:
                vital_dict = patient_data["vital_signs"].dict()
                await vital_signs_service.create(vital_dict)
                counters['vital_signs'] += 1
                logger.info(f"  ✓ Vital signs inserted for {patient_id}")

            # Insert social history (always present)
            if "social_history" in patient_data:
                social_dict = patient_data["social_history"].dict()
                await social_history_service.create(social_dict)
                counters['social_history'] += 1
                logger.info(f"  ✓ Social history inserted for {patient_id}")

            # Insert marital status (always present)
            if "marital" in patient_data:
                marital_dict = patient_data["marital"].dict()
                await marital_service.create(marital_dict)
                counters['marital'] += 1
                logger.info(f"  ✓ Marital status inserted for {patient_id}")

            # Insert menstrual data (if present)
            if "menstrual" in patient_data:
                menstrual_dict = patient_data["menstrual"].dict()
                await menstrual_service.create(menstrual_dict)
                counters['menstrual'] += 1
                logger.info(f"  ✓ Menstrual data inserted for {patient_id}")

            # Insert obstetric data (if present)
            if "obstetric" in patient_data:
                obstetric_dict = patient_data["obstetric"].dict()
                await obstetric_service.create(obstetric_dict)
                counters['obstetric'] += 1
                logger.info(f"  ✓ Obstetric data inserted for {patient_id}")

            # Insert past medical history (if present)
            if "past_medical_history" in patient_data:
                pmh_dict = patient_data["past_medical_history"].dict()
                await past_medical_history_service.create(pmh_dict)
                counters['past_medical_history'] += 1
                logger.info(f"  ✓ Past medical history inserted for {patient_id}")

            # Insert family history (if present)
            if "family_history" in patient_data:
                fh_dict = patient_data["family_history"].dict()
                await family_history_service.create(fh_dict)
                counters['family_history'] += 1
                logger.info(f"  ✓ Family history inserted for {patient_id}")

            # Insert medication history (if present)
            if "medication_history" in patient_data:
                mh_dict = patient_data["medication_history"].dict()
                await medication_history_service.create(mh_dict)
                counters['medication_history'] += 1
                logger.info(f"  ✓ Medication history inserted for {patient_id}")

            # Insert allergy history (if present)
            if "allergy_history" in patient_data:
                ah_dict = patient_data["allergy_history"].dict()
                await allergy_history_service.create(ah_dict)
                counters['allergy_history'] += 1
                logger.info(f"  ✓ Allergy history inserted for {patient_id}")

            # Insert history of present illness (if present)
            if "history_present_illness" in patient_data:
                hpi_dict = patient_data["history_present_illness"].dict()
                await history_present_illness_service.create(hpi_dict)
                counters['history_present_illness'] += 1
                logger.info(f"  ✓ History of present illness inserted for {patient_id}")

            logger.info(f"  Patient {patient_id} processing complete\n")

        # Print summary
        logger.info("=" * 60)
        logger.info("DATABASE POPULATION COMPLETE")
        logger.info("=" * 60)
        logger.info("Records inserted by type:")
        for record_type, count in counters.items():
            logger.info(f"  {record_type.replace('_', ' ').title()}: {count}")

        total_records = sum(counters.values())
        logger.info(f"\nTotal records inserted: {total_records}")
        logger.info(f"Total patients: {len(MOCK_PATIENTS)}")

        # Verify data by checking a few patients
        logger.info("\n" + "=" * 60)
        logger.info("VERIFICATION")
        logger.info("=" * 60)

        # Check first patient (US patient)
        us_patient = await demographics_service.get_by_patient_id("PT0001")
        if us_patient:
            logger.info(f"✓ US Patient PT0001 (Maria Rodriguez) found: {us_patient[0]['first_name']} {us_patient[0]['last_name']}")

        # Check first Chinese patient
        cn_patient = await demographics_service.get_by_patient_id("PT0011")
        if cn_patient:
            logger.info(f"✓ Chinese Patient PT0011 (Wei Zhang) found: {cn_patient[0]['first_name']} {cn_patient[0]['last_name']}")

        # Check elderly patient
        elderly_patient = await demographics_service.get_by_patient_id("PT0020")
        if elderly_patient:
            logger.info(f"✓ Elderly Patient PT0020 (Xiu Huang) found: {elderly_patient[0]['first_name']} {elderly_patient[0]['last_name']}")

        logger.info("\n✅ Mock patient data successfully populated to database!")

    except Exception as e:
        logger.error(f"❌ Error populating database: {str(e)}")
        raise
    finally:
        # Close database connection
        await close_mongo_connection()
        logger.info("Database connection closed")

async def clear_database():
    """Clear all EHR data from the database (use with caution!)"""
    try:
        await connect_to_mongo()
        logger.info("Connected to MongoDB for clearing data")

        # List of all EHR collections
        collections = [
            'demographics', 'vital_signs', 'social_history', 'marital',
            'menstrual', 'obstetric', 'past_medical_history', 'family_history',
            'medication_history', 'allergy_history', 'history_present_illness'
        ]

        for collection_name in collections:
            result = await db.cdss[collection_name].delete_many({})
            logger.info(f"Cleared {result.deleted_count} records from {collection_name}")

        logger.info("✅ Database cleared successfully!")

    except Exception as e:
        logger.error(f"❌ Error clearing database: {str(e)}")
        raise
    finally:
        await close_mongo_connection()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage mock patient data in database")
    parser.add_argument("--clear", action="store_true", help="Clear all data before populating")
    parser.add_argument("--clear-only", action="store_true", help="Only clear data, don't populate")

    args = parser.parse_args()

    async def main():
        if args.clear_only:
            await clear_database()
        elif args.clear:
            await clear_database()
            await populate_database()
        else:
            await populate_database()

    # Run the script
    asyncio.run(main())
