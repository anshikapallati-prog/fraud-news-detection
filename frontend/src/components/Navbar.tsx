/**
 * TruthLens AI — Navbar Component
 */

import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Shield, Menu, X, LogOut, User } from "lucide-react";
import { useAuth } from "../context/useAuth";

const navLinks = [
  { to: "/", label: "Home" },
  { to: "/analyze", label: "Analyze News" },
  { to: "/history", label: "History" },
  { to: "/about", label: "How It Works" },
];

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  function handleLogout() {
    logout();
    setMobileOpen(false);
    navigate("/");
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-card border-b border-white/[0.06] rounded-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2.5 text-white no-underline group flex-shrink-0"
            aria-label="TruthLens AI Home"
          >
            <div className="relative flex-shrink-0">
              <Shield className="w-8 h-8 text-brand-cyan transition-transform group-hover:scale-110" />
              <div className="absolute inset-0 w-8 h-8 bg-brand-cyan/20 rounded-full blur-lg opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
            <span className="text-lg font-bold tracking-tight whitespace-nowrap">
              Truth<span className="gradient-text">Lens</span>{" "}
              <span className="text-xs font-medium text-slate-400 align-top">AI</span>
            </span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const isActive = location.pathname === link.to;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`relative px-4 py-2 text-sm font-medium rounded-lg transition-colors no-underline whitespace-nowrap ${
                    isActive
                      ? "text-brand-cyan"
                      : "text-slate-300 hover:text-white hover:bg-white/[0.05]"
                  }`}
                >
                  {link.label}
                  {isActive && (
                    <motion.div
                      layoutId="nav-indicator"
                      className="absolute bottom-0 left-2 right-2 h-0.5 bg-gradient-to-r from-brand-cyan to-brand-indigo rounded-full"
                      transition={{ type: "spring", stiffness: 400, damping: 30 }}
                    />
                  )}
                </Link>
              );
            })}
          </div>

          {/* Desktop auth area */}
          {user ? (
            <div className="hidden md:flex items-center gap-3">
              <span
                className="hidden lg:flex items-center gap-1.5 text-xs text-slate-300 max-w-[160px] truncate"
                title={user.email}
              >
                <User className="w-3.5 h-3.5 text-brand-cyan flex-shrink-0" />
                {user.email}
              </span>
              <span className="lg:hidden text-brand-cyan" title={user.email}>
                <User className="w-4 h-4" />
              </span>
              <button
                onClick={handleLogout}
                className="btn-secondary !py-2 !px-4 !text-xs !whitespace-nowrap"
                aria-label="Sign out"
              >
                <LogOut className="w-3.5 h-3.5" /> Sign Out
              </button>
            </div>
          ) : (
            <div className="hidden md:flex items-center gap-2">
              <Link
                to="/login"
                className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white transition-colors no-underline whitespace-nowrap"
              >
                Sign In
              </Link>
              <Link to="/analyze" className="btn-primary !py-2 !px-5 !text-sm">
                Start Analysis
              </Link>
            </div>
          )}

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 text-slate-300 hover:text-white bg-transparent border-none cursor-pointer"
            aria-label={mobileOpen ? "Close menu" : "Open menu"}
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile nav */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="md:hidden overflow-hidden border-t border-white/[0.06]"
          >
            <div className="px-4 py-3 space-y-1">
              {navLinks.map((link) => {
                const isActive = location.pathname === link.to;
                return (
                  <Link
                    key={link.to}
                    to={link.to}
                    onClick={() => setMobileOpen(false)}
                    className={`block px-4 py-2.5 text-sm font-medium rounded-lg transition-colors no-underline ${
                      isActive
                        ? "text-brand-cyan bg-white/[0.05]"
                        : "text-slate-300 hover:text-white hover:bg-white/[0.05]"
                    }`}
                  >
                    {link.label}
                  </Link>
                );
              })}
              <Link
                to="/analyze"
                onClick={() => setMobileOpen(false)}
                className="btn-primary w-full justify-center !mt-3 !text-sm"
              >
                Start Analysis
              </Link>
              {user ? (
                <button
                  onClick={handleLogout}
                  className="btn-secondary w-full justify-center !mt-2 !text-sm"
                  aria-label="Sign out"
                >
                  <LogOut className="w-4 h-4" /> Sign Out ({user.email})
                </button>
              ) : (
                <Link
                  to="/login"
                  onClick={() => setMobileOpen(false)}
                  className="btn-secondary w-full justify-center !mt-2 !text-sm"
                >
                  Sign In
                </Link>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
