import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { DataTable } from "@/components/ui/data-table";
import { Button } from "@/components/ui/button";
import { Plus, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { COURSES } from "@/lib/mockData";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

export default function Courses() {
  const [data, setData] = useState(COURSES);
  const [searchTerm, setSearchTerm] = useState("");
  const { toast } = useToast();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentItem, setCurrentItem] = useState<any>(null);

  const filteredData = data.filter(item => 
    item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const newItem = {
      id: currentItem ? currentItem.id : `c${Date.now()}`,
      name: formData.get("name") as string,
      code: formData.get("code") as string,
      teacher: formData.get("teacher") as string,
      schedule: formData.get("schedule") as string,
      students: currentItem ? currentItem.students : 0
    };

    if (currentItem) {
      setData(data.map(i => i.id === currentItem.id ? { ...i, ...newItem } : i));
      toast({ title: "Curso actualizado", description: "Los datos han sido guardados correctamente." });
    } else {
      setData([...data, newItem]);
      toast({ title: "Curso creado", description: "El nuevo curso ha sido registrado." });
    }
    setIsDialogOpen(false);
    setCurrentItem(null);
  };

  const handleDelete = (item: any) => {
    if (confirm(`¿Estás seguro de eliminar el curso ${item.name}?`)) {
      setData(data.filter(i => i.id !== item.id));
      toast({ title: "Curso eliminado", variant: "destructive" });
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Cursos</h1>
            <p className="text-muted-foreground">Gestión de materias y clases</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => setCurrentItem(null)}>
                <Plus className="mr-2 h-4 w-4" /> Nuevo Curso
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>{currentItem ? "Editar Curso" : "Nuevo Curso"}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSave} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Nombre del Curso</Label>
                  <Input id="name" name="name" defaultValue={currentItem?.name} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="code">Código</Label>
                  <Input id="code" name="code" defaultValue={currentItem?.code} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="teacher">Profesor Asignado</Label>
                  <Input id="teacher" name="teacher" defaultValue={currentItem?.teacher} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="schedule">Horario</Label>
                  <Input id="schedule" name="schedule" defaultValue={currentItem?.schedule} required />
                </div>
                <DialogFooter>
                  <Button type="submit">Guardar</Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        <div className="flex items-center gap-2 max-w-sm">
          <Search className="h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Buscar por nombre o código..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <DataTable 
          data={filteredData}
          columns={[
            { header: "Código", accessorKey: "code" },
            { header: "Nombre", accessorKey: "name" },
            { header: "Profesor", accessorKey: "teacher" },
            { header: "Horario", accessorKey: "schedule" },
            { header: "Estudiantes", accessorKey: "students" },
          ]}
          onEdit={(item) => {
            setCurrentItem(item);
            setIsDialogOpen(true);
          }}
          onDelete={handleDelete}
        />
      </div>
    </DashboardLayout>
  );
}
