import numpy as np

def estimate_heart_rate(face_roi):
    """Placeholder heart-rate estimator."""
    mean_intensity = int(face_roi.mean()) if face_roi.size else 70
    return np.clip(60 + (mean_intensity % 40), 50, 120)

def estimate_temperature(face_roi):
    """Placeholder temperature estimator."""
    mean_intensity = float(face_roi.mean()) if face_roi.size else 36.5
    return round(36.0 + ((mean_intensity % 15) / 10.0), 1)

def estimate_respiratory_rate(face_roi):
    """Placeholder respiratory-rate estimator."""
    mean_intensity = int(face_roi.mean()) if face_roi.size else 16
    return np.clip(12 + (mean_intensity % 18), 10, 30)