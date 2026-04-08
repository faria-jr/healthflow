import { NextResponse, type NextRequest } from "next/server";

// Bypass de autenticação - redireciona login/register para dashboard
// e permite acesso a todas as rotas protegidas
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Se tentar acessar login ou register, redireciona para dashboard
  if (pathname === "/login" || pathname === "/register") {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // Permite acesso a todas as outras rotas
  return NextResponse.next();
}

export const config = {
  matcher: ["/login", "/register", "/dashboard/:path*"],
};
