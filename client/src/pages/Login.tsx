import { useState } from "react";
import { useAuth, Role } from "@/lib/auth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { GraduationCap, User, Shield, BookOpen, Eye, EyeOff } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Login() {
  const { login } = useAuth();
  const { toast } = useToast();
  const [isRegistering, setIsRegistering] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("admin@escuela.edu");
  const [password, setPassword] = useState("password");
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (role: Role) => {
    if (isRegistering) {
      // Simulate registration
      toast({
        title: "Cuenta creada",
        description: `Bienvenido, ${name}. Tu cuenta de ${role} ha sido creada exitosamente.`,
      });
      // Auto login after registration for demo
      setTimeout(() => {
        login(role);
      }, 1000);
    } else {
      // Login
      setTimeout(() => {
        login(role);
      }, 500);
    }
  };

  const toggleMode = () => {
    setIsRegistering(!isRegistering);
    // Reset demo credentials if switching to register, or restore if login
    if (!isRegistering) {
      setEmail("");
      setPassword("");
      setName("");
    } else {
      setEmail("admin@escuela.edu");
      setPassword("password");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-muted/20 p-4">
      <div className="mb-8 text-center">
        <div className="inline-flex items-center justify-center p-3 bg-primary rounded-xl mb-4 shadow-lg">
          <GraduationCap className="h-8 w-8 text-primary-foreground" />
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">EduManager</h1>
        <p className="text-muted-foreground mt-2">Sistema de Gestión Académica Escolar</p>
      </div>

      <Card className="w-full max-w-md shadow-xl border-0">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">
            {isRegistering ? "Crear Cuenta" : "Iniciar Sesión"}
          </CardTitle>
          <CardDescription className="text-center">
            {isRegistering 
              ? "Ingresa tus datos para registrarte en el sistema" 
              : "Seleccione su rol para ingresar al sistema demostrativo"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="admin" className="w-full">
            <TabsList className="grid w-full grid-cols-3 mb-4">
              <TabsTrigger value="admin">Admin</TabsTrigger>
              <TabsTrigger value="teacher">Profesor</TabsTrigger>
              <TabsTrigger value="student">Estudiante</TabsTrigger>
            </TabsList>
            
            <div className="space-y-4">
              {isRegistering && (
                <div className="space-y-2">
                  <Label htmlFor="name">Nombre Completo</Label>
                  <Input 
                    id="name" 
                    type="text" 
                    placeholder="Juan Pérez" 
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>
              )}
              
              <div className="space-y-2">
                <Label htmlFor="email">Correo Electrónico</Label>
                <Input 
                  id="email" 
                  type="email" 
                  placeholder="nombre@escuela.edu" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Contraseña</Label>
                <div className="relative">
                  <Input 
                    id="password" 
                    type={showPassword ? "text" : "password"} 
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pr-10"
                  />
                  <Button 
                    type="button"
                    variant="ghost" 
                    size="icon" 
                    className="absolute right-0 top-0 h-full px-3 text-muted-foreground hover:text-foreground"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    <span className="sr-only">
                      {showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
                    </span>
                  </Button>
                </div>
              </div>

              <TabsContent value="admin">
                <Button className="w-full mt-2" onClick={() => handleSubmit("admin")}>
                  <Shield className="mr-2 h-4 w-4" />
                  {isRegistering ? "Registrar Administrador" : "Entrar como Administrador"}
                </Button>
              </TabsContent>
              <TabsContent value="teacher">
                <Button className="w-full mt-2" onClick={() => handleSubmit("teacher")}>
                  <BookOpen className="mr-2 h-4 w-4" />
                  {isRegistering ? "Registrar Profesor" : "Entrar como Profesor"}
                </Button>
              </TabsContent>
              <TabsContent value="student">
                <Button className="w-full mt-2" onClick={() => handleSubmit("student")}>
                  <User className="mr-2 h-4 w-4" />
                  {isRegistering ? "Registrar Estudiante" : "Entrar como Estudiante"}
                </Button>
              </TabsContent>
            </div>
          </Tabs>

          <div className="mt-6 text-center text-sm">
            <span className="text-muted-foreground">
              {isRegistering ? "¿Ya tienes una cuenta?" : "¿No tienes cuenta?"}
            </span>
            <Button variant="link" className="p-0 h-auto ml-2" onClick={toggleMode}>
              {isRegistering ? "Inicia Sesión" : "Regístrate aquí"}
            </Button>
          </div>
        </CardContent>
        <CardFooter className="flex justify-center border-t p-4 bg-muted/10">
          <p className="text-xs text-muted-foreground">
            Demo Version • Bootstrap Style (Tailwind Impl)
          </p>
        </CardFooter>
      </Card>
    </div>
  );
}
