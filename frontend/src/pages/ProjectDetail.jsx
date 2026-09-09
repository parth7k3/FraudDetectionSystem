import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { 
  ArrowLeft, AlertTriangle, AlertCircle, Building, 
  MapPin, Calendar, CheckCircle, Send
} from 'lucide-react';
import { usePortal } from '../context/PortalContext';

const ProjectDetail = () => {
  const { id } = useParams();
  const { isInvestigator, toggleMode } = usePortal();

  const [dossier, setDossier] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionChoice, setActionChoice] = useState('FIELD_INSPECTION');
  const [notes, setNotes] = useState('');
  const [saving, setSaving] = useState(false);
  const [feedbackSuccess, setFeedbackSuccess] = useState('');

  const loadProject = () => {
    axios.get(`http://localhost:8000/api/projects/${id}`)
      .then(res => {
        setDossier(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load project dossier:', err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadProject();
  }, [id]);

  const handleFeedbackSubmit = (e) => {
    e.preventDefault();
    setSaving(true);
    setFeedbackSuccess('');

    axios.post('http://localhost:8000/api/investigation/feedback', {
      project_id: id,
      action: actionChoice,
      notes: notes,
      officer: 'Senior Vigilance Auditor'
    })
      .then(() => {
        setSaving(false);
        setFeedbackSuccess('Vigilance determination successfully logged to case file.');
        setNotes('');
        loadProject();
      })
      .catch(err => {
        console.error('Failed to save feedback:', err);
        setSaving(false);
      });
  };

  if (loading) return <div className="loading-container">Loading project case file...</div>;
  if (!dossier || !dossier.project) return <div className="card">Project not found.</div>;

  const { project, billings, duplicate_matches, feedback_history } = dossier;
  const sanctioned = Number(project.sanctioned_amount || 0);
  const spent = Number(project.amount_spent || 0);
  const released = Number(project.amount_released || 0);
  const progress = Number(project.completion_percentage || 0);
  const utilization = sanctioned > 0 ? ((spent / sanctioned) * 100).toFixed(1) : 0;

  return (
    <div className="detail-page">
      <div className="detail-top-nav">
        <Link to="/projects" className="back-link">
          <ArrowLeft size={16} /> Back to Public Project Explorer
        </Link>
        <div className="mode-indicator-pill">
          Viewing as: <strong>{isInvestigator ? 'Authorized Investigator' : 'Public Citizen'}</strong>
          {!isInvestigator && (
            <button onClick={toggleMode} className="inline-switch-btn">
              Switch to Vigilance View
            </button>
          )}
        </div>
      </div>

      <div className="card project-hero-card">
        <div className="hero-header">
          <div className="hero-id-tag">{project.project_id}</div>
          <div className="hero-status">
            {project.project_status === 'COMPLETED' ? (
              <span className="badge low-risk"><CheckCircle size={12} /> Completed</span>
            ) : (
              <span className="badge medium-risk">Ongoing Work</span>
            )}
          </div>
        </div>

        <h1 className="hero-title">{project.project_name}</h1>

        <div className="hero-meta-row">
          <div className="meta-block">
            <MapPin size={15} />
            <span>{project.district}, {project.state}</span>
          </div>
          <div className="meta-block">
            <Building size={15} />
            <span>Executing Contractor: <strong>{project.contractor_name || 'Departmental'}</strong></span>
          </div>
          <div className="meta-block">
            <Calendar size={15} />
            <span>Commencement: {project.start_date || 'N/A'}</span>
          </div>
        </div>

        <div className="hero-stats-grid">
          <div className="hero-stat">
            <span className="lbl">Sanctioned Budget</span>
            <span className="val">₹{(sanctioned / 100000).toFixed(2)} Lakh</span>
          </div>
          <div className="hero-stat">
            <span className="lbl">Disbursed Funds</span>
            <span className="val">₹{(released / 100000).toFixed(2)} Lakh</span>
          </div>
          <div className="hero-stat">
            <span className="lbl">Actual Expenditure</span>
            <span className="val">₹{(spent / 100000).toFixed(2)} Lakh</span>
          </div>
          <div className="hero-stat">
            <span className="lbl">Budget Utilization</span>
            <span className="val">{utilization}%</span>
          </div>
          <div className="hero-stat highlight-stat">
            <span className="lbl">Physical Completion</span>
            <span className="val">{progress}%</span>
          </div>
        </div>

        <div className="hero-progress-section">
          <div className="progress-labels">
            <span>Physical Execution Milestone</span>
            <span>{progress}% Reported</span>
          </div>
          <div className="hero-progress-track">
            <div className="hero-progress-fill" style={{ width: `${Math.min(100, progress)}%` }} />
          </div>
        </div>
      </div>

      {isInvestigator && (
        <div className="card vigilance-panel">
          <div className="vigilance-header">
            <div className="vigilance-title-wrap">
              <AlertTriangle className="vigilance-icon" size={24} />
              <div>
                <h2>Vigilance Anomaly Radar & Risk Assessment</h2>
                <p className="vigilance-sub">Internal AI audit signals, component price benchmarking, and scheme compliance.</p>
              </div>
            </div>
            <div className={`risk-score-display ${project.badge_class}`}>
              <span className="score-val">{project.risk_score}</span>
              <span className="score-max">/100</span>
              <span className="score-priority">{project.priority_level} RISK</span>
            </div>
          </div>

          <div className="recommendation-banner">
            <strong>Official Guidance:</strong> {project.recommendation}
          </div>

          {project.all_signals && project.all_signals.length > 0 && (
            <div className="signals-section">
              <h4>Flagged Review Factors:</h4>
              <ul className="signals-list">
                {project.all_signals.map((sig, idx) => (
                  <li key={idx} className="signal-item">
                    <AlertCircle size={15} />
                    <span>{sig}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {billings.some(b => b.is_anomaly) && (
            <div className="component-anomaly-section">
              <h4>Component Pricing Outliers (Exceeding Benchmark Tolerances)</h4>
              <table className="anomaly-table">
                <thead>
                  <tr>
                    <th>Item Description</th>
                    <th>Category</th>
                    <th>Billed Unit Rate</th>
                    <th>Schedule Benchmark</th>
                    <th>Deviation %</th>
                    <th>Audit Status</th>
                  </tr>
                </thead>
                <tbody>
                  {billings.filter(b => b.is_anomaly).map((b, i) => (
                    <tr key={i}>
                      <td className="bold">{b.item_description}</td>
                      <td>{b.category}</td>
                      <td className="bold">₹{Number(b.unit_rate || 0).toLocaleString()}</td>
                      <td>₹{Number(b.benchmark_rate || 0).toLocaleString()}</td>
                      <td className="highlight-deviation">+{b.deviation_pct}%</td>
                      <td>
                        <span className="badge high-risk">{b.anomaly_severity}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {duplicate_matches && duplicate_matches.length > 0 && (
            <div className="duplicates-warning-section">
              <h4>Potential Duplicate / Split-Tender Matches Identified by NLP</h4>
              <div className="dup-match-cards">
                {duplicate_matches.map((dup, i) => {
                  const otherName = dup.project_1_id === id ? dup.project_2_name : dup.project_1_name;
                  const otherId = dup.project_1_id === id ? dup.project_2_id : dup.project_1_id;
                  const otherContractor = dup.project_1_id === id ? dup.project_2_contractor : dup.project_1_contractor;

                  return (
                    <div key={i} className="dup-match-card">
                      <div className="dup-score-badge">{dup.similarity_score}% Semantic Match</div>
                      <div className="dup-details">
                        <Link to={`/projects/${otherId}`} className="dup-title-link">
                          {otherName} ({otherId})
                        </Link>
                        <span className="dup-contractor">Awarded to: {otherContractor}</span>
                        <div className="dup-flags">
                          {dup.flags.map((f, j) => <span key={j} className="flag-tag">{f}</span>)}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div className="audit-action-form-box">
            <h4>Record Investigator Determination</h4>
            <form onSubmit={handleFeedbackSubmit} className="feedback-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Auditor Action:</label>
                  <select value={actionChoice} onChange={(e) => setActionChoice(e.target.value)}>
                    <option value="FIELD_INSPECTION">Order Field Vigilance Inspection</option>
                    <option value="REQUEST_JUSTIFICATION">Request Itemized Price Justification</option>
                    <option value="WITHHOLD_DISBURSEMENT">Recommend Withholding Next Milestone Payment</option>
                    <option value="CLEARED_LEGITIMATE">Clear Flag (Legitimate Geographical Variance)</option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Vigilance Audit Remarks / Case Notes:</label>
                <textarea 
                  rows={3} 
                  value={notes} 
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Record justification, physical observation notes, or contractor correspondence..."
                  required
                />
              </div>

              <button type="submit" disabled={saving} className="primary submit-audit-btn">
                <Send size={15} /> {saving ? 'Logging Case Action...' : 'Save Vigilance Determination'}
              </button>

              {feedbackSuccess && <div className="feedback-success-banner">{feedbackSuccess}</div>}
            </form>
          </div>

          {feedback_history && feedback_history.length > 0 && (
            <div className="audit-history-box">
              <h4>Case File Audit History</h4>
              <div className="history-timeline">
                {feedback_history.map((h, i) => (
                  <div key={i} className="history-item">
                    <span className="history-time">{h.timestamp}</span>
                    <strong className="history-action">{h.action}</strong>
                    <p className="history-notes">{h.notes}</p>
                    <span className="history-officer">Officer: {h.officer}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="card public-billings-card">
        <div className="card-header-bar">
          <div>
            <h3>Disclosed Contractor Billing Invoices</h3>
            <p className="sub-header-p">Itemized materials, machinery, and execution bills submitted for this project.</p>
          </div>
          <span className="record-count">{billings.length} Invoices Filed</span>
        </div>

        <div className="ledger-table-wrap">
          <table className="ledger-table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Item Description</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Billed Unit Rate</th>
                <th>Standard Rate</th>
                <th>Total Billed</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {billings.map((b, i) => (
                <tr key={i} className={isInvestigator && b.is_anomaly ? 'anomaly-row' : ''}>
                  <td className="mono bold">{b.invoice_no}</td>
                  <td><strong>{b.item_description}</strong></td>
                  <td>{b.category}</td>
                  <td>{b.quantity} {b.unit}</td>
                  <td className="bold">₹{Number(b.unit_rate || 0).toLocaleString()}</td>
                  <td className="benchmark-val">
                    {Number(b.benchmark_rate || 0) > 0 ? `₹${Number(b.benchmark_rate).toLocaleString()}` : 'N/A'}
                  </td>
                  <td className="bold highlight-amount">₹{Number(b.total_amount || 0).toLocaleString()}</td>
                  <td>{b.billing_date}</td>
                  <td>
                    {b.status === 'PAID' ? (
                      <span className="badge low-risk">Disbursed</span>
                    ) : (
                      <span className="badge medium-risk">Pending</span>
                    )}
                    {isInvestigator && b.is_anomaly && (
                      <div className="table-anomaly-tag">+{b.deviation_pct}% Outlier</div>
                    )}
                  </td>
                </tr>
              ))}
              {billings.length === 0 && (
                <tr>
                  <td colSpan={9} style={{ textAlign: 'center', padding: '2rem' }}>
                    No contractor invoices have been uploaded for this project yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetail;
