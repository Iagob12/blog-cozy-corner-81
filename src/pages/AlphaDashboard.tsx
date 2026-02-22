import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { RadarOportunidades } from '@/components/alpha/RadarOportunidades';
import { SwingTradeAnalysis } from '@/components/alpha/SwingTradeAnalysis';
import { AlertsFeed } from '@/components/alpha/AlertsFeed';
import { PortfolioBuilder } from '@/components/alpha/PortfolioBuilder';
import { Target, TrendingUp, Bell, Briefcase } from 'lucide-react';

export function AlphaDashboard() {
  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Alpha Terminal</h1>
          <p className="text-muted-foreground">
            Sistema de Inteligência Tática - Meta: 5% ao mês
          </p>
        </div>
      </div>

      <Tabs defaultValue="portfolio" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="portfolio" className="flex items-center gap-2">
            <Briefcase className="w-4 h-4" />
            Carteira
          </TabsTrigger>
          <TabsTrigger value="radar" className="flex items-center gap-2">
            <Target className="w-4 h-4" />
            Radar
          </TabsTrigger>
          <TabsTrigger value="swing" className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            Swing Trade
          </TabsTrigger>
          <TabsTrigger value="alerts" className="flex items-center gap-2">
            <Bell className="w-4 h-4" />
            Alertas
          </TabsTrigger>
        </TabsList>

        <TabsContent value="portfolio">
          <PortfolioBuilder />
        </TabsContent>

        <TabsContent value="radar">
          <RadarOportunidades />
        </TabsContent>

        <TabsContent value="swing">
          <SwingTradeAnalysis />
        </TabsContent>

        <TabsContent value="alerts">
          <AlertsFeed />
        </TabsContent>
      </Tabs>
    </div>
  );
}
