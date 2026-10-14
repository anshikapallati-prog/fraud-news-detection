/**
 * TruthLens AI — About / How It Works Page
 */

import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
  Info,
  FileText,
  Server,
  Cpu,
  BarChart3,
  ShieldCheck,
  ArrowDown,
  ArrowRight,
  AlertTriangle,
} from "lucide-react";

const workflowSteps = [
  {
    number: "01",
    icon: FileText,
    title: "You Submit Text",
    detail:
      "Paste any news headline, article, or social media post into the analysis text area. The text is validated on the frontend for length and completeness.",
  },
  {
    number: "02",
    icon: Server,
    title: "Backend Validates Input",
    detail:
      "The FastAPI backend receives your text, validates it using Pydantic schemas, and ensures it meets the required length constraints.",
  },
  {
    number: "03",
    icon: Cpu,
    title: "AI Analyzes the Text",
    detail:
      "The backend sends your text to the Groq API, which runs a large language model. The model analyzes language patterns, claims, tone, and potential misinformation signals.",
  },
  {
    number: "04",
    icon: BarChart3,
    title: "Structured Results Returned",
    detail:
      "The AI returns a structured JSON response containing a classification, explanation, suspicious signals, claims to verify, and fact-checking guidance.",
  },
  {
    number: "05",
    icon: ShieldCheck,
    title: "You Review & Verify",
    detail:
      "The results are displayed in a clear dashboard. You can follow the recommended fact-checking steps to independently verify the claims using reputable sources.",
  },
];

const limitations = [
  "The AI analyzes text patterns only — it does not access the internet or real-time databases.",
  "Classifications are based on language analysis, not independent fact-checking.",
  "The AI can be wrong. Always verify results with reputable, independent sources.",
  "Professional-sounding text can still contain misinformation.",
  "Emotional language alone is not proof of falsehood.",
  "Submitted text is sent to the Groq API for processing. No content is stored on our server.",
];

export default function AboutPage() {
  return (
    <div className="min-h-screen pt-24 pb-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="text-center"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <Info className="w-8 h-8 text-brand-cyan" />
            <h1 className="text-3xl sm:text-4xl font-bold text-white">
              How It <span className="gradient-text">Works</span>
            </h1>
          </div>
          <p className="text-slate-400 max-w-2xl mx-auto text-lg">
            Understand the complete workflow behind TruthLens AI — from the text
            you submit to the analysis you receive.
          </p>
        </motion.div>

        {/* Workflow */}
        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-white text-center mb-8">
            The Analysis <span className="gradient-text">Pipeline</span>
          </h2>

          <div className="space-y-4">
            {workflowSteps.map((step, index) => (
              <div key={step.title}>
                <motion.div
                  initial={{ opacity: 0, x: -15 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  className="glass-card p-6 flex gap-5 items-start"
                >
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-brand-cyan/15 to-brand-indigo/15 border border-brand-cyan/15 flex items-center justify-center flex-shrink-0">
                    <step.icon className="w-5 h-5 text-brand-cyan" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold text-brand-cyan tracking-widest mb-1">
                      STEP {step.number}
                    </div>
                    <h3 className="text-lg font-semibold text-white mb-1">
                      {step.title}
                    </h3>
                    <p className="text-sm text-slate-400 leading-relaxed">
                      {step.detail}
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

                {index < workflowSteps.length - 1 && (
                  <div className="flex justify-center py-2">
                    <ArrowDown className="w-4 h-4 text-navy-600" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Technology stack */}
        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-white text-center">
            Technology <span className="gradient-text">Stack</span>
          </h2>

          <div className="grid sm:grid-cols-2 gap-4">
            {[
              {
                label: "Frontend",
                items: ["React + Vite", "TypeScript", "Tailwind CSS", "Framer Motion"],
              },
              {
                label: "Backend",
                items: ["Python", "FastAPI", "Pydantic", "Groq SDK"],
              },
              {
                label: "AI",
                items: ["Groq API", "LLaMA 3.3 70B", "Structured JSON Output"],
              },
              {
                label: "Storage",
                items: ["Browser localStorage", "No server-side storage"],
              },
            ].map((stack) => (
              <div key={stack.label} className="glass-card p-5 space-y-3">
                <h3 className="text-sm font-semibold text-brand-cyan uppercase tracking-wider">
                  {stack.label}
                </h3>
                <ul className="space-y-1.5">
                  {stack.items.map((item) => (
                    <li
                      key={item}
                      className="text-sm text-slate-400 flex items-center gap-2"
                    >
                      <span className="w-1 h-1 rounded-full bg-brand-indigo" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* Important Limitations */}
        <section className="space-y-6">
          <h2 className="text-2xl font-bold text-white text-center">
            Important <span className="gradient-text-warm">Limitations</span>
          </h2>

          <div className="glass-card p-6 sm:p-8 border-status-amber/15 space-y-4">
            <div className="flex items-center gap-3 mb-2">
              <AlertTriangle className="w-5 h-5 text-status-amber" />
              <h3 className="text-lg font-semibold text-white">
                Please Read Before Using
              </h3>
            </div>
            <ul className="space-y-3">
              {limitations.map((item, index) => (
                <li
                  key={index}
                  className="flex items-start gap-3 text-sm text-slate-400 leading-relaxed"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-status-amber flex-shrink-0 mt-1.5" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* CTA */}
        <div className="text-center">
          <Link to="/analyze" className="btn-primary text-base">
            Try It Now <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
