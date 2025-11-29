import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { DataTable } from "@/components/ui/data-table";
import { Button } from "@/components/ui/button";
import { Plus, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { GRADES } from "@/lib/mockData";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

export default function Grades() {
  const [data, setData] = useState(GRADES);
  const [searchTerm, setSearchTerm] = useState("");
  const { toast } = useToast();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentItem, setCurrentItem] = useState<any>(null);

  const filteredData = data.filter(item => 
    item.student.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.course.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const newItem = {
      id: currentItem ? currentItem.id : `g${Date.now()}`,
      student: formData.get("student") as string,
      course: formData.get("course") as string,
      grade: Number(formData.get("grade")),
      date: new Date().toISOString().split('T')[0],
      type: formData.get("type") as string,
    };

    if (currentItem) {
      setData(data.map(i => i.id === currentItem.id ? { ...i, ...newItem } : i));
      toast({ title: "Calificación actualizada", description: "Los datos han sido guardados correctamente." });
    } else {
      setData([...data, newItem]);
      toast({ title: "Calificación registrada", description: "La nueva nota ha sido guardada." });
    }
    setIsDialogOpen(false);
    setCurrentItem(null);
  };

  const handleDelete = (item: any) => {
    if (confirm(`¿Estás seguro de eliminar esta calificación?`)) {
      setData(data.filter(i => i.id !== item.id));
      toast({ title: "Calificación eliminada", variant: "destructive" });
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Calificaciones</h1>
            <p className="text-muted-foreground">Registro académico y notas</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => setCurrentItem(null)}>
                <Plus className="mr-2 h-4 w-4" /> Registrar Nota
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>{currentItem ? "Editar Calificación" : "Registrar Calificación"}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSave} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="student">Estudiante</Label>
                  <Input id="student" name="student" defaultValue={currentItem?.student} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="course">Curso / Materia</Label>
                  <Input id="course" name="course" defaultValue={currentItem?.course} required />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="type">Tipo de Evaluación</Label>
                    <Input id="type" name="type" placeholder="Examen, Tarea..." defaultValue={currentItem?.type} required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="grade">Nota (0-100)</Label>
                    <Input id="grade" name="grade" type="number" min="0" max="100" defaultValue={currentItem?.grade} required />
                  </div>
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
            placeholder="Buscar estudiante o curso..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <DataTable 
          data={filteredData}
          columns={[
            { header: "Estudiante", accessorKey: "student" },
            { header: "Curso", accessorKey: "course" },
            { header: "Evaluación", accessorKey: "type" },
            { header: "Fecha", accessorKey: "date" },
            { 
              header: "Nota", 
              accessorKey: "grade",
              cell: (item) => (
                <span className={`font-bold ${item.grade >= 60 ? "text-green-600" : "text-red-600"}`}>
                  {item.grade}
                </span>
              )
            },
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
