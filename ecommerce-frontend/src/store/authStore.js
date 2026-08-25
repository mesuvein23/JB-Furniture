import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      access: null,
      refresh: null,

      setAuth: ({ user, access, refresh }) =>
        set({ user, access, refresh }),

      setAccess: (access) => set({ access }),

      logout: () => set({ user: null, access: null, refresh: null }),
    }),
    { name: 'auth-storage' }
  )
);