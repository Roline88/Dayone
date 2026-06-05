import torch
import torch.nn as nn
import torch.nn.functional as F


class TriageClassifier(nn.Module):
    """Neural network classifier for patient triage (GREEN/YELLOW/RED).

    Input: 13 features (8 vitals + 5 tests)
    Output: 3 classes (GREEN=0, YELLOW=1, RED=2)
    """

    def __init__(self, input_size: int = 13, hidden_size: int = 64, num_classes: int = 3, dropout: float = 0.2):
        super().__init__()

        self.fc1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.dropout1 = nn.Dropout(dropout)

        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.bn2 = nn.BatchNorm1d(hidden_size // 2)
        self.dropout2 = nn.Dropout(dropout)

        self.fc3 = nn.Linear(hidden_size // 2, hidden_size // 4)
        self.bn3 = nn.BatchNorm1d(hidden_size // 4)
        self.dropout3 = nn.Dropout(dropout)

        self.fc4 = nn.Linear(hidden_size // 4, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through network.

        Args:
            x: Input tensor of shape (batch_size, 13)

        Returns:
            Logits of shape (batch_size, 3)
        """
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout1(x)

        x = self.fc2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout2(x)

        x = self.fc3(x)
        x = self.bn3(x)
        x = F.relu(x)
        x = self.dropout3(x)

        x = self.fc4(x)
        return x

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        """Get probability predictions.

        Args:
            x: Input tensor

        Returns:
            Probabilities for each class (batch_size, 3)
        """
        logits = self.forward(x)
        probabilities = F.softmax(logits, dim=1)
        return probabilities

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """Get class predictions.

        Args:
            x: Input tensor

        Returns:
            Predicted class indices (batch_size,)
        """
        logits = self.forward(x)
        return torch.argmax(logits, dim=1)
