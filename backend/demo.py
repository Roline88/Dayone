from triage_engine import ThresholdEvaluator, TriageLevel
from patient_simulator import PatientSimulator
import json


def print_patient_report(vitals, tests, result, patient_num=1):
    """Prints a formatted patient triage report."""
    print(f"\n{'='*70}")
    print(f"PATIENT #{patient_num} - TRIAGE REPORT")
    print(f"{'='*70}\n")

    print("VITAL SIGNS:")
    print(f"  BP: {vitals.systolic_bp}/{vitals.diastolic_bp} mmHg")
    print(f"  HR: {vitals.heart_rate} bpm")
    print(f"  Temp: {vitals.temperature}°C")
    print(f"  RR: {vitals.respiratory_rate} breaths/min")
    print(f"  Blood Glucose: {vitals.blood_glucose} mg/dL")
    print(f"  pH: {vitals.blood_ph}")
    print(f"  HCO3: {vitals.bicarbonate} mEq/L\n")

    print("FLUID TESTS:")
    print(f"  Urine Protein: {tests.urine_protein} g/dL")
    print(f"  Urine Glucose: {tests.urine_glucose} g/dL")
    print(f"  Hemoglobin: {tests.capillary_hemoglobin} g/dL")
    print(f"  Hematocrit: {tests.capillary_hematocrit}%")
    print(f"  Lactate: {tests.blood_lactate} mmol/L\n")

    # Traffic light output
    if result.level == TriageLevel.GREEN:
        symbol = "[GREEN]"
    elif result.level == TriageLevel.YELLOW:
        symbol = "[YELLOW]"
    else:
        symbol = "[RED]"

    print(f"TRIAGE OUTCOME: {symbol} {result.level.value}")
    print(f"Risk Score: {result.score:.2f}/1.0")
    print(f"Action: {result.action_required}\n")

    if result.violations:
        print("PARAMETERS OUT OF RANGE:")
        for param, (value, thresholds) in result.violations.items():
            print(f"  OUT OF RANGE - {param}: {value}")
            print(f"     Allowed Range: {thresholds}")
    else:
        print("All parameters within normal range")

    print(f"\n{'='*70}\n")


def run_demo(num_patients=5):
    """Runs a demo with simulated patients."""
    print("\n" + "="*70)
    print("CLINICAL TRIAGE SYSTEM - PATIENT SIMULATION DEMO")
    print("Using traffic light classification (Green/Yellow/Red)")
    print("="*70)

    evaluator = ThresholdEvaluator()
    results_summary = {
        "total": num_patients,
        "green": 0,
        "yellow": 0,
        "red": 0,
    }

    for i in range(num_patients):
        vitals, tests = PatientSimulator.generate_random_patient()
        result = evaluator.evaluate(vitals, tests)
        print_patient_report(vitals, tests, result, i + 1)

        if result.level == TriageLevel.GREEN:
            results_summary["green"] += 1
        elif result.level == TriageLevel.YELLOW:
            results_summary["yellow"] += 1
        else:
            results_summary["red"] += 1

    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total Patients: {results_summary['total']}")
    print(f"[GREEN] Low Risk: {results_summary['green']} ({results_summary['green']/num_patients*100:.1f}%)")
    print(f"[YELLOW] Moderate Risk: {results_summary['yellow']} ({results_summary['yellow']/num_patients*100:.1f}%)")
    print(f"[RED] High Risk: {results_summary['red']} ({results_summary['red']/num_patients*100:.1f}%)")
    print("="*70 + "\n")

    return results_summary


def run_specific_scenarios():
    """Runs specific patient scenarios for demonstration."""
    print("\n" + "="*70)
    print("CLINICAL TRIAGE SYSTEM - SPECIFIC SCENARIOS")
    print("="*70)

    evaluator = ThresholdEvaluator()

    print("\n[SCENARIO 1: HEALTHY PATIENT]")
    vitals, tests = PatientSimulator.generate_healthy_patient()
    result = evaluator.evaluate(vitals, tests)
    print_patient_report(vitals, tests, result, 1)

    print("\n[SCENARIO 2: MODERATE RISK PATIENT]")
    vitals, tests = PatientSimulator.generate_moderate_patient()
    result = evaluator.evaluate(vitals, tests)
    print_patient_report(vitals, tests, result, 2)

    print("\n[SCENARIO 3: CRITICAL PATIENT]")
    vitals, tests = PatientSimulator.generate_critical_patient()
    result = evaluator.evaluate(vitals, tests)
    print_patient_report(vitals, tests, result, 3)


if __name__ == "__main__":
    # Run demo with random patients
    run_demo(5)

    # Run specific scenarios
    run_specific_scenarios()
