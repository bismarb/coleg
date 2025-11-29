import { createContext, useContext, useState, ReactNode, useEffect } from "react";
import { useLocation } from "wouter";

export type Role = "admin" | "teacher" | "student";

export interface User {
  id: string;
  name: string;
  email: string;
  role: Role;
  avatar?: string;
}

interface AuthContextType {
  user: User | null;
  login: (role: Role) => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const MOCK_USERS: Record<Role, User> = {
  admin: {
    id: "u1",
    name: "Administrador Principal",
    email: "admin@escuela.edu",
    role: "admin",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
  },
  teacher: {
    id: "u2",
    name: "Prof. Juan Pérez",
    email: "juan.perez@escuela.edu",
    role: "teacher",
    avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
  },
  student: {
    id: "u3",
    name: "Ana García",
    email: "ana.garcia@alumno.edu",
    role: "student",
    avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
  }
};

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [_, setLocation] = useLocation();

  useEffect(() => {
    // Simulate session check
    const storedRole = localStorage.getItem("mock_auth_role") as Role | null;
    if (storedRole && MOCK_USERS[storedRole]) {
      setUser(MOCK_USERS[storedRole]);
    }
    setIsLoading(false);
  }, []);

  const login = (role: Role) => {
    const user = MOCK_USERS[role];
    localStorage.setItem("mock_auth_role", role);
    setUser(user);
    setLocation("/dashboard");
  };

  const logout = () => {
    localStorage.removeItem("mock_auth_role");
    setUser(null);
    setLocation("/login");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
