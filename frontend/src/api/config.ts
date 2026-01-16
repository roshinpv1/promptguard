import { apiClient } from "./client";
import type { ConfigResponse, ConfigUpdateRequest } from "../types";

export const configApi = {
  getConfig: async (): Promise<ConfigResponse> => {
    const response = await apiClient.get<ConfigResponse>("/api/v1/config");
    return response.data;
  },

  updateConfig: async (request: ConfigUpdateRequest): Promise<ConfigResponse> => {
    const response = await apiClient.put<ConfigResponse>("/api/v1/config", request);
    return response.data;
  },

  validateConfig: async (configYaml: string): Promise<{ valid: boolean; error?: string }> => {
    const response = await apiClient.post("/api/v1/config/validate", configYaml, {
      headers: { "Content-Type": "text/plain" },
    });
    return response.data;
  },
};

