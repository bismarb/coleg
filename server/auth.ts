import passport from "passport";
import { Strategy as LocalStrategy } from "passport-local";
import bcrypt from "bcrypt";
import { storage } from "./storage";
import type { User } from "@shared/schema";
import type { Request, Response, NextFunction } from "express";

// Configure Passport Local Strategy
passport.use(
  new LocalStrategy(
    {
      usernameField: "email",
      passwordField: "password",
    },
    async (email, password, done) => {
      try {
        const user = await storage.getUserByEmail(email);
        
        if (!user) {
          return done(null, false, { message: "Credenciales incorrectas" });
        }

        const isValidPassword = await bcrypt.compare(password, user.password);
        
        if (!isValidPassword) {
          return done(null, false, { message: "Credenciales incorrectas" });
        }

        return done(null, user);
      } catch (error) {
        return done(error);
      }
    }
  )
);

// Serialize user for session
passport.serializeUser((user: Express.User, done) => {
  done(null, (user as User).id);
});

// Deserialize user from session
passport.deserializeUser(async (id: string, done) => {
  try {
    const user = await storage.getUserById(id);
    done(null, user || null);
  } catch (error) {
    done(error);
  }
});

// Hash password utility
export async function hashPassword(password: string): Promise<string> {
  return await bcrypt.hash(password, 10);
}

// Middleware to check if user is authenticated
export function isAuthenticated(req: Request, res: Response, next: NextFunction) {
  if (req.isAuthenticated()) {
    return next();
  }
  res.status(401).json({ message: "No autorizado" });
}

// Middleware to check if user has required role
export function hasRole(...allowedRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.isAuthenticated()) {
      return res.status(401).json({ message: "No autorizado" });
    }

    const user = req.user as User;
    if (!allowedRoles.includes(user.role)) {
      return res.status(403).json({ message: "Acceso denegado" });
    }

    next();
  };
}

// Extended Express types
declare global {
  namespace Express {
    interface User {
      id: string;
      email: string;
      name: string;
      role: string;
      avatar?: string | null;
    }
  }
}

export default passport;
