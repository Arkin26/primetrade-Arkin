import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ProtectedRoute } from './components/ProtectedRoute';
import { ToastProvider } from './components/ui/Toast';
import { AuthProvider } from './context/AuthContext';
import { AuthPage } from './pages/AuthPage';
import { DashboardPage } from './pages/DashboardPage';

export default function App() {
  return (
    <ToastProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<AuthPage />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ToastProvider>
  );
}
