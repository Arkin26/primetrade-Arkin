import { useEffect, useState, type FormEvent } from 'react';
import { api, ApiClientError } from '../api/client';
import type { Task, TaskStatus } from '../api/types';
import { AdminPanel } from '../components/admin/AdminPanel';
import { Header } from '../components/layout/Header';
import { Badge, statusLabel, statusVariant } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { Input, Select, Textarea } from '../components/ui/Input';
import { useToast } from '../components/ui/Toast';
import { useAuth } from '../context/AuthContext';
import './DashboardPage.css';

const FILTERS: { label: string; value: TaskStatus | 'all' }[] = [
  { label: 'All', value: 'all' },
  { label: 'Pending', value: 'pending' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' },
];

const emptyForm = { title: '', description: '', status: 'pending' as TaskStatus };

export function DashboardPage() {
  const { token } = useAuth();
  const { showSuccess, showError } = useToast();
  const [activeTab, setActiveTab] = useState<'tasks' | 'admin'>('tasks');
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<TaskStatus | 'all'>('all');
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const loadTasks = async () => {
    if (!token) return;
    setLoading(true);
    try {
      const data = await api.getTasks(token);
      setTasks(data.items);
    } catch (err) {
      showError(
        'Failed to load tasks',
        err instanceof ApiClientError ? err.message : 'Unknown error',
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, [token]);

  const filteredTasks =
    filter === 'all' ? tasks : tasks.filter((t) => t.status === filter);

  const stats = {
    total: tasks.length,
    pending: tasks.filter((t) => t.status === 'pending').length,
    completed: tasks.filter((t) => t.status === 'completed').length,
  };

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };

  const handleEdit = (task: Task) => {
    setEditingId(task.id);
    setForm({
      title: task.title,
      description: task.description ?? '',
      status: task.status,
    });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!token) return;
    setSubmitting(true);
    try {
      if (editingId) {
        await api.updateTask(token, editingId, {
          title: form.title,
          description: form.description || undefined,
          status: form.status,
        });
        showSuccess('Task updated', 'Your changes have been saved.');
      } else {
        await api.createTask(token, {
          title: form.title,
          description: form.description || undefined,
          status: form.status,
        });
        showSuccess('Task created', 'A new task has been added.');
      }
      resetForm();
      await loadTasks();
    } catch (err) {
      showError(
        editingId ? 'Update failed' : 'Create failed',
        err instanceof ApiClientError ? err.message : 'Unknown error',
      );
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!token) return;
    if (!window.confirm('Delete this task?')) return;
    try {
      await api.deleteTask(token, id);
      showSuccess('Task deleted', 'The task has been removed.');
      if (editingId === id) resetForm();
      await loadTasks();
    } catch (err) {
      showError(
        'Delete failed',
        err instanceof ApiClientError ? err.message : 'Unknown error',
      );
    }
  };

  return (
    <div className="page">
      <div className="page-inner">
        <Header activeTab={activeTab} onTabChange={setActiveTab} />

        {activeTab === 'admin' ? (
          <Card title="User management" subtitle="View users and update roles (admin only).">
            <AdminPanel />
          </Card>
        ) : (
          <>
            <div className="dashboard-stats">
              <div className="stat-card">
                <div className="stat-value">{stats.total}</div>
                <div className="stat-label">Total tasks</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{stats.pending}</div>
                <div className="stat-label">Pending</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{stats.completed}</div>
                <div className="stat-label">Completed</div>
              </div>
            </div>

            <div className="dashboard-grid">
              <Card
                title={editingId ? 'Edit task' : 'New task'}
                subtitle={editingId ? 'Update task details below.' : 'Create a new task to get started.'}
                muted
              >
                <form className="task-form" onSubmit={handleSubmit}>
                  <Input
                    label="Title"
                    placeholder="What needs to be done?"
                    value={form.title}
                    onChange={(e) => setForm({ ...form, title: e.target.value })}
                    required
                  />
                  <Textarea
                    label="Description"
                    placeholder="Optional details..."
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                  />
                  <Select
                    label="Status"
                    value={form.status}
                    onChange={(e) =>
                      setForm({ ...form, status: e.target.value as TaskStatus })
                    }
                  >
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                  </Select>
                  <div className="task-form-actions">
                    {editingId && (
                      <Button type="button" variant="secondary" onClick={resetForm}>
                        Cancel
                      </Button>
                    )}
                    <Button type="submit" disabled={submitting}>
                      {submitting ? 'Saving...' : editingId ? 'Save changes' : 'Add task'}
                    </Button>
                  </div>
                </form>
              </Card>

              <div>
                <div className="task-filters">
                  {FILTERS.map((f) => (
                    <button
                      key={f.value}
                      type="button"
                      className={`filter-pill ${filter === f.value ? 'active' : ''}`}
                      onClick={() => setFilter(f.value)}
                    >
                      {f.label}
                    </button>
                  ))}
                </div>

                {loading ? (
                  <p style={{ color: 'var(--text-secondary)' }}>Loading tasks...</p>
                ) : filteredTasks.length === 0 ? (
                  <div className="task-empty">
                    <h3>No tasks yet</h3>
                    <p>Create your first task using the form on the left.</p>
                  </div>
                ) : (
                  <div className="task-list">
                    {filteredTasks.map((task) => (
                      <div key={task.id} className="task-item">
                        <div className="task-item-content">
                          <div className="task-item-title">{task.title}</div>
                          {task.description && (
                            <div className="task-item-desc">{task.description}</div>
                          )}
                          <div className="task-item-meta">
                            <Badge variant={statusVariant(task.status)}>
                              {statusLabel(task.status)}
                            </Badge>
                            <span className="task-item-date">
                              {new Date(task.created_at).toLocaleDateString()}
                            </span>
                          </div>
                        </div>
                        <div className="task-item-actions">
                          <Button variant="secondary" size="sm" onClick={() => handleEdit(task)}>
                            Edit
                          </Button>
                          <Button variant="tertiary" size="sm" onClick={() => handleDelete(task.id)}>
                            Delete
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
