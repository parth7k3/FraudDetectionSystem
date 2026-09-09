import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { AlertTriangle, ArrowRight, Tag, Split, FileCheck } from 'lucide-react';

const DuplicateDetector = () => {
  const [data, setData] = useState({ duplicates: [], renamed: [], loading: true });
  const [activeTab, setActiveTab] = useState('projects');

  useEffect(() => {
    axios.get('http://localhost:8000/api/investigation/duplicates')
      .then(res => {
        setData({
          duplicates: res.data.duplicate_projects || [],
          renamed: res.data.renamed_billing_items || [],
          loading: false
        });
      })
      .catch(err => {
        console.error('Failed to load duplicate analysis:', err);
        setData(prev => ({ ...prev, loading: false }));
      });
  }, []);

  if (data.loading) return <div className="loading-container">Running NLP semantic duplicate analysis...</div>;

  const { duplicates, renamed } = data;

  return (
    <div className="duplicates-page">
      <div className="page-header">
        <div className="header-meta">
          <span className="section-tag">AI Vigilance Intelligence</span>
          <h1 className="page-title">Semantic Name & Duplicate Work Detector</h1>
          <p className="page-subtitle">
            NLP-powered identification of works billed under altered terminology, repeated project scope, or split tenders.
          </p>
        </div>

        <div className="tab-pill-box">
          <button 
            className={`tab-pill-btn ${activeTab === 'projects' ? 'active' : ''}`}
            onClick={() => setActiveTab('projects')}
          >
            <Split size={14} /> Duplicate Project Works ({duplicates.length})
          </button>
          <button 
            className={`tab-pill-btn ${activeTab === 'items' ? 'active' : ''}`}
            onClick={() => setActiveTab('items')}
          >
            <Tag size={14} /> Renamed Billing Items ({renamed.length})
          </button>
        </div>
      </div>

      {activeTab === 'projects' && (
        <div className="duplicate-pairs-list">
          {duplicates.map((dup, i) => (
            <div key={i} className={`card duplicate-pair-card ${dup.risk_level === 'HIGH' ? 'high-risk-pair' : ''}`}>
              <div className="pair-score-header">
                <div className="pair-match-metric">
                  <span className="metric-num">{dup.similarity_score}%</span>
                  <span className="metric-lbl">Semantic Equivalence</span>
                </div>
                <div className="pair-status-tags">
                  <span className={`badge ${dup.risk_level === 'HIGH' ? 'high-risk' : 'medium-risk'}`}>
                    {dup.risk_level} AUDIT PRIORITY
                  </span>
                  {dup.is_same_contractor && (
                    <span className="badge medium-risk">Identical Contractor</span>
                  )}
                  {dup.is_same_district && (
                    <span className="badge low-risk">Same District</span>
                  )}
                </div>
              </div>

              <div className="side-by-side-grid">
                <div className="compare-side side-a">
                  <div className="side-label">Sanction A • {dup.project_1_id}</div>
                  <h4 className="side-title">{dup.project_1_name}</h4>
                  <div className="side-meta">
                    <span>Contractor: <strong>{dup.project_1_contractor}</strong></span>
                    <span>Sanction: <strong>₹{Number(dup.project_1_amount || 0).toLocaleString()}</strong></span>
                  </div>
                  <Link to={`/projects/${dup.project_1_id}`} className="side-link">
                    Inspect Case File A <ArrowRight size={13} />
                  </Link>
                </div>

                <div className="vs-divider">
                  <span>VS</span>
                </div>

                <div className="compare-side side-b">
                  <div className="side-label">Sanction B • {dup.project_2_id}</div>
                  <h4 className="side-title">{dup.project_2_name}</h4>
                  <div className="side-meta">
                    <span>Contractor: <strong>{dup.project_2_contractor}</strong></span>
                    <span>Sanction: <strong>₹{Number(dup.project_2_amount || 0).toLocaleString()}</strong></span>
                  </div>
                  <Link to={`/projects/${dup.project_2_id}`} className="side-link">
                    Inspect Case File B <ArrowRight size={13} />
                  </Link>
                </div>
              </div>

              <div className="pair-flags-footer">
                <span className="flags-label">Investigation Signals:</span>
                <div className="flags-wrap">
                  {dup.flags.map((f, j) => (
                    <span key={j} className="audit-flag-chip">
                      <AlertTriangle size={12} /> {f}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}

          {duplicates.length === 0 && (
            <div className="card empty-state">
              <FileCheck size={32} />
              <p>No project-level semantic duplicates detected above threshold.</p>
            </div>
          )}
        </div>
      )}

      {activeTab === 'items' && (
        <div className="card table-card">
          <div className="card-header-bar">
            <h3>Renamed / Altered Billing Descriptions Across Invoices</h3>
            <span className="record-count">{renamed.length} Cross-Matches Detected</span>
          </div>

          <div className="ledger-table-wrap">
            <table className="ledger-table">
              <thead>
                <tr>
                  <th>Original Item Claimed</th>
                  <th>Invoice & Project A</th>
                  <th>Rate A</th>
                  <th>Matched Alternate Item</th>
                  <th>Invoice & Project B</th>
                  <th>Rate B</th>
                  <th>Similarity</th>
                  <th>Rate Variance</th>
                  <th>Signal</th>
                </tr>
              </thead>
              <tbody>
                {renamed.map((r, i) => (
                  <tr key={i} className="anomaly-row">
                    <td className="bold">{r.item_1}</td>
                    <td className="mono">{r.invoice_1} ({r.project_1})</td>
                    <td className="bold">₹{r.unit_rate_1.toLocaleString()}</td>
                    <td className="bold">{r.item_2}</td>
                    <td className="mono">{r.invoice_2} ({r.project_2})</td>
                    <td className="bold">₹{r.unit_rate_2.toLocaleString()}</td>
                    <td>
                      <span className="badge medium-risk">{r.similarity_score}%</span>
                    </td>
                    <td className="bold highlight-deviation">
                      {r.rate_difference_pct > 0 ? `+${r.rate_difference_pct}%` : '0%'}
                    </td>
                    <td>
                      <span className="badge high-risk">{r.risk_signal}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default DuplicateDetector;
