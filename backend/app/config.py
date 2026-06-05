import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "triage_classifier.pt"))
MCPHASES_PATH = os.getenv("MCPHASES_PATH", str(BASE_DIR / "data" / "mcphases"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ENSEMBLE_NN_WEIGHT = float(os.getenv("ENSEMBLE_NN_WEIGHT", "0.6"))
ENSEMBLE_THRESHOLD_WEIGHT = float(os.getenv("ENSEMBLE_THRESHOLD_WEIGHT", "0.4"))

# Neural network config
NN_INPUT_SIZE = 13  # 8 vitals + 5 tests
NN_HIDDEN_SIZE = 64
NN_NUM_CLASSES = 3  # GREEN, YELLOW, RED
NN_DROPOUT = 0.2
NN_LEARNING_RATE = 0.001
NN_BATCH_SIZE = 32
NN_EPOCHS = 50
NN_EARLY_STOPPING_PATIENCE = 5
