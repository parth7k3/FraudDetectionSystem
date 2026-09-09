import { useState, useEffect } from 'react';
import axios from 'axios';
import { Building, Search } from 'lucide-react';
import { usePortal } from '../context/PortalContext';

const Contractors = () => {
  const { isInvestigator } = usePortal();
  const [contractors, setContractors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');

  useEffect(() => {
    axios.get('http://localhost:8000/api/contractors')
      .then(res => {
        setContractors(res.data.contractors || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load contractors:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading-container">Loading implementing agency profiles...</div>;

  const filtered = contractors.filter(c => 
    (c.contractor_name || '').toLowerCase().includes(query.toLowerCase()) ||
    (c.gstin || '').toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="contractors-page">
      <div className="page-header">
        <div className="header-meta">
          <span className="section-tag">Agency & Contractor Directory</span>
          <h1 className="page-title">Implementing Agencies & Contractors</h1>
          <p className="page-subtitle">
            Transparent public disclosure of executing agencies, contract allocations, disbursed values, and compliance records.
          </p>
        </div>
      </div>

      <div className="card filter-card">
        <div className="search-input-wrap">
          <Search size={16} className="search-icon" />
          <input 
            type="text" 
            placeholder="Search by contractor name or GSTIN..." 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="filter-search"
          />
        </div>
      </div>

      <div className="contractors-grid">
        {filtered.map((c, i) => {
          const sanctionedLakh = (Number(c.sanctioned_total || 0) / 100000).toFixed(2);
          const spentLakh = (Number(c.spent_total || 0) / 100000).toFixed(2);
          const hasFlags = c.pricing_outliers_count > 0 || c.flagged_projects_count > 0;

          return (
            <div key={i} className={`card contractor-card ${isInvestigator && hasFlags ? 'card-has-flags' : ''}`}>
              <div className="contractor-header">
                <div className="contractor-avatar">
                  <Building size={20} />
                </div>
                <div className="contractor-title-block">
                  <h3>{c.contractor_name}</h3>
                  <span className="contractor-gstin">GSTIN: {c.gstin}</span>
                </div>
              </div>

              <div className="contractor-stats-grid">
                <div className="c-stat">
                  <span className="lbl">Sanctioned Works</span>
                  <span className="val">{c.total_projects}</span>
                </div>
                <div className="c-stat">
                  <span className="lbl">Completed</span>
                  <span className="val">{c.completed_projects}</span>
                </div>
                <div className="c-stat">
                  <span className="lbl">Disbursed</span>
                  <span className="val highlight">₹{spentLakh} L</span>
                </div>
              </div>

              {isInvestigator && (
                <div className="contractor-audit-summary">
                  <div className="audit-row">
                    <span>Component Pricing Outliers:</span>
                    <strong className={c.pricing_outliers_count > 0 ? 'text-danger' : ''}>
                      {c.pricing_outliers_count} Items
                    </strong>
                  </div>
                  <div className="audit-row">
                    <span>Flagged High-Risk Works:</span>
                    <strong className={c.flagged_projects_count > 0 ? 'text-danger' : ''}>
                      {c.flagged_projects_count} Works
                    </strong>
                  </div>
                </div>
              )}

              <div className="contractor-footer">
                <span className="invoices-count">{c.invoices_count} Total Invoices Filed</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Contractors;
