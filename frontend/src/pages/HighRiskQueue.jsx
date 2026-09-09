import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { AlertTriangle, ChevronRight, AlertCircle, ShieldCheck } from 'lucide-react';
import { usePortal } from '../context/PortalContext';

const HighRiskQueue = () => {
  const { isInvestigator, toggleMode } = usePortal();
  const [queueData, setQueueData] = useState({ queue: [], loading: true });
  const [priorityFilter, setPriorityFilter] = useState('ALL');

  useEffect(() => {
    axios.get('http://localhost:8000/api/investigation/queue')
      .then(res => {
        setQueueData({
          queue: res.data.queue || [],
          loading: false
        });
      })
      .catch(err => {
        console.error('Failed to load vigilance queue:', err);
        setQueueData(prev => ({ ...prev, loading: false }));
      });
  }, []);

  if (queueData.loading) return <div className="loading-container">Compiling prioritized vigilance audit queue...</div>;

  const { queue } = queueData;

  const filteredQueue = queue.filter(p => {
    if (priorityFilter === 'ALL') return true;
    return p.priority_level === priorityFilter;
  });

  return (
    <div className="queue-page">
      <div className="page-header">
        <div className="header-meta">
          <span className="section-tag">Vigilance & Audit Suite</span>
          <h1 className="page-title">Prioritized High-Risk Queue</h1>
          <p className="page-subtitle">
            Ranked list of works requiring scrutiny based on rule violations, component pricing anomalies, and progress-expenditure disparity.
          </p>
        </div>

        {!isInvestigator && (
          <div className="alert-notice-box">
            <span>You are currently in Public View. Switch to Investigator Mode to access active vigilance controls.</span>
            <button onClick={toggleMode} className="primary switch-mode-btn">
              Enable Investigator View
            </button>
          </div>
        )}
      </div>

      <div className="card filter-card">
        <div className="queue-filter-bar">
          <div className="filter-tab-group">
            <button 
              className={`filter-btn ${priorityFilter === 'ALL' ? 'active' : ''}`}
              onClick={() => setPriorityFilter('ALL')}
            >
              All Flagged Works ({queue.length})
            </button>
            <button 
              className={`filter-btn high ${priorityFilter === 'HIGH' ? 'active' : ''}`}
              onClick={() => setPriorityFilter('HIGH')}
            >
              High Priority ({queue.filter(p => p.priority_level === 'HIGH').length})
            </button>
            <button 
              className={`filter-btn medium ${priorityFilter === 'MEDIUM' ? 'active' : ''}`}
              onClick={() => setPriorityFilter('MEDIUM')}
            >
              Medium Priority ({queue.filter(p => p.priority_level === 'MEDIUM').length})
            </button>
          </div>
        </div>
      </div>

      <div className="project-list">
        {filteredQueue.map(p => {
          const sanctioned = Number(p.sanctioned_amount || 0);
          const spent = Number(p.amount_spent || 0);

          return (
            <div key={p.project_id} className={`card project-card ${p.badge_class}`}>
              <div className="project-card-header">
                <div className="project-info">
                  <div className="card-top-id-row">
                    <span className="mono-id">{p.project_id}</span>
                    <span className="location-crumb">{p.district}, {p.state}</span>
                  </div>
                  <h3>{p.project_name}</h3>
                  <span className="contractor-crumb">Agency: <strong>{p.contractor_name || 'N/A'}</strong></span>
                </div>

                <div className="risk-score-badge-box">
                  <div className={`risk-pill ${p.badge_class}`}>
                    <AlertTriangle size={14} />
                    <span>{p.risk_score} / 100</span>
                  </div>
                  <span className="priority-text">{p.priority_level} PRIORITY</span>
                </div>
              </div>

              <div className="project-stats">
                <div className="stat-item">
                  <span className="label">Sanctioned</span>
                  <span className="val">₹{(sanctioned / 100000).toFixed(2)} L</span>
                </div>
                <div className="stat-item">
                  <span className="label">Expenditure</span>
                  <span className="val">₹{(spent / 100000).toFixed(2)} L</span>
                </div>
                <div className="stat-item">
                  <span className="label">Completion</span>
                  <span className="val highlight">{p.completion_percentage}%</span>
                </div>
                <div className="stat-item">
                  <span className="label">Max Item Markup</span>
                  <span className="val text-danger">
                    {p.max_component_deviation_pct > 0 ? `+${p.max_component_deviation_pct}%` : 'Normal'}
                  </span>
                </div>
              </div>

              {p.all_signals && p.all_signals.length > 0 && (
                <div className="review-reasons">
                  <strong>Detected Anomaly Signals:</strong>
                  <ul className="signals-bullets">
                    {p.all_signals.map((sig, idx) => (
                      <li key={idx}>
                        <AlertCircle size={13} />
                        <span>{sig}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="project-footer">
                <div className="recommendation-snippet">
                  <span>{p.recommendation}</span>
                </div>
                <Link to={`/projects/${p.project_id}`} className="investigate-btn">
                  Open Investigation Dossier <ChevronRight size={16} />
                </Link>
              </div>
            </div>
          );
        })}

        {filteredQueue.length === 0 && (
          <div className="card empty-state">
            <ShieldCheck size={32} />
            <p>No projects match the selected priority filter.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default HighRiskQueue;
