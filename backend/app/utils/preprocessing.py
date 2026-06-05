import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple


class FeatureScaler:
    """Scales patient features for neural network input."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit(self, features: np.ndarray) -> None:
        """Fit scaler on training data."""
        self.scaler.fit(features)
        self.is_fitted = True

    def transform(self, features: np.ndarray) -> np.ndarray:
        """Transform features using fitted scaler."""
        if not self.is_fitted:
            raise ValueError("Scaler must be fitted before transforming")
        return self.scaler.transform(features)

    def fit_transform(self, features: np.ndarray) -> np.ndarray:
        """Fit scaler and transform in one step."""
        self.fit(features)
        return self.scaler.transform(features)

    def inverse_transform(self, features: np.ndarray) -> np.ndarray:
        """Reverse the scaling."""
        if not self.is_fitted:
            raise ValueError("Scaler must be fitted before inverse transforming")
        return self.scaler.inverse_transform(features)


def vitals_tests_to_features(systolic_bp, diastolic_bp, heart_rate, temperature,
                               respiratory_rate, blood_glucose, blood_ph, bicarbonate,
                               urine_protein, urine_glucose, capillary_hemoglobin,
                               capillary_hematocrit, blood_lactate) -> np.ndarray:
    """Convert patient vitals and tests to feature array."""
    features = np.array([
        systolic_bp,
        diastolic_bp,
        heart_rate,
        temperature,
        respiratory_rate,
        blood_glucose,
        blood_ph,
        bicarbonate,
        urine_protein,
        urine_glucose,
        capillary_hemoglobin,
        capillary_hematocrit,
        blood_lactate,
    ], dtype=np.float32)
    return features.reshape(1, -1)
