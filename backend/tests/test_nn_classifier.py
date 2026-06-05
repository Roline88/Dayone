"""Unit tests for neural network classifier."""

import pytest
import torch
import numpy as np
from app.models.nn_model import TriageClassifier
from app.training.dataset import TriageDataset


@pytest.fixture
def model():
    return TriageClassifier(input_size=13, hidden_size=64, num_classes=3, dropout=0.2)


@pytest.fixture
def sample_data():
    """Create sample training data."""
    features = np.random.randn(32, 13).astype(np.float32)
    labels = np.random.randint(0, 3, 32)
    return features, labels


def test_model_initialization(model):
    """Test that model initializes correctly."""
    assert model is not None
    assert isinstance(model, TriageClassifier)


def test_model_forward_pass(model, sample_data):
    """Test forward pass through model."""
    features, _ = sample_data
    features_tensor = torch.from_numpy(features).float()

    output = model(features_tensor)

    assert output.shape == (32, 3)  # batch_size=32, num_classes=3


def test_model_predict_proba(model, sample_data):
    """Test probability predictions."""
    features, _ = sample_data
    features_tensor = torch.from_numpy(features).float()

    proba = model.predict_proba(features_tensor)

    assert proba.shape == (32, 3)
    assert torch.allclose(proba.sum(dim=1), torch.ones(32))  # Probabilities sum to 1


def test_model_predict(model, sample_data):
    """Test class predictions."""
    features, _ = sample_data
    features_tensor = torch.from_numpy(features).float()

    predictions = model.predict(features_tensor)

    assert predictions.shape == (32,)
    assert torch.all(predictions >= 0) and torch.all(predictions < 3)


def test_model_save_load(model, tmp_path):
    """Test model saving and loading."""
    model_path = tmp_path / "model.pt"

    # Save model
    torch.save(model.state_dict(), model_path)
    assert model_path.exists()

    # Load model
    new_model = TriageClassifier()
    new_model.load_state_dict(torch.load(model_path))

    # Verify models produce same output
    test_input = torch.randn(10, 13)
    output1 = model(test_input)
    output2 = new_model(test_input)

    assert torch.allclose(output1, output2, atol=1e-6)


def test_dataset_initialization(sample_data):
    """Test TriageDataset initialization."""
    features, labels = sample_data
    dataset = TriageDataset(features, labels)

    assert len(dataset) == 32


def test_dataset_getitem(sample_data):
    """Test dataset item retrieval."""
    features, labels = sample_data
    dataset = TriageDataset(features, labels)

    sample_features, sample_label = dataset[0]

    assert sample_features.shape == (13,)
    assert isinstance(sample_label, torch.Tensor)
    assert 0 <= sample_label.item() < 3


def test_dataset_batch_loading(sample_data):
    """Test loading batches from dataset."""
    from torch.utils.data import DataLoader

    features, labels = sample_data
    dataset = TriageDataset(features, labels)
    loader = DataLoader(dataset, batch_size=8)

    batch_features, batch_labels = next(iter(loader))

    assert batch_features.shape == (8, 13)
    assert batch_labels.shape == (8,)
