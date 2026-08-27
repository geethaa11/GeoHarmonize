import { useState, useMemo } from "react";
import Topbar from "../components/Topbar";
import ParcelMap from "../components/ParcelMap";
import StatusBadge from "../components/StatusBadge";
import { landRecords } from "../data/mockData";

const FILTERS = ["all", "harmonized", "conflict", "processing"];

export default function MapExplorer() {
  const [filter, setFilter] = useState("all");

  const filtered = useMemo(
    () => (filter === "all" ? landRecords : landRecords.filter((r) => r.status === filter)),
    [filter]
  );

  return (
    <div>
      <Topbar title="Map Explorer" subtitle="Visualize harmonized parcels across data sources" />

      <div className="px-6 md:px-8 py-6 space-y-4">
        <div className="flex flex-wrap gap-2">
          {FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-full text-sm border capitalize transition-colors ${
                filter === f
                  ? "bg-ink-800 text-white border-ink-800"
                  : "bg-white text-ink-600/70 border-ink/10 hover:border-ink/30"
              }`}
            >
              {f}
            </button>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <ParcelMap height="560px" records={filtered} />
          </div>

          <div className="bg-white border border-ink/10 rounded-lg p-4 max-h-[560px] overflow-y-auto">
            <h2 className="font-display font-semibold text-ink-800 mb-3">
              {filtered.length} parcel{filtered.length !== 1 ? "s" : ""}
            </h2>
            <ul className="space-y-3">
              {filtered.map((r) => (
                <li key={r.id} className="border border-ink/10 rounded-md p-3">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono text-xs text-ink-600/60">{r.id}</span>
                    <StatusBadge status={r.status} />
                  </div>
                  <p className="text-sm font-medium text-ink-800">{r.village} · Survey {r.surveyNo}</p>
                  <p className="text-xs text-ink-600/60 mt-0.5">{r.owner} · {r.areaSqm} sqm</p>
                  {r.conflictReason && (
                    <p className="text-xs text-alert mt-1">{r.conflictReason}</p>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
