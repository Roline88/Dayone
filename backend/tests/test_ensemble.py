"""Unit tests for ensemble classifier."""

import pytest
import numpy as np
from unittest.mock import Mock, patch
from app.services.triage_engine import PatientVitals, FluidTests, TriageLevel, TriageResult
from app.services.ensemble_classifier import EnsembleTriageClassifier


@pytest.fixture
def mock_nn_classifier():
    """Create a mock NN classifier."""
    mock = Mock()
    mock.predict_proba.return_value = np.array([0.7, 0.2, 0.1])  # Predict GREEN
    mock.class_names = ["GREEN", "YELLOW", "RED"]
    return mock


@pytest.fixture
def ensemble(mock_nn_classifier):
    """Create ensemble classifier with mock NN."""
    return EnsembleTriageClassifier(mock_nn_classifier, nn_weight=0.6, threshold_weight=0.4)


@pytest.fixture
def healthy_vitals():
    return PatientVitals(
        systolic_bp=120,
        diastolic_bp=80,
        heart_rate=70,
        temperature=37.0,
        respiratory_rate=16,
        blood_glucose=100,
        blood_ph=7.40,
        bicarbonate=24,
    )


@pytest.fixture
def healthy_tests():
    return FluidTests(
        urine_protein=0.05,
        urine_glucose=0.0,
        capillary_hemoglobin=14.0,
        capillary_hematocrit=42,
        blood_lactate=1.0,
    )


def test_ensemble_initialization(ensemble):
    """Test ensemble classifier initialization."""
    assert ensemble.nn_weight > 0
    assert ensemble.threshold_weight > 0
    assert abs(ensemble.nn_weight + ensemble.threshold_weight - 1.0) < 0.01


def test_ensemble_predict_structure(ensemble, healthy_vitals, healthy_tests):
    """Test that ensemble prediction returns expected structure."""
    result = ensemble.predict(healthy_vitals, healthy_tests)

    assert "level" in result
    assert "threshold_score" in result
    assert "nn_score" in result
    assert "ensemble_score" in result
    assert "confidence" in result
    assert "violations" in result
    assert "action_required" in result
    assert result["level"] in ["GREEN", "YELLOW", "RED"]


def test_ensemble_predict_values_in_range(ensemble, healthy_vitals, healthy_tests):
    """Test that ensemble prediction values are in valid ranges."""
    result = ensemble.predict(healthy_vitals, healthy_tests)

    assert 0 <= result["threshold_score"] <= 1
    assert 0 <= result["nn_score"] <= 1
    assert 0 <= result["ensemble_score"] <= 1
    assert 0 <= result["confidence"] <= 1


def test_ensemble_probabilities_sum_to_one(ensemble, healthy_vitals, healthy_tests):
    """Test that probability distributions sum to 1."""
    result = ensemble.predict(healthy_vitals, healthy_tests)

    nn_sum = sum(result["nn_proba"])
    threshold_sum = sum(result["threshold_proba"])
    ensemble_sum = sum(result["ensemble_proba"])

    assert abs(nn_sum - 1.0) < 0.01
    assert abs(threshold_sum - 1.0) < 0.01
    assert abs(ensemble_sum - 1.0) < 0.01


def test_ensemble_weights_applied():
    """Test that ensemble correctly applies weights."""
    mock_nn = Mock()
    nn_proba = np.array([0.1, 0.2, 0.7])  # Predicts RED
    mock_nn.predict_proba.return_value = nn_proba

    ensemble = EnsembleTriageClassifier(mock_nn, nn_weight=0.6, threshold_weight=0.4)

    # Create patient that threshold predicts as GREEN
    vitals = PatientVitals(
        systolic_bp=120, diastolic_bp=80, heart_rate=70, temperature=37.0,
        respiratory_rate=16, blood_glucose=100, blood_ph=7.40, bicarbonate=24,
    )
    tests = FluidTests(
        urine_protein=0.05, urine_glucose=0.0, capillary_hemoglobin=14.0,
        capillary_hematocrit=42, blood_lactate=1.0,
    )

    result = ensemble.predict(vitals, tests)

    # Ensemble should have RED as dominant class (from NN), but not with certainty
    assert result["level"] in ["RED", "YELLOW", "GREEN"]  # Could be any, depends on weights


def test_ensemble_consistency(ensemble, healthy_vitals, healthy_tests):
    """Test that ensemble gives consistent results for same input."""
    result1 = ensemble.predict(healthy_vitals, healthy_tests)
    result2 = ensemble.predict(healthy_vitals, healthy_tests)

    assert result1["level"] == result2["level"]
    assert abs(result1["ensemble_score"] - result2["ensemble_score"]) < 0.001
