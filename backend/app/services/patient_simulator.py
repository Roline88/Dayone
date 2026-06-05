import random
from typing import List, Tuple
from app.services.triage_engine import PatientVitals, FluidTests


class PatientSimulator:
    """Generates realistic patient vital signs and test results."""

    @staticmethod
    def generate_healthy_patient() -> Tuple[PatientVitals, FluidTests]:
        """Generates a healthy patient with normal vital signs."""
        vitals = PatientVitals(
            systolic_bp=random.randint(110, 135),
            diastolic_bp=random.randint(70, 85),
            heart_rate=random.randint(60, 85),
            temperature=round(random.uniform(36.8, 37.2), 1),
            respiratory_rate=random.randint(14, 18),
            blood_glucose=random.randint(95, 120),
            blood_ph=round(random.uniform(7.38, 7.42), 2),
            bicarbonate=random.randint(23, 25),
        )
        tests = FluidTests(
            urine_protein=round(random.uniform(0, 0.05), 2),
            urine_glucose=0.0,
            capillary_hemoglobin=round(random.uniform(13, 15), 1),
            capillary_hematocrit=random.randint(38, 44),
            blood_lactate=round(random.uniform(0.5, 1.2), 1),
        )
        return vitals, tests

    @staticmethod
    def generate_moderate_patient() -> Tuple[PatientVitals, FluidTests]:
        """Generates a patient with moderate symptoms/anomalies."""
        vitals = PatientVitals(
            systolic_bp=random.randint(135, 155),
            diastolic_bp=random.randint(85, 100),
            heart_rate=random.randint(100, 120),
            temperature=round(random.uniform(37.5, 38.2), 1),
            respiratory_rate=random.randint(20, 25),
            blood_glucose=random.randint(140, 200),
            blood_ph=round(random.uniform(7.32, 7.38), 2),
            bicarbonate=random.randint(20, 23),
        )
        tests = FluidTests(
            urine_protein=round(random.uniform(0.1, 0.25), 2),
            urine_glucose=round(random.uniform(0, 0.5), 1),
            capillary_hemoglobin=round(random.uniform(10, 12.5), 1),
            capillary_hematocrit=random.randint(32, 38),
            blood_lactate=round(random.uniform(1.5, 2.5), 1),
        )
        return vitals, tests

    @staticmethod
    def generate_critical_patient() -> Tuple[PatientVitals, FluidTests]:
        """Generates a patient in critical condition."""
        vitals = PatientVitals(
            systolic_bp=random.randint(85, 100),
            diastolic_bp=random.randint(50, 65),
            heart_rate=random.randint(130, 160),
            temperature=round(random.uniform(38.5, 40.5), 1),
            respiratory_rate=random.randint(28, 40),
            blood_glucose=random.randint(250, 450),
            blood_ph=round(random.uniform(7.1, 7.25), 2),
            bicarbonate=random.randint(12, 18),
        )
        tests = FluidTests(
            urine_protein=round(random.uniform(0.5, 1.0), 2),
            urine_glucose=round(random.uniform(1.0, 3.0), 1),
            capillary_hemoglobin=round(random.uniform(7, 9), 1),
            capillary_hematocrit=random.randint(20, 30),
            blood_lactate=round(random.uniform(4.0, 8.0), 1),
        )
        return vitals, tests

    @staticmethod
    def generate_random_patient() -> Tuple[PatientVitals, FluidTests]:
        """Generates a patient with random vital signs."""
        choice = random.choice(["healthy", "moderate", "critical"])
        if choice == "healthy":
            return PatientSimulator.generate_healthy_patient()
        elif choice == "moderate":
            return PatientSimulator.generate_moderate_patient()
        else:
            return PatientSimulator.generate_critical_patient()

    @staticmethod
    def generate_batch(count: int, patient_type: str = "random") -> List[Tuple[PatientVitals, FluidTests]]:
        """Generates a batch of patient records."""
        batch = []
        for _ in range(count):
            if patient_type == "healthy":
                batch.append(PatientSimulator.generate_healthy_patient())
            elif patient_type == "moderate":
                batch.append(PatientSimulator.generate_moderate_patient())
            elif patient_type == "critical":
                batch.append(PatientSimulator.generate_critical_patient())
            else:
                batch.append(PatientSimulator.generate_random_patient())
        return batch
