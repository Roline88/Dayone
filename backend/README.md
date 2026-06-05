# Clinical Triage System - Backend

Production-grade AI-powered clinical triage system using ensemble learning (neural network + threshold-based classification).

## Project Structure

```
backend/
├── main.py                           # FastAPI application entry point
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
│
├── app/
│   ├── __init__.py
│   ├── config.py                     # Configuration and environment variables
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── data_models.py            # Pydantic request/response schemas
│   │   └── nn_model.py               # PyTorch neural network architecture
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── triage_engine.py          # Threshold-based triage logic
│   │   ├── patient_simulator.py      # Synthetic patient data generation
│   │   ├── mcphases_loader.py        # MCPhases dataset loading and preparation
│   │   ├── nn_classifier.py          # Neural network inference wrapper
│   │   └── ensemble_classifier.py    # Combines NN + threshold predictions
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── triage.py                 # API endpoint definitions
│   │
│   ├── training/
│   │   ├── __init__.py
│   │   ├── dataset.py                # PyTorch Dataset class
│   │   ├── trainer.py                # Training loop with early stopping
│   │   └── train.py                  # Training script entry point
│   │
│   └── utils/
│       ├── __init__.py
│       └── preprocessing.py          # Feature scaling and normalization
│
├── tests/
│   ├── __init__.py
│   ├── test_triage_engine.py         # Threshold logic unit tests
│   ├── test_nn_classifier.py         # Neural network unit tests
│   ├── test_ensemble.py              # Ensemble classifier tests
│   └── test_routes.py                # FastAPI endpoint tests
│
└── models/
    └── triage_classifier.pt          # Trained model weights (generated)
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create or update `.env` file:
```env
DEBUG=False
MODEL_PATH=./models/triage_classifier.pt
MCPHASES_PATH=./data/mcphases
ENSEMBLE_NN_WEIGHT=0.6
ENSEMBLE_THRESHOLD_WEIGHT=0.4
```

## Training the Model

Train the neural network on synthetic data:

```bash
python -m app.training.train
```

This will:
- Generate 2000 synthetic patient samples using PatientSimulator
- Split into train (70%), validation (15%), test (15%)
- Normalize features using StandardScaler
- Train neural network with early stopping
- Save model weights to `models/triage_classifier.pt`
- Save scaler to `models/scaler.pkl`

Output:
```
Epoch 1/50 | Train Loss: 1.2345 | Val Loss: 1.1234 | Val Acc: 0.6543
Epoch 2/50 | Train Loss: 0.9876 | Val Loss: 0.8765 | Val Acc: 0.7234
...
Test Accuracy: 0.8912
```

## Running the API

Start the FastAPI server:

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Interactive API Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. Single Patient Triage

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{
    "vitals": {
      "systolic_bp": 120,
      "diastolic_bp": 80,
      "heart_rate": 70,
      "temperature": 37.0,
      "respiratory_rate": 16,
      "blood_glucose": 100,
      "blood_ph": 7.40,
      "bicarbonate": 24
    },
    "tests": {
      "urine_protein": 0.05,
      "urine_glucose": 0.0,
      "capillary_hemoglobin": 14.0,
      "capillary_hematocrit": 42,
      "blood_lactate": 1.0
    }
  }'
```

**Response:**
```json
{
  "level": "GREEN",
  "display_name": "GREEN Risk: Routine care - stable patient",
  "threshold_score": 1.0,
  "nn_score": 0.92,
  "ensemble_score": 0.97,
  "confidence": 0.97,
  "violations": {},
  "action_required": "Routine care - stable patient"
}
```

### 2. Batch Patient Triage

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/batch-triage \
  -H "Content-Type: application/json" \
  -d '{
    "patients": [
      { "vitals": {...}, "tests": {...} },
      { "vitals": {...}, "tests": {...} }
    ]
  }'
```

**Response:**
```json
{
  "total": 2,
  "results": [
    { "level": "GREEN", ... },
    { "level": "YELLOW", ... }
  ],
  "summary": {
    "GREEN": 1,
    "YELLOW": 1,
    "RED": 0
  }
}
```

### 3. Health Check

```bash
curl http://localhost:8000/api/v1/health
```

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### Specific Test File
```bash
pytest tests/test_triage_engine.py -v
pytest tests/test_nn_classifier.py -v
pytest tests/test_ensemble.py -v
pytest tests/test_routes.py -v
```

### With Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## Architecture

### Threshold-Based Classification
- **GREEN**: Normal vital signs (optimal ranges)
- **YELLOW**: Concerning but not critical (warning ranges)
- **RED**: Emergency/critical (danger ranges)

### Neural Network
- **Architecture**: 3-layer MLP
  - Input: 13 features (8 vitals + 5 tests)
  - Hidden: 64 → 32 → 16 neurons
  - Output: 3 classes (softmax)
- **Regularization**: Batch normalization, dropout (0.2)
- **Training**: Adam optimizer, early stopping

### Ensemble Strategy
- **NN Weight**: 0.6 (60%)
- **Threshold Weight**: 0.4 (40%)
- **Combination**: Weighted average of probability distributions
- **Benefit**: Combines data-driven learning with clinical expertise

## Features

### Vital Signs Monitored
- Systolic/Diastolic BP (mmHg)
- Heart Rate (bpm)
- Temperature (°C)
- Respiratory Rate (breaths/min)
- Blood Glucose (mg/dL)
- Blood pH
- Bicarbonate (mEq/L)

### Fluid Tests
- Urine Protein (g/dL)
- Urine Glucose (g/dL)
- Capillary Hemoglobin (g/dL)
- Capillary Hematocrit (%)
- Blood Lactate (mmol/L)

## Development

### Adding New Features

1. **Add validation thresholds** in `app/services/triage_engine.py`
2. **Update data models** in `app/models/data_models.py`
3. **Retrain model** with `python -m app.training.train`
4. **Update tests** in `tests/`

### Model Improvements

- Increase training data: Modify `num_samples` in `app/training/train.py`
- Adjust network architecture: Edit `app/models/nn_model.py`
- Change ensemble weights: Update `app/config.py`
- Try data augmentation: Expand `PatientSimulator` generators

## Performance Metrics

After training on 2000 synthetic samples:
- **Overall Accuracy**: ~89%
- **GREEN Accuracy**: ~91%
- **YELLOW Accuracy**: ~85%
- **RED Accuracy**: ~89%

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | False | Enable debug mode |
| `MODEL_PATH` | `./models/triage_classifier.pt` | Path to saved model |
| `MCPHASES_PATH` | `./data/mcphases` | MCPhases dataset path |
| `ENSEMBLE_NN_WEIGHT` | 0.6 | Weight for NN in ensemble |
| `ENSEMBLE_THRESHOLD_WEIGHT` | 0.4 | Weight for threshold in ensemble |

## Troubleshooting

### Model not loading
```
Error: FileNotFoundError: Model file not found
```
Solution: Run `python -m app.training.train` to generate the model first.

### CUDA not available
```
Using device: cpu
```
Solution: GPU optional; CPU training will work but be slower.

### Port already in use
```
OSError: [Errno 48] Address already in use
```
Solution: Use different port: `python main.py --port 8001`

## License

MIT
