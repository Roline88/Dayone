"""FastAPI routes for triage endpoints."""

from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.data_models import (
    PatientVitalsRequest, FluidTestsRequest, PatientRequest,
    BatchTriageRequest, TriageOutcome, BatchTriageResponse, TriageViolation
)
from app.services.triage_engine import PatientVitals, FluidTests
from app.services.ensemble_classifier import EnsembleTriageClassifier

router = APIRouter(tags=["triage"])

# Global ensemble classifier (initialized on app startup)
_ensemble_classifier: EnsembleTriageClassifier = None


def set_ensemble_classifier(classifier: EnsembleTriageClassifier):
    """Set the global ensemble classifier."""
    global _ensemble_classifier
    _ensemble_classifier = classifier


def get_ensemble_classifier() -> EnsembleTriageClassifier:
    """Get the global ensemble classifier."""
    if _ensemble_classifier is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Triage classifier not initialized"
        )
    return _ensemble_classifier


@router.post("/triage", response_model=TriageOutcome)
async def triage_patient(vitals: PatientVitalsRequest, tests: FluidTestsRequest) -> TriageOutcome:
    """Classify a single patient into triage level.

    Returns:
        - level: GREEN (low risk), YELLOW (moderate risk), or RED (high risk)
        - threshold_score: Score from threshold-based classifier (0-1)
        - nn_score: Score from neural network classifier (0-1)
        - ensemble_score: Combined score (0-1)
        - confidence: Confidence in prediction (0-1)
        - violations: Parameters outside normal range
        - action_required: Recommended action
    """
    try:
        classifier = get_ensemble_classifier()

        vitals_obj = PatientVitals(
            systolic_bp=vitals.systolic_bp,
            diastolic_bp=vitals.diastolic_bp,
            heart_rate=vitals.heart_rate,
            temperature=vitals.temperature,
            respiratory_rate=vitals.respiratory_rate,
            blood_glucose=vitals.blood_glucose,
            blood_ph=vitals.blood_ph,
            bicarbonate=vitals.bicarbonate,
        )

        tests_obj = FluidTests(
            urine_protein=tests.urine_protein,
            urine_glucose=tests.urine_glucose,
            capillary_hemoglobin=tests.capillary_hemoglobin,
            capillary_hematocrit=tests.capillary_hematocrit,
            blood_lactate=tests.blood_lactate,
        )

        result = classifier.predict(vitals_obj, tests_obj)

        # Convert violations dict to Pydantic model
        violations_model = {}
        for param, (value, allowed_range) in result["violations"].items():
            violations_model[param] = TriageViolation(
                value=value,
                allowed_range=allowed_range
            )

        return TriageOutcome(
            level=result["level"],
            display_name=f"{result['level']} Risk: {result['action_required']}",
            threshold_score=result["threshold_score"],
            nn_score=result["nn_score"],
            ensemble_score=result["ensemble_score"],
            confidence=result["confidence"],
            violations=violations_model,
            action_required=result["action_required"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Triage prediction failed: {str(e)}"
        )


@router.post("/batch-triage", response_model=BatchTriageResponse)
async def batch_triage(batch: BatchTriageRequest) -> BatchTriageResponse:
    """Classify multiple patients at once.

    Args:
        batch: Request containing list of patients

    Returns:
        Results for all patients plus summary statistics
    """
    try:
        classifier = get_ensemble_classifier()
        results = []

        for patient in batch.patients:
            vitals_obj = PatientVitals(
                systolic_bp=patient.vitals.systolic_bp,
                diastolic_bp=patient.vitals.diastolic_bp,
                heart_rate=patient.vitals.heart_rate,
                temperature=patient.vitals.temperature,
                respiratory_rate=patient.vitals.respiratory_rate,
                blood_glucose=patient.vitals.blood_glucose,
                blood_ph=patient.vitals.blood_ph,
                bicarbonate=patient.vitals.bicarbonate,
            )

            tests_obj = FluidTests(
                urine_protein=patient.tests.urine_protein,
                urine_glucose=patient.tests.urine_glucose,
                capillary_hemoglobin=patient.tests.capillary_hemoglobin,
                capillary_hematocrit=patient.tests.capillary_hematocrit,
                blood_lactate=patient.tests.blood_lactate,
            )

            result = classifier.predict(vitals_obj, tests_obj)

            violations_model = {}
            for param, (value, allowed_range) in result["violations"].items():
                violations_model[param] = TriageViolation(
                    value=value,
                    allowed_range=allowed_range
                )

            outcome = TriageOutcome(
                level=result["level"],
                display_name=f"{result['level']} Risk: {result['action_required']}",
                threshold_score=result["threshold_score"],
                nn_score=result["nn_score"],
                ensemble_score=result["ensemble_score"],
                confidence=result["confidence"],
                violations=violations_model,
                action_required=result["action_required"]
            )
            results.append(outcome)

        # Compute summary
        summary = {
            "GREEN": sum(1 for r in results if r.level == "GREEN"),
            "YELLOW": sum(1 for r in results if r.level == "YELLOW"),
            "RED": sum(1 for r in results if r.level == "RED"),
        }

        return BatchTriageResponse(
            total=len(results),
            results=results,
            summary=summary
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch triage prediction failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        get_ensemble_classifier()
        return {"status": "healthy", "model_loaded": True}
    except HTTPException:
        return {"status": "unhealthy", "model_loaded": False}
