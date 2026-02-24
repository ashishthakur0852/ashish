import { create } from 'zustand';

export type ReportRole = 'operations' | 'compliance' | 'executive' | 'ship_officer';

interface ReportState {
  role: ReportRole;
  darkMode: boolean;
  selectedDataset: string;
  selectedColumns: string[];
  setRole: (role: ReportRole) => void;
  toggleDarkMode: () => void;
  setDataset: (dataset: string) => void;
  setColumns: (columns: string[]) => void;
}

export const useReportStore = create<ReportState>((set) => ({
  role: 'operations',
  darkMode: false,
  selectedDataset: 'fleet_performance',
  selectedColumns: ['vessel_name', 'voyage_code', 'voyage_hours', 'cargo_tonnage'],
  setRole: (role) => set({ role }),
  toggleDarkMode: () => set((s) => ({ darkMode: !s.darkMode })),
  setDataset: (selectedDataset) => set({ selectedDataset }),
  setColumns: (selectedColumns) => set({ selectedColumns }),
}));
