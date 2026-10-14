/**
 * TruthLens AI — Feature Cards Component
 */

import { motion } from "framer-motion";
import { Brain, Languages, CheckCircle2 } from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "AI-Assisted Analysis",
    description:
      "Powered by advanced language models through Groq, TruthLens analyzes text patterns, claims, and language signals to assess news content.",
    gradient: "from-brand-cyan to-brand-blue",
  },
  {
    icon: Languages,
    title: "Language Pattern Detection",
    description:
      "Identifies sensationalism, unsupported claims, missing attribution, emotional manipulation, and other common misinformation signals.",
    gradient: "from-brand-indigo to-brand-purple",
  },
  {
    icon: CheckCircle2,
    title: "Verification Guidance",
    description:
      "Provides concrete fact-checking steps and highlights claims that should be independently verified through reputable sources.",
    gradient: "from-brand-purple to-status-amber",
  },
];

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.15 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function FeatureCards() {
  return (
    <section className="py-24 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section heading */}
        <div className="text-center mb-16">
          <motion.h2
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-3xl sm:text-4xl font-bold text-white"
          >
            How TruthLens <span className="gradient-text">Helps You</span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.15 }}
            className="mt-4 text-slate-400 text-lg max-w-2xl mx-auto"
          >
            Three powerful capabilities working together to help you navigate the information landscape.
          </motion.p>
        </div>

        {/* Cards */}
        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-6 lg:gap-8"
        >
          {features.map((feature) => (
            <motion.div
              key={feature.title}
              variants={item}
              className="glass-card glass-card-hover p-8 space-y-5"
            >
              <div
                className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center shadow-lg`}
              >
                <feature.icon className="w-6 h-6 text-navy-950" />
              </div>
              <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
