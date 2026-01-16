import { apiClient } from "./client";
import type { TestAPIRequest, TestAPIResponse } from "../types";

export const testApi = {
  testExternalAPI: async (request: TestAPIRequest): Promise<TestAPIResponse> => {
    const response = await apiClient.post<TestAPIResponse>("/api/v1/test-api", request);
    return response.data;
  },
};

