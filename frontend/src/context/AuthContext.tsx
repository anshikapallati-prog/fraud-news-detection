/**
 * TruthLens AI — Authentication Context
 * Holds the signed-in account and session helpers for the whole app.
 */

import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { ReactNode } from "react";
import {
  clearToken,
  fetchCurrentUser,
  loginAccount,
  registerAccount,
} from "../api/client";
import type { AuthUser } from "../api/client";
import { AuthContext } from "./auth-context";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  // Restore the session on first load.
  useEffect(() => {
    let cancelled = false;
    fetchCurrentUser()
      .then((account) => {
        if (!cancelled) setUser(account);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const payload = await loginAccount(email, password);
    setUser(payload.user);
  }, []);

  const register = useCallback(async (email: string, password: string) => {
    const payload = await registerAccount(email, password);
    setUser(payload.user);
  }, []);

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, loading, login, register, logout }),
    [user, loading, login, register, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
