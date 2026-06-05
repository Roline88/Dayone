"""FastAPI application for clinical triage system."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch
from pathlib import Path
import pickle

from app.config import MODEL_PATH, ENSEMBLE_NN_WEIGHT, ENSEMBLE_THRESHOLD_WEIGHT
from app.services.nn_classifier import NNTriageClassifier
from app.services.ensemble_classifier import EnsembleTriageClassifier
from app.routes import triage

# Initialize FastAPI app
app = FastAPI(
    title="Clinical Triage System",
    description="AI-powered patient triage classification using ensemble learning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Load models and initialize classifier on startup."""
    try:
        print("[STARTUP] Loading neural network model...")

        model_path = MODEL_PATH
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        scaler_path = Path(model_path).parent / "scaler.pkl"
        if not scaler_path.exists():
            print(f"Warning: Scaler file not found: {scaler_path}")
            scaler_path = None

        # Initialize NN classifier
        nn_classifier = NNTriageClassifier(
            model_path=model_path,
            scaler_path=str(scaler_path) if scaler_path else None,
            device="cuda" if torch.cuda.is_available() else "cpu"
        )

        # Initialize ensemble classifier
        ensemble_classifier = EnsembleTriageClassifier(
            nn_classifier=nn_classifier,
            nn_weight=ENSEMBLE_NN_WEIGHT,
            threshold_weight=ENSEMBLE_THRESHOLD_WEIGHT
        )

        # Register classifier with routes
        triage.set_ensemble_classifier(ensemble_classifier)

        print("[STARTUP] ✓ Models loaded successfully")
        print(f"[STARTUP] Using weights: NN={ENSEMBLE_NN_WEIGHT}, Threshold={ENSEMBLE_THRESHOLD_WEIGHT}")

    except Exception as e:
        print(f"[STARTUP] ✗ Failed to load models: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("[SHUTDOWN] Shutting down application")


# Include routes
app.include_router(triage.router, prefix="/api/v1", tags=["triage"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Clinical Triage System API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/api/v1/info")
async def info():
    """Get system information."""
    return {
        "system": "Clinical Triage System",
        "version": "1.0.0",
        "endpoints": {
            "triage": "POST /api/v1/triage - Classify single patient",
            "batch_triage": "POST /api/v1/batch-triage - Classify multiple patients",
            "health": "GET /api/v1/health - System health check",
            "docs": "GET /docs - Interactive API documentation",
        },
        "ensemble_config": {
            "nn_weight": ENSEMBLE_NN_WEIGHT,
            "threshold_weight": ENSEMBLE_THRESHOLD_WEIGHT,
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
