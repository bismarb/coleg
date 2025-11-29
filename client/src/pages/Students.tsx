import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { DataTable } from "@/components/ui/data-table";
import { Button } from "@/components/ui/button";
import { Plus, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { STUDENTS } from "@/lib/mockData";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

export default function Students() {
  const [data, setData] = useState(STUDENTS);
  const [searchTerm, setSearchTerm] = useState("");
  const { toast } = useToast();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentStudent, setCurrentStudent] = useState<any>(null);

  const filteredData = data.filter(student => 
    student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.grade.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const newStudent = {
      id: currentStudent ? currentStudent.id : `s${Date.now()}`,
      name: formData.get("name") as string,
      grade: formData.get("grade") as string,
      status: "Activo",
      attendance: "100%",
      gpa: 0.0
    };

    if (currentStudent) {
      setData(data.map(s => s.id === currentStudent.id ? { ...s, ...newStudent } : s));
      toast({ title: "Estudiante actualizado", description: "Los datos han sido guardados correctamente." });
    } else {
      setData([...data, newStudent]);
      toast({ title: "Estudiante creado", description: "El nuevo estudiante ha sido registrado." });
    }
    setIsDialogOpen(false);
    setCurrentStudent(null);
  };

  const handleDelete = (item: any) => {
    if (confirm(`¿Estás seguro de eliminar a ${item.name}?`)) {
      setData(data.filter(s => s.id !== item.id));
      toast({ title: "Estudiante eliminado", variant: "destructive" });
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Estudiantes</h1>
            <p className="text-muted-foreground">Gestión de alumnos matriculados</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => setCurrentStudent(null)}>
                <Plus className="mr-2 h-4 w-4" /> Nuevo Estudiante
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>{currentStudent ? "Editar Estudiante" : "Nuevo Estudiante"}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSave} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Nombre Completo</Label>
                  <Input id="name" name="name" defaultValue={currentStudent?.name} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="grade">Grado / Curso</Label>
                  <Input id="grade" name="grade" defaultValue={currentStudent?.grade} required />
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
            placeholder="Buscar por nombre..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <DataTable 
          data={filteredData}
          columns={[
            { header: "Nombre", accessorKey: "name" },
            { header: "Grado", accessorKey: "grade" },
            { 
              header: "Estado", 
              accessorKey: "status",
              cell: (item) => (
                <span className={`px-2 py-1 rounded-full text-xs font-medium 
                  ${item.status === 'Activo' ? 'bg-green-100 text-green-700' : 
                    item.status === 'En Riesgo' ? 'bg-yellow-100 text-yellow-700' : 
                    'bg-gray-100 text-gray-700'}`}>
                  {item.status}
                </span>
              )
            },
            { header: "Asistencia", accessorKey: "attendance" },
            { header: "Promedio (GPA)", accessorKey: "gpa" },
          ]}
          onEdit={(item) => {
            setCurrentStudent(item);
            setIsDialogOpen(true);
          }}
          onDelete={handleDelete}
        />
      </div>
    </DashboardLayout>
  );
}
