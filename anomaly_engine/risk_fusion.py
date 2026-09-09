def fuse_risk_signals(projects, duplicate_signals):
    duplicate_map = {}
    for dup in duplicate_signals:
        p1, p2 = dup.get("project_1_id"), dup.get("project_2_id")
        score = dup.get("similarity_score", 0)
        
        for pid, other_id, other_name in [(p1, p2, dup.get("project_2_name")), (p2, p1, dup.get("project_1_name"))]:
            if pid not in duplicate_map or score > duplicate_map[pid]["score"]:
                duplicate_map[pid] = {
                    "score": score,
                    "matched_project_id": other_id,
                    "matched_project_name": other_name,
                    "is_same_contractor": dup.get("is_same_contractor", False)
                }

    fused = []
    for p in projects:
        pid = p.get("project_id")
        
        failed_rules = int(p.get("review_required") or 0)
        rule_score = min(100.0, failed_rules * 35.0)
        ml_score = float(p.get("ml_anomaly_score", 15.0))
        
        max_dev = float(p.get("max_component_deviation_pct", 0.0))
        component_score = min(100.0, max(0.0, (max_dev / 1.5)))
        
        dup_info = duplicate_map.get(pid)
        dup_score = 0.0
        if dup_info:
            dup_score = dup_info["score"]
            if dup_info["is_same_contractor"]:
                dup_score = min(100.0, dup_score * 1.25)

        combined = (rule_score * 0.25) + (ml_score * 0.35) + (component_score * 0.25) + (dup_score * 0.15)
        
        if failed_rules > 0 or max_dev > 100 or (dup_score > 75 and dup_info and dup_info.get("is_same_contractor")):
            combined = max(combined, 75.0)

        final_score = round(min(99.0, max(5.0, combined)), 1)
        
        if final_score >= 70:
            level = "HIGH"
            badge = "high-risk"
            rec = "Action Required: Immediate vigilance inspection of measurement books, physical assets, and invoice line items."
        elif final_score >= 40:
            level = "MEDIUM"
            badge = "medium-risk"
            rec = "Review Recommended: Request itemized price justification and latest milestone photographs from executing agency."
        else:
            level = "LOW"
            badge = "low-risk"
            rec = "Standard Monitoring: Project milestones and financial utilization align with scheduled benchmarks."

        signals = list(p.get("anomaly_factors", []))
        if failed_rules > 0:
            signals.append(f"Failed {failed_rules} mandatory scheme compliance checks")
        if dup_info and dup_info["score"] >= 50:
            signals.append(f"High name/scope similarity ({dup_info['score']}%) with {dup_info['matched_project_name']} [{dup_info['matched_project_id']}]")

        fused.append({
            **p,
            "risk_score": final_score,
            "priority_level": level,
            "badge_class": badge,
            "recommendation": rec,
            "all_signals": signals,
            "signal_breakdown": {
                "rule_compliance": round(rule_score, 1),
                "ml_anomaly": round(ml_score, 1),
                "component_pricing": round(component_score, 1),
                "nlp_similarity": round(dup_score, 1)
            },
            "duplicate_reference": dup_info
        })

    fused.sort(key=lambda x: x["risk_score"], reverse=True)
    return fused
