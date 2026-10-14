/**
 * TruthLens AI — LocalStorage Utilities
 * Manages analysis history in the browser.
 */

import type { AnalysisHistoryItem, AnalysisResult, Classification } from "../types";

const STORAGE_KEY = "truthlens_history";
const MAX_HISTORY_ITEMS = 20;

const VALID_CLASSIFICATIONS: Classification[] = [
  "Likely Real",
  "Likely Fake",
  "Unverified / Insufficient Evidence",
];

/**
 * Validate an unknown value parsed from localStorage.
 * Corrupted or foreign data is discarded instead of crashing the UI.
 */
function isValidHistoryItem(value: unknown): value is AnalysisHistoryItem {
  if (typeof value !== "object" || value === null) return false;
  const item = value as Record<string, unknown>;
  if (typeof item.id !== "string" || item.id.length === 0) return false;
  if (typeof item.timestamp !== "string") return false;
  if (typeof item.inputPreview !== "string") return false;
  if (!VALID_CLASSIFICATIONS.includes(item.classification as Classification)) {
    return false;
  }
  const result = item.result as Record<string, unknown> | null;
  if (typeof result !== "object" || result === null) return false;
  if (!VALID_CLASSIFICATIONS.includes(result.classification as Classification)) {
    return false;
  }
  for (const key of ["explanation", "summary"] as const) {
    if (typeof result[key] !== "string") return false;
  }
  for (const key of [
    "suspicious_signals",
    "claims_to_verify",
    "verification_steps",
    "evidence_limitations",
  ] as const) {
    if (!Array.isArray(result[key])) return false;
  }
  return true;
}

/**
 * Generate a simple unique ID.
 */
function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substring(2, 9);
}

/**
 * Retrieve all history items from localStorage.
 */
export function getHistory(): AnalysisHistoryItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    // Drop corrupted entries; cap length as a safety net.
    return parsed.filter(isValidHistoryItem).slice(0, MAX_HISTORY_ITEMS);
  } catch {
    return [];
  }
}

/**
 * Save a new analysis result to history.
 * Stores only a preview of the input text (first 120 chars).
 */
export function saveToHistory(
  inputText: string,
  result: AnalysisResult
): AnalysisHistoryItem {
  const history = getHistory();

  const item: AnalysisHistoryItem = {
    id: generateId(),
    timestamp: new Date().toISOString(),
    inputPreview: inputText.substring(0, 120) + (inputText.length > 120 ? "…" : ""),
    classification: result.classification,
    result,
  };

  // Add to front, cap at MAX
  history.unshift(item);
  if (history.length > MAX_HISTORY_ITEMS) {
    history.pop();
  }

  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  return item;
}

/**
 * Delete a single history item by ID.
 */
export function deleteHistoryItem(id: string): void {
  const history = getHistory().filter((item) => item.id !== id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

/**
 * Clear all history.
 */
export function clearHistory(): void {
  localStorage.removeItem(STORAGE_KEY);
}
