import { NavLink } from "react-router-dom";
import { LayoutGrid, Map, Layers, Table2, AlertTriangle, Compass } from "lucide-react";

const links = [
  { to: "/", label: "Overview", icon: LayoutGrid, end: true },
  { to: "/map", label: "Map Explorer", icon: Map },
  { to: "/sources", label: "Data Sources", icon: Layers },
  { to: "/records", label: "Land Records", icon: Table2 },
  { to: "/conflicts", label: "Conflicts", icon: AlertTriangle },
];

export default function Sidebar() {
  return (
    <aside className="hidden md:flex flex-col w-60 shrink-0 bg-ink-800 text-paper h-screen sticky top-0">
      <div className="flex items-center gap-2 px-5 py-6 border-b border-white/10">
        <Compass size={22} className="text-seal-light" strokeWidth={1.75} />
        <div className="leading-tight">
          <p className="font-display font-semibold tracking-wide text-[15px]">GeoDesk</p>
          <p className="text-[11px] text-white/50 font-mono">SIH26013</p>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {links.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm transition-colors ${
                isActive
                  ? "bg-white/10 text-white font-medium"
                  : "text-white/60 hover:text-white hover:bg-white/5"
              }`
            }
          >
            <Icon size={17} strokeWidth={1.75} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-5 py-4 border-t border-white/10 text-[11px] text-white/40 font-mono leading-relaxed">
        Ministry of Rural Development
        <br />
        Disaster Management Theme
      </div>
    </aside>
  );
}
