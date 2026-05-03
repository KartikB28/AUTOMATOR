import { create } from 'zustand';

export const useStore = create((set, get) => ({
  botStatus: {},
  setBotStatus: (status) => set({ botStatus: status }),

  niches: [],
  setNiches: (niches) => set({ niches }),
  selectedNicheId: null,
  setSelectedNicheId: (id) => set({ selectedNicheId: id }),

  systemStats: null,
  setSystemStats: (stats) => set({ systemStats: stats }),

  apiSettings: null,
  setApiSettings: (s) => set({ apiSettings: s }),
}));
