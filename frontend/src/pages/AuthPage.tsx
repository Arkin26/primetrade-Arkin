import { useState, type FormEvent } from 'react';
import { Navigate } from 'react-router-dom';
import { ApiClientError } from '../api/client';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { useToast } from '../components/ui/Toast';
import { useAuth } from '../context/AuthContext';
import './AuthPage.css';

type Mode = 'login' | 'register';

export function AuthPage() {
  const { user, loading, login, register } = useAuth();
  const { showSuccess, showError } = useToast();
  const [mode, setMode] = useState<Mode>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (loading) {
    return null;
  }

  if (user) {
    return <Navigate to="/dashboard" replace />;
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      if (mode === 'login') {
        await login(email, password);
        showSuccess('Welcome back', 'You have been signed in successfully.');
      } else {
        await register(email, password);
        showSuccess('Account created', 'Your account is ready to use.');
      }
    } catch (err) {
      const message =
        err instanceof ApiClientError
          ? err.message
          : 'Something went wrong. Please try again.';
      showError(mode === 'login' ? 'Login failed' : 'Registration failed', message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-hero">
        <h1>Manage tasks with clarity</h1>
        <p>
          A clean workspace for your assignments. Register, sign in, and manage tasks
          with role-based access built in.
        </p>
        <div className="auth-hero-tags">
          <Badge variant="accent">JWT Auth</Badge>
          <Badge>RBAC</Badge>
          <Badge>REST API</Badge>
        </div>
      </div>

      <div className="auth-panel">
        <div className="auth-card">
          <div className="auth-tabs">
            <button
              type="button"
              className={`auth-tab ${mode === 'login' ? 'active' : ''}`}
              onClick={() => setMode('login')}
            >
              Sign in
            </button>
            <button
              type="button"
              className={`auth-tab ${mode === 'register' ? 'active' : ''}`}
              onClick={() => setMode('register')}
            >
              Register
            </button>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div>
              <h2 className="auth-form-title">
                {mode === 'login' ? 'Welcome back' : 'Create account'}
              </h2>
              <p className="auth-form-subtitle">
                {mode === 'login'
                  ? 'Enter your credentials to access your dashboard.'
                  : 'Sign up to start managing your tasks.'}
              </p>
            </div>

            <Input
              label="Email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />

            <Input
              label="Password"
              type="password"
              placeholder="Min. 8 characters"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
            />

            <Button type="submit" disabled={submitting} style={{ width: '100%' }}>
              {submitting
                ? 'Please wait...'
                : mode === 'login'
                  ? 'Sign in'
                  : 'Create account'}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
