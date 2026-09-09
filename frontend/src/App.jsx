import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { 
  Home, FolderKanban, FileText, AlertTriangle, 
  Split, Building, Eye, ShieldAlert, Sparkles 
} from 'lucide-react';
import './App.css';

import { PortalProvider, usePortal } from './context/PortalContext';

// Pages
import Overview from './pages/Overview';
import PublicExplorer from './pages/PublicExplorer';
import ProjectDetail from './pages/ProjectDetail';
import ContractorBillings from './pages/ContractorBillings';
import HighRiskQueue from './pages/HighRiskQueue';
import DuplicateDetector from './pages/DuplicateDetector';
import Contractors from './pages/Contractors';

const Sidebar = () => {
  const { pathname } = useLocation();
  const { isInvestigator } = usePortal();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="portal-emblem">MPLADS</div>
        <h2>Project Monitor</h2>
        <span className="subtitle">
          {isInvestigator ? 'Vigilance & Audit Suite' : 'Citizen Transparency Portal'}
        </span>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Public Records</div>
        <Link 
          to="/" 
          className={`nav-item ${pathname === '/' ? 'active' : ''}`}
        >
          <span className="nav-icon"><Home size={18} /></span>
          Overview
        </Link>
        <Link 
          to="/projects" 
          className={`nav-item ${pathname.startsWith('/projects') ? 'active' : ''}`}
        >
          <span className="nav-icon"><FolderKanban size={18} /></span>
          Project Explorer
        </Link>
        <Link 
          to="/billings" 
          className={`nav-item ${pathname === '/billings' ? 'active' : ''}`}
        >
          <span className="nav-icon"><FileText size={18} /></span>
          Contractor Billings
        </Link>
        <Link 
          to="/contractors" 
          className={`nav-item ${pathname === '/contractors' ? 'active' : ''}`}
        >
          <span className="nav-icon"><Building size={18} /></span>
          Agencies & Contractors
        </Link>

        {/* Investigator-Specific Section */}
        {isInvestigator && (
          <>
            <div className="nav-section-label vigilance-label">Vigilance Intelligence</div>
            <Link 
              to="/high-risk" 
              className={`nav-item vigilance-item ${pathname === '/high-risk' ? 'active' : ''}`}
            >
              <span className="nav-icon"><AlertTriangle size={18} /></span>
              High-Risk Queue
            </Link>
            <Link 
              to="/duplicates" 
              className={`nav-item vigilance-item ${pathname === '/duplicates' ? 'active' : ''}`}
            >
              <span className="nav-icon"><Split size={18} /></span>
              Duplicate & Name Detector
            </Link>
          </>
        )}
      </nav>

      <div className="sidebar-footer">
        <div className="jurisdiction-tag">
          Government of India • Ministry of Statistics & Programme Implementation
        </div>
      </div>
    </aside>
  );
};

const Topbar = () => {
  const { mode, toggleMode, isInvestigator } = usePortal();

  return (
    <header className="topbar">
      <div className="portal-badge-group">
        <span className="gov-seal-pill">National MPLAD Transparency Grid</span>
        <span className="system-status-indicator">
          <span className="status-dot"></span> Live Public Feed
        </span>
      </div>

      {/* Mode Switcher */}
      <div className="header-controls">
        <div className="mode-toggle-box">
          <span className="mode-status-text">
            {isInvestigator ? 'Audit Mode Active' : 'Public Access Mode'}
          </span>
          <button 
            onClick={toggleMode} 
            className={`mode-toggle-button ${isInvestigator ? 'investigator-active' : 'public-active'}`}
            title="Toggle between Public Citizen view and Vigilance Investigator view"
          >
            {isInvestigator ? (
              <>
                <ShieldAlert size={15} />
                <span>Investigator View</span>
              </>
            ) : (
              <>
                <Eye size={15} />
                <span>Public View</span>
              </>
            )}
          </button>
        </div>
      </div>
    </header>
  );
};

const Layout = ({ children }) => (
  <div className="app-layout">
    <Sidebar />
    <main className="main-content">
      <Topbar />
      <div className="content-area">
        {children}
      </div>
    </main>
  </div>
);

const AppContent = () => (
  <Router>
    <Layout>
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/projects" element={<PublicExplorer />} />
        <Route path="/projects/:id" element={<ProjectDetail />} />
        <Route path="/billings" element={<ContractorBillings />} />
        <Route path="/high-risk" element={<HighRiskQueue />} />
        <Route path="/duplicates" element={<DuplicateDetector />} />
        <Route path="/contractors" element={<Contractors />} />
      </Routes>
    </Layout>
  </Router>
);

const App = () => (
  <PortalProvider>
    <AppContent />
  </PortalProvider>
);

export default App;
