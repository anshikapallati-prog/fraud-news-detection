/**
 * TruthLens AI — Analysis Loader Component
 * Animated skeleton loading state during AI analysis.
 */

import { motion } from "framer-motion";
import { Cpu, Sparkles } from "lucide-react";

const loadingSteps = [
  "Sending text to AI model…",
  "Analyzing language patterns…",
  "Extracting claims…",
  "Identifying suspicious signals…",
  "Generating verification steps…",
  "Compiling results…",
];

export default function AnalysisLoader() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-card p-8 sm:p-10 space-y-8"
    >
      {/* Header */}
      <div className="flex items-center gap-4">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 rounded-xl bg-gradient-to-br from-brand-cyan/20 to-brand-indigo/20 border border-brand-cyan/20 flex items-center justify-center"
        >
          <Cpu className="w-6 h-6 text-brand-cyan" />
        </motion.div>
        <div>
          <h3 className="text-lg font-semibold text-white">Analyzing Your Text</h3>
          <p className="text-sm text-slate-400">This usually takes 10–30 seconds</p>
        </div>
      </div>

      {/* Animated progress steps */}
      <div className="space-y-3">
        {loadingSteps.map((step, index) => (
          <motion.div
            key={step}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 2.5, duration: 0.4 }}
            className="flex items-center gap-3"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: index * 2.5, duration: 0.3 }}
            >
              <Sparkles className="w-3.5 h-3.5 text-brand-cyan" />
            </motion.div>
            <span className="text-sm text-slate-400">{step}</span>
          </motion.div>
        ))}
      </div>

      {/* Shimmer skeleton */}
      <div className="space-y-4 pt-4">
        <div className="shimmer-line h-8 w-2/3" />
        <div className="shimmer-line h-4 w-full" />
        <div className="shimmer-line h-4 w-5/6" />
        <div className="shimmer-line h-4 w-4/6" />
        <div className="grid grid-cols-2 gap-4 pt-2">
          <div className="shimmer-line h-20" />
          <div className="shimmer-line h-20" />
        </div>
      </div>
    </motion.div>
  );
}
