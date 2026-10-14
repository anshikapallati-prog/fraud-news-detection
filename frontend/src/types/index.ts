/**
 * TruthLens AI — TypeScript Type Definitions
 */

export type Classification =
  | "Likely Real"
  | "Likely Fake"
  | "Unverified / Insufficient Evidence";

export interface AnalysisResult {
  classification: Classification;
  explanation: string;
  summary: string;
  suspicious_signals: string[];
  claims_to_verify: string[];
  verification_steps: string[];
  evidence_limitations: string[];
  /** "ai" = language-model assessment, "offline" = local heuristic fallback. */
  mode?: "ai" | "offline";
}

export interface AnalysisHistoryItem {
  id: string;
  timestamp: string;
  inputPreview: string;
  classification: Classification;
  result: AnalysisResult;
}

export interface ApiError {
  error: string;
  detail?: string | null;
}
