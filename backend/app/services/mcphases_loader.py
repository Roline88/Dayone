import os
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List
from app.services.patient_simulator import PatientSimulator
from app.services.triage_engine import ThresholdEvaluator, TriageLevel


class MCPhasesLoader:
    """Loads and prepares MCPhases dataset for training.

    MCPhases contains hormonal and physiological data, but lacks traditional vital signs.
    We augment it with synthetic patient data from PatientSimulator to create training labels
    based on threshold-based triage rules.
    """

    def __init__(self, data_dir: str = None):
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parent.parent.parent / "data"
        self.evaluator = ThresholdEvaluator()

    def generate_synthetic_training_data(self, num_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic patient data for training.

        Args:
            num_samples: Number of synthetic samples to generate

        Returns:
            Tuple of (features, labels) where:
                - features: (num_samples, 13) array of patient data
                - labels: (num_samples,) array of class labels (0=GREEN, 1=YELLOW, 2=RED)
        """
        features_list = []
        labels_list = []

        for _ in range(num_samples):
            vitals, tests = PatientSimulator.generate_random_patient()
            result = self.evaluator.evaluate(vitals, tests)

            features = np.array([
                vitals.systolic_bp,
                vitals.diastolic_bp,
                vitals.heart_rate,
                vitals.temperature,
                vitals.respiratory_rate,
                vitals.blood_glucose,
                vitals.blood_ph,
                vitals.bicarbonate,
                tests.urine_protein,
                tests.urine_glucose,
                tests.capillary_hemoglobin,
                tests.capillary_hematocrit,
                tests.blood_lactate,
            ], dtype=np.float32)

            label = self._triage_level_to_label(result.level)

            features_list.append(features)
            labels_list.append(label)

        features_array = np.array(features_list)
        labels_array = np.array(labels_list)

        return features_array, labels_array

    @staticmethod
    def _triage_level_to_label(level: TriageLevel) -> int:
        """Convert TriageLevel enum to numeric label."""
        level_map = {
            TriageLevel.GREEN: 0,
            TriageLevel.YELLOW: 1,
            TriageLevel.RED: 2,
        }
        return level_map[level]

    @staticmethod
    def _label_to_triage_level(label: int) -> TriageLevel:
        """Convert numeric label to TriageLevel enum."""
        label_map = {
            0: TriageLevel.GREEN,
            1: TriageLevel.YELLOW,
            2: TriageLevel.RED,
        }
        return label_map[label]

    def create_train_val_test_split(self, features: np.ndarray, labels: np.ndarray,
                                     train_ratio: float = 0.7,
                                     val_ratio: float = 0.15) -> Tuple[Tuple, Tuple, Tuple]:
        """Split data into train/val/test sets.

        Args:
            features: Feature array (num_samples, 13)
            labels: Label array (num_samples,)
            train_ratio: Fraction for training
            val_ratio: Fraction for validation (rest goes to test)

        Returns:
            Tuple of ((X_train, y_train), (X_val, y_val), (X_test, y_test))
        """
        num_samples = len(features)
        indices = np.random.permutation(num_samples)

        train_size = int(train_ratio * num_samples)
        val_size = int(val_ratio * num_samples)

        train_idx = indices[:train_size]
        val_idx = indices[train_size:train_size + val_size]
        test_idx = indices[train_size + val_size:]

        X_train, y_train = features[train_idx], labels[train_idx]
        X_val, y_val = features[val_idx], labels[val_idx]
        X_test, y_test = features[test_idx], labels[test_idx]

        return (X_train, y_train), (X_val, y_val), (X_test, y_test)

    def get_class_distribution(self, labels: np.ndarray) -> dict:
        """Get distribution of classes in dataset."""
        unique, counts = np.unique(labels, return_counts=True)
        distribution = {
            "GREEN": int(counts[unique == 0][0]) if 0 in unique else 0,
            "YELLOW": int(counts[unique == 1][0]) if 1 in unique else 0,
            "RED": int(counts[unique == 2][0]) if 2 in unique else 0,
        }
        return distribution
