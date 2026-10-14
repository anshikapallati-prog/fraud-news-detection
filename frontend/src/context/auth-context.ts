/**
 * TruthLens AI — Auth context object and types (no components here,
 * so React fast-refresh stays happy).
 */

import { createContext } from "react";
import type { AuthUser } from "../api/client";

export interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextValue | null>(null);
