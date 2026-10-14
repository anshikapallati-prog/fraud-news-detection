/**
 * TruthLens AI — Result Card Component
 * Displays the main classification result with explanation.
 */

import { motion } from "framer-motion";
import {
  ShieldCheck,
  ShieldAlert,
  ShieldQuestion,
  Copy,
  RefreshCw,
  Clock,
  WifiOff,
} from "lucide-react";
import { useState } from "react";
import type { AnalysisResult, Classification } from "../types";

interface ResultCardProps {
  result: AnalysisResult;
  timestamp?: string;
  onAnalyzeAnother: () => void;
}

function getStatusConfig(classification: Classification) {
  switch (classification) {
    case "Likely Real":
      return {
        icon: ShieldCheck,
        className: "status-real",
        borderClass: "border-status-green/30",
        label: "Likely Real",
        description: "This text shows characteristics typically found in legitimate news reporting.",
      };
    case "Likely Fake":
      return {
        icon: ShieldAlert,
        className: "status-fake",
        borderClass: "border-status-red/30",
        label: "Likely Fake",
        description: "This text contains patterns commonly associated with misinformation.",
      };
    default:
      return {
        icon: ShieldQuestion,
        className: "status-unverified",
        borderClass: "border-status-amber/30",
        label: "Unverified / Insufficient Evidence",
        description: "There is not enough information to make a reliable determination.",
      };
  }
}

export default function ResultCard({
  result,
  timestamp,
  onAnalyzeAnother,
}: ResultCardProps) {
  const [copied, setCopied] = useState(false);
  const config = getStatusConfig(result.classification);
  const StatusIcon = config.icon;

  async function copyResults() {
    const text = `TruthLens AI Analysis Results
═══════════════════════════════
Classification: ${result.classification}
${result.mode === "offline" ? "Mode: OFFLINE heuristic check (not an AI assessment)\n" : ""}
Explanation: ${result.explanation}

Summary: ${result.summary}

Suspicious Signals:
${result.suspicious_signals.length > 0 ? result.suspicious_signals.map((s) => `  • ${s}`).join("\n") : "  None identified"}

Claims to Verify:
${result.claims_to_verify.length > 0 ? result.claims_to_verify.map((c) => `  • ${c}`).join("\n") : "  None identified"}

Verification Steps:
${result.verification_steps.map((v) => `  • ${v}`).join("\n")}

Limitations:
${result.evidence_limitations.map((e) => `  • ${e}`).join("\n")}

⚠️ Disclaimer: This is an AI-generated assessment, not definitive proof.
Always verify with independent, reputable sources.
${timestamp ? `\nAnalysis Date: ${new Date(timestamp).toLocaleString()}` : ""}`;

    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard not available
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`glass-card p-6 sm:p-8 space-y-6 border ${config.borderClass}`}
    >
      {/* Offline banner — never present a heuristic result as AI output */}
      {result.mode === "offline" && (
        <div
          role="note"
          className="flex items-start gap-3 px-4 py-3 rounded-xl bg-status-amber/[0.08] border border-status-amber/25"
        >
          <WifiOff className="w-4 h-4 text-status-amber flex-shrink-0 mt-0.5" />
          <p className="text-xs text-slate-300 leading-relaxed">
            <strong className="text-status-amber font-semibold">
              Offline heuristic check.
            </strong>{" "}
            The AI service was unreachable (missing or invalid Groq key), so
            this assessment comes from local text-pattern rules — not the
            language model. Add a valid key in{" "}
            <code className="text-slate-200">backend/.env</code> for full AI
            analysis.
          </p>
        </div>
      )}

      {/* Classification badge */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${config.className} border`}>
            <StatusIcon className="w-7 h-7" />
          </div>
          <div>
            <div className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">
              Assessment
            </div>
            <h3 className={`text-xl sm:text-2xl font-bold ${config.className.includes("real") ? "text-status-green" : config.className.includes("fake") ? "text-status-red" : "text-status-amber"}`}>
              {config.label}
            </h3>
          </div>
        </div>

        {/* Timestamp */}
        {timestamp && (
          <div className="flex items-center gap-1.5 text-xs text-slate-500">
            <Clock className="w-3 h-3" />
            {new Date(timestamp).toLocaleString()}
          </div>
        )}
      </div>

      {/* Explanation */}
      <div className="space-y-2">
        <h4 className="text-sm font-semibold text-slate-300">Explanation</h4>
        <p className="text-sm text-slate-400 leading-relaxed">{result.explanation}</p>
      </div>

      {/* Summary */}
      <div className="space-y-2">
        <h4 className="text-sm font-semibold text-slate-300">Article Summary</h4>
        <p className="text-sm text-slate-400 leading-relaxed">{result.summary}</p>
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3 pt-2">
        <button
          onClick={onAnalyzeAnother}
          className="btn-primary !py-2 !px-5 !text-sm"
          aria-label="Analyze another article"
        >
          <RefreshCw className="w-4 h-4" /> Analyze Another
        </button>
        <button
          onClick={copyResults}
          className="btn-secondary !py-2 !px-5 !text-sm"
          aria-label="Copy results to clipboard"
        >
          <Copy className="w-4 h-4" /> {copied ? "Copied!" : "Copy Results"}
        </button>
      </div>

      {/* Disclaimer */}
      <p className="text-xs text-slate-500 pt-2 border-t border-white/[0.06]">
        ⚠️ This is an AI-generated assessment based on text-pattern analysis.
        It is not definitive proof of truth or falsehood. Always verify with
        independent, reputable sources.
      </p>
    </motion.div>
  );
}
