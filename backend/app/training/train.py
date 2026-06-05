"""Training script for triage classifier model."""

import torch
from torch.utils.data import DataLoader
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.config import (
    MODEL_PATH, NN_INPUT_SIZE, NN_HIDDEN_SIZE, NN_NUM_CLASSES,
    NN_DROPOUT, NN_LEARNING_RATE, NN_BATCH_SIZE, NN_EPOCHS, NN_EARLY_STOPPING_PATIENCE
)
from app.models.nn_model import TriageClassifier
from app.training.trainer import TriageTrainer
from app.training.dataset import TriageDataset
from app.services.mcphases_loader import MCPhasesLoader
from app.utils.preprocessing import FeatureScaler


def main():
    print("=" * 70)
    print("TRIAGE CLASSIFIER TRAINING")
    print("=" * 70)

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\nUsing device: {device}")

    # Load and prepare data
    print("\n[1/5] Loading and preparing data...")
    loader = MCPhasesLoader()
    features, labels = loader.generate_synthetic_training_data(num_samples=2000)
    print(f"Generated {len(features)} samples")

    distribution = loader.get_class_distribution(labels)
    print(f"Class distribution: {distribution}")

    # Split data
    print("\n[2/5] Splitting data into train/val/test...")
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = loader.create_train_val_test_split(
        features, labels, train_ratio=0.7, val_ratio=0.15
    )
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

    # Normalize features
    print("\n[3/5] Normalizing features...")
    scaler = FeatureScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # Create datasets and dataloaders
    train_dataset = TriageDataset(X_train_scaled, y_train)
    val_dataset = TriageDataset(X_val_scaled, y_val)
    test_dataset = TriageDataset(X_test_scaled, y_test)

    train_loader = DataLoader(train_dataset, batch_size=NN_BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=NN_BATCH_SIZE)
    test_loader = DataLoader(test_dataset, batch_size=NN_BATCH_SIZE)

    # Initialize model
    print("\n[4/5] Initializing model...")
    model = TriageClassifier(
        input_size=NN_INPUT_SIZE,
        hidden_size=NN_HIDDEN_SIZE,
        num_classes=NN_NUM_CLASSES,
        dropout=NN_DROPOUT
    )
    print(f"Model architecture:\n{model}")

    # Train model
    print("\n[5/5] Training model...")
    trainer = TriageTrainer(model, device=device)
    history = trainer.train(
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=NN_EPOCHS,
        learning_rate=NN_LEARNING_RATE,
        patience=NN_EARLY_STOPPING_PATIENCE
    )

    # Evaluate on test set
    print("\n[EVALUATION] Evaluating on test set...")
    test_results = trainer.evaluate(test_loader)
    print(f"Test Accuracy: {test_results['overall_accuracy']:.4f}")
    print(f"Per-class Accuracy: {test_results['per_class_accuracy']}")

    # Save model
    print(f"\n[SAVE] Saving model to {MODEL_PATH}...")
    Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print("✓ Model saved successfully")

    # Save scaler
    scaler_path = Path(MODEL_PATH).parent / "scaler.pkl"
    import pickle
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
    print(f"✓ Scaler saved to {scaler_path}")

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
