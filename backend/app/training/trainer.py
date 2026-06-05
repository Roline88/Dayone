import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from app.models.nn_model import TriageClassifier
import numpy as np


class TriageTrainer:
    """Trainer for TriageClassifier neural network."""

    def __init__(self, model: TriageClassifier, device: torch.device = None):
        self.model = model
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def train_epoch(self, train_loader: DataLoader, optimizer: optim.Optimizer, criterion: nn.Module) -> float:
        """Train one epoch.

        Returns:
            Average loss for the epoch
        """
        self.model.train()
        total_loss = 0.0

        for features, labels in train_loader:
            features, labels = features.to(self.device), labels.to(self.device)

            optimizer.zero_grad()
            logits = self.model(features)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        return total_loss / len(train_loader)

    def validate(self, val_loader: DataLoader, criterion: nn.Module) -> tuple:
        """Validate on validation set.

        Returns:
            Tuple of (average_loss, accuracy)
        """
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for features, labels in val_loader:
                features, labels = features.to(self.device), labels.to(self.device)

                logits = self.model(features)
                loss = criterion(logits, labels)
                total_loss += loss.item()

                predictions = torch.argmax(logits, dim=1)
                correct += (predictions == labels).sum().item()
                total += labels.size(0)

        avg_loss = total_loss / len(val_loader)
        accuracy = correct / total
        return avg_loss, accuracy

    def train(self, train_loader: DataLoader, val_loader: DataLoader,
              num_epochs: int = 50, learning_rate: float = 0.001,
              patience: int = 5) -> dict:
        """Full training loop with early stopping.

        Args:
            train_loader: DataLoader for training set
            val_loader: DataLoader for validation set
            num_epochs: Maximum number of epochs
            learning_rate: Learning rate for optimizer
            patience: Number of epochs without improvement before stopping

        Returns:
            Dictionary with training history
        """
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

        history = {
            "train_loss": [],
            "val_loss": [],
            "val_accuracy": [],
        }

        best_val_loss = float("inf")
        epochs_without_improvement = 0

        for epoch in range(num_epochs):
            train_loss = self.train_epoch(train_loader, optimizer, criterion)
            val_loss, val_accuracy = self.validate(val_loader, criterion)

            history["train_loss"].append(train_loss)
            history["val_loss"].append(val_loss)
            history["val_accuracy"].append(val_accuracy)

            print(f"Epoch {epoch+1}/{num_epochs} | Train Loss: {train_loss:.4f} | "
                  f"Val Loss: {val_loss:.4f} | Val Acc: {val_accuracy:.4f}")

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                epochs_without_improvement = 0
                self._save_checkpoint("best_model.pt")
            else:
                epochs_without_improvement += 1
                if epochs_without_improvement >= patience:
                    print(f"Early stopping at epoch {epoch+1}")
                    break

        return history

    def _save_checkpoint(self, filename: str):
        """Save model checkpoint."""
        torch.save(self.model.state_dict(), filename)

    def evaluate(self, test_loader: DataLoader) -> dict:
        """Evaluate on test set.

        Returns:
            Dictionary with metrics per class
        """
        self.model.eval()
        predictions = []
        true_labels = []

        with torch.no_grad():
            for features, labels in test_loader:
                features = features.to(self.device)
                logits = self.model(features)
                preds = torch.argmax(logits, dim=1)
                predictions.extend(preds.cpu().numpy())
                true_labels.extend(labels.numpy())

        predictions = np.array(predictions)
        true_labels = np.array(true_labels)

        accuracy = np.mean(predictions == true_labels)
        per_class_acc = {}
        for class_idx in range(3):
            class_mask = true_labels == class_idx
            if class_mask.sum() > 0:
                per_class_acc[["GREEN", "YELLOW", "RED"][class_idx]] = \
                    np.mean(predictions[class_mask] == true_labels[class_mask])

        return {
            "overall_accuracy": accuracy,
            "per_class_accuracy": per_class_acc,
            "predictions": predictions,
            "true_labels": true_labels,
        }
