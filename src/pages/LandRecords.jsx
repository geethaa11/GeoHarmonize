import { useState, useMemo } from "react";
import { Search } from "lucide-react";
import Topbar from "../components/Topbar";
import StatusBadge from "../components/StatusBadge";
import { landRecords } from "../data/mockData";

export default function LandRecords() {
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return landRecords;
    return landRecords.filter(
      (r) =>
        r.id.toLowerCase().includes(q) ||
        r.village.toLowerCase().includes(q) ||
        r.surveyNo.toLowerCase().includes(q) ||
        r.owner.toLowerCase().includes(q)
    );
  }, [query]);

  return (
    <div>
      <Topbar title="Land Records" subtitle="Harmonized parcel register across all connected sources" />

      <div className="px-6 md:px-8 py-6 space-y-4">
        <div className="flex items-center gap-2 bg-white border border-ink/10 rounded-md px-3 py-2 max-w-md">
          <Search size={15} className="text-ink-600/50" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by parcel ID, village, survey no. or owner"
            className="w-full text-sm outline-none placeholder:text-ink-600/40"
          />
        </div>

        <div className="bg-white border border-ink/10 rounded-lg overflow-x-auto">
          <table className="w-full text-sm min-w-[820px]">
            <thead>
              <tr className="text-left text-xs uppercase tracking-wide text-ink-600/50 border-b border-ink/10">
                <th className="px-4 py-3 font-medium">Parcel ID</th>
                <th className="px-4 py-3 font-medium">Village</th>
                <th className="px-4 py-3 font-medium">Survey No.</th>
                <th className="px-4 py-3 font-medium">Owner</th>
                <th className="px-4 py-3 font-medium">Area (sqm)</th>
                <th className="px-4 py-3 font-medium">Confidence</th>
                <th className="px-4 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((r) => (
                <tr key={r.id} className="border-b border-ink/5 last:border-0 hover:bg-paper-dim/40">
                  <td className="px-4 py-3 font-mono text-xs text-ink-800">{r.id}</td>
                  <td className="px-4 py-3 text-ink-800">{r.village}</td>
                  <td className="px-4 py-3 font-mono text-xs text-ink-600/70">{r.surveyNo}</td>
                  <td className="px-4 py-3 text-ink-800">{r.owner}</td>
                  <td className="px-4 py-3 text-ink-600/70">{r.areaSqm.toLocaleString()}</td>
                  <td className="px-4 py-3">
                    {r.confidence > 0 ? (
                      <div className="flex items-center gap-2">
                        <div className="w-16 h-1.5 bg-paper-dim rounded-full overflow-hidden">
                          <div
                            className="h-full bg-contour"
                            style={{ width: `${r.confidence}%` }}
                          />
                        </div>
                        <span className="text-xs font-mono text-ink-600/70">{r.confidence}%</span>
                      </div>
                    ) : (
                      <span className="text-xs text-ink-600/40">—</span>
                    )}
                  </td>
                  <td className="px-4 py-3">
                    <StatusBadge status={r.status} />
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-4 py-10 text-center text-sm text-ink-600/50">
                    No parcels match "{query}". Try a different survey number or owner name.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
