"use client";

import { useAuthStore } from "@/stores/auth-store";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AppointmentCard } from "@/components/appointment-card";
import { Button } from "@/components/ui/button";
import {
  usePatientAppointments,
  useUpdateAppointmentStatus,
} from "@/hooks/use-appointments";
import { Calendar, Clock, FileText, User } from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  const { user } = useAuthStore();
  
  // TODO: In production, get patientId from user context/profile
  // This should come from an API call to get patient by user_id
  const patientId = user ? 1 : 0; // Placeholder until auth integration is complete

  const { data: appointments, isLoading } = usePatientAppointments(patientId);
  const updateStatus = useUpdateAppointmentStatus();

  const upcomingAppointments = appointments?.filter(
    (a) => a.status === "scheduled" || a.status === "confirmed"
  );
  const pastAppointments = appointments?.filter(
    (a) => a.status === "completed" || a.status === "cancelled" || a.status === "no_show"
  );

  const handleCancel = (appointmentId: number) => {
    updateStatus.mutate({
      appointmentId,
      status: "cancelled",
      reason: "Cancelado pelo paciente",
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-muted-foreground">
          Bem-vindo de volta, {user?.email || "Paciente"}
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Próximas Consultas
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {upcomingAppointments?.length || 0}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Consultas Realizadas
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {pastAppointments?.filter((a) => a.status === "completed").length || 0}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Prontuários
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {pastAppointments?.filter((a) => a.status === "completed").length || 0}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Ações Rápidas
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/doctors">
              <Button size="sm" className="w-full">
                <Calendar className="h-4 w-4 mr-2" />
                Agendar
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>

      {/* Appointments Tabs */}
      <Tabs defaultValue="upcoming" className="space-y-4">
        <TabsList>
          <TabsTrigger value="upcoming">
            Próximas ({upcomingAppointments?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="history">
            Histórico ({pastAppointments?.length || 0})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="upcoming">
          {isLoading ? (
            <div className="text-center py-8">Carregando...</div>
          ) : upcomingAppointments?.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <Calendar className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground mb-4">
                  Você não tem consultas agendadas
                </p>
                <Link href="/doctors">
                  <Button>Agendar Consulta</Button>
                </Link>
              </CardContent>
            </Card>
          ) : (
            <div className="grid md:grid-cols-2 gap-4">
              {upcomingAppointments?.map((appointment) => (
                <AppointmentCard
                  key={appointment.id}
                  appointment={appointment}
                  showDoctor
                  onCancel={() => handleCancel(appointment.id)}
                />
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="history">
          {isLoading ? (
            <div className="text-center py-8">Carregando...</div>
          ) : pastAppointments?.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">
                  Você ainda não tem consultas no histórico
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid md:grid-cols-2 gap-4">
              {pastAppointments?.map((appointment) => (
                <AppointmentCard
                  key={appointment.id}
                  appointment={appointment}
                  showDoctor
                />
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
