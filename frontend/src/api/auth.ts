import { apiClient } from './client';
import type { AuthResponse, User } from '@/types';

export const authApi = {
  login: async (username: string, password: string) => {
    const { data } = await apiClient.post<{ data: AuthResponse }>('/api/v1/auth/login', {
      username,
      password,
    });
    return data.data;
  },

  logout: async () => {
    await apiClient.post('/api/v1/auth/logout');
  },

  getCurrentUser: async () => {
    const { data } = await apiClient.get<{ data: User }>('/api/v1/auth/me');
    return data.data;
  },
};
