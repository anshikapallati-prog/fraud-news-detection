/**
 * TruthLens AI — Login / Register Page
 * Demo-grade local accounts: register in seconds, session token kept in the
 * browser. Accounts live in the local server database (never leave your PC).
 */

import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Shield,
  Mail,
  Lock,
  AlertCircle,
  Loader2,
  LogIn,
  UserPlus,
} from "lucide-react";
import { useAuth } from "../context/useAuth";

type Mode = "login" | "register";

const EMAIL_PATTERN = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

export default function LoginPage() {
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const redirectTo =
    (location.state as { from?: string } | null)?.from || "/analyze";

  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  function validate(): string | null {
    if (!EMAIL_PATTERN.test(email.trim())) {
      return "Enter a valid email address.";
    }
    if (password.length < 8) {
      return "Password must be at least 8 characters.";
    }
    if (mode === "register" && password !== confirm) {
      return "Passwords do not match.";
    }
    return null;
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const problem = validate();
    if (problem) {
      setError(problem);
      return;
    }
    setError("");
    setBusy(true);
    try {
      if (mode === "login") {
        await login(email.trim(), password);
      } else {
        await register(email.trim(), password);
      }
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong. Try again."
      );
    } finally {
      setBusy(false);
    }
  }

  function switchMode(next: Mode) {
    setMode(next);
    setError("");
    setConfirm("");
  }

  return (
    <div className="min-h-screen pt-28 pb-16 flex items-start justify-center">
      <div className="w-full max-w-md mx-auto px-4 sm:px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="glass-card p-6 sm:p-8 space-y-6"
        >
          {/* Header */}
          <div className="text-center space-y-2">
            <div className="w-12 h-12 mx-auto rounded-2xl bg-gradient-to-br from-brand-cyan/20 to-brand-indigo/20 border border-brand-cyan/20 flex items-center justify-center">
              <Shield className="w-6 h-6 text-brand-cyan" />
            </div>
            <h1 className="text-2xl font-bold text-white">
              {mode === "login" ? "Welcome back" : "Create your account"}
            </h1>
            <p className="text-sm text-slate-400">
              {mode === "login"
                ? "Sign in to analyze news and view your history."
                : "Register in seconds — no email confirmation needed for this demo."}
            </p>
          </div>

          {/* Mode tabs */}
          <div
            className="grid grid-cols-2 gap-1 p-1 rounded-xl bg-white/[0.04] border border-white/[0.06]"
            role="tablist"
            aria-label="Sign in or register"
          >
            {(["login", "register"] as Mode[]).map((m) => (
              <button
                key={m}
                role="tab"
                aria-selected={mode === m}
                onClick={() => switchMode(m)}
                className={`py-2 text-sm font-medium rounded-lg transition-all border-none cursor-pointer ${
                  mode === m
                    ? "bg-gradient-to-r from-brand-cyan/20 to-brand-indigo/20 text-white"
                    : "bg-transparent text-slate-400 hover:text-white"
                }`}
              >
                {m === "login" ? "Sign In" : "Register"}
              </button>
            ))}
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4" noValidate>
            <div className="space-y-1.5">
              <label
                htmlFor="auth-email"
                className="text-xs font-medium text-slate-300"
              >
                Email address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
                <input
                  id="auth-email"
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  disabled={busy}
                  className="w-full bg-white/[0.03] border border-white/[0.08] rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 outline-none focus:border-brand-cyan/50 transition-colors"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label
                htmlFor="auth-password"
                className="text-xs font-medium text-slate-300"
              >
                Password
                {mode === "register" && (
                  <span className="text-slate-500"> (min. 8 characters)</span>
                )}
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
                <input
                  id="auth-password"
                  type="password"
                  autoComplete={
                    mode === "login" ? "current-password" : "new-password"
                  }
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  disabled={busy}
                  className="w-full bg-white/[0.03] border border-white/[0.08] rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 outline-none focus:border-brand-cyan/50 transition-colors"
                />
              </div>
            </div>

            {mode === "register" && (
              <div className="space-y-1.5">
                <label
                  htmlFor="auth-confirm"
                  className="text-xs font-medium text-slate-300"
                >
                  Confirm password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
                  <input
                    id="auth-confirm"
                    type="password"
                    autoComplete="new-password"
                    value={confirm}
                    onChange={(e) => setConfirm(e.target.value)}
                    placeholder="••••••••"
                    disabled={busy}
                    className="w-full bg-white/[0.03] border border-white/[0.08] rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 outline-none focus:border-brand-cyan/50 transition-colors"
                  />
                </div>
              </div>
            )}

            {error && (
              <motion.div
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                role="alert"
                className="flex items-start gap-2 text-sm text-status-red px-4 py-2.5 rounded-xl bg-status-red/[0.08] border border-status-red/20"
              >
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                {error}
              </motion.div>
            )}

            <button
              type="submit"
              disabled={busy}
              className="btn-primary w-full justify-center !py-2.5"
            >
              {busy ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  {mode === "login" ? "Signing in…" : "Creating account…"}
                </>
              ) : mode === "login" ? (
                <>
                  <LogIn className="w-4 h-4" /> Sign In
                </>
              ) : (
                <>
                  <UserPlus className="w-4 h-4" /> Create Account
                </>
              )}
            </button>
          </form>

          {/* Footer note */}
          <p className="text-xs text-slate-500 text-center leading-relaxed border-t border-white/[0.06] pt-4">
            Demo authentication — accounts are stored in this computer's local
            server database only.{" "}
            <Link to="/about" className="text-brand-cyan hover:underline">
              Learn how it works
            </Link>
          </p>
        </motion.div>
      </div>
    </div>
  );
}
