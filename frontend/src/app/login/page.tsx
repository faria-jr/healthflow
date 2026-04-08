"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/auth-store";

// Bypass de autenticação - redireciona direto para dashboard
export default function LoginPage() {
  const router = useRouter();
  const { setUser } = useAuthStore();

  useEffect(() => {
    // Cria um usuário mockado e redireciona
    setUser({
      id: "mock-user-id",
      email: "usuario@exemplo.com",
      role: "patient",
    });
    router.replace("/dashboard");
  }, [router, setUser]);

  return (
    <div className="container mx-auto px-4 py-12 max-w-md">
      <div className="text-center">
        <p className="text-muted-foreground">Redirecionando...</p>
      </div>
    </div>
  );
}
