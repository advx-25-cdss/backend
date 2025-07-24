"""
Mock patient data for testing the EHR system.
This file contains 20 diverse patients with comprehensive medical records.
"""

from datetime import datetime
from models.ehr_models import (
    Demographics, Menstrual, Obstetric, Marital,
    PastMedicalHistory, FamilyHistory, MedicationHistory, AllergyHistory,
    SocialHistory, VitalSigns
)

# Helper function to create patient IDs
def generate_patient_id(index):
    return f"PT{str(index).zfill(4)}"

# Mock data for 20 diverse patients
MOCK_PATIENTS = [
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0001",
            first_name="Maria",
            last_name="Rodriguez",
            date_of_birth=datetime(1985, 3, 15),
            gender="female",
            phone="+1-555-0101",
            email="maria.rodriguez@email.com",
            address="1234 Maple Street, Los Angeles, CA 90210",
            emergency_contact_name="Carlos Rodriguez",
            emergency_contact_phone="+1-555-0102",
            insurance_info="Blue Cross Blue Shield - Policy #BC123456"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0001",
            temperature=36.8,
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            heart_rate=72,
            respiratory_rate=16,
            oxygen_saturation=98.5,
            height=165.0,
            weight=65.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0001",
            smoking_status="never",
            alcohol_use="occasional",
            drug_use="never",
            occupation="Software Engineer",
            education_level="Bachelor's Degree",
            exercise_frequency="3-4 times per week",
            diet_type="Mediterranean",
            living_situation="Lives with spouse and 2 children"
        ),
        "menstrual": Menstrual(
            _id="",
            patient_id="PT0001",
            last_menstrual_period=datetime(2025, 7, 10),
            cycle_length=28,
            flow_duration=5,
            flow_intensity="normal",
            cycle_regularity="regular",
            contraceptive_method="Birth control pills"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0001",
            marital_status="married",
            spouse_name="Carlos Rodriguez",
            marriage_date=datetime(2010, 6, 20),
            number_of_children=2,
            family_support_system="Strong family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0002",
            first_name="James",
            last_name="Washington",
            date_of_birth=datetime(1972, 11, 8),
            gender="male",
            phone="+1-555-0201",
            email="j.washington@email.com",
            address="567 Oak Avenue, Atlanta, GA 30309",
            emergency_contact_name="Sarah Washington",
            emergency_contact_phone="+1-555-0202",
            insurance_info="Aetna - Policy #AE789012"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0002",
            temperature=37.0,
            blood_pressure_systolic=140,
            blood_pressure_diastolic=90,
            heart_rate=78,
            respiratory_rate=18,
            oxygen_saturation=97.8,
            height=180.0,
            weight=85.0,
            pain_scale=2
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0002",
            smoking_status="former",
            smoking_years=15,
            alcohol_use="moderate",
            drug_use="never",
            occupation="Construction Manager",
            education_level="High School Diploma",
            exercise_frequency="2-3 times per week",
            diet_type="Standard American",
            living_situation="Lives with spouse"
        ),
        "past_medical_history": PastMedicalHistory(
            _id="",
            patient_id="PT0002",
            medical_conditions=[
                {"condition": "Hypertension", "diagnosed_date": datetime(2020, 5, 15), "status": "active"},
                {"condition": "Type 2 Diabetes", "diagnosed_date": datetime(2018, 8, 22), "status": "active"}
            ],
            chronic_diseases=["Hypertension", "Type 2 Diabetes"]
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0002",
            marital_status="married",
            spouse_name="Sarah Washington",
            marriage_date=datetime(1995, 9, 12),
            number_of_children=3,
            family_support_system="Strong family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0003",
            first_name="Yuki",
            last_name="Tanaka",
            date_of_birth=datetime(1990, 7, 22),
            gender="female",
            phone="+1-555-0301",
            email="yuki.tanaka@email.com",
            address="890 Cherry Blossom Lane, San Francisco, CA 94102",
            emergency_contact_name="Hiroshi Tanaka",
            emergency_contact_phone="+1-555-0302",
            insurance_info="Kaiser Permanente - Policy #KP345678"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0003",
            temperature=36.5,
            blood_pressure_systolic=110,
            blood_pressure_diastolic=70,
            heart_rate=65,
            respiratory_rate=14,
            oxygen_saturation=99.2,
            height=155.0,
            weight=52.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0003",
            smoking_status="never",
            alcohol_use="never",
            drug_use="never",
            occupation="Graphic Designer",
            education_level="Master's Degree",
            exercise_frequency="Daily yoga and walking",
            diet_type="Vegetarian",
            living_situation="Lives alone"
        ),
        "menstrual": Menstrual(
            _id="",
            patient_id="PT0003",
            last_menstrual_period=datetime(2025, 7, 5),
            cycle_length=30,
            flow_duration=4,
            flow_intensity="light",
            cycle_regularity="regular",
            contraceptive_method="None"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0003",
            marital_status="single",
            number_of_children=0,
            family_support_system="Close family relationships"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0004",
            first_name="Ahmed",
            last_name="Al-Hassan",
            date_of_birth=datetime(1965, 4, 12),
            gender="male",
            phone="+1-555-0401",
            email="ahmed.alhassan@email.com",
            address="456 Desert Rose Drive, Phoenix, AZ 85001",
            emergency_contact_name="Fatima Al-Hassan",
            emergency_contact_phone="+1-555-0402",
            insurance_info="Cigna - Policy #CG901234"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0004",
            temperature=36.9,
            blood_pressure_systolic=135,
            blood_pressure_diastolic=85,
            heart_rate=70,
            respiratory_rate=16,
            oxygen_saturation=98.0,
            height=175.0,
            weight=78.0,
            pain_scale=1
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0004",
            smoking_status="never",
            alcohol_use="never",
            drug_use="never",
            occupation="Engineering Professor",
            education_level="PhD",
            exercise_frequency="Walking daily",
            diet_type="Halal",
            living_situation="Lives with spouse and children"
        ),
        "family_history": FamilyHistory(
            _id="",
            patient_id="PT0004",
            paternal_history=[
                {"condition": "Heart Disease", "relative": "Father", "age_of_onset": 65}
            ],
            maternal_history=[
                {"condition": "Diabetes", "relative": "Mother", "age_of_onset": 55}
            ]
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0004",
            marital_status="married",
            spouse_name="Fatima Al-Hassan",
            marriage_date=datetime(1990, 8, 15),
            number_of_children=4,
            family_support_system="Extended family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0005",
            first_name="Emily",
            last_name="O'Connor",
            date_of_birth=datetime(1995, 12, 3),
            gender="female",
            phone="+1-555-0501",
            email="emily.oconnor@email.com",
            address="123 Shamrock Street, Boston, MA 02101",
            emergency_contact_name="Patrick O'Connor",
            emergency_contact_phone="+1-555-0502",
            insurance_info="Harvard Pilgrim - Policy #HP567890"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0005",
            temperature=36.7,
            blood_pressure_systolic=105,
            blood_pressure_diastolic=65,
            heart_rate=68,
            respiratory_rate=15,
            oxygen_saturation=99.0,
            height=170.0,
            weight=58.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0005",
            smoking_status="never",
            alcohol_use="occasional",
            drug_use="never",
            occupation="Medical Student",
            education_level="Graduate Student",
            exercise_frequency="5-6 times per week",
            diet_type="Balanced",
            living_situation="Lives with roommates"
        ),
        "allergy_history": AllergyHistory(
            _id="",
            patient_id="PT0005",
            drug_allergies=[
                {"drug": "Penicillin", "reaction": "Rash", "severity": "mild"}
            ],
            food_allergies=[
                {"food": "Shellfish", "reaction": "Hives", "severity": "moderate"}
            ]
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0005",
            marital_status="single",
            number_of_children=0,
            family_support_system="Strong family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0006",
            first_name="Robert",
            last_name="Johnson",
            date_of_birth=datetime(1955, 9, 18),
            gender="male",
            phone="+1-555-0601",
            email="robert.johnson@email.com",
            address="789 Pine Street, Seattle, WA 98101",
            emergency_contact_name="Margaret Johnson",
            emergency_contact_phone="+1-555-0602",
            insurance_info="Medicare - Policy #MC123789"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0006",
            temperature=37.1,
            blood_pressure_systolic=150,
            blood_pressure_diastolic=95,
            heart_rate=82,
            respiratory_rate=20,
            oxygen_saturation=96.5,
            height=178.0,
            weight=92.0,
            pain_scale=4
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0006",
            smoking_status="former",
            smoking_packs_per_day=1.0,
            smoking_years=30,
            alcohol_use="moderate",
            drug_use="never",
            occupation="Retired Mechanic",
            education_level="High School Diploma",
            exercise_frequency="Light walking",
            diet_type="Standard",
            living_situation="Lives with spouse"
        ),
        "past_medical_history": PastMedicalHistory(
            _id="",
            patient_id="PT0006",
            medical_conditions=[
                {"condition": "COPD", "diagnosed_date": datetime(2019, 3, 10), "status": "active"},
                {"condition": "Arthritis", "diagnosed_date": datetime(2015, 6, 5), "status": "active"}
            ],
            surgeries=[
                {"surgery": "Knee Replacement", "date": datetime(2020, 11, 15), "hospital": "Seattle General"}
            ]
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0006",
            marital_status="married",
            spouse_name="Margaret Johnson",
            marriage_date=datetime(1978, 5, 20),
            number_of_children=2,
            family_support_system="Strong family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0007",
            first_name="Priya",
            last_name="Patel",
            date_of_birth=datetime(1988, 1, 25),
            gender="female",
            phone="+1-555-0701",
            email="priya.patel@email.com",
            address="321 Bollywood Boulevard, New York, NY 10001",
            emergency_contact_name="Raj Patel",
            emergency_contact_phone="+1-555-0702",
            insurance_info="Empire Blue Cross - Policy #EB456123"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0007",
            temperature=36.6,
            blood_pressure_systolic=115,
            blood_pressure_diastolic=75,
            heart_rate=70,
            respiratory_rate=16,
            oxygen_saturation=98.8,
            height=162.0,
            weight=60.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0007",
            smoking_status="never",
            alcohol_use="never",
            drug_use="never",
            occupation="Financial Analyst",
            education_level="Master's Degree",
            exercise_frequency="4-5 times per week",
            diet_type="Vegetarian",
            living_situation="Lives with spouse"
        ),
        "obstetric": Obstetric(
            _id="",
            patient_id="PT0007",
            gravida=2,
            para=1,
            abortions=1,
            living_children=1,
            delivery_method=["vaginal"],
            current_pregnancy_status=True,
            expected_due_date=datetime(2025, 12, 15)
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0007",
            marital_status="married",
            spouse_name="Raj Patel",
            marriage_date=datetime(2015, 11, 8),
            number_of_children=1,
            family_support_system="Extended family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0008",
            first_name="Marcus",
            last_name="Thompson",
            date_of_birth=datetime(1998, 6, 14),
            gender="male",
            phone="+1-555-0801",
            email="marcus.thompson@email.com",
            address="654 Basketball Court, Chicago, IL 60601",
            emergency_contact_name="Linda Thompson",
            emergency_contact_phone="+1-555-0802",
            insurance_info="Blue Cross Blue Shield - Policy #BC789456"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0008",
            temperature=36.8,
            blood_pressure_systolic=118,
            blood_pressure_diastolic=78,
            heart_rate=60,
            respiratory_rate=14,
            oxygen_saturation=99.5,
            height=188.0,
            weight=75.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0008",
            smoking_status="never",
            alcohol_use="occasional",
            drug_use="never",
            occupation="College Student/Part-time Basketball Coach",
            education_level="College Student",
            exercise_frequency="Daily athletic training",
            diet_type="High protein",
            living_situation="Lives in dormitory"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0008",
            marital_status="single",
            number_of_children=0,
            family_support_system="Close family relationships"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0009",
            first_name="Chen",
            last_name="Li",
            date_of_birth=datetime(1978, 10, 30),
            gender="other",
            phone="+1-555-0901",
            email="chen.li@email.com",
            address="987 Dragon Street, Portland, OR 97201",
            emergency_contact_name="Wei Li",
            emergency_contact_phone="+1-555-0902",
            insurance_info="Providence Health - Policy #PH321654"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0009",
            temperature=36.7,
            blood_pressure_systolic=125,
            blood_pressure_diastolic=82,
            heart_rate=74,
            respiratory_rate=17,
            oxygen_saturation=98.2,
            height=168.0,
            weight=70.0,
            pain_scale=1
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0009",
            smoking_status="never",
            alcohol_use="occasional",
            drug_use="never",
            occupation="Art Therapist",
            education_level="Master's Degree",
            exercise_frequency="3-4 times per week",
            diet_type="Pescatarian",
            living_situation="Lives with partner"
        ),
        "medication_history": MedicationHistory(
            _id="",
            patient_id="PT0009",
            current_medications=[
                {"name": "Levothyroxine", "dosage": "50mcg", "frequency": "Daily", "start_date": datetime(2020, 1, 1)}
            ]
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0009",
            marital_status="single",
            number_of_children=0,
            family_support_system="Strong community support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0010",
            first_name="Isabella",
            last_name="Santos",
            date_of_birth=datetime(1940, 2, 14),
            gender="female",
            phone="+1-555-1001",
            email="isabella.santos@email.com",
            address="159 Sunshine Avenue, Miami, FL 33101",
            emergency_contact_name="Maria Santos-Garcia",
            emergency_contact_phone="+1-555-1002",
            insurance_info="Medicare + Medicaid - Policy #MM987654"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0010",
            temperature=36.9,
            blood_pressure_systolic=160,
            blood_pressure_diastolic=100,
            heart_rate=85,
            respiratory_rate=22,
            oxygen_saturation=95.0,
            height=158.0,
            weight=68.0,
            pain_scale=6
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0010",
            smoking_status="never",
            alcohol_use="never",
            drug_use="never",
            occupation="Retired Teacher",
            education_level="Bachelor's Degree",
            exercise_frequency="Light walking with assistance",
            diet_type="Heart-healthy",
            living_situation="Lives with daughter's family"
        ),
        "past_medical_history": PastMedicalHistory(
            _id="",
            patient_id="PT0010",
            medical_conditions=[
                {"condition": "Osteoporosis", "diagnosed_date": datetime(2015, 4, 20), "status": "active"},
                {"condition": "Hypertension", "diagnosed_date": datetime(2010, 7, 12), "status": "active"},
                {"condition": "Cataracts", "diagnosed_date": datetime(2018, 9, 8), "status": "treated"}
            ],
            surgeries=[
                {"surgery": "Cataract Surgery", "date": datetime(2019, 1, 15), "hospital": "Miami Eye Center"}
            ]
        ),
        "menstrual": Menstrual(
            _id="",
            patient_id="PT0010",
            menopause_status=True,
            notes="Menopause at age 52"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0010",
            marital_status="widowed",
            spouse_name="Carlos Santos (deceased)",
            marriage_date=datetime(1960, 6, 10),
            number_of_children=3,
            family_support_system="Lives with family, strong support"
        )
    },
    # Additional 10 Chinese patients based in China
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0011",
            first_name="Wei",
            last_name="Zhang",
            date_of_birth=datetime(1987, 8, 18),
            gender="male",
            phone="+86-138-0013-8888",
            email="wei.zhang@qq.com",
            address="Building 5, Unit 2, Room 301, Chaoyang District, Beijing 100020",
            emergency_contact_name="Li Zhang",
            emergency_contact_phone="+86-138-0013-8889",
            insurance_info="Beijing Social Insurance - Policy #BJ2024001"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0011",
            temperature=36.8,
            blood_pressure_systolic=122,
            blood_pressure_diastolic=78,
            heart_rate=68,
            respiratory_rate=16,
            oxygen_saturation=98.7,
            height=175.0,
            weight=70.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0011",
            smoking_status="current",
            smoking_packs_per_day=0.5,
            smoking_years=10,
            alcohol_use="moderate",
            drug_use="never",
            occupation="Software Developer",
            education_level="Bachelor's Degree",
            exercise_frequency="Weekend basketball",
            diet_type="Traditional Chinese",
            living_situation="Lives with parents and wife"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0011",
            marital_status="married",
            spouse_name="Li Zhang",
            marriage_date=datetime(2020, 10, 1),
            number_of_children=0,
            family_support_system="Traditional extended family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0012",
            first_name="Mei",
            last_name="Wang",
            date_of_birth=datetime(1992, 3, 8),
            gender="female",
            phone="+86-139-2012-6666",
            email="mei.wang@163.com",
            address="Lane 1234, Huaihai Road, Xuhui District, Shanghai 200030",
            emergency_contact_name="Jun Wang",
            emergency_contact_phone="+86-139-2012-6667",
            insurance_info="Shanghai Medical Insurance - Policy #SH2024002"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0012",
            temperature=36.5,
            blood_pressure_systolic=108,
            blood_pressure_diastolic=68,
            heart_rate=72,
            respiratory_rate=15,
            oxygen_saturation=99.1,
            height=162.0,
            weight=55.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0012",
            smoking_status="never",
            alcohol_use="never",
            drug_use="never",
            occupation="English Teacher",
            education_level="Master's Degree",
            exercise_frequency="Daily Tai Chi",
            diet_type="Vegetarian Buddhist",
            living_situation="Lives with roommate"
        ),
        "menstrual": Menstrual(
            _id="",
            patient_id="PT0012",
            last_menstrual_period=datetime(2025, 7, 12),
            cycle_length=28,
            flow_duration=5,
            flow_intensity="normal",
            cycle_regularity="regular",
            contraceptive_method="None"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0012",
            marital_status="single",
            number_of_children=0,
            family_support_system="Close family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0013",
            first_name="Xiaoming",
            last_name="Liu",
            date_of_birth=datetime(1975, 11, 22),
            gender="male",
            phone="+86-137-7013-9999",
            email="xiaoming.liu@sina.com",
            address="Unit 15-6, Tianhe District, Guangzhou 510630",
            emergency_contact_name="Xiaoli Liu",
            emergency_contact_phone="+86-137-7013-9998",
            insurance_info="Guangdong Provincial Insurance - Policy #GD2024003"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0013",
            temperature=37.0,
            blood_pressure_systolic=145,
            blood_pressure_diastolic=92,
            heart_rate=76,
            respiratory_rate=18,
            oxygen_saturation=97.5,
            height=168.0,
            weight=80.0,
            pain_scale=2
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0013",
            smoking_status="former",
            smoking_packs_per_day=1.0,
            smoking_years=20,
            alcohol_use="heavy",
            alcohol_frequency="Daily beer with dinner",
            drug_use="never",
            occupation="Factory Manager",
            education_level="Technical Diploma",
            exercise_frequency="Rarely",
            diet_type="Traditional Cantonese",
            living_situation="Lives with wife and child"
        ),
        "past_medical_history": PastMedicalHistory(
            _id="",
            patient_id="PT0013",
            medical_conditions=[
                {"condition": "Hypertension", "diagnosed_date": datetime(2022, 6, 15), "status": "active"},
                {"condition": "Fatty Liver", "diagnosed_date": datetime(2023, 3, 8), "status": "active"}
            ],
            chronic_diseases=["Hypertension", "Fatty Liver Disease"]
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0013",
            marital_status="married",
            spouse_name="Xiaoli Liu",
            marriage_date=datetime(2005, 5, 1),
            number_of_children=1,
            family_support_system="Traditional family structure"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0014",
            first_name="Jing",
            last_name="Chen",
            date_of_birth=datetime(1985, 7, 14),
            gender="female",
            phone="+86-151-0514-7777",
            email="jing.chen@126.com",
            address="Apartment 8-12, Yanta District, Xi'an 710075",
            emergency_contact_name="Ming Chen",
            emergency_contact_phone="+86-151-0514-7776",
            insurance_info="Shaanxi Medical Insurance - Policy #SN2024004"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0014",
            temperature=36.6,
            blood_pressure_systolic=118,
            blood_pressure_diastolic=75,
            heart_rate=70,
            respiratory_rate=16,
            oxygen_saturation=98.9,
            height=165.0,
            weight=58.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0014",
            smoking_status="never",
            alcohol_use="occasional",
            drug_use="never",
            occupation="Traditional Chinese Medicine Doctor",
            education_level="Medical Degree",
            exercise_frequency="Daily Qigong",
            diet_type="Traditional Chinese Medicine principles",
            living_situation="Lives with husband and two children"
        ),
        "obstetric": Obstetric(
            _id="",
            patient_id="PT0014",
            gravida=2,
            para=2,
            abortions=0,
            living_children=2,
            delivery_method=["vaginal", "c-section"],
            current_pregnancy_status=False
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0014",
            marital_status="married",
            spouse_name="Ming Chen",
            marriage_date=datetime(2012, 8, 18),
            number_of_children=2,
            family_support_system="Extended family and in-laws support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0015",
            first_name="Qiang",
            last_name="Zhou",
            date_of_birth=datetime(1960, 12, 5),
            gender="male",
            phone="+86-189-1560-5555",
            email="qiang.zhou@yahoo.com",
            address="Building 23, Jiangbei District, Chongqing 400020",
            emergency_contact_name="Ping Zhou",
            emergency_contact_phone="+86-189-1560-5554",
            insurance_info="Chongqing Senior Insurance - Policy #CQ2024005"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0015",
            temperature=36.9,
            blood_pressure_systolic=155,
            blood_pressure_diastolic=98,
            heart_rate=80,
            respiratory_rate=20,
            oxygen_saturation=96.2,
            height=170.0,
            weight=75.0,
            pain_scale=3
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0015",
            smoking_status="current",
            smoking_packs_per_day=1.5,
            smoking_years=40,
            alcohol_use="heavy",
            alcohol_frequency="Daily baijiu",
            drug_use="never",
            occupation="Retired Construction Worker",
            education_level="Elementary School",
            exercise_frequency="Morning park walks",
            diet_type="Sichuan cuisine",
            living_situation="Lives with wife"
        ),
        "past_medical_history": PastMedicalHistory(
            _id="",
            patient_id="PT0015",
            medical_conditions=[
                {"condition": "COPD", "diagnosed_date": datetime(2020, 9, 12), "status": "active"},
                {"condition": "Type 2 Diabetes", "diagnosed_date": datetime(2018, 4, 20), "status": "active"},
                {"condition": "Hypertension", "diagnosed_date": datetime(2015, 2, 8), "status": "active"}
            ],
            chronic_diseases=["COPD", "Type 2 Diabetes", "Hypertension"]
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0015",
            marital_status="married",
            spouse_name="Ping Zhou",
            marriage_date=datetime(1985, 3, 15),
            number_of_children=2,
            family_support_system="Adult children provide support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0016",
            first_name="Yan",
            last_name="Xu",
            date_of_birth=datetime(1995, 4, 28),
            gender="female",
            phone="+86-177-1695-3333",
            email="yan.xu@qq.com",
            address="Room 1205, Binjiang District, Hangzhou 310051",
            emergency_contact_name="Hao Xu",
            emergency_contact_phone="+86-177-1695-3332",
            insurance_info="Zhejiang Medical Insurance - Policy #ZJ2024006"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0016",
            temperature=36.7,
            blood_pressure_systolic=110,
            blood_pressure_diastolic=70,
            heart_rate=65,
            respiratory_rate=14,
            oxygen_saturation=99.3,
            height=168.0,
            weight=52.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0016",
            smoking_status="never",
            alcohol_use="never",
            drug_use="never",
            occupation="E-commerce Manager",
            education_level="Master's Degree",
            exercise_frequency="Yoga 4 times per week",
            diet_type="Health-conscious, low sodium",
            living_situation="Lives alone, close to family"
        ),
        "menstrual": Menstrual(
            _id="",
            patient_id="PT0016",
            last_menstrual_period=datetime(2025, 7, 8),
            cycle_length=30,
            flow_duration=4,
            flow_intensity="light",
            cycle_regularity="regular",
            contraceptive_method="IUD"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0016",
            marital_status="single",
            number_of_children=0,
            family_support_system="Close-knit family"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0017",
            first_name="Gang",
            last_name="Li",
            date_of_birth=datetime(1968, 9, 3),
            gender="male",
            phone="+86-158-6817-4444",
            email="gang.li@sohu.com",
            address="Unit 7-8, Heping District, Tianjin 300050",
            emergency_contact_name="Hui Li",
            emergency_contact_phone="+86-158-6817-4443",
            insurance_info="Tianjin Municipal Insurance - Policy #TJ2024007"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0017",
            temperature=37.1,
            blood_pressure_systolic=148,
            blood_pressure_diastolic=94,
            heart_rate=78,
            respiratory_rate=19,
            oxygen_saturation=97.0,
            height=172.0,
            weight=82.0,
            pain_scale=4
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0017",
            smoking_status="former",
            smoking_packs_per_day=2.0,
            smoking_years=25,
            alcohol_use="moderate",
            drug_use="never",
            occupation="Taxi Driver",
            education_level="High School",
            exercise_frequency="Occasional walking",
            diet_type="Northern Chinese cuisine",
            living_situation="Lives with wife and elderly mother"
        ),
        "past_medical_history": PastMedicalHistory(
            _id="",
            patient_id="PT0017",
            medical_conditions=[
                {"condition": "Lumbar Disc Disease", "diagnosed_date": datetime(2021, 11, 5), "status": "active"},
                {"condition": "Hypertension", "diagnosed_date": datetime(2019, 7, 18), "status": "active"}
            ],
            chronic_diseases=["Lumbar Disc Disease", "Hypertension"]
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0017",
            marital_status="married",
            spouse_name="Hui Li",
            marriage_date=datetime(1995, 10, 20),
            number_of_children=1,
            family_support_system="Multi-generational household"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0018",
            first_name="Ling",
            last_name="Wu",
            date_of_birth=datetime(1990, 6, 12),
            gender="female",
            phone="+86-134-1890-2222",
            email="ling.wu@gmail.com",
            address="Building 45, Nanshan District, Shenzhen 518054",
            emergency_contact_name="Jun Wu",
            emergency_contact_phone="+86-134-1890-2221",
            insurance_info="Shenzhen Tech Insurance - Policy #SZ2024008"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0018",
            temperature=36.8,
            blood_pressure_systolic=125,
            blood_pressure_diastolic=80,
            heart_rate=74,
            respiratory_rate=16,
            oxygen_saturation=98.6,
            height=160.0,
            weight=62.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0018",
            smoking_status="never",
            alcohol_use="occasional",
            drug_use="never",
            occupation="Financial Analyst",
            education_level="Master's Degree",
            exercise_frequency="Swimming twice weekly",
            diet_type="Balanced modern diet",
            living_situation="Lives with husband"
        ),
        "obstetric": Obstetric(
            _id="",
            patient_id="PT0018",
            gravida=1,
            para=0,
            abortions=0,
            living_children=0,
            current_pregnancy_status=True,
            expected_due_date=datetime(2025, 11, 20)
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0018",
            marital_status="married",
            spouse_name="Jun Wu",
            marriage_date=datetime(2022, 2, 14),
            number_of_children=0,
            family_support_system="Young couple with distant family support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0019",
            first_name="Bin",
            last_name="Yang",
            date_of_birth=datetime(2001, 1, 16),
            gender="male",
            phone="+86-187-0119-1111",
            email="bin.yang@student.edu.cn",
            address="Dormitory 6, Room 412, Wuhan University, Wuhan 430072",
            emergency_contact_name="Feng Yang",
            emergency_contact_phone="+86-187-0119-1110",
            insurance_info="Student Medical Insurance - Policy #WH2024009"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0019",
            temperature=36.6,
            blood_pressure_systolic=115,
            blood_pressure_diastolic=75,
            heart_rate=62,
            respiratory_rate=14,
            oxygen_saturation=99.5,
            height=178.0,
            weight=68.0,
            pain_scale=0
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0019",
            smoking_status="never",
            alcohol_use="occasional",
            drug_use="never",
            occupation="University Student (Computer Science)",
            education_level="University Student",
            exercise_frequency="Basketball 3 times per week",
            diet_type="Cafeteria food, instant noodles",
            living_situation="University dormitory with roommates"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0019",
            marital_status="single",
            number_of_children=0,
            family_support_system="Parents provide financial support"
        )
    },
    {
        "demographics": Demographics(
            _id="",
            patient_id="PT0020",
            first_name="Xiu",
            last_name="Huang",
            date_of_birth=datetime(1945, 5, 20),
            gender="female",
            phone="+86-133-4520-8888",
            email="xiu.huang@163.com",
            address="Lane 567, Jingan District, Shanghai 200040",
            emergency_contact_name="Wei Huang",
            emergency_contact_phone="+86-133-4520-8887",
            insurance_info="Shanghai Senior Citizen Insurance - Policy #SH2024010"
        ),
        "vital_signs": VitalSigns(
            _id="",
            patient_id="PT0020",
            temperature=36.8,
            blood_pressure_systolic=165,
            blood_pressure_diastolic=102,
            heart_rate=88,
            respiratory_rate=22,
            oxygen_saturation=94.5,
            height=155.0,
            weight=60.0,
            pain_scale=5
        ),
        "social_history": SocialHistory(
            _id="",
            patient_id="PT0020",
            smoking_status="never",
            alcohol_use="never",
            drug_use="never",
            occupation="Retired Seamstress",
            education_level="Elementary School",
            exercise_frequency="Daily morning exercises in park",
            diet_type="Traditional Shanghai cuisine",
            living_situation="Lives with son's family"
        ),
        "past_medical_history": PastMedicalHistory(
            _id="",
            patient_id="PT0020",
            medical_conditions=[
                {"condition": "Osteoarthritis", "diagnosed_date": datetime(2018, 3, 12), "status": "active"},
                {"condition": "Hypertension", "diagnosed_date": datetime(2012, 8, 25), "status": "active"},
                {"condition": "Osteoporosis", "diagnosed_date": datetime(2020, 6, 10), "status": "active"},
                {"condition": "Cataracts", "diagnosed_date": datetime(2022, 1, 8), "status": "treated"}
            ],
            surgeries=[
                {"surgery": "Cataract Surgery (both eyes)", "date": datetime(2022, 4, 15), "hospital": "Shanghai Eye Hospital"}
            ]
        ),
        "menstrual": Menstrual(
            _id="",
            patient_id="PT0020",
            menopause_status=True,
            notes="Menopause at age 50"
        ),
        "marital": Marital(
            _id="",
            patient_id="PT0020",
            marital_status="widowed",
            spouse_name="Ming Huang (deceased)",
            marriage_date=datetime(1968, 9, 25),
            number_of_children=2,
            family_support_system="Lives with son's family, traditional care"
        )
    }
]

def get_patient_data(patient_id: str = None):
    """
    Get mock patient data by patient ID or return all patients.

    Args:
        patient_id: Optional patient ID to filter by

    Returns:
        Dictionary containing patient data or list of all patients
    """
    if patient_id:
        for patient in MOCK_PATIENTS:
            if patient["demographics"].patient_id == patient_id:
                return patient
        return None
    return MOCK_PATIENTS

def get_all_demographics():
    """Get demographics for all mock patients."""
    return [patient["demographics"] for patient in MOCK_PATIENTS]

def get_all_vital_signs():
    """Get vital signs for all mock patients that have them."""
    return [patient["vital_signs"] for patient in MOCK_PATIENTS if "vital_signs" in patient]

# Summary of our mock patients:
"""
Patient Diversity Summary:
Original 10 patients (PT0001-PT0010):
1. PT0001 - Maria Rodriguez (Hispanic/Latino female, 39, software engineer)
2. PT0002 - James Washington (African American male, 52, construction manager, hypertension/diabetes)
3. PT0003 - Yuki Tanaka (Japanese female, 34, graphic designer, vegetarian)
4. PT0004 - Ahmed Al-Hassan (Middle Eastern male, 59, professor, religious dietary restrictions)
5. PT0005 - Emily O'Connor (Irish American female, 29, medical student, allergies)
6. PT0006 - Robert Johnson (Caucasian male, 69, retired, COPD/arthritis)
7. PT0007 - Priya Patel (Indian female, 37, financial analyst, currently pregnant)
8. PT0008 - Marcus Thompson (African American male, 26, college student/athlete)
9. PT0009 - Chen Li (Chinese non-binary, 46, art therapist, thyroid condition)
10. PT0010 - Isabella Santos (Hispanic elderly female, 85, retired teacher, multiple chronic conditions)

Additional 10 Chinese patients based in China (PT0011-PT0020):
11. PT0011 - Wei Zhang (Chinese male, 37, software developer, Beijing, smoker)
12. PT0012 - Mei Wang (Chinese female, 33, English teacher, Shanghai, vegetarian Buddhist)
13. PT0013 - Xiaoming Liu (Chinese male, 49, factory manager, Guangzhou, hypertension/fatty liver)
14. PT0014 - Jing Chen (Chinese female, 40, TCM doctor, Xi'an, 2 children)
15. PT0015 - Qiang Zhou (Chinese male, 64, retired construction worker, Chongqing, COPD/diabetes/hypertension)
16. PT0016 - Yan Xu (Chinese female, 30, e-commerce manager, Hangzhou, health-conscious)
17. PT0017 - Gang Li (Chinese male, 56, taxi driver, Tianjin, lumbar disc disease)
18. PT0018 - Ling Wu (Chinese female, 35, financial analyst, Shenzhen, currently pregnant)
19. PT0019 - Bin Yang (Chinese male, 24, university student, Wuhan, athlete)
20. PT0020 - Xiu Huang (Chinese elderly female, 80, retired seamstress, Shanghai, multiple chronic conditions)

Diversity now includes:
- Ages: 22-85 years (expanded range)
- Geographic locations: US states + major Chinese cities (Beijing, Shanghai, Guangzhou, Xi'an, Chongqing, Hangzhou, Tianjin, Shenzhen, Wuhan)
- Cultural contexts: Western healthcare system + Chinese healthcare system
- Traditional practices: TCM, Tai Chi, Qigong, traditional Chinese diet
- Chinese-specific elements: Chinese phone numbers (+86), Chinese email providers (QQ, 163, 126), Chinese insurance systems
- Lifestyle variations: Traditional extended family living, modern urban professionals, university dormitory life
- Medical conditions common in China: Fatty liver disease, traditional smoking/alcohol patterns
- Educational diversity: Elementary school to medical degree (including TCM)
- Occupational diversity: Traditional (seamstress, factory worker) to modern (e-commerce, tech)

This comprehensive dataset now provides excellent coverage for testing EHR systems in both Western and Chinese healthcare contexts.
"""
