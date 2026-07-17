import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppShell } from './components/layout/AppShell';
import { LandingView } from './views/Landing';
import { LoginView } from './views/Auth';
import { DashboardView } from './views/Dashboard';
import { ScanView } from './views/Scan';
import { MigrateView } from './views/Migrate';
import { useAuthStore } from './stores/useAuthStore';
import { useEndpointStore } from './stores/useEndpointStore';

function App() {
  const { isAuthenticated } = useAuthStore();
  const { stats } = useEndpointStore();

  return (
    <BrowserRouter>
      {!isAuthenticated ? (
        <Routes>
          <Route path="/" element={<LandingView />} />
          <Route path="/login" element={<LoginView />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      ) : (
        <AppShell stats={stats}>
          <Routes>
            <Route path="/" element={<DashboardView />} />
            <Route path="/scan" element={<ScanView />} />
            <Route path="/migrate" element={<MigrateView />} />
            <Route path="/login" element={<Navigate to="/" replace />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AppShell>
      )}
    </BrowserRouter>
  );
}

export default App;
