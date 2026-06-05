"""Ensemble classifier combining neural network and threshold-based approaches."""

import numpy as np
from typing import Tuple, Dict, Any

from app.services.triage_engine import (
    PatientVitals, FluidTests, ThresholdEvaluator, TriageLevel, TriageResult
)
from app.services.nn_classifier import NNTriageClassifier


class EnsembleTriageClassifier:
    """Combines NN and threshold-based predictions."""

    def __init__(self, nn_classifier: NNTriageClassifier, nn_weight: float = 0.6,
                 threshold_weight: float = 0.4):
        """Initialize ensemble.

        Args:
            nn_classifier: Trained neural network classifier
            nn_weight: Weight for NN predictions (0-1)
            threshold_weight: Weight for threshold predictions (0-1)
        """
        self.nn_classifier = nn_classifier
        self.threshold_evaluator = ThresholdEvaluator()

        # Normalize weights
        total = nn_weight + threshold_weight
        self.nn_weight = nn_weight / total
        self.threshold_weight = threshold_weight / total

        self.class_names = ["GREEN", "YELLOW", "RED"]
        self.class_to_idx = {name: i for i, name in enumerate(self.class_names)}

    def predict(self, vitals: PatientVitals, tests: FluidTests) -> Dict[str, Any]:
        """Predict triage level using ensemble.

        Args:
            vitals: Patient vitals
            tests: Fluid tests

        Returns:
            Dictionary with ensemble prediction and component predictions
        """
        # Get threshold-based prediction
        threshold_result = self.threshold_evaluator.evaluate(vitals, tests)
        threshold_proba = self._triage_result_to_proba(threshold_result)
        threshold_score = threshold_result.score

        # Get NN prediction
        vitals_dict = {
            "systolic_bp": vitals.systolic_bp,
            "diastolic_bp": vitals.diastolic_bp,
            "heart_rate": vitals.heart_rate,
            "temperature": vitals.temperature,
            "respiratory_rate": vitals.respiratory_rate,
            "blood_glucose": vitals.blood_glucose,
            "blood_ph": vitals.blood_ph,
            "bicarbonate": vitals.bicarbonate,
        }
        tests_dict = {
            "urine_protein": tests.urine_protein,
            "urine_glucose": tests.urine_glucose,
            "capillary_hemoglobin": tests.capillary_hemoglobin,
            "capillary_hematocrit": tests.capillary_hematocrit,
            "blood_lactate": tests.blood_lactate,
        }

        nn_proba = self.nn_classifier.predict_proba(vitals_dict, tests_dict)
        nn_score = np.max(nn_proba)

        # Combine predictions
        ensemble_proba = (self.nn_weight * nn_proba +
                         self.threshold_weight * threshold_proba)

        ensemble_level_idx = np.argmax(ensemble_proba)
        ensemble_level = self.class_names[ensemble_level_idx]
        ensemble_score = np.max(ensemble_proba)
        confidence = ensemble_proba[ensemble_level_idx]

        return {
            "level": ensemble_level,
            "threshold_score": float(threshold_score),
            "nn_score": float(nn_score),
            "ensemble_score": float(ensemble_score),
            "confidence": float(confidence),
            "violations": threshold_result.violations,
            "action_required": threshold_result.action_required,
            "nn_proba": nn_proba.tolist(),
            "threshold_proba": threshold_proba.tolist(),
            "ensemble_proba": ensemble_proba.tolist(),
        }

    def _triage_result_to_proba(self, result: TriageResult) -> np.ndarray:
        """Convert TriageResult to probability distribution.

        Uses the score to create a pseudo-probability that favors the predicted class.
        """
        level_idx = self.class_to_idx[result.level.name]
        proba = np.zeros(3)

        if result.level == TriageLevel.GREEN:
            proba[0] = result.score
            proba[1] = (1 - result.score) * 0.7
            proba[2] = (1 - result.score) * 0.3
        elif result.level == TriageLevel.YELLOW:
            proba[0] = (1 - result.score) * 0.3
            proba[1] = result.score
            proba[2] = (1 - result.score) * 0.7
        else:  # RED
            proba[0] = (1 - result.score) * 0.1
            proba[1] = (1 - result.score) * 0.3
            proba[2] = result.score

        return proba / proba.sum()
