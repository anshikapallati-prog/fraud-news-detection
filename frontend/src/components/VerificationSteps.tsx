/**
 * TruthLens AI — Verification Steps Component
 */

import { motion } from "framer-motion";
import { CheckCircle2, AlertCircle } from "lucide-react";

interface VerificationStepsProps {
  steps: string[];
  limitations: string[];
}

export default function VerificationSteps({
  steps,
  limitations,
}: VerificationStepsProps) {
  return (
    <div className="space-y-4">
      {/* Verification steps */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        className="glass-card p-6 space-y-4"
      >
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-brand-indigo/10 flex items-center justify-center">
            <CheckCircle2 className="w-4.5 h-4.5 text-brand-indigo" />
          </div>
          <div>
            <h4 className="text-base font-semibold text-white">
              Recommended Fact-Checking Steps
            </h4>
            <p className="text-xs text-slate-500">
              Actions you can take to verify the claims
            </p>
          </div>
        </div>

        <ol className="space-y-2">
          {steps.map((step, index) => (
            <motion.li
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + index * 0.08 }}
              className="flex items-start gap-3 text-sm text-slate-300 px-3 py-2.5 rounded-lg bg-brand-indigo/[0.04] border border-brand-indigo/10"
            >
              <span className="w-5 h-5 rounded-full bg-brand-indigo/15 text-brand-indigo text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                {index + 1}
              </span>
              {step}
            </motion.li>
          ))}
        </ol>
      </motion.div>

      {/* Evidence limitations */}
      {limitations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.4 }}
          className="glass-card p-6 space-y-4 border-white/[0.04]"
        >
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-slate-500/10 flex items-center justify-center">
              <AlertCircle className="w-4.5 h-4.5 text-slate-400" />
            </div>
            <h4 className="text-base font-semibold text-white">
              Analysis Limitations
            </h4>
          </div>

          <ul className="space-y-2">
            {limitations.map((limitation, index) => (
              <li
                key={index}
                className="flex items-start gap-3 text-sm text-slate-400 px-3 py-2 rounded-lg bg-white/[0.02]"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-slate-500 flex-shrink-0 mt-1.5" />
                {limitation}
              </li>
            ))}
          </ul>
        </motion.div>
      )}
    </div>
  );
}
