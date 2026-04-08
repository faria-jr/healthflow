"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/stores/auth-store";

// Componente que garante um usuário mockado para bypass de autenticação
export function AuthBypass({ children }: { children: React.ReactNode }) {
  const { user, setUser } = useAuthStore();

  useEffect(() => {
    // Se não houver usuário, cria um mockado
    if (!user) {
      setUser({
        id: "mock-user-id",
        email: "usuario@exemplo.com",
        role: "patient",
      });
    }
  }, [user, setUser]);

  return <>{children}</>;
}
