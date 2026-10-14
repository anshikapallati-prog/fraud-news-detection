/**
 * TruthLens AI — App Component
 * Root component with routing, auth provider, and layout.
 */

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from "react-router-dom";
import type { ReactNode } from "react";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import HomePage from "./pages/HomePage";
import AnalyzePage from "./pages/AnalyzePage";
import HistoryPage from "./pages/HistoryPage";
import AboutPage from "./pages/AboutPage";
import LoginPage from "./pages/LoginPage";
import { AuthProvider } from "./context/AuthContext";
import { useAuth } from "./context/useAuth";

/**
 * Route guard: signed-out visitors are sent to /login and brought back
 * to the page they wanted after signing in.
 */
function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen pt-28 flex items-start justify-center">
        <div className="shimmer-line h-8 w-48" aria-label="Loading session" />
      </div>
    );
  }
  if (!user) {
    return (
      <Navigate to="/login" replace state={{ from: location.pathname }} />
    );
  }
  return <>{children}</>;
}

export default function App() {
  return (
    <Router>
      <AuthProvider>
        {/* Background mesh */}
        <div className="bg-mesh" />

        <div className="flex flex-col min-h-screen">
          <Navbar />

          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route
                path="/analyze"
                element={
                  <ProtectedRoute>
                    <AnalyzePage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/history"
                element={
                  <ProtectedRoute>
                    <HistoryPage />
                  </ProtectedRoute>
                }
              />
              <Route path="/about" element={<AboutPage />} />
            </Routes>
          </main>

          <Footer />
        </div>
      </AuthProvider>
    </Router>
  );
}
