import numpy as np
from sklearn.ensemble import IsolationForest

def analyze_component_pricing(billings):
    analyzed = []
    for bill in billings:
        rate = float(bill.get("unit_rate", 0) or 0)
        bench = float(bill.get("benchmark_rate", 0) or 0)

        deviation = round(((rate - bench) / bench) * 100, 1) if bench > 0 else 0.0
        flagged = False
        severity = "NORMAL"
        msg = "Within standard tender tolerance (+/- 15%)."

        if deviation > 75:
            flagged = True
            severity = "CRITICAL"
            msg = f"Rate ₹{rate:,.0f} is {deviation}% above benchmark (₹{bench:,.0f}). Requires audit review."
        elif deviation > 25:
            flagged = True
            severity = "ELEVATED"
            msg = f"Rate ₹{rate:,.0f} is {deviation}% above benchmark (₹{bench:,.0f})."
        elif bench == 0 and bill.get("category") == "Prohibited Category":
            flagged = True
            severity = "PROHIBITED"
            msg = "Item listed under restricted/prohibited works with no approved schedule rate."

        analyzed.append({
            **bill,
            "deviation_pct": deviation,
            "is_anomaly": flagged,
            "anomaly_severity": severity,
            "explanation": msg
        })
    return analyzed

def run_project_ml_anomaly_detection(projects, analyzed_billings):
    if not projects:
        return [], {}

    max_devs = {}
    for b in analyzed_billings:
        pid = b.get("project_id")
        dev = b.get("deviation_pct", 0)
        if pid not in max_devs or dev > max_devs[pid]:
            max_devs[pid] = dev

    rows = []
    for p in projects:
        sanctioned = float(p.get("sanctioned_amount") or 1)
        spent = float(p.get("amount_spent") or 0)
        progress = float(p.get("completion_percentage") or 0)

        util = spent / max(1.0, sanctioned)
        disparity = util - (progress / 100.0)
        cost_rate = spent / max(1.0, progress)
        max_dev = max_devs.get(p.get("project_id"), 0.0)

        rows.append([util, disparity, cost_rate, max_dev])

    X = np.array(rows)
    contamination = min(0.35, max(0.1, 3.0 / max(3, len(projects))))
    clf = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
    clf.fit(X)

    raw_scores = clf.decision_function(X)
    preds = clf.predict(X)

    min_s, max_s = np.min(raw_scores), np.max(raw_scores)
    diff = max_s - min_s if (max_s - min_s) > 1e-6 else 1.0

    enriched = []
    for i, p in enumerate(projects):
        sanctioned = float(p.get("sanctioned_amount") or 1)
        spent = float(p.get("amount_spent") or 0)
        progress = float(p.get("completion_percentage") or 0)
        max_dev = max_devs.get(p.get("project_id"), 0.0)

        risk_val = float(np.clip(round((1.0 - ((raw_scores[i] - min_s) / diff)) * 100, 1), 5.0, 95.0))
        is_outlier = bool(preds[i] == -1)

        factors = []
        spent_pct = round((spent / max(1.0, sanctioned)) * 100, 1)
        gap = round(spent_pct - progress, 1)

        if gap > 30:
            factors.append(f"Severe physical-financial disparity: {spent_pct}% spent vs {progress}% progress (Gap: +{gap}%)")
            risk_val = max(risk_val, 80.0)
            is_outlier = True

        if spent > sanctioned:
            factors.append(f"Cost Overrun: Expenditure exceeds sanctioned budget by ₹{spent - sanctioned:,.0f}")
            risk_val = max(risk_val, 75.0)
            is_outlier = True

        if max_dev > 50:
            factors.append(f"Contractor billing contains components up to {max_dev}% above standard Schedule of Rates")
            risk_val = max(risk_val, 70.0)
            is_outlier = True

        if not factors and is_outlier:
            factors.append("Multi-factor statistical outlier detected by Isolation Forest engine")

        enriched.append({
            **p,
            "ml_anomaly_score": risk_val,
            "is_ml_anomaly": is_outlier,
            "anomaly_factors": factors,
            "max_component_deviation_pct": max_dev
        })

    metadata = {
        "model_type": "IsolationForest",
        "contamination": contamination,
        "n_estimators": 100,
        "total_analyzed": len(projects),
        "anomalies_detected": int(sum(1 for p in enriched if p["is_ml_anomaly"]))
    }
    return enriched, metadata
