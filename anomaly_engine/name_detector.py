import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ABBREVIATIONS = {
    r"\bconst\.?\b": "construction",
    r"\brenov\.?\b": "renovation",
    r"\bw/o\b": "without",
    r"\bw/\b": "with",
    r"\bsec-?(\d+)\b": r"sector \1",
    r"\bsec\b": "sector",
    r"\bb/w\b": "between",
    r"\bgovt\.?\b": "government",
    r"\bpvt\.?\b": "private",
    r"\bcc\b": "cement concrete",
    r"\brcc\b": "reinforced cement concrete",
    r"\brd\.?\b": "road",
    r"\bstr\.?\b": "street",
    r"\bsch\.?\b": "school",
    r"\bpri\.?\b": "primary",
    r"\bhosp\.?\b": "hospital",
    r"\bph-?(\d+)\b": r"phase \1",
    r"\bph\b": "phase",
    r"\bdist\.?\b": "district",
    r"\bblks?\b": "blocks",
    r"\bpavg?\b": "paving",
    r"\binst\.?\b": "installation",
    r"\bcomm\.?\b": "community",
    r"\bdrkg?\b": "drinking",
    r"\bwt?r\b": "water",
    r"\boht\b": "overhead tank"
}

SYNONYMS = {
    r"\b(pavement|paver|interlocking tiles?|paving blocks?|tiles? laying)\b": "pavement_work",
    r"\b(primary school|govt school|government school|school)\b": "school_site",
    r"\b(cc road|cement concrete road|road|street|pathway)\b": "roadway",
    r"\b(drinking water|ro plant|water supply|potable water)\b": "water_supply_asset",
    r"\b(solar high mast|solar led|streetlights?|solar lights?)\b": "solar_lighting_system",
}

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    for pat, rep in ABBREVIATIONS.items():
        text = re.sub(pat, rep, text)
    for pat, rep in SYNONYMS.items():
        text = re.sub(pat, rep, text)
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def calculate_similarity_matrix(corpus):
    if not corpus:
        return []
    cleaned = [normalize_text(t) for t in corpus]
    if not any(t.strip() for t in cleaned):
        import numpy as np
        return np.zeros((len(corpus), len(corpus)))
    
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
    tfidf = vec.fit_transform(cleaned)
    return cosine_similarity(tfidf, tfidf)

def _get_val(d, *keys, default=""):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default

def detect_duplicate_projects(projects, threshold=0.35):
    if len(projects) < 2:
        return []

    names = [_get_val(p, "project_name", "Project Name") for p in projects]
    sim = calculate_similarity_matrix(names)

    duplicates = []
    n = len(projects)
    for i in range(n):
        for j in range(i + 1, n):
            score = float(sim[i][j])
            p1, p2 = projects[i], projects[j]
            
            c1 = _get_val(p1, "contractor_name", "Contractor Name", default="N/A")
            c2 = _get_val(p2, "contractor_name", "Contractor Name", default="N/A")
            d1 = _get_val(p1, "district", "District", default="N/A")
            d2 = _get_val(p2, "district", "District", default="N/A")

            same_contractor = (c1 != "N/A" and c1 == c2)
            same_district = (d1 != "N/A" and d1 == d2)

            effective_score = min(1.0, score * 1.2) if (same_contractor and same_district) else score
            if effective_score < threshold:
                continue

            pct = round(effective_score * 100, 1)
            flags = []
            if pct >= 60:
                flags.append("High semantic equivalence in work description")
            elif pct >= 35:
                flags.append("Substantial overlap in scope and asset type")

            if same_contractor:
                flags.append(f"Awarded to identical contractor: {c1}")
            if same_district:
                flags.append(f"Located in same district: {d1}")

            duplicates.append({
                "project_1_id": _get_val(p1, "project_id", "Project ID"),
                "project_1_name": _get_val(p1, "project_name", "Project Name"),
                "project_1_contractor": c1,
                "project_1_amount": _get_val(p1, "sanctioned_amount", "Sanctioned Amount", default=0),
                "project_2_id": _get_val(p2, "project_id", "Project ID"),
                "project_2_name": _get_val(p2, "project_name", "Project Name"),
                "project_2_contractor": c2,
                "project_2_amount": _get_val(p2, "sanctioned_amount", "Sanctioned Amount", default=0),
                "similarity_score": pct,
                "is_same_contractor": same_contractor,
                "is_same_district": same_district,
                "flags": flags,
                "risk_level": "HIGH" if (pct >= 60 or (pct >= 40 and same_contractor)) else "MEDIUM"
            })

    duplicates.sort(key=lambda x: x["similarity_score"], reverse=True)
    return duplicates

def detect_renamed_billing_items(billings, threshold=0.35):
    if len(billings) < 2:
        return []

    descs = [_get_val(b, "item_description", "Item Description") for b in billings]
    sim = calculate_similarity_matrix(descs)

    matches = []
    n = len(billings)
    for i in range(n):
        for j in range(i + 1, n):
            score = float(sim[i][j])
            b1, b2 = billings[i], billings[j]

            if _get_val(b1, "invoice_no") == _get_val(b2, "invoice_no"):
                continue

            if score >= threshold:
                r1 = float(_get_val(b1, "unit_rate", default=0) or 0)
                r2 = float(_get_val(b2, "unit_rate", default=0) or 0)
                diff_pct = 0.0
                if min(r1, r2) > 0:
                    diff_pct = round(abs(r1 - r2) / min(r1, r2) * 100, 1)

                matches.append({
                    "item_1": _get_val(b1, "item_description"),
                    "invoice_1": _get_val(b1, "invoice_no"),
                    "project_1": _get_val(b1, "project_id"),
                    "contractor_1": _get_val(b1, "contractor_name"),
                    "unit_rate_1": r1,
                    "item_2": _get_val(b2, "item_description"),
                    "invoice_2": _get_val(b2, "invoice_no"),
                    "project_2": _get_val(b2, "project_id"),
                    "contractor_2": _get_val(b2, "contractor_name"),
                    "unit_rate_2": r2,
                    "similarity_score": round(score * 100, 1),
                    "rate_difference_pct": diff_pct,
                    "risk_signal": "Renamed component with price variance" if diff_pct > 10 else "Potential duplicate work entry"
                })

    matches.sort(key=lambda x: x["similarity_score"], reverse=True)
    return matches
