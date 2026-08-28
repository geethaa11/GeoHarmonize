import { useEffect, useState } from "react";
import { Search } from "lucide-react";
import Topbar from "../components/Topbar";
import StatusBadge from "../components/StatusBadge";
import { getParcels } from "../api/api";

export default function LandRecords() {
  const [query, setQuery] = useState("");
  const [parcels, setParcels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadParcels() {
      try {
        const data = await getParcels();
        setParcels(data.parcels || []);
      } catch (err) {
        setError("Unable to load land records from backend.");
      } finally {
        setLoading(false);
      }
    }

    loadParcels();
  }, []);

  const q = query.trim().toLowerCase();

  const filtered = parcels.filter((r) => {
    if (!q) return true;

    return (
      r.parcel_id?.toLowerCase().includes(q) ||
      r.land_type?.toLowerCase().includes(q) ||
      r.source?.toLowerCase().includes(q)
    );
  });

  return (
    <div>
      <Topbar
        title="Land Records"
        subtitle="Harmonized parcel register across all connected sources"
      />

      <div className="px-6 md:px-8 py-6 space-y-4">
        <div className="flex items-center gap-2 bg-white border border-ink/10 rounded-md px-3 py-2 max-w-md">
          <Search size={15} className="text-ink-600/50" />

          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by parcel ID, land type or source"
            className="w-full text-sm outline-none placeholder:text-ink-600/40"
          />
        </div>

        {loading && (
          <p className="text-sm text-ink-600/60">
            Loading land records...
          </p>
        )}

        {error && (
          <p className="text-sm text-alert">
            {error}
          </p>
        )}

        {!loading && !error && (
          <div className="bg-white border border-ink/10 rounded-lg overflow-x-auto">
            <table className="w-full text-sm min-w-[820px]">
              <thead>
                <tr className="text-left text-xs uppercase tracking-wide text-ink-600/50 border-b border-ink/10">
                  <th className="px-4 py-3 font-medium">Parcel ID</th>
                  <th className="px-4 py-3 font-medium">Land Type</th>
                  <th className="px-4 py-3 font-medium">Source</th>
                  <th className="px-4 py-3 font-medium">Area (sqm)</th>
                  <th className="px-4 py-3 font-medium">Confidence</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                </tr>
              </thead>

              <tbody>
                {filtered.map((r) => (
                  <tr
                    key={r.parcel_id}
                    className="border-b border-ink/5 last:border-0 hover:bg-paper-dim/40"
                  >
                    <td className="px-4 py-3 font-mono text-xs text-ink-800">
                      {r.parcel_id}
                    </td>

                    <td className="px-4 py-3 text-ink-800">
                      {r.land_type || "—"}
                    </td>

                    <td className="px-4 py-3 text-ink-600/70">
                      {r.source || "—"}
                    </td>

                    <td className="px-4 py-3 text-ink-600/70">
                      {typeof r.area === "number"
                        ? r.area.toLocaleString()
                        : "—"}
                    </td>

                    <td className="px-4 py-3">
                      {typeof r.confidence === "number" ? (
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-1.5 bg-paper-dim rounded-full overflow-hidden">
                            <div
                              className="h-full bg-contour"
                              style={{
                                width: `${r.confidence * 100}%`,
                              }}
                            />
                          </div>

                          <span className="text-xs font-mono text-ink-600/70">
                            {Math.round(r.confidence * 100)}%
                          </span>
                        </div>
                      ) : (
                        <span className="text-xs text-ink-600/40">
                          —
                        </span>
                      )}
                    </td>

                    <td className="px-4 py-3">
                      <StatusBadge status={r.status} />
                    </td>
                  </tr>
                ))}

                {filtered.length === 0 && (
                  <tr>
                    <td
                      colSpan={6}
                      className="px-4 py-10 text-center text-sm text-ink-600/50"
                    >
                      No parcels found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
