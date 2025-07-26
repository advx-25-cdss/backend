import asyncio
import httpx
from datetime import date
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"


async def test_ehr_system():
    """Comprehensive test of the EHR CRUD system"""

    async with httpx.AsyncClient() as client:
        print("🏥 Testing EHR System CRUD Operations\n")

        # Test 1: Health Check
        print("1. Testing Health Check...")
        response = await client.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")

        # Test 2: Demographics CRUD
        print("2. Testing Demographics CRUD...")

        # Create demographics
        demo_data = {
            "patient_id": "PATIENT001",
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1990-05-15",
            "gender": "female",
            "phone": "+1234567890",
            "email": "jane.doe@email.com",
            "address": "123 Main St, City, State 12345",
            "emergency_contact_name": "John Doe",
            "emergency_contact_phone": "+1234567891",
            "insurance_info": "Blue Cross Blue Shield",
        }

        response = await client.post(
            f"{BASE_URL}/api/ehr/demographics/", json=demo_data
        )
        print(f"   Create Demographics - Status: {response.status_code}")
        if response.status_code == 200:
            demo_record = response.json()
            demo_id = demo_record["id"]
            print(f"   Created record ID: {demo_id}")

            # Read demographics
            response = await client.get(f"{BASE_URL}/api/ehr/demographics/{demo_id}")
            print(f"   Read Demographics - Status: {response.status_code}")

            # Update demographics
            update_data = {**demo_data, "phone": "+9876543210"}
            response = await client.put(
                f"{BASE_URL}/api/ehr/demographics/{demo_id}", json=update_data
            )
            print(f"   Update Demographics - Status: {response.status_code}")

        print()

        # Test 3: Vital Signs CRUD
        print("3. Testing Vital Signs CRUD...")

        vital_data = {
            "patient_id": "PATIENT001",
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "heart_rate": 72,
            "respiratory_rate": 16,
            "temperature": 98.6,
            "oxygen_saturation": 98,
            "height": 165.0,
            "weight": 65.0,
            "bmi": 23.9,
            "pain_scale": 2,
        }

        response = await client.post(
            f"{BASE_URL}/api/ehr/vital-signs/", json=vital_data
        )
        print(f"   Create Vital Signs - Status: {response.status_code}")
        if response.status_code == 200:
            vital_record = response.json()
            vital_id = vital_record["id"]
            print(f"   Created record ID: {vital_id}")

        print()

        # Test 4: Medical History CRUD
        print("4. Testing Past Medical History CRUD...")

        pmh_data = {
            "patient_id": "PATIENT001",
            "medical_conditions": [
                {
                    "condition": "Hypertension",
                    "date_diagnosed": "2020-01-15",
                    "status": "active",
                },
                {
                    "condition": "Diabetes Type 2",
                    "date_diagnosed": "2019-06-20",
                    "status": "controlled",
                },
            ],
            "surgeries": [
                {
                    "procedure": "Appendectomy",
                    "date": "2015-03-10",
                    "surgeon": "Dr. Smith",
                    "complications": "none",
                }
            ],
            "chronic_diseases": ["Hypertension", "Diabetes"],
            "immunizations": [
                {"vaccine": "COVID-19", "date": "2021-04-15", "lot_number": "ABC123"},
                {"vaccine": "Flu", "date": "2023-10-01", "lot_number": "XYZ789"},
            ],
        }

        response = await client.post(
            f"{BASE_URL}/api/ehr/past-medical-history/", json=pmh_data
        )
        print(f"   Create Past Medical History - Status: {response.status_code}")
        if response.status_code == 200:
            pmh_record = response.json()
            print(f"   Created record ID: {pmh_record['id']}")

        print()

        # Test 5: Medication History CRUD
        print("5. Testing Medication History CRUD...")

        med_data = {
            "patient_id": "PATIENT001",
            "current_medications": [
                {
                    "name": "Lisinopril",
                    "dosage": "10mg",
                    "frequency": "once daily",
                    "start_date": "2020-01-15",
                    "prescriber": "Dr. Johnson",
                },
                {
                    "name": "Metformin",
                    "dosage": "500mg",
                    "frequency": "twice daily",
                    "start_date": "2019-06-20",
                    "prescriber": "Dr. Wilson",
                },
            ],
            "over_the_counter": [
                {"name": "Ibuprofen", "dosage": "200mg", "frequency": "as needed"}
            ],
            "medication_adherence": "good",
            "side_effects_experienced": ["mild dizziness"],
        }

        response = await client.post(
            f"{BASE_URL}/api/ehr/medication-history/", json=med_data
        )
        print(f"   Create Medication History - Status: {response.status_code}")
        if response.status_code == 200:
            med_record = response.json()
            print(f"   Created record ID: {med_record['id']}")

        print()

        # Test 6: Allergy History CRUD
        print("6. Testing Allergy History CRUD...")

        allergy_data = {
            "patient_id": "PATIENT001",
            "drug_allergies": [
                {
                    "allergen": "Penicillin",
                    "reaction": "rash",
                    "severity": "moderate",
                    "date_discovered": "2010-05-01",
                }
            ],
            "food_allergies": [
                {
                    "allergen": "Shellfish",
                    "reaction": "hives",
                    "severity": "mild",
                    "date_discovered": "2005-08-15",
                }
            ],
            "environmental_allergies": [
                {
                    "allergen": "Pollen",
                    "reaction": "sneezing",
                    "severity": "mild",
                    "date_discovered": "childhood",
                }
            ],
            "latex_allergy": False,
            "contrast_allergy": False,
            "carries_epipen": False,
        }

        response = await client.post(
            f"{BASE_URL}/api/ehr/allergy-history/", json=allergy_data
        )
        print(f"   Create Allergy History - Status: {response.status_code}")
        if response.status_code == 200:
            allergy_record = response.json()
            print(f"   Created record ID: {allergy_record['id']}")

        print()

        # Test 7: Get all records for patient
        print("7. Testing Patient Record Retrieval...")

        endpoints = [
            "demographics",
            "vital-signs",
            "past-medical-history",
            "medication-history",
            "allergy-history",
        ]

        for endpoint in endpoints:
            response = await client.get(
                f"{BASE_URL}/api/ehr/{endpoint}/patient/PATIENT001"
            )
            print(
                f"   {endpoint.title()} for PATIENT001 - Status: {response.status_code}, Records: {len(response.json()) if response.status_code == 200 else 0}"
            )

        print()

        # Test 8: Pagination test
        print("8. Testing Pagination...")
        response = await client.get(f"{BASE_URL}/api/ehr/demographics/?skip=0&limit=10")
        print(
            f"   Demographics with pagination - Status: {response.status_code}, Records: {len(response.json()) if response.status_code == 200 else 0}"
        )

        print("\n✅ EHR System Test Complete!")


if __name__ == "__main__":
    print("Starting EHR System Tests...")
    print("Make sure the server is running on http://localhost:8000")
    print("Run: python main.py")
    print("-" * 50)
    asyncio.run(test_ehr_system())
