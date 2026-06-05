from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple


class TriageLevel(Enum):
    GREEN = "Low Risk: Routine Care"
    YELLOW = "Moderate Risk: Urgent Referral"
    RED = "High Risk: Emergency Transport"


@dataclass
class PatientVitals:
    systolic_bp: int
    diastolic_bp: int
    heart_rate: int
    temperature: float
    respiratory_rate: int
    blood_glucose: float
    blood_ph: float
    bicarbonate: float


@dataclass
class FluidTests:
    urine_protein: float
    urine_glucose: float
    capillary_hemoglobin: float
    capillary_hematocrit: float
    blood_lactate: float


@dataclass
class TriageResult:
    level: TriageLevel
    score: float
    violations: Dict[str, list]
    action_required: str


class ThresholdEvaluator:
    """Evaluates patient vitals and tests against clinical thresholds."""

    RED_THRESHOLDS = {
        "systolic_bp": {"min": 90, "max": 180},
        "diastolic_bp": {"min": 60, "max": 120},
        "heart_rate": {"min": 40, "max": 140},
        "temperature": {"min": 35.5, "max": 39.5},
        "respiratory_rate": {"min": 8, "max": 30},
        "blood_glucose": {"min": 40, "max": 400},
        "blood_ph": {"min": 7.1, "max": 7.5},
        "bicarbonate": {"min": 15, "max": 30},
        "urine_protein": {"max": 0.5},
        "urine_glucose": {"max": 1.0},
        "capillary_hemoglobin": {"min": 7.0, "max": 20.0},
        "capillary_hematocrit": {"min": 20, "max": 60},
        "blood_lactate": {"max": 4.0},
    }

    YELLOW_THRESHOLDS = {
        "systolic_bp": {"min": 100, "max": 160},
        "diastolic_bp": {"min": 65, "max": 100},
        "heart_rate": {"min": 50, "max": 120},
        "temperature": {"min": 36.5, "max": 38.5},
        "respiratory_rate": {"min": 12, "max": 25},
        "blood_glucose": {"min": 70, "max": 250},
        "blood_ph": {"min": 7.25, "max": 7.40},
        "bicarbonate": {"min": 20, "max": 26},
        "urine_protein": {"max": 0.3},
        "urine_glucose": {"max": 0.5},
        "capillary_hemoglobin": {"min": 10.0, "max": 18.0},
        "capillary_hematocrit": {"min": 30, "max": 50},
        "blood_lactate": {"max": 2.0},
    }

    GREEN_THRESHOLDS = {
        "systolic_bp": {"min": 110, "max": 140},
        "diastolic_bp": {"min": 70, "max": 90},
        "heart_rate": {"min": 60, "max": 100},
        "temperature": {"min": 36.8, "max": 37.5},
        "respiratory_rate": {"min": 14, "max": 20},
        "blood_glucose": {"min": 90, "max": 130},
        "blood_ph": {"min": 7.35, "max": 7.45},
        "bicarbonate": {"min": 22, "max": 26},
        "urine_protein": {"max": 0.1},
        "urine_glucose": {"max": 0.1},
        "capillary_hemoglobin": {"min": 12.0, "max": 16.0},
        "capillary_hematocrit": {"min": 36, "max": 46},
        "blood_lactate": {"max": 1.5},
    }

    @staticmethod
    def _check_threshold(value: float, thresholds: Dict) -> bool:
        """Returns True if value is within thresholds."""
        if "min" in thresholds and value < thresholds["min"]:
            return False
        if "max" in thresholds and value > thresholds["max"]:
            return False
        return True

    @staticmethod
    def _get_violations(vitals: PatientVitals, tests: FluidTests, level_thresholds: Dict) -> Dict[str, list]:
        """Returns dict of violated parameters."""
        violations = {}

        patient_data = {
            "systolic_bp": vitals.systolic_bp,
            "diastolic_bp": vitals.diastolic_bp,
            "heart_rate": vitals.heart_rate,
            "temperature": vitals.temperature,
            "respiratory_rate": vitals.respiratory_rate,
            "blood_glucose": vitals.blood_glucose,
            "blood_ph": vitals.blood_ph,
            "bicarbonate": vitals.bicarbonate,
            "urine_protein": tests.urine_protein,
            "urine_glucose": tests.urine_glucose,
            "capillary_hemoglobin": tests.capillary_hemoglobin,
            "capillary_hematocrit": tests.capillary_hematocrit,
            "blood_lactate": tests.blood_lactate,
        }

        for param, value in patient_data.items():
            if param in level_thresholds:
                if not ThresholdEvaluator._check_threshold(value, level_thresholds[param]):
                    violations[param] = [value, level_thresholds[param]]

        return violations

    def evaluate(self, vitals: PatientVitals, tests: FluidTests) -> TriageResult:
        """Classify patient into triage level based on vital signs and tests.

        RED thresholds: Emergency danger signs
        YELLOW thresholds: Warnings/concerning
        GREEN thresholds: Normal/optimal
        """
        red_violations = self._get_violations(vitals, tests, self.RED_THRESHOLDS)
        if red_violations:
            red_score = max(0.1, 1 - (len(red_violations) / 13))
            return TriageResult(
                level=TriageLevel.RED,
                score=red_score,
                violations=red_violations,
                action_required="Emergency transport - critical condition"
            )

        yellow_violations = self._get_violations(vitals, tests, self.YELLOW_THRESHOLDS)
        if yellow_violations:
            yellow_score = 0.5 + (0.5 * (1 - min(len(yellow_violations) / 13, 1)))
            return TriageResult(
                level=TriageLevel.YELLOW,
                score=yellow_score,
                violations=yellow_violations,
                action_required="Urgent referral - monitor closely"
            )

        return TriageResult(
            level=TriageLevel.GREEN,
            score=1.0,
            violations={},
            action_required="Routine care - stable patient"
        )
