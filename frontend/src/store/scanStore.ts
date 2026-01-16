import { create } from "zustand";
import { scansApi } from "../api/scans";
import type { ScanResponse, ScanSummary } from "../types";

interface ScanState {
  currentScan: ScanResponse | null;
  scanHistory: ScanSummary[];
  loading: boolean;
  error: string | null;
  fetchScans: () => Promise<void>;
  createScan: (request: any) => Promise<ScanResponse>;
  getScan: (runId: string) => Promise<void>;
  clearError: () => void;
}

export const useScanStore = create<ScanState>((set, get) => ({
  currentScan: null,
  scanHistory: [],
  loading: false,
  error: null,

  fetchScans: async () => {
    set({ loading: true, error: null });
    try {
      const response = await scansApi.listScans();
      set({ scanHistory: response.scans, loading: false });
    } catch (error: any) {
      set({ error: error.message || "Failed to fetch scans", loading: false });
    }
  },

  createScan: async (request) => {
    set({ loading: true, error: null });
    try {
      const scan = await scansApi.createScan(request);
      set({ currentScan: scan, loading: false });
      // Refresh history
      await get().fetchScans();
      return scan;
    } catch (error: any) {
      set({ error: error.message || "Failed to create scan", loading: false });
      throw error;
    }
  },

  getScan: async (runId: string) => {
    set({ loading: true, error: null });
    try {
      const scan = await scansApi.getScan(runId);
      set({ currentScan: scan, loading: false });
    } catch (error: any) {
      set({ error: error.message || "Failed to fetch scan", loading: false });
    }
  },

  clearError: () => set({ error: null }),
}));

