import os
import numpy as np
from joblib import load

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'heading_classifier.joblib')
LABEL_PATH = os.path.join(os.path.dirname(__file__), 'label_encoder.joblib')

# Fallback: simple rule-based
HEADING_THRESHOLDS = [18, 15, 12]  # Example font sizes for H1, H2, H3


def load_classifier():
    if os.path.exists(MODEL_PATH) and os.path.exists(LABEL_PATH):
        clf = load(MODEL_PATH)
        le = load(LABEL_PATH)
        return clf, le
    return None, None

def predict_heading_level(features, clf, le):
    font_size = features[0]
    if clf and le:
        import numpy as np
        proba = clf.predict_proba(np.asarray([features]))[0]
        idx = np.argmax(proba)
        label = le.inverse_transform([idx])[0]
        conf = proba[idx]
        if label in ['H1', 'H2', 'H3'] and conf > 0.5:
            return label, conf
        return None, 0.0
    # Rule-based fallback
    if font_size >= HEADING_THRESHOLDS[0]:
        return 'H1', 0.7
    elif font_size >= HEADING_THRESHOLDS[1]:
        return 'H2', 0.6
    elif font_size >= HEADING_THRESHOLDS[2]:
        return 'H3', 0.5
    return None, 0.0 