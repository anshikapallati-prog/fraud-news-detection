/**
 * TruthLens AI — History Page
 */

import { useState } from "react";
import { motion } from "framer-motion";
import { Clock } from "lucide-react";
import AnalysisHistory from "../components/AnalysisHistory";
import ResultCard from "../components/ResultCard";
import SuspiciousSignals from "../components/SuspiciousSignals";
import ClaimList from "../components/ClaimList";
import VerificationSteps from "../components/VerificationSteps";
import type { AnalysisHistoryItem } from "../types";

export default function HistoryPage() {
  const [selectedItem, setSelectedItem] = useState<AnalysisHistoryItem | null>(null);

  function handleSelectItem(item: AnalysisHistoryItem) {
    setSelectedItem(item);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function handleBack() {
    setSelectedItem(null);
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
            <Clock className="w-8 h-8 text-brand-cyan" />
            <h1 className="text-3xl sm:text-4xl font-bold text-white">
              Analysis <span className="gradient-text">History</span>
            </h1>
          </div>
          <p className="text-slate-400 max-w-xl mx-auto">
            Your recent analyses are stored locally in your browser. No data is
            sent to any server.
          </p>
        </motion.div>

        {/* Content */}
        {selectedItem ? (
          <div className="space-y-6">
            {/* Back button */}
            <button
              onClick={handleBack}
              className="btn-secondary !py-2 !px-4 !text-sm"
            >
              ← Back to History
            </button>

            {/* Preview of original text */}
            <div className="glass-card p-4">
              <div className="text-xs text-slate-500 mb-1 font-medium">
                Original Text Preview
              </div>
              <p className="text-sm text-slate-400">{selectedItem.inputPreview}</p>
            </div>

            {/* Results */}
            <ResultCard
              result={selectedItem.result}
              timestamp={selectedItem.timestamp}
              onAnalyzeAnother={handleBack}
            />
            <div className="grid md:grid-cols-2 gap-6">
              <SuspiciousSignals
                signals={selectedItem.result.suspicious_signals}
              />
              <ClaimList claims={selectedItem.result.claims_to_verify} />
            </div>
            <VerificationSteps
              steps={selectedItem.result.verification_steps}
              limitations={selectedItem.result.evidence_limitations}
            />
          </div>
        ) : (
          <AnalysisHistory onSelectItem={handleSelectItem} />
        )}
      </div>
    </div>
  );
}
