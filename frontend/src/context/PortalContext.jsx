import { createContext, useContext, useState, useEffect } from 'react';

const PortalContext = createContext();

export const PortalProvider = ({ children }) => {
  // 'public' or 'investigator'
  const [mode, setMode] = useState(() => {
    return localStorage.getItem('portal_mode') || 'public';
  });

  const toggleMode = () => {
    const nextMode = mode === 'public' ? 'investigator' : 'public';
    setMode(nextMode);
    localStorage.setItem('portal_mode', nextMode);
  };

  return (
    <PortalContext.Provider value={{ mode, setMode, toggleMode, isInvestigator: mode === 'investigator' }}>
      {children}
    </PortalContext.Provider>
  );
};

export const usePortal = () => useContext(PortalContext);
