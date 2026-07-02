import type { TaskStatus, UserRole } from '../../api/types';
import './Badge.css';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'accent' | 'pending' | 'progress' | 'completed' | 'admin' | 'user';
}

export function Badge({ children, variant = 'default' }: BadgeProps) {
  return <span className={`badge badge-${variant}`}>{children}</span>;
}

export function statusVariant(status: TaskStatus): BadgeProps['variant'] {
  if (status === 'in_progress') return 'progress';
  if (status === 'completed') return 'completed';
  return 'pending';
}

export function roleVariant(role: UserRole): BadgeProps['variant'] {
  return role === 'admin' ? 'admin' : 'user';
}

export function statusLabel(status: TaskStatus): string {
  if (status === 'in_progress') return 'In Progress';
  if (status === 'completed') return 'Completed';
  return 'Pending';
}
