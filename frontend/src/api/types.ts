export type UserRole = 'user' | 'admin';
export type TaskStatus = 'pending' | 'in_progress' | 'completed';

export interface User {
  id: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface PaginatedTasks {
  items: Task[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterResponse extends AuthResponse {
  user: User;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: { field: string; message: string }[] | null;
  };
}
