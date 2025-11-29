import { useState } from "react";
import { Link, useLocation } from "wouter";
import { useAuth } from "@/lib/auth";
import { 
  LayoutDashboard, 
  Users, 
  GraduationCap, 
  BookOpen, 
  FileText, 
  Settings, 
  LogOut, 
  Menu, 
  X,
  Bell,
  Search
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [location] = useLocation();
  const { user, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigation = [
    { name: "Panel de Control", href: "/dashboard", icon: LayoutDashboard },
    { name: "Estudiantes", href: "/students", icon: Users },
    { name: "Profesores", href: "/teachers", icon: GraduationCap },
    { name: "Cursos", href: "/courses", icon: BookOpen },
    { name: "Calificaciones", href: "/grades", icon: FileText },
    { name: "Configuración", href: "/settings", icon: Settings },
  ];

  const NavItem = ({ item, mobile = false }: { item: typeof navigation[0], mobile?: boolean }) => {
    const isActive = location === item.href;
    return (
      <Link href={item.href}>
        <div 
          className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors cursor-pointer
            ${isActive 
              ? "bg-primary/10 text-primary" 
              : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            }
            ${mobile ? "w-full" : ""}
          `}
          onClick={() => mobile && setIsMobileMenuOpen(false)}
        >
          <item.icon className="h-4 w-4" />
          {item.name}
        </div>
      </Link>
    );
  };

  return (
    <div className="min-h-screen bg-muted/20 flex">
      {/* Sidebar Desktop */}
      <div className="hidden md:flex flex-col w-64 border-r bg-background h-screen sticky top-0">
        <div className="p-6 border-b flex items-center gap-2">
          <div className="bg-primary rounded-lg p-1">
            <GraduationCap className="h-6 w-6 text-primary-foreground" />
          </div>
          <span className="font-bold text-lg">EduManager</span>
        </div>
        <div className="flex-1 py-6 px-3 space-y-1">
          {navigation.map((item) => (
            <NavItem key={item.name} item={item} />
          ))}
        </div>
        <div className="p-4 border-t">
          <div className="flex items-center gap-3 mb-4 px-2">
            <Avatar>
              <AvatarImage src={user?.avatar} />
              <AvatarFallback>{user?.name.charAt(0)}</AvatarFallback>
            </Avatar>
            <div className="overflow-hidden">
              <p className="text-sm font-medium truncate">{user?.name}</p>
              <p className="text-xs text-muted-foreground truncate capitalize">{user?.role}</p>
            </div>
          </div>
          <Button variant="outline" className="w-full justify-start gap-2" onClick={logout}>
            <LogOut className="h-4 w-4" />
            Cerrar Sesión
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-16 border-b bg-background flex items-center justify-between px-4 md:px-6 sticky top-0 z-10">
          <div className="flex items-center gap-4 md:hidden">
            <Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="-ml-2">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="w-64 p-0">
                <div className="p-6 border-b flex items-center gap-2">
                  <div className="bg-primary rounded-lg p-1">
                    <GraduationCap className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <span className="font-bold text-lg">EduManager</span>
                </div>
                <div className="py-6 px-3 space-y-1">
                  {navigation.map((item) => (
                    <NavItem key={item.name} item={item} mobile />
                  ))}
                </div>
                <div className="absolute bottom-0 w-full p-4 border-t bg-background">
                   <Button variant="outline" className="w-full justify-start gap-2" onClick={logout}>
                    <LogOut className="h-4 w-4" />
                    Cerrar Sesión
                  </Button>
                </div>
              </SheetContent>
            </Sheet>
            <span className="font-semibold md:hidden">EduManager</span>
          </div>

          <div className="hidden md:flex flex-1 max-w-md relative ml-4">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder="Buscar estudiantes, cursos..." 
              className="pl-9 bg-muted/40 border-none focus-visible:ring-1"
            />
          </div>

          <div className="flex items-center gap-2 md:gap-4">
            <Button variant="ghost" size="icon" className="text-muted-foreground relative">
              <Bell className="h-5 w-5" />
              <span className="absolute top-2 right-2 h-2 w-2 bg-destructive rounded-full border border-background"></span>
            </Button>
            <Avatar className="md:hidden h-8 w-8">
              <AvatarImage src={user?.avatar} />
              <AvatarFallback>{user?.name.charAt(0)}</AvatarFallback>
            </Avatar>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
}
