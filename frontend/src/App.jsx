import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Bots from './pages/Bots.jsx';
import Content from './pages/Content.jsx';
import Niches from './pages/Niches.jsx';
import Schedule from './pages/Schedule.jsx';
import Analytics from './pages/Analytics.jsx';
import Settings from './pages/Settings.jsx';
import { niches as nichesApi, system } from './api.js';
import { useStore } from './store.js';

export default function App() {
  const setNiches = useStore(s => s.setNiches);
  const setSystemStats = useStore(s => s.setSystemStats);

  useEffect(() => {
    async function init() {
      try {
        const [n, s] = await Promise.all([nichesApi.list(), system.stats()]);
        setNiches(n);
        setSystemStats(s);
      } catch (e) {
        console.error('Init failed:', e);
      }
    }
    init();
    const interval = setInterval(init, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <BrowserRouter>
      <Toaster
        position="bottom-right"
        toastOptions={{
          style: { background: '#1a1a1a', color: '#fff', border: '1px solid #333', fontFamily: 'monospace', fontSize: '13px' },
          success: { iconTheme: { primary: '#00ff88', secondary: '#000' } },
          error: { iconTheme: { primary: '#ff4444', secondary: '#000' } },
        }}
      />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="bots" element={<Bots />} />
          <Route path="content" element={<Content />} />
          <Route path="niches" element={<Niches />} />
          <Route path="schedule" element={<Schedule />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
