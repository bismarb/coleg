import DashboardLayout from "@/components/layout/DashboardLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Switch } from "@/components/ui/switch";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

export default function Settings() {
  const { toast } = useToast();

  const handleSave = () => {
    toast({ title: "Configuración guardada", description: "Los cambios se han aplicado correctamente." });
  };

  return (
    <DashboardLayout>
      <div className="space-y-6 max-w-4xl">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Configuración</h1>
          <p className="text-muted-foreground">Administra las preferencias del sistema escolar</p>
        </div>
        
        <Card>
          <CardHeader>
            <CardTitle>Información de la Institución</CardTitle>
            <CardDescription>Datos generales del colegio o escuela</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="schoolName">Nombre del Colegio</Label>
                <Input id="schoolName" defaultValue="Colegio Nacional Demo" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="address">Dirección</Label>
                <Input id="address" defaultValue="Av. Principal 123, Ciudad" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">Teléfono</Label>
                <Input id="phone" defaultValue="+1 234 567 890" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Correo de Contacto</Label>
                <Input id="email" defaultValue="contacto@escuela.edu" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Preferencias del Sistema</CardTitle>
            <CardDescription>Configuración de notificaciones y visualización</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Modo Oscuro Automático</Label>
                <p className="text-sm text-muted-foreground">Ajustar tema según preferencias del sistema</p>
              </div>
              <Switch defaultChecked />
            </div>
            <Separator />
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Notificaciones por Email</Label>
                <p className="text-sm text-muted-foreground">Enviar reportes semanales a los administradores</p>
              </div>
              <Switch defaultChecked />
            </div>
            <Separator />
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Registro de Actividad</Label>
                <p className="text-sm text-muted-foreground">Guardar logs de acceso de usuarios</p>
              </div>
              <Switch />
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-end gap-4">
          <Button variant="outline">Cancelar</Button>
          <Button onClick={handleSave}>Guardar Cambios</Button>
        </div>
      </div>
    </DashboardLayout>
  );
}
