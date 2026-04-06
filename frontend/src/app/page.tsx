import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Stethoscope, Calendar, Shield, Clock } from "lucide-react";

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-12">
      {/* Hero Section */}
      <section className="text-center mb-16">
        <h1 className="text-4xl md:text-6xl font-bold mb-6">
          Sua saúde em <span className="text-primary">primeiro lugar</span>
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Agende consultas médicas, gerencie seu histórico de saúde e conecte-se
          com os melhores profissionais da sua região.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/doctors">
            <Button size="lg" className="w-full sm:w-auto">
              <Stethoscope className="mr-2 h-5 w-5" />
              Encontrar Médicos
            </Button>
          </Link>
          <Link href="/register">
            <Button size="lg" variant="outline" className="w-full sm:w-auto">
              Criar Conta
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="grid md:grid-cols-3 gap-6 mb-16">
        <Card>
          <CardHeader>
            <Calendar className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Agendamento Fácil</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Agende consultas em poucos cliques. Visualize a disponibilidade em
              tempo real e escolha o melhor horário para você.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <Shield className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Histórico Seguro</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Seu prontuário eletrônico sempre disponível e protegido. Acesse
              receitas, diagnósticos e exames de qualquer lugar.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <Clock className="h-8 w-8 text-primary mb-2" />
            <CardTitle>Lembretes Automáticos</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Receba notificações sobre suas consultas. Nunca mais perca um
              compromisso médico importante.
            </p>
          </CardContent>
        </Card>
      </section>

      {/* CTA Section */}
      <section className="bg-primary/5 rounded-2xl p-8 md:p-12 text-center">
        <h2 className="text-2xl md:text-3xl font-bold mb-4">
          Pronto para cuidar da sua saúde?
        </h2>
        <p className="text-muted-foreground mb-6 max-w-xl mx-auto">
          Cadastre-se gratuitamente e tenha acesso a todos os recursos da
          plataforma. É rápido, fácil e seguro.
        </p>
        <Link href="/register">
          <Button size="lg">Começar Agora</Button>
        </Link>
      </section>
    </div>
  );
}
