"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Bell, Check, Mail, MessageSquare, Smartphone } from "lucide-react";

interface Notification {
  id: number;
  type: "email" | "sms" | "push";
  title: string;
  body: string;
  status: "pending" | "sent" | "read";
  created_at: string;
}

interface NotificationListProps {
  notifications: Notification[];
  onMarkAsRead?: (id: number) => void;
}

export function NotificationList({
  notifications,
  onMarkAsRead,
}: NotificationListProps) {
  const getIcon = (type: string) => {
    switch (type) {
      case "email":
        return <Mail className="h-4 w-4" />;
      case "sms":
        return <Smartphone className="h-4 w-4" />;
      case "push":
        return <Bell className="h-4 w-4" />;
      default:
        return <MessageSquare className="h-4 w-4" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "read":
        return <Badge variant="secondary">Lida</Badge>;
      case "sent":
        return <Badge>Não lida</Badge>;
      default:
        return <Badge variant="outline">Pendente</Badge>;
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bell className="h-5 w-5" />
          Notificações
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {notifications.length === 0 ? (
            <p className="text-muted-foreground text-center py-4">
              Nenhuma notificação
            </p>
          ) : (
            notifications.map((notification) => (
              <div
                key={notification.id}
                className={`flex items-start gap-3 p-3 rounded-lg border ${
                  notification.status === "read" ? "bg-muted" : "bg-card"
                }`}
              >
                <div className="mt-1">{getIcon(notification.type)}</div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">{notification.title}</h4>
                    {getStatusBadge(notification.status)}
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">
                    {notification.body}
                  </p>
                  <p className="text-xs text-muted-foreground mt-2">
                    {new Date(notification.created_at).toLocaleString("pt-BR")}
                  </p>
                </div>
                {notification.status !== "read" && onMarkAsRead && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onMarkAsRead(notification.id)}
                  >
                    <Check className="h-4 w-4" />
                  </Button>
                )}
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}
