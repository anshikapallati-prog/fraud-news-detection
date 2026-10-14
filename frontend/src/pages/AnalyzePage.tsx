/**
 * TruthLens AI — Analyze Page
 * Main analysis dashboard with input, loading, results, and error states.
 */

import { useState } from "react";
import { motion } from "framer-motion";
import { Shield, AlertCircle } from "lucide-react";
import NewsInput from "../components/NewsInput";
import AnalysisLoader from "../components/AnalysisLoader";
import ResultCard from "../components/ResultCard";
import SuspiciousSignals from "../components/SuspiciousSignals";
import ClaimList from "../components/ClaimList";
import VerificationSteps from "../components/VerificationSteps";
import { analyzeNews } from "../api/client";
import { saveToHistory } from "../utils/localStorage";
import type { AnalysisResult } from "../types";

type PageState = "input" | "loading" | "results" | "error";

export default function AnalyzePage() {
  const [state, setState] = useState<PageState>("input");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [timestamp, setTimestamp] = useState("");

  async function handleSubmit(text: string) {
    setState("loading");
    setError("");
    setResult(null);

    try {
      const analysisResult = await analyzeNews(text);
      setResult(analysisResult);
      setTimestamp(new Date().toISOString());
      setState("results");

      // Save to history
      saveToHistory(text, analysisResult);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "An unexpected error occurred. Please try again.";
      setError(message);
      setState("error");
    }
  }

  function handleAnalyzeAnother() {
    setState("input");
    setResult(null);
    setError("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Page header */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="text-center mb-10"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <Shield className="w-8 h-8 text-brand-cyan" />
            <h1 className="text-3xl sm:text-4xl font-bold text-white">
              News <span className="gradient-text">Analyzer</span>
            </h1>
          </div>
          <p className="text-slate-400 max-w-xl mx-auto">
            Paste any news headline, article, or social media post below. Our AI
            will analyze it for potential misinformation patterns and provide
            verification guidance.
          </p>
        </motion.div>

        {/* Main content */}
        <div className="space-y-6">
          {/* Input — always visible when in input state */}
          {state === "input" && (
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.1 }}
            >
              <NewsInput onSubmit={handleSubmit} isLoading={false} />
            </motion.div>
          )}

          {/* Loading state */}
          {state === "loading" && <AnalysisLoader />}

          {/* Error state */}
          {state === "error" && (
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              <div className="glass-card p-6 sm:p-8 border border-status-red/20">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-xl bg-status-red/10 flex items-center justify-center flex-shrink-0">
                    <AlertCircle className="w-6 h-6 text-status-red" />
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-lg font-semibold text-white">
                      Analysis Failed
                    </h3>
                    <p className="text-sm text-slate-400">{error}</p>
                    <button
                      onClick={handleAnalyzeAnother}
                      className="btn-primary !py-2 !px-5 !text-sm mt-3"
                    >
                      Try Again
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Results state */}
          {state === "results" && result && (
            <div className="space-y-6">
              <ResultCard
                result={result}
                timestamp={timestamp}
                onAnalyzeAnother={handleAnalyzeAnother}
              />
              <div className="grid md:grid-cols-2 gap-6">
                <SuspiciousSignals signals={result.suspicious_signals} />
                <ClaimList claims={result.claims_to_verify} />
              </div>
              <VerificationSteps
                steps={result.verification_steps}
                limitations={result.evidence_limitations}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
