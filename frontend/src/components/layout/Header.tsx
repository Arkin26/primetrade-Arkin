import { Badge, roleVariant } from '../ui/Badge';
import { Button } from '../ui/Button';
import { useAuth } from '../../context/AuthContext';
import './Header.css';

interface HeaderProps {
  activeTab: 'tasks' | 'admin';
  onTabChange: (tab: 'tasks' | 'admin') => void;
}

export function Header({ activeTab, onTabChange }: HeaderProps) {
  const { user, logout, isAdmin } = useAuth();

  const initials = user?.email?.slice(0, 2).toUpperCase() ?? '??';

  return (
    <header className="header">
      <div className="header-brand">
        <div className="header-logo">Primetrade</div>
        <div className="header-tagline">Task management dashboard</div>
      </div>

      <div className="header-actions">
        <nav className="header-nav">
          <button
            type="button"
            className={`header-nav-item ${activeTab === 'tasks' ? 'active' : ''}`}
            onClick={() => onTabChange('tasks')}
          >
            Tasks
          </button>
          {isAdmin && (
            <button
              type="button"
              className={`header-nav-item ${activeTab === 'admin' ? 'active' : ''}`}
              onClick={() => onTabChange('admin')}
            >
              Admin
            </button>
          )}
        </nav>

        <div className="header-user">
          <div className="header-avatar">{initials}</div>
          <span className="header-email">{user?.email}</span>
          {user && <Badge variant={roleVariant(user.role)}>{user.role}</Badge>}
        </div>

        <Button variant="secondary" size="sm" onClick={logout}>
          Log out
        </Button>
      </div>
    </header>
  );
}
