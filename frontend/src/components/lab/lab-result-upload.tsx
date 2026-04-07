"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Upload, File, X } from "lucide-react";

interface LabResultUploadProps {
  patientId: number;
  onUpload?: (data: {
    lab_name: string;
    test_type: string;
    result_summary?: string;
    file?: File;
  }) => void;
}

export function LabResultUpload({ patientId, onUpload }: LabResultUploadProps) {
  const [labName, setLabName] = useState("");
  const [testType, setTestType] = useState("");
  const [resultSummary, setResultSummary] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        alert("Arquivo deve ter menos que 10MB");
        return;
      }
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!labName || !testType) {
      alert("Preencha o nome do laboratório e tipo de exame");
      return;
    }

    setIsUploading(true);
    try {
      await onUpload?.({
        lab_name: labName,
        test_type: testType,
        result_summary: resultSummary,
        file: selectedFile || undefined,
      });

      // Reset form
      setLabName("");
      setTestType("");
      setResultSummary("");
      setSelectedFile(null);
    } catch (error) {
      console.error("Upload error:", error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5" />
          Upload de Exame
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="lab-name">Laboratório</Label>
          <Input
            id="lab-name"
            value={labName}
            onChange={(e) => setLabName(e.target.value)}
            placeholder="Nome do laboratório"
          />
        </div>

        <div>
          <Label htmlFor="test-type">Tipo de Exame</Label>
          <Input
            id="test-type"
            value={testType}
            onChange={(e) => setTestType(e.target.value)}
            placeholder="Ex: Hemograma, Raio-X, etc."
          />
        </div>

        <div>
          <Label htmlFor="result-summary">Resumo dos Resultados</Label>
          <Textarea
            id="result-summary"
            value={resultSummary}
            onChange={(e) => setResultSummary(e.target.value)}
            placeholder="Resumo dos resultados (opcional)"
            rows={4}
          />
        </div>

        <div>
          <Label htmlFor="file">Arquivo (PDF, JPG, PNG - max 10MB)</Label>
          <Input
            id="file"
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileSelect}
            className="cursor-pointer"
          />
        </div>

        {selectedFile && (
          <div className="flex items-center gap-2 p-2 bg-muted rounded">
            <File className="h-4 w-4" />
            <span className="flex-1 text-sm truncate">{selectedFile.name}</span>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSelectedFile(null)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        )}

        <Button
          onClick={handleUpload}
          disabled={isUploading || !labName || !testType}
          className="w-full"
        >
          {isUploading ? "Enviando..." : "Enviar Exame"}
        </Button>
      </CardContent>
    </Card>
  );
}
