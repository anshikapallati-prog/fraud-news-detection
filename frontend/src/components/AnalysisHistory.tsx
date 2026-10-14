/**
 * TruthLens AI — Analysis History Component
 * Displays recent analyses stored in localStorage.
 */

import { useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Clock,
  Trash2,
  ExternalLink,
  ShieldCheck,
  ShieldAlert,
  ShieldQuestion,
  Trash,
} from "lucide-react";
import type { AnalysisHistoryItem, Classification } from "../types";
import { getHistory, deleteHistoryItem, clearHistory } from "../utils/localStorage";

function getStatusIcon(classification: Classification) {
  switch (classification) {
    case "Likely Real":
      return <ShieldCheck className="w-4 h-4 text-status-green" />;
    case "Likely Fake":
      return <ShieldAlert className="w-4 h-4 text-status-red" />;
    default:
      return <ShieldQuestion className="w-4 h-4 text-status-amber" />;
  }
}

function getStatusColor(classification: Classification): string {
  switch (classification) {
    case "Likely Real":
      return "text-status-green";
    case "Likely Fake":
      return "text-status-red";
    default:
      return "text-status-amber";
  }
}

interface AnalysisHistoryProps {
  onSelectItem: (item: AnalysisHistoryItem) => void;
}

export default function AnalysisHistory({ onSelectItem }: AnalysisHistoryProps) {
  const [items, setItems] = useState<AnalysisHistoryItem[]>(getHistory());
  const [confirmClear, setConfirmClear] = useState(false);

  function handleDelete(id: string) {
    deleteHistoryItem(id);
    setItems(getHistory());
  }

  function handleClearAll() {
    if (confirmClear) {
      clearHistory();
      setItems([]);
      setConfirmClear(false);
    } else {
      setConfirmClear(true);
      setTimeout(() => setConfirmClear(false), 5000);
    }
  }

  if (items.length === 0) {
    return (
      <div className="glass-card p-8 text-center space-y-4">
        <Clock className="w-12 h-12 text-slate-600 mx-auto" />
        <div>
          <h3 className="text-lg font-semibold text-white">No History Yet</h3>
          <p className="text-sm text-slate-400 mt-1">
            Your recent analyses will appear here. Go to{" "}
            <Link to="/analyze" className="text-brand-cyan hover:underline">
              Analyze News
            </Link>{" "}
            to get started.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">
          {items.length === 1
            ? "1 recent analysis"
            : `${items.length} recent analyses`}
        </p>
        <button
          onClick={handleClearAll}
          className={`text-xs font-medium flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-colors border-none cursor-pointer ${
            confirmClear
              ? "bg-status-red/10 text-status-red"
              : "bg-transparent text-slate-400 hover:text-status-red"
          }`}
          aria-label={confirmClear ? "Confirm clear all history" : "Clear all history"}
        >
          <Trash className="w-3.5 h-3.5" />
          {confirmClear ? "Click again to confirm" : "Clear All"}
        </button>
      </div>

      {/* History list */}
      <div className="space-y-3">
        <AnimatePresence mode="popLayout">
          {items.map((item) => (
            <motion.div
              key={item.id}
              layout
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="glass-card glass-card-hover p-4 sm:p-5 cursor-pointer group"
              onClick={() => onSelectItem(item)}
              role="button"
              tabIndex={0}
              aria-label={`View analysis: ${item.inputPreview}`}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onSelectItem(item);
                }
              }}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-start gap-3 min-w-0 flex-1">
                  {getStatusIcon(item.classification)}
                  <div className="min-w-0 space-y-1.5">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`text-sm font-medium ${getStatusColor(item.classification)}`}>
                        {item.classification}
                      </span>
                      <span className="text-xs text-slate-500 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {new Date(item.timestamp).toLocaleDateString()} at{" "}
                        {new Date(item.timestamp).toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </span>
                    </div>
                    <p className="text-sm text-slate-400 truncate max-w-full">
                      {item.inputPreview}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 flex-shrink-0">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(item.id);
                    }}
                    className="p-1.5 text-slate-500 hover:text-status-red transition-colors opacity-0 group-hover:opacity-100 bg-transparent border-none cursor-pointer rounded-lg hover:bg-status-red/10"
                    aria-label="Delete this analysis"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                  <ExternalLink className="w-4 h-4 text-slate-600 group-hover:text-brand-cyan transition-colors" />
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
