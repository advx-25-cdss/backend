from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime, timezone

class Case(BaseModel):
    _id: str  # ObjectId
    patient_id: str
    case_number: str
    soap: str
    case_date: datetime
    transcriptions: Optional[str] = None
    status: Literal['open', 'closed', 'in_progress'] = 'open'
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class Test(BaseModel):
    _id: str # ObjectId
    case_id: str
    patient_id: str
    test_name: str
    test_date: datetime
    notes: Optional[str] = None
    results: Optional[List[dict]] = None  # Changed from Binary to dict for better JSON handling
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class Medicine(BaseModel):
    _id: str  # ObjectId
    case_id: str
    patient_id: str
    medicine_name: str
    dosage: str
    route: Literal['oral', 'topical', 'injection', 'inhalation']
    frequency: str
    start_date: datetime
    end_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class Diagnosis(BaseModel):
    _id: str  # ObjectId
    case_id: str
    patient_id: str
    diagnosis_name: str
    diagnosis_date: datetime
    status: Literal['active', 'resolved', 'recurrent']
    notes: Optional[str] = None
    follow_up: str
    additional_info: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True

class Treatment(BaseModel):
    _id: str  # ObjectId
    case_id: str
    patient_id: str
    treatment_name: str
    treatment_date: datetime
    treatment_type: Literal['medication', 'therapy', 'surgery', 'lifestyle_change']
    outcome: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        allow_population_by_field_name = True
