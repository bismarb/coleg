import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import { DataTable } from "@/components/ui/data-table";
import { Button } from "@/components/ui/button";
import { Plus, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { TEACHERS } from "@/lib/mockData";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

export default function Teachers() {
  const [data, setData] = useState(TEACHERS);
  const [searchTerm, setSearchTerm] = useState("");
  const { toast } = useToast();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [currentItem, setCurrentItem] = useState<any>(null);

  const filteredData = data.filter(item => 
    item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.department.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const newItem = {
      id: currentItem ? currentItem.id : `t${Date.now()}`,
      name: formData.get("name") as string,
      department: formData.get("department") as string,
      subjects: (formData.get("subjects") as string).split(",").map(s => s.trim()),
      status: "Activo"
    };

    if (currentItem) {
      setData(data.map(i => i.id === currentItem.id ? { ...i, ...newItem } : i));
      toast({ title: "Profesor actualizado", description: "Los datos han sido guardados correctamente." });
    } else {
      setData([...data, newItem]);
      toast({ title: "Profesor creado", description: "El nuevo profesor ha sido registrado." });
    }
    setIsDialogOpen(false);
    setCurrentItem(null);
  };

  const handleDelete = (item: any) => {
    if (confirm(`¿Estás seguro de eliminar a ${item.name}?`)) {
      setData(data.filter(i => i.id !== item.id));
      toast({ title: "Profesor eliminado", variant: "destructive" });
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Profesores</h1>
            <p className="text-muted-foreground">Gestión del cuerpo docente</p>
          </div>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button onClick={() => setCurrentItem(null)}>
                <Plus className="mr-2 h-4 w-4" /> Nuevo Profesor
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>{currentItem ? "Editar Profesor" : "Nuevo Profesor"}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSave} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Nombre Completo</Label>
                  <Input id="name" name="name" defaultValue={currentItem?.name} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="department">Departamento</Label>
                  <Input id="department" name="department" defaultValue={currentItem?.department} required />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="subjects">Asignaturas (separadas por coma)</Label>
                  <Input id="subjects" name="subjects" defaultValue={currentItem?.subjects.join(", ")} required />
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
            { header: "Departamento", accessorKey: "department" },
            { 
              header: "Asignaturas", 
              accessorKey: "subjects",
              cell: (item) => item.subjects.join(", ")
            },
            { 
              header: "Estado", 
              accessorKey: "status",
              cell: (item) => (
                <span className={`px-2 py-1 rounded-full text-xs font-medium 
                  ${item.status === 'Activo' ? 'bg-blue-100 text-blue-700' : 
                    'bg-orange-100 text-orange-700'}`}>
                  {item.status}
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
