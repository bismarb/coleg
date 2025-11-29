import DashboardLayout from "@/components/layout/DashboardLayout";
import { StatCard } from "@/components/dashboard/StatCard";
import { STATS, ENROLLMENT_DATA, PERFORMANCE_DATA } from "@/lib/mockData";
import { Users, GraduationCap, BookOpen, Activity } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";

export default function Dashboard() {
  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Panel Administrativo</h1>
            <p className="text-muted-foreground">Resumen general del sistema académico.</p>
          </div>
          {/* Placeholder for date/actions if needed */}
        </div>

        {/* Stats Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatCard 
            title="Total Estudiantes" 
            value={STATS.totalStudents} 
            icon={Users} 
            trend="+12%" 
            trendUp={true}
            description="desde el mes pasado"
          />
          <StatCard 
            title="Total Profesores" 
            value={STATS.totalTeachers} 
            icon={GraduationCap} 
            description="84 activos"
          />
          <StatCard 
            title="Cursos Activos" 
            value={STATS.activeCourses} 
            icon={BookOpen} 
            description="Semestre actual"
          />
          <StatCard 
            title="Tasa de Aprobación" 
            value={`${STATS.passRate}%`} 
            icon={Activity} 
            trend="+2.5%" 
            trendUp={true}
            description="promedio general"
          />
        </div>

        {/* Charts Grid */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
          
          {/* Enrollment Chart */}
          <Card className="col-span-4">
            <CardHeader>
              <CardTitle>Matrícula Estudiantil</CardTitle>
            </CardHeader>
            <CardContent className="pl-2">
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={ENROLLMENT_DATA}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                    <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value}`} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: "hsl(var(--card))", borderColor: "hsl(var(--border))" }}
                      itemStyle={{ color: "hsl(var(--foreground))" }}
                    />
                    <Line type="monotone" dataKey="students" stroke="hsl(var(--primary))" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          {/* Performance Chart */}
          <Card className="col-span-3">
            <CardHeader>
              <CardTitle>Rendimiento por Materia</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={PERFORMANCE_DATA} layout="vertical" margin={{ top: 0, right: 0, bottom: 0, left: 40 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="hsl(var(--border))" />
                    <XAxis type="number" hide />
                    <YAxis dataKey="subject" type="category" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} width={80} />
                    <Tooltip 
                      cursor={{ fill: 'transparent' }}
                      contentStyle={{ backgroundColor: "hsl(var(--card))", borderColor: "hsl(var(--border))" }}
                    />
                    <Bar dataKey="A" stackId="a" fill="hsl(var(--chart-1))" radius={[0, 4, 4, 0]} />
                    <Bar dataKey="B" stackId="a" fill="hsl(var(--chart-2))" />
                    <Bar dataKey="C" stackId="a" fill="hsl(var(--chart-3))" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
