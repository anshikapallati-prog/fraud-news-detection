/**
 * TruthLens AI — Hero Section
 */

import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles, Search, ShieldCheck } from "lucide-react";

export default function HeroSection() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden pt-16">
      {/* Decorative orbs */}
      <div className="absolute top-20 left-1/4 w-72 h-72 bg-brand-cyan/[0.07] rounded-full blur-[100px] animate-[float_6s_ease-in-out_infinite]" />
      <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-brand-indigo/[0.06] rounded-full blur-[120px] animate-[float_8s_ease-in-out_infinite_1s]" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-brand-purple/[0.04] rounded-full blur-[150px]" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left: Text content */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
            className="space-y-8"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
            >
              <span className="inline-flex items-center gap-2 px-4 py-1.5 text-xs font-medium text-brand-cyan bg-brand-cyan/[0.08] border border-brand-cyan/20 rounded-full">
                <Sparkles className="w-3.5 h-3.5" />
                AI-Powered Analysis
              </span>
            </motion.div>

            {/* Headline */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight text-white text-balance">
              Question the News.{" "}
              <span className="gradient-text">Discover the Signals.</span>
            </h1>

            {/* Description */}
            <p className="text-lg sm:text-xl text-slate-400 leading-relaxed max-w-lg">
              Paste any news headline, article, or social media post. TruthLens AI analyzes
              the text for potential misinformation patterns and guides you toward reliable
              fact-checking.
            </p>

            {/* CTAs */}
            <div className="flex flex-wrap gap-4">
              <Link to="/analyze" className="btn-primary text-base">
                Analyze News <ArrowRight className="w-4 h-4" />
              </Link>
              <Link to="/about" className="btn-secondary text-base">
                How It Works
              </Link>
            </div>

            {/* Stats */}
            <div className="flex gap-8 pt-4">
              {[
                { value: "3", label: "Analysis verdicts" },
                { value: "10–30s", label: "Typical analysis time" },
                { value: "500", label: "Demo dataset texts" },
              ].map((stat) => (
                <div key={stat.label}>
                  <div className="text-xl font-bold gradient-text">{stat.value}</div>
                  <div className="text-xs text-slate-500 mt-0.5">{stat.label}</div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Right: Abstract visual */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="hidden lg:flex justify-center"
          >
            <div className="relative w-full max-w-md">
              {/* Main card */}
              <div className="glass-card p-8 space-y-6 animate-[glow_2s_ease-in-out_infinite_alternate]">
                {/* Mock analysis header */}
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-cyan to-brand-indigo flex items-center justify-center">
                    <Search className="w-5 h-5 text-navy-950" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-white">Analysis Complete</div>
                    <div className="text-xs text-slate-400">Powered by LLM</div>
                  </div>
                </div>

                {/* Mock result bars */}
                <div className="space-y-3">
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Language Analysis</span>
                      <span className="text-brand-cyan">Complete</span>
                    </div>
                    <div className="h-1.5 bg-navy-700 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: "85%" }}
                        transition={{ duration: 1.5, delay: 1 }}
                        className="h-full bg-gradient-to-r from-brand-cyan to-brand-indigo rounded-full"
                      />
                    </div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Claim Extraction</span>
                      <span className="text-brand-indigo">Complete</span>
                    </div>
                    <div className="h-1.5 bg-navy-700 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: "70%" }}
                        transition={{ duration: 1.5, delay: 1.3 }}
                        className="h-full bg-gradient-to-r from-brand-indigo to-brand-purple rounded-full"
                      />
                    </div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Pattern Detection</span>
                      <span className="text-brand-purple">Complete</span>
                    </div>
                    <div className="h-1.5 bg-navy-700 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: "92%" }}
                        transition={{ duration: 1.5, delay: 1.6 }}
                        className="h-full bg-gradient-to-r from-brand-purple to-status-amber rounded-full"
                      />
                    </div>
                  </div>
                </div>

                {/* Mock verdict */}
                <div className="flex items-center gap-2 px-4 py-3 rounded-xl bg-status-amber/[0.08] border border-status-amber/20">
                  <ShieldCheck className="w-5 h-5 text-status-amber flex-shrink-0" />
                  <span className="text-sm font-medium text-status-amber">
                    Requires Verification
                  </span>
                </div>
              </div>

              {/* Floating mini cards */}
              <motion.div
                animate={{ y: [-5, 5, -5] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                className="absolute -top-4 -right-4 glass-card px-3 py-2 text-xs text-brand-cyan flex items-center gap-1.5"
              >
                <Sparkles className="w-3 h-3" /> AI Analysis
              </motion.div>
              <motion.div
                animate={{ y: [5, -5, 5] }}
                transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                className="absolute -bottom-3 -left-3 glass-card px-3 py-2 text-xs text-brand-indigo flex items-center gap-1.5"
              >
                <ShieldCheck className="w-3 h-3" /> Fact-Check Guide
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
