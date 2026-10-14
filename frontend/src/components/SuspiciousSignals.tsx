/**
 * TruthLens AI — Suspicious Signals Component
 */

import { motion } from "framer-motion";
import { AlertTriangle } from "lucide-react";

interface SuspiciousSignalsProps {
  signals: string[];
}

export default function SuspiciousSignals({ signals }: SuspiciousSignalsProps) {
  if (signals.length === 0) {
    return (
      <div className="glass-card p-6 space-y-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-status-green/10 flex items-center justify-center">
            <AlertTriangle className="w-4.5 h-4.5 text-status-green" />
          </div>
          <h4 className="text-base font-semibold text-white">Suspicious Signals</h4>
        </div>
        <p className="text-sm text-slate-400">
          No suspicious language patterns were identified in this text.
        </p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className="glass-card p-6 space-y-4"
    >
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-status-amber/10 flex items-center justify-center">
          <AlertTriangle className="w-4.5 h-4.5 text-status-amber" />
        </div>
        <div>
          <h4 className="text-base font-semibold text-white">Suspicious Signals</h4>
          <p className="text-xs text-slate-500">
            {signals.length} pattern{signals.length !== 1 ? "s" : ""} detected
          </p>
        </div>
      </div>

      <ul className="space-y-2">
        {signals.map((signal, index) => (
          <motion.li
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.15 + index * 0.08 }}
            className="flex items-start gap-3 text-sm text-slate-300 px-3 py-2.5 rounded-lg bg-status-amber/[0.04] border border-status-amber/10"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-status-amber flex-shrink-0 mt-1.5" />
            {signal}
          </motion.li>
        ))}
      </ul>
    </motion.div>
  );
}
