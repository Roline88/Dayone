import torch
from torch.utils.data import Dataset
import numpy as np


class TriageDataset(Dataset):
    """PyTorch Dataset for patient triage classification."""

    def __init__(self, features: np.ndarray, labels: np.ndarray, scaler=None):
        """Initialize dataset.

        Args:
            features: (num_samples, 13) array of patient features
            labels: (num_samples,) array of class labels (0, 1, 2)
            scaler: Optional sklearn scaler for feature normalization
        """
        self.features = torch.from_numpy(features).float()
        self.labels = torch.from_numpy(labels).long()
        self.scaler = scaler

        if self.scaler is not None:
            self.features = torch.from_numpy(self.scaler.transform(features)).float()

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> tuple:
        """Get single sample.

        Returns:
            Tuple of (features, label)
        """
        return self.features[idx], self.labels[idx]
