import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { ShieldAlert } from 'lucide-react';
import { usePortal } from '../context/PortalContext';

const Overview = () => {
  const { isInvestigator } = usePortal();
  const [data, setData] = useState({ projects: [], loading: true });

  useEffect(() => {
    axios.get('http://localhost:8000/api/projects')
      .then(res => setData({ projects: res.data.projects || [], loading: false }))
      .catch(err => {
        console.error('Failed to load dashboard:', err);
        setData(prev => ({ ...prev, loading: false }));
      });
  }, []);

  if (data.loading) return <div className="loading-container">Loading public transparency dashboard...</div>;

  const { projects } = data;
  const totalProjects = projects.length;
  const totalSanctioned = projects.reduce((sum, p) => sum + Number(p.sanctioned_amount || 0), 0);
  const totalSpent = projects.reduce((sum, p) => sum + Number(p.amount_spent || 0), 0);
  const completedCount = projects.filter(p => p.project_status === 'COMPLETED').length;
  const ongoingCount = projects.filter(p => p.project_status === 'ONGOING').length;
  
  const highRiskCount = projects.filter(p => p.priority_level === 'HIGH').length;
  const pricingOutlierCount = projects.filter(p => Number(p.max_component_deviation_pct || 0) > 30).length;

  return (
    <div className="overview-page">
      <div className="page-header">
        <div className="header-meta">
          <span className="section-tag">
            {isInvestigator ? 'Vigilance & Audit Oversight' : 'Citizen Transparency Portal'}
          </span>
          <h1 className="page-title">MPLADS Project Monitoring Overview</h1>
          <p className="page-subtitle">
            {isInvestigator 
              ? 'Multi-signal oversight platform combining ML anomaly detection, component pricing benchmarking, and scheme compliance.'
              : 'Public disclosure of development projects, financial allocations, physical progress, and contractor billings.'}
          </p>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="card stat-card">
          <div className="stat-label">Sanctioned Projects</div>
          <div className="stat-value">{totalProjects}</div>
          <div className="stat-sub">{completedCount} Completed • {ongoingCount} In Progress</div>
        </div>

        <div className="card stat-card">
          <div className="stat-label">Total Sanctioned Funds</div>
          <div className="stat-value">₹{(totalSanctioned / 10000000).toFixed(2)} Cr</div>
          <div className="stat-sub">Across All Constituencies</div>
        </div>

        <div className="card stat-card">
          <div className="stat-label">Public Expenditure</div>
          <div className="stat-value">₹{(totalSpent / 10000000).toFixed(2)} Cr</div>
          <div className="stat-sub">
            {((totalSpent / (totalSanctioned || 1)) * 100).toFixed(1)}% Overall Utilization
          </div>
        </div>

        {!isInvestigator ? (
          <div className="card stat-card">
            <div className="stat-label">Transparent Contractor Invoices</div>
            <div className="stat-value">100% Disclosed</div>
            <div className="stat-sub">
              <Link to="/billings" className="stat-link">Browse Bill Ledger &rarr;</Link>
            </div>
          </div>
        ) : (
          <div className="card stat-card risk-flagged">
            <div className="stat-label">High-Priority Audit Flags</div>
            <div className="stat-value text-danger">{highRiskCount}</div>
            <div className="stat-sub">
              <Link to="/high-risk" className="stat-link text-danger">Review Investigation Queue &rarr;</Link>
            </div>
          </div>
        )}
      </div>

      {isInvestigator && (
        <div className="card investigator-alert-banner">
          <div className="alert-banner-content">
            <div className="alert-banner-icon">
              <ShieldAlert size={24} />
            </div>
            <div className="alert-banner-text">
              <h4>Active Vigilance Signals Detected</h4>
              <p>
                The ML Anomaly Engine has flagged <strong>{pricingOutlierCount} projects</strong> with component pricing above Schedule of Rates tolerances, and identified potential semantic duplicate submissions.
              </p>
            </div>
          </div>
          <div className="alert-banner-actions">
            <Link to="/high-risk" className="btn-alert-action primary">View High-Risk Queue</Link>
            <Link to="/duplicates" className="btn-alert-action secondary">Inspect Duplicates</Link>
          </div>
        </div>
      )}

      <div className="card table-card">
        <div className="card-header-bar">
          <div>
            <h3>Active Project Pipeline</h3>
            <p className="sub-header-p">Snapshot of development works across sectors and districts.</p>
          </div>
          <Link to="/projects" className="view-all-link">
            Explore All Projects ({projects.length}) &rarr;
          </Link>
        </div>

        <div className="pipeline-table-wrapper">
          <table className="pipeline-table">
            <thead>
              <tr>
                <th>Project ID</th>
                <th>Work Description</th>
                <th>Executing Agency</th>
                <th>District</th>
                <th>Physical Progress</th>
                <th>Sanctioned / Spent</th>
                <th>Status</th>
                {isInvestigator && <th>Vigilance Score</th>}
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {projects.slice(0, 6).map(p => {
                const sanctioned = Number(p.sanctioned_amount || 0);
                const spent = Number(p.amount_spent || 0);

                return (
                  <tr key={p.project_id}>
                    <td className="mono bold">{p.project_id}</td>
                    <td className="bold">{p.project_name}</td>
                    <td>{p.contractor_name || 'Departmental'}</td>
                    <td>{p.district}</td>
                    <td>
                      <div className="completion-bar-container">
                        <div className="completion-bar-bg">
                          <div 
                            className="completion-bar-fill" 
                            style={{ width: `${Math.min(100, p.completion_percentage || 0)}%` }} 
                          />
                        </div>
                        <span className="completion-percent">{p.completion_percentage}%</span>
                      </div>
                    </td>
                    <td>
                      <span className="fin-spent">₹{(spent / 100000).toFixed(1)}L</span> / 
                      <span className="fin-sanctioned"> ₹{(sanctioned / 100000).toFixed(1)}L</span>
                    </td>
                    <td>
                      {p.project_status === 'COMPLETED' ? (
                        <span className="badge low-risk">Completed</span>
                      ) : (
                        <span className="badge medium-risk">Ongoing</span>
                      )}
                    </td>

                    {isInvestigator && (
                      <td>
                        <span className={`risk-tag ${p.badge_class}`}>
                          {p.risk_score}/100
                        </span>
                      </td>
                    )}

                    <td>
                      <Link to={`/projects/${p.project_id}`} className="row-action-link">
                        Dossier &rarr;
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Overview;
