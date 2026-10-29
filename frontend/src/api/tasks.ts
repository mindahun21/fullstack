import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api';

export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE';

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: TaskStatus;
  created_at?: string;
  updated_at?: string;
}

export interface TaskPayload {
  title: string;
  description?: string;
  status?: TaskStatus;
}

export const taskApi = {
  getAll: async (): Promise<Task[]> => {
    const res = await axios.get<Task[]>(`${API_BASE_URL}/tasks`);
    return res.data;
  },

  getById: async (id: number): Promise<Task> => {
    const res = await axios.get<Task>(`${API_BASE_URL}/tasks/${id}`);
    return res.data;
  },

  create: async (payload: TaskPayload): Promise<Task> => {
    const res = await axios.post<Task>(`${API_BASE_URL}/tasks`, payload);
    return res.data;
  },

  update: async (id: number, payload: TaskPayload): Promise<Task> => {
    const res = await axios.put<Task>(`${API_BASE_URL}/tasks/${id}`, payload);
    return res.data;
  },

  delete: async (id: number): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/tasks/${id}`);
  },
};
