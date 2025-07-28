import re
import numpy as np
import langid
import pycountry
import os

def detect_language(text):
    if text.strip():
        try:
            lang_code, score = langid.classify(text)
            try:
                lang = pycountry.languages.get(alpha_2=lang_code)
                return lang.name if lang else lang_code
            except Exception:
                return lang_code
        except Exception:
            return 'unknown'
    return 'unknown'

def extract_features_from_page(span, page, page_num):
    text = span['text']
    font_size = span['size']
    font_name = span['font']
    is_bold = 'Bold' in font_name or 'bold' in font_name
    is_italic = 'Italic' in font_name or 'Oblique' in font_name
    is_caps = text.isupper() and len(text) > 2
    x0, y0, x1, y1 = span['bbox']
    width = x1 - x0
    height = y1 - y0
    page_width, page_height = page.rect.width, page.rect.height
    is_centered = abs((x0 + x1) / 2 - page_width / 2) < page_width * 0.15
    alignment = 'center' if is_centered else ('left' if x0 < page_width * 0.25 else 'right')
    numbered = bool(re.match(r"^(\d+\.|[A-Z]\.|Section|Chapter) ", text.strip(), re.IGNORECASE))
    rel_y = y0 / page_height
    color_int = span.get('color', 0)
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    color_hex = f"#{r:02X}{g:02X}{b:02X}"
    lang = detect_language(text)
    return {
        'font_size': font_size,
        'is_bold': is_bold,
        'is_italic': is_italic,
        'is_caps': is_caps,
        'width_ratio': width / page_width,
        'height_ratio': height / page_height,
        'is_centered': is_centered,
        'alignment': alignment,
        'numbered': numbered,
        'rel_y': rel_y,
        'lang': lang,
        'color': color_hex
    }

def extract_title_candidate(candidates):
    best = None
    best_score = -1
    for cand in candidates:
        features = cand['features']
        text = cand['text']
        page = cand['page']
        if page != 1 or len(text.strip()) < 3:
            continue
        score = features['font_size'] * 1.5 + features['is_bold'] * 1.0 + features['is_centered'] * 1.0 - features['rel_y'] * 0.5
        if score > best_score:
            best_score = score
            best = (text, min(1.0, 0.7 + 0.3 * (score / (features['font_size'] + 1e-3))))
    if best:
        return best
    for cand in candidates:
        if cand['page'] == 1 and len(cand['text'].strip()) > 3:
            return cand['text'], 0.5
    return '', 0.0 