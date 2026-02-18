import { Terminal, Zap } from "lucide-react";

const AlphaHeader = () => {
  return (
    <header className="border-b border-border bg-card/30 backdrop-blur-sm">
      <div className="max-w-[1440px] mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Terminal className="w-5 h-5 text-primary" />
            <h1 className="font-display font-bold text-lg tracking-tight text-foreground">
              ALPHA<span className="text-primary">TERMINAL</span>
            </h1>
          </div>
          <div className="hidden sm:flex items-center gap-1 px-2 py-0.5 rounded-full bg-primary/10 border border-primary/20">
            <Zap className="w-3 h-3 text-primary" />
            <span className="text-[10px] font-mono text-primary font-medium">LIVE</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-[10px] font-mono text-muted-foreground hidden sm:block">
            {new Date().toLocaleDateString("pt-BR", {
              weekday: "long",
              day: "2-digit",
              month: "long",
              year: "numeric",
            })}
          </span>
          <div className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
        </div>
      </div>
    </header>
  );
};

export default AlphaHeader;
