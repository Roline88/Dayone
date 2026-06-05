from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, Optional


class PatientVitalsRequest(BaseModel):
    systolic_bp: int = Field(..., ge=40, le=300, description="Systolic blood pressure (mmHg)")
    diastolic_bp: int = Field(..., ge=30, le=200, description="Diastolic blood pressure (mmHg)")
    heart_rate: int = Field(..., ge=30, le=200, description="Heart rate (bpm)")
    temperature: float = Field(..., ge=30.0, le=45.0, description="Temperature (°C)")
    respiratory_rate: int = Field(..., ge=5, le=60, description="Respiratory rate (breaths/min)")
    blood_glucose: float = Field(..., ge=10, le=600, description="Blood glucose (mg/dL)")
    blood_ph: float = Field(..., ge=6.5, le=8.0, description="Blood pH")
    bicarbonate: float = Field(..., ge=5, le=50, description="Bicarbonate (mEq/L)")


class FluidTestsRequest(BaseModel):
    urine_protein: float = Field(..., ge=0.0, le=10.0, description="Urine protein (g/dL)")
    urine_glucose: float = Field(..., ge=0.0, le=10.0, description="Urine glucose (g/dL)")
    capillary_hemoglobin: float = Field(..., ge=3.0, le=25.0, description="Capillary hemoglobin (g/dL)")
    capillary_hematocrit: int = Field(..., ge=10, le=80, description="Capillary hematocrit (%)")
    blood_lactate: float = Field(..., ge=0.0, le=20.0, description="Blood lactate (mmol/L)")


class TriageViolation(BaseModel):
    value: float
    allowed_range: Dict[str, float]


class TriageOutcome(BaseModel):
    level: Literal["GREEN", "YELLOW", "RED"]
    display_name: str
    threshold_score: float = Field(..., ge=0.0, le=1.0)
    nn_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    ensemble_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    violations: Dict[str, TriageViolation]
    action_required: str


class PatientRequest(BaseModel):
    vitals: PatientVitalsRequest
    tests: FluidTestsRequest


class BatchTriageRequest(BaseModel):
    patients: list[PatientRequest]


class BatchTriageResponse(BaseModel):
    total: int
    results: list[TriageOutcome]
    summary: Dict[str, int]
