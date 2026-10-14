/**
 * TruthLens AI — API Client
 * Shared Axios instance for backend communication.
 */

import axios from "axios";
import type { AnalysisResult, ApiError } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const TOKEN_KEY = "truthlens_token";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000, // 90 seconds to allow for AI processing
  headers: {
    "Content-Type": "application/json",
  },
});

/* ─── Session token helpers ─────────────────────────────────────────────── */

export function getToken(): string | null {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export function setToken(token: string): void {
  try {
    localStorage.setItem(TOKEN_KEY, token);
  } catch {
    // Storage unavailable (private mode) — session lasts for this tab only.
  }
}

export function clearToken(): void {
  try {
    localStorage.removeItem(TOKEN_KEY);
  } catch {
    // Nothing to clear.
  }
}

// Attach the session token to every request when present.
apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// A 401 from OUR backend always means the session is invalid
// (AI-service failures are mapped to 502, never 401), so drop the token.
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      clearToken();
    }
    return Promise.reject(error);
  }
);

/* ─── Auth API ──────────────────────────────────────────────────────────── */

export interface AuthUser {
  id: number;
  email: string;
  created_at: string;
}

export interface AuthPayload {
  user: AuthUser;
  token: string;
  token_type: string;
}

export async function registerAccount(
  email: string,
  password: string
): Promise<AuthPayload> {
  try {
    const response = await apiClient.post<AuthPayload>("/api/auth/register", {
      email,
      password,
    });
    setToken(response.data.token);
    return response.data;
  } catch (error) {
    throw toFriendlyError(error, "Could not create your account. Please try again.");
  }
}

export async function loginAccount(
  email: string,
  password: string
): Promise<AuthPayload> {
  try {
    const response = await apiClient.post<AuthPayload>("/api/auth/login", {
      email,
      password,
    });
    setToken(response.data.token);
    return response.data;
  } catch (error) {
    throw toFriendlyError(error, "Could not sign you in. Please try again.");
  }
}

export async function fetchCurrentUser(): Promise<AuthUser | null> {
  if (!getToken()) return null;
  try {
    const response = await apiClient.get<AuthUser>("/api/auth/me");
    return response.data;
  } catch {
    clearToken();
    return null;
  }
}

/**
 * Convert an Axios failure into a readable Error.
 * Handles our { error } shape and FastAPI { detail } validation errors.
 */
function toFriendlyError(error: unknown, fallback: string): Error {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      const data = error.response.data as
        | (ApiError & { detail?: unknown })
        | undefined;
      if (data && typeof data.error === "string" && data.error) {
        return new Error(data.error);
      }
      if (typeof data === "string" && data) {
        return new Error(data);
      }
      if (data && typeof data.detail === "string" && data.detail) {
        return new Error(data.detail);
      }
      if (data && Array.isArray(data.detail)) {
        const first = data.detail[0] as { msg?: unknown };
        if (first && typeof first.msg === "string") {
          return new Error(`Invalid input: ${first.msg}`);
        }
      }
      return new Error(`Server error (${error.response.status})`);
    }
    if (error.code === "ECONNABORTED") {
      return new Error("The request timed out. Please try again.");
    }
    return new Error(
      "Could not connect to the TruthLens AI server. Is the backend running?"
    );
  }
  return new Error(fallback);
}

/**
 * Submit news text for AI analysis.
 */
export async function analyzeNews(text: string): Promise<AnalysisResult> {
  try {
    const response = await apiClient.post<AnalysisResult>("/api/analyze", {
      text,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      if (error.response) {
        const data = error.response.data as (ApiError & { detail?: unknown }) | undefined;
        // Our own backend errors: { error: string }
        if (data && typeof data.error === "string" && data.error) {
          throw new Error(data.error);
        }
        // FastAPI validation errors: { detail: [{ msg, ... }] }
        if (data && Array.isArray(data.detail)) {
          const first = data.detail[0] as { msg?: unknown };
          if (first && typeof first.msg === "string") {
            throw new Error(`Invalid input: ${first.msg}`);
          }
        }
        throw new Error(`Server error (${error.response.status})`);
      }
      if (error.code === "ECONNABORTED") {
        throw new Error(
          "The analysis request timed out. Please try again with a shorter text."
        );
      }
      throw new Error(
        "Could not connect to the TruthLens AI server. Is the backend running?"
      );
    }
    throw new Error("An unexpected error occurred. Please try again.");
  }
}

/**
 * Check backend health.
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await apiClient.get("/api/health");
    return response.data.status === "ok";
  } catch {
    return false;
  }
}
