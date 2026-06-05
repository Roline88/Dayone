"""Neural network classifier wrapper for inference."""

import torch
import numpy as np
from pathlib import Path
from typing import Tuple
import pickle

from app.models.nn_model import TriageClassifier
from app.utils.preprocessing import FeatureScaler, vitals_tests_to_features


class NNTriageClassifier:
    """Wrapper for neural network inference."""

    def __init__(self, model_path: str, scaler_path: str = None, device: str = None):
        """Initialize classifier.

        Args:
            model_path: Path to saved model weights
            scaler_path: Path to saved feature scaler
            device: torch device (cpu or cuda)
        """
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        self.model = TriageClassifier()
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        self.scaler = None
        if scaler_path and Path(scaler_path).exists():
            with open(scaler_path, "rb") as f:
                self.scaler = pickle.load(f)

        self.class_names = ["GREEN", "YELLOW", "RED"]

    def predict_proba(self, vitals_dict: dict, tests_dict: dict) -> np.ndarray:
        """Get probability predictions.

        Args:
            vitals_dict: Dict with keys: systolic_bp, diastolic_bp, heart_rate, etc.
            tests_dict: Dict with keys: urine_protein, urine_glucose, etc.

        Returns:
            Probabilities for each class (3,)
        """
        features = vitals_tests_to_features(
            vitals_dict["systolic_bp"],
            vitals_dict["diastolic_bp"],
            vitals_dict["heart_rate"],
            vitals_dict["temperature"],
            vitals_dict["respiratory_rate"],
            vitals_dict["blood_glucose"],
            vitals_dict["blood_ph"],
            vitals_dict["bicarbonate"],
            tests_dict["urine_protein"],
            tests_dict["urine_glucose"],
            tests_dict["capillary_hemoglobin"],
            tests_dict["capillary_hematocrit"],
            tests_dict["blood_lactate"],
        )

        if self.scaler:
            features = self.scaler.transform(features)

        features_tensor = torch.from_numpy(features).float().to(self.device)

        with torch.no_grad():
            probabilities = self.model.predict_proba(features_tensor)
            probabilities = probabilities.cpu().numpy()[0]

        return probabilities

    def predict(self, vitals_dict: dict, tests_dict: dict) -> Tuple[str, float]:
        """Get class prediction.

        Args:
            vitals_dict: Patient vitals
            tests_dict: Patient fluid tests

        Returns:
            Tuple of (class_name, confidence)
        """
        probabilities = self.predict_proba(vitals_dict, tests_dict)
        class_idx = np.argmax(probabilities)
        confidence = probabilities[class_idx]

        return self.class_names[class_idx], confidence
