/**
 * TruthLens AI — Footer Component
 */

import { Shield, Heart } from "lucide-react";
import { Link } from "react-router-dom";

const CURRENT_YEAR = new Date().getFullYear();

export default function Footer() {
  return (
    <footer className="border-t border-white/[0.06] mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <Shield className="w-6 h-6 text-brand-cyan" />
              <span className="text-lg font-bold text-white">
                Truth<span className="gradient-text">Lens</span> AI
              </span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed max-w-xs">
              AI-assisted news analysis to help you identify potential misinformation signals.
              Always verify with independent sources.
            </p>
          </div>

          {/* Links */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">
              Navigation
            </h3>
            <div className="flex flex-col gap-2">
              {[
                { to: "/", label: "Home" },
                { to: "/analyze", label: "Analyze News" },
                { to: "/history", label: "Analysis History" },
                { to: "/about", label: "How It Works" },
              ].map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  className="text-sm text-slate-400 hover:text-brand-cyan transition-colors no-underline"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">
              Disclaimer
            </h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              TruthLens AI uses language models to analyze text patterns. Results are
              not definitive proof of truth or falsehood. Always consult reputable,
              independent sources.
            </p>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-10 pt-6 border-t border-white/[0.06] flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-xs text-slate-500">
            © {CURRENT_YEAR} TruthLens AI. Built for educational purposes.
          </p>
          <p className="text-xs text-slate-500 flex items-center gap-1">
            Made with <Heart className="w-3 h-3 text-status-red" /> for responsible AI
          </p>
        </div>
      </div>
    </footer>
  );
}
