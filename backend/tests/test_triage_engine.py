"""Unit tests for threshold-based triage engine."""

import pytest
from app.services.triage_engine import (
    PatientVitals, FluidTests, ThresholdEvaluator, TriageLevel
)


@pytest.fixture
def evaluator():
    return ThresholdEvaluator()


@pytest.fixture
def healthy_patient():
    vitals = PatientVitals(
        systolic_bp=120,
        diastolic_bp=80,
        heart_rate=70,
        temperature=37.0,
        respiratory_rate=16,
        blood_glucose=100,
        blood_ph=7.40,
        bicarbonate=24,
    )
    tests = FluidTests(
        urine_protein=0.05,
        urine_glucose=0.0,
        capillary_hemoglobin=14.0,
        capillary_hematocrit=42,
        blood_lactate=1.0,
    )
    return vitals, tests


@pytest.fixture
def moderate_patient():
    vitals = PatientVitals(
        systolic_bp=165,  # Above YELLOW max (160)
        diastolic_bp=105,  # Above YELLOW max (100)
        heart_rate=125,  # Above YELLOW max (120)
        temperature=38.8,  # Above YELLOW max (38.5)
        respiratory_rate=26,  # Above YELLOW max (25)
        blood_glucose=260,  # Above YELLOW max (250)
        blood_ph=7.20,  # Below YELLOW min (7.25)
        bicarbonate=19,  # Below YELLOW min (20)
    )
    tests = FluidTests(
        urine_protein=0.4,  # Above YELLOW max (0.3)
        urine_glucose=0.6,  # Above YELLOW max (0.5)
        capillary_hemoglobin=9.5,  # Below YELLOW min (10.0)
        capillary_hematocrit=29,  # Below YELLOW min (30)
        blood_lactate=2.2,  # Above YELLOW max (2.0)
    )
    return vitals, tests


@pytest.fixture
def critical_patient():
    vitals = PatientVitals(
        systolic_bp=90,
        diastolic_bp=55,
        heart_rate=135,
        temperature=39.2,
        respiratory_rate=32,
        blood_glucose=350,
        blood_ph=7.18,
        bicarbonate=16,
    )
    tests = FluidTests(
        urine_protein=0.6,
        urine_glucose=1.5,
        capillary_hemoglobin=8.0,
        capillary_hematocrit=25,
        blood_lactate=5.0,
    )
    return vitals, tests


def test_healthy_patient_classification(evaluator, healthy_patient):
    """Test that healthy patient is classified as GREEN."""
    vitals, tests = healthy_patient
    result = evaluator.evaluate(vitals, tests)
    assert result.level == TriageLevel.GREEN
    assert result.score == 1.0
    assert len(result.violations) == 0


def test_moderate_patient_classification(evaluator, moderate_patient):
    """Test that moderate patient is classified as YELLOW."""
    vitals, tests = moderate_patient
    result = evaluator.evaluate(vitals, tests)
    assert result.level == TriageLevel.YELLOW
    assert result.score > 0
    assert len(result.violations) > 0


def test_critical_patient_classification(evaluator, critical_patient):
    """Test that critical patient is classified as RED."""
    vitals, tests = critical_patient
    result = evaluator.evaluate(vitals, tests)
    assert result.level == TriageLevel.RED
    assert len(result.violations) > 0


def test_violations_detected(evaluator):
    """Test that violations are correctly identified."""
    vitals = PatientVitals(
        systolic_bp=95,  # Below RED min (90 is ok, but 95 is upper)
        diastolic_bp=150,  # Way above RED max (120)
        heart_rate=150,  # Above RED max (140)
        temperature=40.0,  # Above RED max (39.5)
        respiratory_rate=35,  # Above RED max (30)
        blood_glucose=450,  # Above RED max (400)
        blood_ph=7.08,  # Below RED min (7.1)
        bicarbonate=12,  # Below RED min (15)
    )
    tests = FluidTests(
        urine_protein=1.0,  # Above RED max (0.5)
        urine_glucose=2.0,  # Above RED max (1.0)
        capillary_hemoglobin=6.0,  # Below RED min (7.0)
        capillary_hematocrit=18,  # Below RED min (20)
        blood_lactate=6.0,  # Above RED max (4.0)
    )

    result = evaluator.evaluate(vitals, tests)
    assert result.level == TriageLevel.RED
    assert len(result.violations) > 0


def test_boundary_values():
    """Test edge cases at threshold boundaries."""
    evaluator = ThresholdEvaluator()

    # Test values that violate YELLOW but not RED (should be YELLOW)
    vitals = PatientVitals(
        systolic_bp=165,  # Above YELLOW max (160), within RED (90-180)
        diastolic_bp=105,  # Above YELLOW max (100), within RED (60-120)
        heart_rate=125,  # Above YELLOW max (120), within RED (40-140)
        temperature=37.0,  # Within YELLOW
        respiratory_rate=20,  # Within YELLOW
        blood_glucose=100,  # Within YELLOW
        blood_ph=7.40,  # Within YELLOW
        bicarbonate=24,  # Within YELLOW
    )
    tests = FluidTests(
        urine_protein=0.05,  # Within YELLOW
        urine_glucose=0.0,  # Within YELLOW
        capillary_hemoglobin=14.0,  # Within YELLOW
        capillary_hematocrit=40,  # Within YELLOW
        blood_lactate=1.0,  # Within YELLOW
    )
    result = evaluator.evaluate(vitals, tests)
    assert result.level == TriageLevel.YELLOW
