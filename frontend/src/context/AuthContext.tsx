import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';
import { api } from '../api/client';
import type { User } from '../api/types';

const TOKEN_KEY = 'primetrade_token';

interface AuthContextValue {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  isAdmin: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY));
  const [loading, setLoading] = useState(true);

  const persistToken = (value: string | null) => {
    if (value) {
      localStorage.setItem(TOKEN_KEY, value);
    } else {
      localStorage.removeItem(TOKEN_KEY);
    }
    setToken(value);
  };

  const refreshUser = useCallback(async () => {
    const stored = localStorage.getItem(TOKEN_KEY);
    if (!stored) {
      setUser(null);
      return;
    }
    const profile = await api.me(stored);
    setUser(profile);
    setToken(stored);
  }, []);

  useEffect(() => {
    (async () => {
      try {
        if (token) {
          await refreshUser();
        }
      } catch {
        persistToken(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    })();
  }, [token, refreshUser]);

  const login = async (email: string, password: string) => {
    const res = await api.login(email, password);
    persistToken(res.access_token);
    const profile = await api.me(res.access_token);
    setUser(profile);
  };

  const register = async (email: string, password: string) => {
    const res = await api.register(email, password);
    persistToken(res.access_token);
    setUser(res.user);
  };

  const logout = () => {
    persistToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      token,
      loading,
      login,
      register,
      logout,
      refreshUser,
      isAdmin: user?.role === 'admin',
    }),
    [user, token, loading, refreshUser],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
