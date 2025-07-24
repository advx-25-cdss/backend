# EHR System - Electronic Health Records CRUD API

A comprehensive Electronic Health Records (EHR) system built with FastAPI and MongoDB, featuring full CRUD operations for multiple medical collections.

## 🏥 Features

### Complete EHR Collections
- **Demographics** - Patient basic information and contact details
- **Menstrual History** - Menstrual cycle tracking and reproductive health
- **Obstetric History** - Pregnancy and delivery history (Gravida, Para, etc.)
- **Marital Status** - Marital information and family dynamics
- **History of Present Illness** - Current medical complaints and symptoms
- **Past Medical History** - Previous conditions, surgeries, and hospitalizations
- **Family History** - Genetic predispositions and family medical history
- **Medication History** - Current and past medications, adherence tracking
- **Allergy History** - Drug, food, and environmental allergies
- **Social History** - Lifestyle factors (smoking, alcohol, occupation)
- **Vital Signs** - Physical measurements and vital parameters

### CRUD Operations
Each collection supports:
- ✅ **Create** - Add new records
- ✅ **Read** - Get by ID, patient ID, or list all with pagination
- ✅ **Update** - Modify existing records
- ✅ **Delete** - Remove records

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (local or Atlas)

### Installation

1. **Clone and navigate to the backend directory**
```bash
cd backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your MongoDB connection string
```

4. **Start the server**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📋 API Endpoints

### Base Endpoints
- `GET /` - API status
- `GET /health` - Health check

### EHR Endpoints Pattern
Each collection follows the same REST pattern:

```
POST   /api/ehr/{collection}/                    # Create record
GET    /api/ehr/{collection}/{record_id}         # Get by ID
GET    /api/ehr/{collection}/patient/{patient_id} # Get by patient
GET    /api/ehr/{collection}/?skip=0&limit=100   # List with pagination
PUT    /api/ehr/{collection}/{record_id}         # Update record
DELETE /api/ehr/{collection}/{record_id}         # Delete record
```

### Available Collections
- `demographics`
- `menstrual`
- `obstetric`
- `marital`
- `history-present-illness`
- `past-medical-history`
- `family-history`
- `medication-history`
- `allergy-history`
- `social-history`
- `vital-signs`

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Make sure the server is running first
python main.py

# In another terminal, run tests
python test_ehr_system.py
```

The test covers:
- Health checks
- CRUD operations for multiple collections
- Patient-specific record retrieval
- Pagination functionality

## 📊 Example Usage

### Create a Demographics Record
```bash
curl -X POST "http://localhost:8000/api/ehr/demographics/" \
-H "Content-Type: application/json" \
-d '{
  "patient_id": "PATIENT001",
  "first_name": "Jane",
  "last_name": "Doe",
  "date_of_birth": "1990-05-15",
  "gender": "female",
  "phone": "+1234567890",
  "email": "jane.doe@email.com"
}'
```

### Get All Records for a Patient
```bash
curl "http://localhost:8000/api/ehr/demographics/patient/PATIENT001"
```

### Create Vital Signs
```bash
curl -X POST "http://localhost:8000/api/ehr/vital-signs/" \
-H "Content-Type: application/json" \
-d '{
  "patient_id": "PATIENT001",
  "blood_pressure_systolic": 120,
  "blood_pressure_diastolic": 80,
  "heart_rate": 72,
  "temperature": 98.6,
  "oxygen_saturation": 98
}'
```

## 🏗️ Architecture

### Project Structure
```
backend/
├── main.py                 # FastAPI app and router setup
├── database.py            # MongoDB connection setup
├── settings.py            # Environment configuration
├── requirements.txt       # Python dependencies
├── test_ehr_system.py    # Comprehensive tests
├── models/
│   └── ehr_models.py     # Pydantic models for all collections
├── services/
│   └── ehr_service.py    # Database service layer
└── routers/ehr/
    ├── demographics_router.py
    ├── menstrual_router.py
    ├── obstetric_router.py
    ├── marital_router.py
    ├── history_present_illness_router.py
    ├── past_medical_history_router.py
    ├── family_history_router.py
    ├── medication_history_router.py
    ├── allergy_history_router.py
    ├── social_history_router.py
    └── vital_signs_router.py
```

### Technology Stack
- **FastAPI** - Modern Python web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation and serialization
- **MongoDB** - NoSQL database for flexible medical records
- **Python-dotenv** - Environment variable management

## 🔧 Configuration

### Environment Variables (.env)
```env
MONGODB_URI=mongodb://localhost:27017
DEBUG=True
LOG_LEVEL=INFO
```

### MongoDB Collections
The system automatically creates these collections:
- `demographics`
- `menstrual`
- `obstetric`
- `marital`
- `history_present_illness`
- `past_medical_history`
- `family_history`
- `medication_history`
- `allergy_history`
- `social_history`
- `vital_signs`

## 🚑 Medical Data Models

### Demographics
- Patient ID, name, contact info
- Date of birth, gender
- Emergency contacts, insurance

### Menstrual History
- Last menstrual period, cycle length
- Flow details, contraceptive methods
- Menopause status

### Obstetric History
- Gravida, Para, Abortions
- Pregnancy history, delivery methods
- Current pregnancy status

### Vital Signs
- Blood pressure, heart rate
- Temperature, oxygen saturation
- Height, weight, BMI, pain scale

### Medical Histories
- Past conditions, surgeries
- Family medical history
- Current/past medications
- Known allergies and reactions

## 🔒 Security Considerations

- Input validation with Pydantic
- MongoDB injection prevention
- CORS configuration for web clients
- Timezone-aware datetime handling

## 📈 Scalability Features

- Async/await for high concurrency
- Connection pooling with Motor
- Pagination for large datasets
- Modular router architecture

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This is a mock EHR system for development purposes. For production medical applications, ensure compliance with HIPAA, GDPR, and other relevant healthcare data regulations.
