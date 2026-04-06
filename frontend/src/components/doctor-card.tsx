"use client";

import { Doctor } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { formatCurrency } from "@/lib/utils";
import { Stethoscope, Calendar } from "lucide-react";
import Link from "next/link";

interface DoctorCardProps {
  doctor: Doctor;
}

export function DoctorCard({ doctor }: DoctorCardProps) {
  const initials = doctor.full_name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-center gap-4">
        <Avatar className="h-12 w-12">
          <AvatarFallback className="bg-primary text-primary-foreground">
            {initials}
          </AvatarFallback>
        </Avatar>
        <div className="flex-1">
          <CardTitle className="text-lg">{doctor.full_name}</CardTitle>
          <div className="flex items-center gap-2 mt-1">
            <Badge variant="secondary">{doctor.specialty}</Badge>
            <span className="text-sm text-muted-foreground">{doctor.crm}</span>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {doctor.bio && (
          <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
            {doctor.bio}
          </p>
        )}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Stethoscope className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm">
              {doctor.consultation_fee
                ? formatCurrency(doctor.consultation_fee)
                : "Consultar valor"}
            </span>
          </div>
          <Link href={`/doctors/${doctor.id}`}>
            <Button size="sm">
              <Calendar className="h-4 w-4 mr-2" />
              Agendar
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
