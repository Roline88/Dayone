from dataclasses import asdict, dataclass
from triage_engine import PatientVitals, FluidTests, ThresholdEvaluator, TriageResult
from patient_simulator import PatientSimulator
import json
from typing import Dict, Any


@dataclass
class PatientReportJSON:
    patient_id: int
    vitals: Dict[str, Any]
    tests: Dict[str, Any]
    triage_result: Dict[str, Any]


def patient_to_json(vitals: PatientVitals, tests: FluidTests, result: TriageResult, patient_id: int = 1) -> Dict[str, Any]:
    """Convert patient data and result to JSON-serializable dict."""
    return {
        "patient_id": patient_id,
        "vitals": {
            "systolic_bp": vitals.systolic_bp,
            "diastolic_bp": vitals.diastolic_bp,
            "heart_rate": vitals.heart_rate,
            "temperature": vitals.temperature,
            "respiratory_rate": vitals.respiratory_rate,
            "blood_glucose": vitals.blood_glucose,
            "blood_ph": vitals.blood_ph,
            "bicarbonate": vitals.bicarbonate,
        },
        "fluid_tests": {
            "urine_protein": tests.urine_protein,
            "urine_glucose": tests.urine_glucose,
            "capillary_hemoglobin": tests.capillary_hemoglobin,
            "capillary_hematocrit": tests.capillary_hematocrit,
            "blood_lactate": tests.blood_lactate,
        },
        "triage_outcome": {
            "level": result.level.name,
            "display_name": result.level.value,
            "risk_score": round(result.score, 3),
            "action_required": result.action_required,
            "violations": {
                param: {"value": value, "allowed_range": thresholds}
                for param, (value, thresholds) in result.violations.items()
            }
        }
    }


def generate_test_batch(count: int = 10) -> str:
    """Generate a batch of test patients and return as JSON."""
    evaluator = ThresholdEvaluator()
    patients = []

    for i in range(count):
        vitals, tests = PatientSimulator.generate_random_patient()
        result = evaluator.evaluate(vitals, tests)
        patient_data = patient_to_json(vitals, tests, result, i + 1)
        patients.append(patient_data)

    output = {
        "generated_at": "2026-06-05T00:00:00Z",
        "total_patients": count,
        "patients": patients,
        "summary": {
            "green": sum(1 for p in patients if p["triage_outcome"]["level"] == "GREEN"),
            "yellow": sum(1 for p in patients if p["triage_outcome"]["level"] == "YELLOW"),
            "red": sum(1 for p in patients if p["triage_outcome"]["level"] == "RED"),
        }
    }

    return json.dumps(output, indent=2)


if __name__ == "__main__":
    batch_json = generate_test_batch(10)
    print(batch_json)

    with open("patient_batch_output.json", "w") as f:
        f.write(batch_json)
    print("\n✓ Saved to patient_batch_output.json")
