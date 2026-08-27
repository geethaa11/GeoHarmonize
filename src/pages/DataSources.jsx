import { useState } from "react";
import { UploadCloud, FileCheck2 } from "lucide-react";
import Topbar from "../components/Topbar";
import StatusBadge from "../components/StatusBadge";
import { dataSources } from "../data/mockData";

function formatDate(iso) {
  return new Date(iso).toLocaleString("en-IN", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function DataSources() {
  const [dragOver, setDragOver] = useState(false);
  const [queuedFile, setQueuedFile] = useState(null);

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) setQueuedFile(file.name);
  }

  function handleSelect(e) {
    const file = e.target.files?.[0];
    if (file) setQueuedFile(file.name);
  }

  return (
    <div>
      <Topbar title="Data Sources" subtitle="Connect and monitor incoming geospatial and tabular datasets" />

      <div className="px-6 md:px-8 py-6 space-y-6">
        {/* Upload zone — wired to backend upload endpoint by the team */}
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragOver ? "border-contour bg-contour/5" : "border-ink/15 bg-white"
          }`}
        >
          {queuedFile ? (
            <div className="flex flex-col items-center gap-2">
              <FileCheck2 size={28} className="text-contour" />
              <p className="text-sm text-ink-800 font-medium">{queuedFile}</p>
              <p className="text-xs text-ink-600/60">
                Queued locally — hook this up to the backend ingest endpoint to actually submit it.
              </p>
              <button
                onClick={() => setQueuedFile(null)}
                className="mt-2 text-xs text-alert hover:underline"
              >
                Remove
              </button>
            </div>
          ) : (
            <label className="flex flex-col items-center gap-2 cursor-pointer">
              <UploadCloud size={28} className="text-ink-600/50" />
              <p className="text-sm text-ink-800 font-medium">
                Drop a SHP, GeoTIFF, GeoJSON, CSV or XML file here
              </p>
              <p className="text-xs text-ink-600/60">or click to browse</p>
              <input type="file" className="hidden" onChange={handleSelect} />
            </label>
          )}
        </div>

        {/* Source list */}
        <div className="bg-white border border-ink/10 rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase tracking-wide text-ink-600/50 border-b border-ink/10">
                <th className="px-4 py-3 font-medium">Source</th>
                <th className="px-4 py-3 font-medium">Format</th>
                <th className="px-4 py-3 font-medium">Coord. System</th>
                <th className="px-4 py-3 font-medium">Records</th>
                <th className="px-4 py-3 font-medium">Last Sync</th>
                <th className="px-4 py-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {dataSources.map((s) => (
                <tr key={s.id} className="border-b border-ink/5 last:border-0 hover:bg-paper-dim/40">
                  <td className="px-4 py-3">
                    <p className="font-medium text-ink-800">{s.name}</p>
                    <p className="text-xs text-ink-600/50">{s.type}</p>
                  </td>
                  <td className="px-4 py-3 font-mono text-xs text-ink-600/70">{s.format}</td>
                  <td className="px-4 py-3 font-mono text-xs text-ink-600/70">{s.coordSystem}</td>
                  <td className="px-4 py-3 text-ink-800">{s.records.toLocaleString()}</td>
                  <td className="px-4 py-3 text-xs text-ink-600/60">{formatDate(s.lastSync)}</td>
                  <td className="px-4 py-3">
                    <StatusBadge status={s.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
