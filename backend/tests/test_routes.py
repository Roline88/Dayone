"""Integration tests for FastAPI routes."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.routes import triage
from main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_ensemble_classifier():
    """Create mock ensemble classifier."""
    mock = Mock()
    mock.predict.return_value = {
        "level": "GREEN",
        "threshold_score": 0.95,
        "nn_score": 0.92,
        "ensemble_score": 0.94,
        "confidence": 0.94,
        "violations": {},
        "action_required": "Routine care - stable patient",
        "nn_proba": [0.7, 0.2, 0.1],
        "threshold_proba": [0.8, 0.15, 0.05],
        "ensemble_proba": [0.75, 0.18, 0.07],
    }
    return mock


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Clinical Triage System" in response.json()["message"]


def test_info_endpoint(client):
    """Test info endpoint."""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data
    assert "ensemble_config" in data


@patch('app.routes.triage.get_ensemble_classifier')
def test_triage_endpoint_success(mock_get_classifier, client, mock_ensemble_classifier):
    """Test successful triage prediction."""
    mock_get_classifier.return_value = mock_ensemble_classifier

    payload = {
        "vitals": {
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "heart_rate": 70,
            "temperature": 37.0,
            "respiratory_rate": 16,
            "blood_glucose": 100,
            "blood_ph": 7.40,
            "bicarbonate": 24,
        },
        "tests": {
            "urine_protein": 0.05,
            "urine_glucose": 0.0,
            "capillary_hemoglobin": 14.0,
            "capillary_hematocrit": 42,
            "blood_lactate": 1.0,
        }
    }

    response = client.post("/api/v1/triage", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["level"] == "GREEN"
    assert "threshold_score" in data
    assert "nn_score" in data
    assert "ensemble_score" in data
    assert "confidence" in data


@patch('app.routes.triage.get_ensemble_classifier')
def test_triage_endpoint_classifier_not_initialized(mock_get_classifier, client):
    """Test triage endpoint when classifier not initialized."""
    from fastapi import HTTPException
    mock_get_classifier.side_effect = HTTPException(status_code=503)

    payload = {
        "vitals": {
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "heart_rate": 70,
            "temperature": 37.0,
            "respiratory_rate": 16,
            "blood_glucose": 100,
            "blood_ph": 7.40,
            "bicarbonate": 24,
        },
        "tests": {
            "urine_protein": 0.05,
            "urine_glucose": 0.0,
            "capillary_hemoglobin": 14.0,
            "capillary_hematocrit": 42,
            "blood_lactate": 1.0,
        }
    }

    response = client.post("/api/v1/triage", json=payload)
    assert response.status_code == 503


@patch('app.routes.triage.get_ensemble_classifier')
def test_batch_triage_endpoint(mock_get_classifier, client, mock_ensemble_classifier):
    """Test batch triage endpoint."""
    mock_get_classifier.return_value = mock_ensemble_classifier

    payload = {
        "patients": [
            {
                "vitals": {
                    "systolic_bp": 120, "diastolic_bp": 80, "heart_rate": 70,
                    "temperature": 37.0, "respiratory_rate": 16, "blood_glucose": 100,
                    "blood_ph": 7.40, "bicarbonate": 24,
                },
                "tests": {
                    "urine_protein": 0.05, "urine_glucose": 0.0, "capillary_hemoglobin": 14.0,
                    "capillary_hematocrit": 42, "blood_lactate": 1.0,
                }
            },
            {
                "vitals": {
                    "systolic_bp": 145, "diastolic_bp": 95, "heart_rate": 105,
                    "temperature": 37.8, "respiratory_rate": 22, "blood_glucose": 180,
                    "blood_ph": 7.35, "bicarbonate": 20,
                },
                "tests": {
                    "urine_protein": 0.2, "urine_glucose": 0.3, "capillary_hemoglobin": 11.0,
                    "capillary_hematocrit": 34, "blood_lactate": 1.8,
                }
            }
        ]
    }

    response = client.post("/api/v1/batch-triage", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 2
    assert len(data["results"]) == 2
    assert "summary" in data


def test_triage_endpoint_invalid_input(client):
    """Test triage endpoint with invalid input."""
    payload = {
        "vitals": {
            "systolic_bp": "invalid",  # Should be int
            "diastolic_bp": 80,
            "heart_rate": 70,
            "temperature": 37.0,
            "respiratory_rate": 16,
            "blood_glucose": 100,
            "blood_ph": 7.40,
            "bicarbonate": 24,
        },
        "tests": {
            "urine_protein": 0.05,
            "urine_glucose": 0.0,
            "capillary_hemoglobin": 14.0,
            "capillary_hematocrit": 42,
            "blood_lactate": 1.0,
        }
    }

    response = client.post("/api/v1/triage", json=payload)
    assert response.status_code == 422  # Validation error
