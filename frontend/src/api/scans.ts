import { apiClient } from "./client";
import type { ScanRequest, ScanResponse, ScanListResponse } from "../types";

export const scansApi = {
  createScan: async (request: ScanRequest): Promise<ScanResponse> => {
    const response = await apiClient.post<ScanResponse>("/api/v1/scans", request);
    return response.data;
  },

  listScans: async (page: number = 1, pageSize: number = 20): Promise<ScanListResponse> => {
    const response = await apiClient.get<ScanListResponse>("/api/v1/scans", {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },

  getScan: async (runId: string): Promise<ScanResponse> => {
    const response = await apiClient.get<ScanResponse>(`/api/v1/scans/${runId}`);
    return response.data;
  },

  getScanResults: async (runId: string): Promise<any> => {
    const response = await apiClient.get(`/api/v1/scans/${runId}/results`);
    return response.data;
  },

  deleteScan: async (runId: string): Promise<void> => {
    await apiClient.delete(`/api/v1/scans/${runId}`);
  },
};

