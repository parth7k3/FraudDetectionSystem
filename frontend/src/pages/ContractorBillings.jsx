import { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, AlertCircle } from 'lucide-react';
import { usePortal } from '../context/PortalContext';

const ContractorBillings = () => {
  const { isInvestigator } = usePortal();
  const [billings, setBillings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('ALL');

  useEffect(() => {
    axios.get('http://localhost:8000/api/public/billings')
      .then(res => {
        setBillings(res.data.billings || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load billings:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading-container">Loading transparent billing ledger...</div>;

  const categories = ['ALL', ...new Set(billings.map(b => b.category).filter(Boolean))];

  const filtered = billings.filter(b => {
    const q = query.toLowerCase();
    const matchSearch = 
      (b.contractor_name || '').toLowerCase().includes(q) ||
      (b.invoice_no || '').toLowerCase().includes(q) ||
      (b.item_description || '').toLowerCase().includes(q) ||
      (b.project_id || '').toLowerCase().includes(q);

    const matchCategory = category === 'ALL' || b.category === category;
    return matchSearch && matchCategory;
  });

  const totalFilteredAmount = filtered.reduce((acc, b) => acc + Number(b.total_amount || 0), 0);

  return (
    <div className="billings-page">
      <div className="page-header">
        <div className="header-meta">
          <span className="section-tag">Public Transparency Portal</span>
          <h1 className="page-title">Contractor Billing & Invoices Ledger</h1>
          <p className="page-subtitle">
            Publicly disclosed itemized contractor invoices, unit rates, material quantities, and disbursement status.
          </p>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="card stat-card">
          <div className="stat-label">Disclosed Invoices</div>
          <div className="stat-value">{billings.length}</div>
        </div>
        <div className="card stat-card">
          <div className="stat-label">Total Disbursed Volume</div>
          <div className="stat-value">₹{(totalFilteredAmount / 100000).toFixed(2)} Lakh</div>
        </div>
        <div className="card stat-card">
          <div className="stat-label">Active Contractors</div>
          <div className="stat-value">{new Set(billings.map(b => b.contractor_name)).size}</div>
        </div>
      </div>

      <div className="card filter-card">
        <div className="filter-group">
          <div className="search-input-wrap">
            <Search size={16} className="search-icon" />
            <input 
              type="text" 
              placeholder="Search contractor, invoice #, item, or project ID..." 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="filter-search"
            />
          </div>

          <div className="select-wrap">
            <label>Item Category:</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)}>
              {categories.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
        </div>
      </div>

      <div className="card table-card">
        <div className="card-header-bar">
          <h3>Itemized Billing Ledger</h3>
          <span className="record-count">{filtered.length} Invoices Recorded</span>
        </div>

        <div className="ledger-table-wrap">
          <table className="ledger-table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Project</th>
                <th>Contractor & GSTIN</th>
                <th>Item Description</th>
                <th>Qty / Unit</th>
                <th>Billed Unit Rate</th>
                <th>Standard Benchmark</th>
                <th>Total Billed</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(b => {
                const billedRate = Number(b.unit_rate || 0);
                const benchmarkRate = Number(b.benchmark_rate || 0);
                const devPct = Number(b.deviation_pct || 0);
                const isOutlier = b.is_anomaly;

                return (
                  <tr key={b.invoice_no + b.item_description} className={isInvestigator && isOutlier ? 'anomaly-row' : ''}>
                    <td className="mono bold">{b.invoice_no}</td>
                    <td className="mono">{b.project_id}</td>
                    <td>
                      <div className="contractor-cell">
                        <strong>{b.contractor_name}</strong>
                        <span className="gstin-sub">{b.gstin}</span>
                      </div>
                    </td>
                    <td>
                      <div className="item-cell">
                        <span className="item-name">{b.item_description}</span>
                        <span className="category-sub">{b.category}</span>
                      </div>
                    </td>
                    <td>{b.quantity} {b.unit}</td>
                    <td className="bold">₹{billedRate.toLocaleString()}</td>
                    <td className="benchmark-val">
                      {benchmarkRate > 0 ? `₹${benchmarkRate.toLocaleString()}` : 'N/A'}
                    </td>
                    <td className="bold highlight-amount">₹{Number(b.total_amount || 0).toLocaleString()}</td>
                    <td>{b.billing_date}</td>
                    <td>
                      {b.status === 'PAID' ? (
                        <span className="badge low-risk">Paid</span>
                      ) : b.status === 'APPROVED' ? (
                        <span className="badge medium-risk">Approved</span>
                      ) : (
                        <span className="badge high-risk">Under Review</span>
                      )}

                      {isInvestigator && isOutlier && (
                        <div className="table-anomaly-tag">
                          <AlertCircle size={10} /> +{devPct}% vs SoR
                        </div>
                      )}
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

export default ContractorBillings;
