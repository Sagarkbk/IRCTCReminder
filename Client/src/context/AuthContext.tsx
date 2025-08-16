import { createContext, useState, type ReactNode } from "react";

export interface User {
  id: string;
  email: string;
  username: string;
  calendar_enabled: boolean;
  telegram_enabled: boolean;
}

export interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (userData: User) => void;
  logout: () => void;
  setError: (error: string | null) => void;
  setIsLoading: (loading: boolean) => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    try {
      const user = localStorage.getItem("user");
      return user ? JSON.parse(user) : null;
    } catch (error) {
      console.error("Failed to parse stored user data:", error);
      localStorage.removeItem("user");
      return null;
    }
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = (userData: User) => {
    setUser(userData);
    localStorage.setItem("user", JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
    localStorage.removeItem("jwt_token");
  };

  const contextValue = {
    isAuthenticated: !!user,
    user: user,
    isLoading,
    error,
    login: login,
    logout: logout,
    setIsLoading,
    setError,
  };

  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
}
