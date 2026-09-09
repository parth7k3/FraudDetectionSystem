from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn

from data_ingestion.ingestion_service import ingest_file
from data_cleaning.cleaning_service import clean_data
from rule_engine.rule_engine_service import run_rules_on_dataframe
from rule_engine.rule_report import generate_rule_report, generate_rule_summary

from anomaly_engine.name_detector import detect_duplicate_projects, detect_renamed_billing_items
from anomaly_engine.pricing_anomaly_detector import analyze_component_pricing, run_project_ml_anomaly_detection
from anomaly_engine.risk_fusion import fuse_risk_signals

app = FastAPI(title="MPLADS Project Monitoring & Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIT_LOG = [
    {
        "id": "FB-001",
        "project_id": "P006",
        "action": "FIELD_INSPECTION_ORDERED",
        "status": "UNDER_INVESTIGATION",
        "notes": "Physical verification ordered for OHT reservoir due to 98% funds drawn against 22% progress.",
        "officer": "Executive Vigilance Officer",
        "timestamp": "2026-09-08 14:30:00"
    }
]

def run_pipeline():
    raw_df = ingest_file("data/raw/sample_projects.csv")
    cleaned_df, _, _ = clean_data(raw_df)
    
    rule_results = run_rules_on_dataframe(cleaned_df)
    rule_report = generate_rule_report(rule_results)
    rule_summary = generate_rule_summary(rule_report)
    
    merged = pd.merge(cleaned_df, rule_summary, on=['project_id', 'project_name'], how='left')
    merged = merged.replace({float('nan'): None, pd.NaT: None})
    for col in merged.select_dtypes(include=['datetime64', 'datetimetz']).columns:
        merged[col] = merged[col].astype(str).replace({'NaT': None})
        
    projects = merged.to_dict(orient='records')
    
    billings_df = pd.read_csv("data/raw/contractor_billings.csv")
    billings = billings_df.replace({float('nan'): None}).to_dict(orient='records')
    analyzed_billings = analyze_component_pricing(billings)
    
    ml_projects, meta = run_project_ml_anomaly_detection(projects, analyzed_billings)
    duplicate_projects = detect_duplicate_projects(projects)
    renamed_items = detect_renamed_billing_items(analyzed_billings)
    fused_projects = fuse_risk_signals(ml_projects, duplicate_projects)
    
    return {
        "projects": fused_projects,
        "billings": analyzed_billings,
        "duplicate_projects": duplicate_projects,
        "renamed_items": renamed_items,
        "ml_metadata": meta,
        "rule_report": rule_report.to_dict(orient='records') if hasattr(rule_report, 'to_dict') else []
    }

@app.get("/api/health")
def health():
    return {"status": "ONLINE", "timestamp": datetime.now().isoformat()}

@app.get("/api/projects")
def get_projects():
    data = run_pipeline()
    return {
        "count": len(data["projects"]),
        "projects": data["projects"],
        "ml_metadata": data["ml_metadata"]
    }

@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    data = run_pipeline()
    matched = [p for p in data["projects"] if p.get("project_id") == project_id]
    if not matched:
        raise HTTPException(status_code=404, detail="Project not found")

    project = matched[0]
    bills = [b for b in data["billings"] if b.get("project_id") == project_id]
    rules = [r for r in data["rule_report"] if r.get("project_id") == project_id]
    dups = [d for d in data["duplicate_projects"] if project_id in (d.get("project_1_id"), d.get("project_2_id"))]
    feedback = [f for f in AUDIT_LOG if f.get("project_id") == project_id]

    return {
        "project": project,
        "billings": bills,
        "rule_compliance": rules,
        "duplicate_matches": dups,
        "feedback_history": feedback
    }

@app.get("/api/public/billings")
def get_billings(contractor: str = None, project_id: str = None, category: str = None):
    data = run_pipeline()
    records = data["billings"]
    
    if contractor:
        records = [b for b in records if contractor.lower() in str(b.get("contractor_name", "")).lower()]
    if project_id:
        records = [b for b in records if project_id.lower() == str(b.get("project_id", "")).lower()]
    if category:
        records = [b for b in records if category.lower() in str(b.get("category", "")).lower()]

    total_amount = sum(float(b.get("total_amount", 0) or 0) for b in records)
    return {
        "total_invoices": len(records),
        "total_billed_amount": total_amount,
        "billings": records
    }

@app.get("/api/investigation/queue")
def get_queue():
    data = run_pipeline()
    ranked = sorted(data["projects"], key=lambda x: x.get("risk_score", 0), reverse=True)
    high = [p for p in ranked if p.get("priority_level") == "HIGH"]
    med = [p for p in ranked if p.get("priority_level") == "MEDIUM"]

    return {
        "total_queue": len(ranked),
        "high_priority_count": len(high),
        "medium_priority_count": len(med),
        "queue": ranked
    }

@app.get("/api/investigation/duplicates")
def get_duplicates():
    data = run_pipeline()
    return {
        "duplicate_projects": data["duplicate_projects"],
        "renamed_billing_items": data["renamed_items"]
    }

@app.get("/api/contractors")
def get_contractors():
    data = run_pipeline()
    stats = {}
    
    for p in data["projects"]:
        c = p.get("contractor_name")
        if not c:
            continue
        if c not in stats:
            stats[c] = {
                "contractor_name": c,
                "gstin": "N/A",
                "total_projects": 0,
                "completed_projects": 0,
                "sanctioned_total": 0.0,
                "spent_total": 0.0,
                "flagged_projects_count": 0,
                "invoices_count": 0,
                "total_billed": 0.0,
                "pricing_outliers_count": 0
            }
        stats[c]["total_projects"] += 1
        if p.get("project_status") == "COMPLETED":
            stats[c]["completed_projects"] += 1
        stats[c]["sanctioned_total"] += float(p.get("sanctioned_amount") or 0)
        stats[c]["spent_total"] += float(p.get("amount_spent") or 0)
        if p.get("priority_level") == "HIGH":
            stats[c]["flagged_projects_count"] += 1

    for b in data["billings"]:
        c = b.get("contractor_name")
        if c in stats:
            stats[c]["gstin"] = b.get("gstin", stats[c]["gstin"])
            stats[c]["invoices_count"] += 1
            stats[c]["total_billed"] += float(b.get("total_amount") or 0)
            if b.get("is_anomaly"):
                stats[c]["pricing_outliers_count"] += 1

    result = sorted(stats.values(), key=lambda x: x["flagged_projects_count"], reverse=True)
    return {"count": len(result), "contractors": result}

@app.post("/api/investigation/feedback")
def save_feedback(payload: dict = Body(...)):
    pid = payload.get("project_id")
    action = payload.get("action")
    if not pid or not action:
        raise HTTPException(status_code=400, detail="Missing project_id or action")

    entry = {
        "id": f"FB-{len(AUDIT_LOG) + 1:03d}",
        "project_id": pid,
        "action": action,
        "status": "LOGGED",
        "notes": payload.get("notes", ""),
        "officer": payload.get("officer", "Authorized Vigilance Auditor"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    AUDIT_LOG.insert(0, entry)
    return {"message": "Success", "entry": entry}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)