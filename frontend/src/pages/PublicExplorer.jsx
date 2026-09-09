import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Search, ArrowRight, Building, MapPin, CheckCircle, Clock } from 'lucide-react';
import { usePortal } from '../context/PortalContext';

const PublicExplorer = () => {
  const { isInvestigator } = usePortal();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('ALL');
  const [selectedStatus, setSelectedStatus] = useState('ALL');

  useEffect(() => {
    axios.get('http://localhost:8000/api/projects')
      .then(res => {
        setProjects(res.data.projects || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load projects', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading-container">Loading public project records...</div>;

  const districts = ['ALL', ...new Set(projects.map(p => p.district).filter(Boolean))];
  const statuses = ['ALL', 'ONGOING', 'COMPLETED'];

  const filtered = projects.filter(p => {
    const q = query.toLowerCase();
    const matchesQuery = 
      (p.project_name || '').toLowerCase().includes(q) ||
      (p.project_id || '').toLowerCase().includes(q) ||
      (p.contractor_name || '').toLowerCase().includes(q);
      
    const matchesDist = selectedDistrict === 'ALL' || p.district === selectedDistrict;
    const matchesStat = selectedStatus === 'ALL' || (p.project_status || '').toUpperCase() === selectedStatus;

    return matchesQuery && matchesDist && matchesStat;
  });

  return (
    <div className="explorer-page">
      <div className="page-header">
        <div className="header-meta">
          <span className="section-tag">Public Transparency Portal</span>
          <h1 className="page-title">MPLADS Project Registry</h1>
          <p className="page-subtitle">
            Open government register of sanctioned development projects, budget utilization, and physical progress.
          </p>
        </div>
      </div>

      <div className="card filter-card">
        <div className="filter-group">
          <div className="search-input-wrap">
            <Search size={16} className="search-icon" />
            <input 
              type="text" 
              placeholder="Search by project name, ID, or contractor..." 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="filter-search"
            />
          </div>

          <div className="select-wrap">
            <label>District:</label>
            <select value={selectedDistrict} onChange={(e) => setSelectedDistrict(e.target.value)}>
              {districts.map(d => <option key={d} value={d}>{d}</option>)}
            </select>
          </div>

          <div className="select-wrap">
            <label>Status:</label>
            <select value={selectedStatus} onChange={(e) => setSelectedStatus(e.target.value)}>
              {statuses.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>
      </div>

      <div className="projects-grid">
        {filtered.map(p => {
          const isDone = (p.project_status || '').toUpperCase() === 'COMPLETED';
          const sanctioned = Number(p.sanctioned_amount || 0);
          const spent = Number(p.amount_spent || 0);

          return (
            <div key={p.project_id} className="card project-item-card">
              <div className="item-card-top">
                <div className="item-id-badge">{p.project_id}</div>
                <div className="item-status-pill">
                  {isDone ? (
                    <span className="status-pill complete"><CheckCircle size={12} /> Completed</span>
                  ) : (
                    <span className="status-pill ongoing"><Clock size={12} /> Ongoing</span>
                  )}
                </div>
              </div>

              <h3 className="item-title">{p.project_name}</h3>

              <div className="item-location">
                <MapPin size={14} />
                <span>{p.district}, {p.state}</span>
              </div>

              <div className="item-contractor">
                <Building size={14} />
                <span>Agency: <strong>{p.contractor_name || 'Departmental Execution'}</strong></span>
              </div>

              <div className="item-financials">
                <div className="fin-col">
                  <span className="fin-lbl">Sanctioned</span>
                  <span className="fin-val">₹{(sanctioned / 100000).toFixed(2)} L</span>
                </div>
                <div className="fin-col">
                  <span className="fin-lbl">Expenditure</span>
                  <span className="fin-val">₹{(spent / 100000).toFixed(2)} L</span>
                </div>
                <div className="fin-col">
                  <span className="fin-lbl">Progress</span>
                  <span className="fin-val highlight">{p.completion_percentage}%</span>
                </div>
              </div>

              <div className="progress-track">
                <div 
                  className="progress-bar-fill" 
                  style={{ width: `${Math.min(100, p.completion_percentage || 0)}%` }} 
                />
              </div>

              {isInvestigator && p.risk_score >= 40 && (
                <div className={`vigilance-alert-pill ${p.badge_class}`}>
                  <span>Audit Priority: <strong>{p.risk_score}/100 ({p.priority_level})</strong></span>
                </div>
              )}

              <div className="item-card-bottom">
                <Link to={`/projects/${p.project_id}`} className="view-dossier-btn">
                  View Project Dossier & Billings <ArrowRight size={14} />
                </Link>
              </div>
            </div>
          );
        })}

        {filtered.length === 0 && (
          <div className="card empty-state">
            <p>No projects match your search criteria.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PublicExplorer;
