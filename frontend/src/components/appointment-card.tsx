"use client";

import { Appointment, AppointmentStatus } from "@/types";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDateTime } from "@/lib/utils";
import { Calendar, Clock, User, Stethoscope } from "lucide-react";

interface AppointmentCardProps {
  appointment: Appointment;
  showPatient?: boolean;
  showDoctor?: boolean;
  onCancel?: () => void;
  onConfirm?: () => void;
  onComplete?: () => void;
}

const statusLabels: Record<AppointmentStatus, string> = {
  scheduled: "Agendada",
  confirmed: "Confirmada",
  completed: "Concluída",
  cancelled: "Cancelada",
  no_show: "Não compareceu",
};

const statusVariants: Record<AppointmentStatus, "default" | "secondary" | "destructive" | "outline"> = {
  scheduled: "secondary",
  confirmed: "default",
  completed: "default",
  cancelled: "destructive",
  no_show: "destructive",
};

export function AppointmentCard({
  appointment,
  showPatient = false,
  showDoctor = false,
  onCancel,
  onConfirm,
  onComplete,
}: AppointmentCardProps) {
  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-muted-foreground" />
            <span className="font-medium">
              {formatDateTime(appointment.scheduled_at)}
            </span>
          </div>
          <Badge variant={statusVariants[appointment.status]}>
            {statusLabels[appointment.status]}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {showPatient && appointment.patient && (
          <div className="flex items-center gap-2">
            <User className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm">{appointment.patient.full_name}</span>
          </div>
        )}
        {showDoctor && appointment.doctor && (
          <div className="flex items-center gap-2">
            <Stethoscope className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm">
              Dr(a). {appointment.doctor.full_name} - {appointment.doctor.specialty}
            </span>
          </div>
        )}
        <div className="flex items-center gap-2">
          <Clock className="h-4 w-4 text-muted-foreground" />
          <span className="text-sm">{appointment.duration_minutes} minutos</span>
        </div>
        {appointment.notes && (
          <p className="text-sm text-muted-foreground">
            {appointment.notes}
          </p>
        )}
        <div className="flex gap-2 pt-2">
          {appointment.status === "scheduled" && onConfirm && (
            <Button size="sm" onClick={onConfirm}>
              Confirmar
            </Button>
          )}
          {appointment.status === "confirmed" && onComplete && (
            <Button size="sm" onClick={onComplete}>
              Concluir
            </Button>
          )}
          {(appointment.status === "scheduled" || appointment.status === "confirmed") && onCancel && (
            <Button size="sm" variant="outline" onClick={onCancel}>
              Cancelar
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
