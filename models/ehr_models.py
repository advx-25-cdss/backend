from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime, date, timezone

class Demographics(BaseModel):
    _id: str
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: Literal["male", "female", "other"]
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_info: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class Menstrual(BaseModel):
    _id: str
    patient_id: str
    last_menstrual_period: Optional[datetime] = None
    cycle_length: Optional[int] = None  # days
    flow_duration: Optional[int] = None  # days
    flow_intensity: Optional[Literal["light", "normal", "heavy"]] = None
    cycle_regularity: Optional[Literal["regular", "irregular"]] = None
    contraceptive_method: Optional[str] = None
    menopause_status: Optional[bool] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class Obstetric(BaseModel):
    _id: str
    patient_id: str
    gravida: Optional[int] = None  # number of pregnancies
    para: Optional[int] = None  # number of births
    abortions: Optional[int] = None
    living_children: Optional[int] = None
    pregnancy_history: Optional[List[dict]] = None  # list of pregnancy details
    delivery_method: Optional[List[Literal["vaginal", "c-section"]]] = None
    complications: Optional[List[str]] = None
    current_pregnancy_status: Optional[bool] = None
    expected_due_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class Marital(BaseModel):
    _id: str
    patient_id: str
    marital_status: Literal["single", "married", "divorced", "widowed", "separated"]  # "single", "married", "divorced", "widowed", "separated"
    spouse_name: Optional[str] = None
    marriage_date: Optional[datetime] = None
    number_of_children: Optional[int] = None
    family_support_system: Optional[str] = None
    domestic_violence_history: Optional[bool] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class HistoryPresentIllness(BaseModel):
    _id: str
    patient_id: str
    chief_complaint: str
    history_of_present_illness: str
    onset: Optional[Literal["sudden", "gradual"]] = None  # "sudden", "gradual"
    duration: Optional[str] = None
    severity: Optional[int] = None  # 1-10 scale
    quality: Optional[str] = None
    radiation: Optional[str] = None
    associated_symptoms: Optional[List[str]] = None
    alleviating_factors: Optional[List[str]] = None
    aggravating_factors: Optional[List[str]] = None
    previous_episodes: Optional[bool] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True


class PastMedicalHistory(BaseModel):
    _id: str
    patient_id: str
    medical_conditions: Optional[List[dict]] = None  # [{"condition": str, "diagnosed_date": date, "status": str}]
    surgeries: Optional[List[dict]] = None  # [{"surgery": str, "date": date, "hospital": str}]
    hospitalizations: Optional[List[dict]] = None  # [{"reason": str, "date": date, "duration": int}]
    chronic_diseases: Optional[List[str]] = None
    immunizations: Optional[List[dict]] = None  # [{"vaccine": str, "date": date}]
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class FamilyHistory(BaseModel):
    _id: str
    patient_id: str
    maternal_history: Optional[List[dict]] = None  # [{"condition": str, "relative": str, "age_of_onset": int}]
    paternal_history: Optional[List[dict]] = None
    siblings_history: Optional[List[dict]] = None
    children_history: Optional[List[dict]] = None
    genetic_disorders: Optional[List[str]] = None
    hereditary_diseases: Optional[List[str]] = None
    family_cancer_history: Optional[List[dict]] = None
    family_heart_disease: Optional[List[dict]] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class MedicationHistory(BaseModel):
    _id: str
    patient_id: str
    current_medications: Optional[List[dict]] = None  # [{"name": str, "dosage": str, "frequency": str, "start_date": date}]
    past_medications: Optional[List[dict]] = None
    over_the_counter: Optional[List[dict]] = None
    supplements: Optional[List[dict]] = None
    herbal_remedies: Optional[List[dict]] = None
    medication_adherence: Optional[str] = None  # "excellent", "good", "fair", "poor"
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class AllergyHistory(BaseModel):
    _id: str
    patient_id: str
    drug_allergies: Optional[List[dict]] = None  # [{"drug": str, "reaction": str, "severity": str}]
    food_allergies: Optional[List[dict]] = None
    environmental_allergies: Optional[List[dict]] = None
    latex_allergy: Optional[bool] = None
    no_known_allergies: Optional[bool] = None
    allergy_testing_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class SocialHistory(BaseModel):
    _id: str
    patient_id: str
    smoking_status: Optional[Literal["never", "former", "current"]] = None
    smoking_packs_per_day: Optional[float] = None
    smoking_years: Optional[int] = None
    alcohol_use: Optional[Literal["never", "occasional", "moderate", "heavy"]] = None
    alcohol_frequency: Optional[str] = None
    drug_use: Optional[Literal["never", "former", "current"]] = None
    occupation: Optional[str] = None
    education_level: Optional[str] = None
    exercise_frequency: Optional[str] = None
    diet_type: Optional[str] = None
    living_situation: Optional[str] = None
    travel_history: Optional[List[dict]] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class VitalSigns(BaseModel):
    _id: str
    patient_id: str
    temperature: Optional[float] = None  # Celsius
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None  # beats per minute
    respiratory_rate: Optional[int] = None  # breaths per minute
    oxygen_saturation: Optional[float] = None  # percentage
    height: Optional[float] = None  # cm
    weight: Optional[float] = None  # kg
    pain_scale: Optional[int] = None  # 0-10
    measurement_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def bmi(self):
        """Calculate BMI based on height and weight."""
        if self.height and self.weight:
            return round(self.weight / ((self.height / 100) ** 2), 2)
        return None

    class Config:
        allow_population_by_field_name = True
