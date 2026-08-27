import { Search, Bell } from "lucide-react";

export default function Topbar({ title, subtitle }) {
  return (
    <header className="flex items-center justify-between px-6 md:px-8 py-5 border-b border-ink/10 bg-paper/80 backdrop-blur sticky top-0 z-10">
      <div>
        <h1 className="font-display text-xl font-semibold text-ink-800">{title}</h1>
        {subtitle && <p className="text-sm text-ink-600/70 mt-0.5">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-2 bg-white border border-ink/10 rounded-md px-3 py-2 text-sm text-ink-600/70 w-64">
          <Search size={15} />
          <span>Search survey no. or parcel ID</span>
        </div>
        <button
          aria-label="Notifications"
          className="relative p-2 rounded-md border border-ink/10 bg-white hover:bg-paper-dim transition-colors"
        >
          <Bell size={16} className="text-ink-700" />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-alert" />
        </button>
      </div>
    </header>
  );
}
