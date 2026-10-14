/**
 * TruthLens AI — News Input Component
 * Text area with character counter, sample text, and validation.
 */

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Send,
  RotateCcw,
  FileText,
  AlertCircle,
  Loader2,
} from "lucide-react";

const SAMPLE_ARTICLES = [
  {
    label: "Sample: Unverified Claim",
    text: `BREAKING: A leaked government document reveals that a secret program has been funding weather modification experiments over major cities for the past decade. Anonymous sources within the agency confirm that the program, codenamed "Project Skyfall," has been responsible for unusual weather patterns observed across the country. Officials have refused to comment on the allegations, fueling speculation among concerned citizens. Experts warn that if true, the implications could be catastrophic for public health and the environment.`,
  },
  {
    label: "Sample: Professional News",
    text: `The Federal Reserve announced Wednesday that it would hold its benchmark interest rate steady at the current target range, citing ongoing uncertainty in the economic outlook. Fed Chair Jerome Powell said in a press conference that the committee would continue monitoring incoming data before making further adjustments. The decision was widely expected by economists and financial analysts. Markets showed modest gains following the announcement, with the S&P 500 rising 0.3% in afternoon trading.`,
  },
  {
    label: "Sample: Sensationalized Content",
    text: `You WON'T believe what doctors are HIDING from you! A miracle fruit discovered in the Amazon rainforest can CURE virtually every known disease, but Big Pharma doesn't want you to know about it! Thousands of people have already been healed, but the mainstream media is REFUSING to cover this story. Share this before it gets DELETED! Click here to learn the ONE secret that pharmaceutical companies are spending BILLIONS to suppress!`,
  },
];

const MAX_LENGTH = 15000;
const MIN_LENGTH = 20;

interface NewsInputProps {
  onSubmit: (text: string) => void;
  isLoading: boolean;
}

export default function NewsInput({ onSubmit, isLoading }: NewsInputProps) {
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const [showSamples, setShowSamples] = useState(false);

  const charCount = text.length;
  const isOverLimit = charCount > MAX_LENGTH;
  const isTooShort = charCount > 0 && charCount < MIN_LENGTH;
  const isValid = charCount >= MIN_LENGTH && charCount <= MAX_LENGTH;

  function handleSubmit() {
    if (!text.trim()) {
      setError("Please enter some text to analyze.");
      return;
    }
    if (charCount < MIN_LENGTH) {
      setError(`Please enter at least ${MIN_LENGTH} characters for a meaningful analysis.`);
      return;
    }
    if (isOverLimit) {
      setError(`Text exceeds the maximum limit of ${MAX_LENGTH.toLocaleString()} characters.`);
      return;
    }
    setError("");
    onSubmit(text.trim());
  }

  function handleClear() {
    setText("");
    setError("");
  }

  function loadSample(sample: string) {
    setText(sample);
    setError("");
    setShowSamples(false);
  }

  return (
    <div className="space-y-4">
      {/* Input area */}
      <div className="glass-card p-1">
        <textarea
          id="news-input"
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            if (error) setError("");
          }}
          placeholder="Paste a news headline, article, or social media post here..."
          rows={8}
          disabled={isLoading}
          aria-label="News text to analyze"
          aria-describedby="char-counter input-error"
          className="w-full bg-transparent text-slate-200 placeholder-slate-500 text-sm leading-relaxed p-5 resize-y border-none outline-none min-h-[180px] font-[inherit]"
        />
      </div>

      {/* Bottom bar */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        {/* Char counter */}
        <div className="flex items-center gap-4">
          <span
            id="char-counter"
            className={`text-xs font-medium tabular-nums ${
              isOverLimit
                ? "text-status-red"
                : isTooShort
                ? "text-status-amber"
                : "text-slate-500"
            }`}
          >
            {charCount.toLocaleString()} / {MAX_LENGTH.toLocaleString()}
          </span>

          {/* Clear button */}
          {text && (
            <button
              onClick={handleClear}
              disabled={isLoading}
              className="text-xs text-slate-400 hover:text-white flex items-center gap-1 transition-colors bg-transparent border-none cursor-pointer"
              aria-label="Clear input"
            >
              <RotateCcw className="w-3 h-3" /> Clear
            </button>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3">
          {/* Sample texts toggle */}
          <button
            onClick={() => setShowSamples(!showSamples)}
            disabled={isLoading}
            className="btn-secondary !py-2 !px-4 !text-xs"
            aria-label="Load sample article"
          >
            <FileText className="w-3.5 h-3.5" />
            {showSamples ? "Hide Samples" : "Try a Sample"}
          </button>

          {/* Submit */}
          <button
            onClick={handleSubmit}
            disabled={isLoading || !isValid}
            className="btn-primary !py-2 !px-5 !text-sm"
            aria-label="Analyze news text"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" /> Analyzing…
              </>
            ) : (
              <>
                <Send className="w-4 h-4" /> Analyze
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          id="input-error"
          role="alert"
          className="flex items-center gap-2 text-sm text-status-red px-4 py-2.5 rounded-xl bg-status-red/[0.08] border border-status-red/20"
        >
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {error}
        </motion.div>
      )}

      {/* Sample articles */}
      {showSamples && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          className="space-y-2"
        >
          {SAMPLE_ARTICLES.map((sample) => (
            <button
              key={sample.label}
              onClick={() => loadSample(sample.text)}
              className="w-full text-left glass-card glass-card-hover p-4 bg-transparent border border-white/[0.06] cursor-pointer"
              aria-label={`Load ${sample.label}`}
            >
              <div className="text-sm font-medium text-brand-cyan mb-1">
                {sample.label}
              </div>
              <div className="text-xs text-slate-400 line-clamp-2">
                {sample.text.substring(0, 150)}…
              </div>
            </button>
          ))}
        </motion.div>
      )}
    </div>
  );
}
