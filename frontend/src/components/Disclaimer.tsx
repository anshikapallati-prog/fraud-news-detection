/**
 * TruthLens AI — Disclaimer Component
 */

import { motion } from "framer-motion";
import { Info } from "lucide-react";

export default function Disclaimer() {
  return (
    <section className="py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="glass-card p-6 sm:p-8 border-brand-indigo/20"
        >
          <div className="flex gap-4 items-start">
            <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-brand-indigo/10 flex items-center justify-center">
              <Info className="w-5 h-5 text-brand-indigo" />
            </div>
            <div className="space-y-3">
              <h3 className="text-lg font-semibold text-white">
                Responsible AI Disclaimer
              </h3>
              <div className="space-y-2 text-sm text-slate-400 leading-relaxed">
                <p>
                  TruthLens AI uses a language model to analyze text patterns. It does{" "}
                  <strong className="text-slate-300">not</strong> access the internet,
                  verify facts against databases, or provide definitive proof of truth
                  or falsehood.
                </p>
                <p>
                  AI-generated assessments can be incorrect. The classification
                  reflects text-pattern analysis, not independent fact-checking.
                  Always verify important claims through reputable, independent news
                  sources and official channels.
                </p>
                <p>
                  Submitted text is sent to the configured AI service (Groq) for
                  analysis. No content is stored on our servers.
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
