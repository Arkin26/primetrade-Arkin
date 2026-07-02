import { useEffect, useState } from 'react';
import { api, ApiClientError } from '../../api/client';
import type { User, UserRole } from '../../api/types';
import { Badge, roleVariant } from '../ui/Badge';
import { useToast } from '../ui/Toast';
import { useAuth } from '../../context/AuthContext';
import './AdminPanel.css';

export function AdminPanel() {
  const { token } = useAuth();
  const { showSuccess, showError } = useToast();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  const loadUsers = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const data = await api.getUsers(token);
      setUsers(data);
    } catch (err) {
      showError(
        'Failed to load users',
        err instanceof ApiClientError ? err.message : 'Unknown error',
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, [token]);

  const handleRoleChange = async (userId: string, role: UserRole) => {
    if (!token) return;
    try {
      const updated = await api.updateUserRole(token, userId, role);
      setUsers((prev) => prev.map((u) => (u.id === userId ? updated : u)));
      showSuccess('Role updated', `User role changed to ${role}.`);
    } catch (err) {
      showError(
        'Update failed',
        err instanceof ApiClientError ? err.message : 'Unknown error',
      );
    }
  };

  if (loading) {
    return <p style={{ color: 'var(--text-secondary)' }}>Loading users...</p>;
  }

  return (
    <div className="admin-table-wrap">
      <table className="admin-table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Joined</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.email}</td>
              <td>
                <Badge variant={roleVariant(user.role)}>{user.role}</Badge>
              </td>
              <td>{user.is_active ? 'Active' : 'Inactive'}</td>
              <td>{new Date(user.created_at).toLocaleDateString()}</td>
              <td>
                <select
                  className="admin-role-select"
                  value={user.role}
                  onChange={(e) => handleRoleChange(user.id, e.target.value as UserRole)}
                >
                  <option value="user">user</option>
                  <option value="admin">admin</option>
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
