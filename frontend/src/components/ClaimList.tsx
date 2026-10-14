/**
 * TruthLens AI — Claim List Component
 */

import { motion } from "framer-motion";
import { Search } from "lucide-react";

interface ClaimListProps {
  claims: string[];
}

export default function ClaimList({ claims }: ClaimListProps) {
  if (claims.length === 0) {
    return (
      <div className="glass-card p-6 space-y-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-brand-blue/10 flex items-center justify-center">
            <Search className="w-4.5 h-4.5 text-brand-blue" />
          </div>
          <h4 className="text-base font-semibold text-white">Claims to Verify</h4>
        </div>
        <p className="text-sm text-slate-400">
          No specific claims requiring independent verification were identified.
        </p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.2 }}
      className="glass-card p-6 space-y-4"
    >
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-brand-blue/10 flex items-center justify-center">
          <Search className="w-4.5 h-4.5 text-brand-blue" />
        </div>
        <div>
          <h4 className="text-base font-semibold text-white">Claims to Verify</h4>
          <p className="text-xs text-slate-500">
            {claims.length} claim{claims.length !== 1 ? "s" : ""} identified
          </p>
        </div>
      </div>

      <ul className="space-y-2">
        {claims.map((claim, index) => (
          <motion.li
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 + index * 0.08 }}
            className="flex items-start gap-3 text-sm text-slate-300 px-3 py-2.5 rounded-lg bg-brand-blue/[0.04] border border-brand-blue/10"
          >
            <span className="w-5 h-5 rounded-md bg-brand-blue/10 text-brand-blue text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
              {index + 1}
            </span>
            {claim}
          </motion.li>
        ))}
      </ul>
    </motion.div>
  );
}
