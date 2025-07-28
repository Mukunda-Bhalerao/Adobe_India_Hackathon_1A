import fitz  # PyMuPDF
import numpy as np
from .features import extract_features_from_page, extract_title_candidate
from .model import load_classifier, predict_heading_level
from .utils import normalize_text

# Load classifier once (if any)
classifier, label_encoder = load_classifier()

HEADING_LEVELS = ['H1', 'H2', 'H3']


def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    all_candidates = []
    for page_num in range(min(50, len(doc))):
        page = doc[page_num]
        blocks = page.get_text("dict")['blocks']
        for block in blocks:
            if block['type'] != 0:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    features = extract_features_from_page(span, page, page_num)
                    all_candidates.append({
                        'features': features,
                        'text': span['text'],
                        'page': page_num  # page number now starts from 0
                    })
    # Estimate title
    title, title_conf = extract_title_candidate(all_candidates)
    # Predict headings
    for cand in all_candidates:
        features = cand['features']
        text = cand['text']
        page = cand['page']
        level, conf = predict_heading_level([
            features['font_size'],
            int(features['is_bold']),
            int(features['is_italic']),
            int(features['is_caps']),
            features['width_ratio'],
            features['height_ratio'],
            int(features['is_centered']),
            int(features['numbered']),
            features['rel_y']
        ], classifier, label_encoder)
        if level:
            outline.append({
                'level': level,
                'text': normalize_text(text),
                'page': page,
                'confidence': float(conf),
                'language': features['lang'],
                'alignment': features['alignment'],
                'bold': features['is_bold'],
                'italic': features['is_italic'],
                'color': features['color']
            })
    return {
        'title': normalize_text(title),
        'outline': outline
    } 