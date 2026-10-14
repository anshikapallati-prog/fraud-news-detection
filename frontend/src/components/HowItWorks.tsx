/**
 * TruthLens AI — How It Works Component
 */

import { motion } from "framer-motion";
import { FileText, Cpu, BarChart3, ArrowDown } from "lucide-react";

const steps = [
  {
    number: "01",
    icon: FileText,
    title: "Paste Your Text",
    description:
      "Copy and paste any news headline, article, or social media post into the analysis input field.",
  },
  {
    number: "02",
    icon: Cpu,
    title: "AI Analyzes Patterns",
    description:
      "The text is sent to our backend, which uses a Groq-hosted language model to analyze language patterns, claims, and potential signals.",
  },
  {
    number: "03",
    icon: BarChart3,
    title: "Review Your Results",
    description:
      "Get a structured assessment with classification, suspicious signals, claims to verify, and recommended fact-checking steps.",
  },
];

export default function HowItWorks() {
  return (
    <section className="py-24 relative">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section heading */}
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-3xl sm:text-4xl font-bold text-white"
          >
            Three Simple <span className="gradient-text">Steps</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.15 }}
            className="mt-4 text-slate-400 text-lg max-w-xl mx-auto"
          >
            From paste to insight in under a minute.
          </motion.p>
        </div>

        {/* Steps */}
        <div className="space-y-6">
          {steps.map((step, index) => (
            <div key={step.number}>
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.15 }}
                className="glass-card glass-card-hover p-6 sm:p-8 flex gap-5 sm:gap-6 items-start"
              >
                {/* Step number */}
                <div className="flex-shrink-0 w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-cyan/20 to-brand-indigo/20 border border-brand-cyan/20 flex items-center justify-center">
                  <step.icon className="w-6 h-6 text-brand-cyan" />
                </div>

                <div className="space-y-2 min-w-0 flex-1">
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-bold text-brand-cyan tracking-widest">
                      STEP {step.number}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-white">{step.title}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">
                    {step.description}
                  </p>
                </div>

                {/* Ghost number fills the empty right side */}
                <div
                  aria-hidden="true"
                  className="hidden sm:block flex-shrink-0 self-center text-6xl font-extrabold leading-none text-white/[0.07] select-none"
                >
                  {step.number}
                </div>
              </motion.div>

              {/* Arrow connector */}
              {index < steps.length - 1 && (
                <div className="flex justify-center py-2">
                  <ArrowDown className="w-5 h-5 text-navy-600" />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
