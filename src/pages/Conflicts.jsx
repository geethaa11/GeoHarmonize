import { useEffect, useState } from "react";
import { AlertTriangle } from "lucide-react";
import Topbar from "../components/Topbar";
import { getConflicts } from "../api/api";

export default function Conflicts() {
  const [conflicts, setConflicts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadConflicts() {
      try {
        const data = await getConflicts();
        setConflicts(data.conflicts || []);
      } catch (err) {
        setError("Unable to load conflicts from backend.");
      } finally {
        setLoading(false);
      }
    }

    loadConflicts();
  }, []);

  return (
    <div>
      <Topbar
        title="Conflicts"
        subtitle="Parcels where sources disagree — needs manual review or a resolution rule"
      />

      <div className="px-6 md:px-8 py-6">
        <div className="space-y-4 max-w-3xl">
          {loading && (
            <p className="text-sm text-ink-600/60">
              Loading conflicts...
            </p>
          )}

          {error && (
            <p className="text-sm text-alert">
              {error}
            </p>
          )}

          {!loading &&
            !error &&
            conflicts.map((c) => (
              <div
                key={c.conflict_id}
                className="bg-white border border-alert/20 rounded-lg p-4"
              >
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 p-1.5 rounded-full bg-alert/10 text-alert shrink-0">
                    <AlertTriangle size={16} />
                  </div>

                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <p className="font-mono text-xs text-ink-600/50">
                        {c.conflict_id}
                      </p>

                      <span className="text-xs font-mono text-ink-600/50">
                        {Math.round((c.confidence || 0) * 100)}% confidence
                      </span>
                    </div>

                    <p className="font-medium text-ink-800 mt-0.5">
                      Parcel {c.parcel_id}
                    </p>

                    <p className="text-sm text-alert mt-1">
                      {c.description}
                    </p>

                    <p className="text-xs text-ink-600/50 mt-2">
                      Type: {c.conflict_type} · Severity: {c.severity}
                    </p>

                    <p className="text-xs text-ink-600/50 mt-1">
                      Sources: {c.source_a} → {c.source_b}
                    </p>

                    <div className="flex gap-2 mt-3">
                      <button className="text-xs px-3 py-1.5 rounded-md bg-ink-800 text-white hover:bg-ink-700 transition-colors">
                        Review parcel
                      </button>

                      <button className="text-xs px-3 py-1.5 rounded-md border border-ink/15 text-ink-700 hover:border-ink/30 transition-colors">
                        Flag for surveyor
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}

          {!loading && !error && conflicts.length === 0 && (
            <p className="text-sm text-ink-600/60">
              No conflicts right now — nice.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}