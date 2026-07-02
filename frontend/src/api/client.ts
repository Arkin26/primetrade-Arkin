import type {
  ApiError,
  AuthResponse,
  PaginatedTasks,
  RegisterResponse,
  Task,
  TaskStatus,
  User,
  UserRole,
} from './types';

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export class ApiClientError extends Error {
  code: string;
  status: number;
  details?: { field: string; message: string }[] | null;

  constructor(message: string, code: string, status: number, details?: ApiError['error']['details']) {
    super(message);
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null,
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 204) {
    return undefined as T;
  }

  const data = await response.json();

  if (!response.ok) {
    const err = data as ApiError;
    throw new ApiClientError(
      err.error?.message ?? 'Something went wrong',
      err.error?.code ?? 'HTTP_ERROR',
      response.status,
      err.error?.details,
    );
  }

  return data as T;
}

export const api = {
  register: (email: string, password: string) =>
    request<RegisterResponse>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  login: (email: string, password: string) =>
    request<AuthResponse>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  me: (token: string) => request<User>('/api/v1/auth/me', {}, token),

  getTasks: (token: string, page = 1, limit = 20) =>
    request<PaginatedTasks>(`/api/v1/tasks?page=${page}&limit=${limit}`, {}, token),

  createTask: (
    token: string,
    data: { title: string; description?: string; status?: TaskStatus },
  ) =>
    request<Task>('/api/v1/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    }, token),

  updateTask: (
    token: string,
    id: string,
    data: { title?: string; description?: string; status?: TaskStatus },
  ) =>
    request<Task>(`/api/v1/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }, token),

  deleteTask: (token: string, id: string) =>
    request<void>(`/api/v1/tasks/${id}`, { method: 'DELETE' }, token),

  getUsers: (token: string) => request<User[]>('/api/v1/users', {}, token),

  updateUserRole: (token: string, userId: string, role: UserRole) =>
    request<User>(`/api/v1/users/${userId}/role`, {
      method: 'PATCH',
      body: JSON.stringify({ role }),
    }, token),
};
