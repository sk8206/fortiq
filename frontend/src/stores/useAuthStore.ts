import { create } from 'zustand';
import type { User } from '@/types';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  setToken: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: !!sessionStorage.getItem('access_token'),
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  setToken: (token) => {
    sessionStorage.setItem('access_token', token);
    set({ isAuthenticated: true });
  },
  logout: () => {
    sessionStorage.removeItem('access_token');
    set({ user: null, isAuthenticated: false });
  },
}));
