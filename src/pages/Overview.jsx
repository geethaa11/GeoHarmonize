import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import Topbar from "../components/Topbar";
import StatCard from "../components/StatCard";
import ParcelMap from "../components/ParcelMap";
import { harmonizationStats, weeklyIngestTrend, conflictBreakdown, activityFeed, dataSources } from "../data/mockData";

const PIE_COLORS = ["#B5533C", "#B08D3E", "#3E7C7C", "#26385A"];

const ACTIVITY_DOT = {
  info: "bg-ink-600",
  conflict: "bg-alert",
  success: "bg-contour",
};

export default function Overview() {
  const { totalParcels, harmonizedParcels, conflictParcels, pendingParcels, sourcesConnected, avgConfidence } =
    harmonizationStats;

  return (
    <div>
      <Topbar
        title="Overview"
        subtitle="Multi-source geospatial harmonization status for urban land records"
      />

      <div className="px-6 md:px-8 py-6 space-y-6">
        {/* Stat row */}
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
          <StatCard label="Total Parcels" value={totalParcels.toLocaleString()} />
          <StatCard label="Harmonized" value={harmonizedParcels.toLocaleString()} accent="contour" />
          <StatCard label="Conflicts" value={conflictParcels.toLocaleString()} accent="alert" />
          <StatCard label="Pending" value={pendingParcels.toLocaleString()} accent="seal" />
          <StatCard label="Sources Live" value={sourcesConnected} note={`${avgConfidence}% avg. confidence`} />
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Map preview */}
          <div className="lg:col-span-2 bg-white border border-ink/10 rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-display font-semibold text-ink-800">Parcel Map Preview</h2>
              <a href="/map" className="text-xs text-contour font-medium hover:underline">
                Open full explorer →
              </a>
            </div>
            <ParcelMap height="360px" />
          </div>

          {/* Conflict breakdown */}
          <div className="bg-white border border-ink/10 rounded-lg p-4">
            <h2 className="font-display font-semibold text-ink-800 mb-3">Conflict Breakdown</h2>
            <ResponsiveContainer width="100%" height={180}>
              <PieChart>
                <Pie
                  data={conflictBreakdown}
                  dataKey="value"
                  nameKey="name"
                  innerRadius={45}
                  outerRadius={75}
                  paddingAngle={2}
                >
                  {conflictBreakdown.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <ul className="mt-2 space-y-1.5">
              {conflictBreakdown.map((c, i) => (
                <li key={c.name} className="flex items-center justify-between text-xs">
                  <span className="flex items-center gap-2 text-ink-600/70">
                    <span
                      className="w-2 h-2 rounded-full"
                      style={{ background: PIE_COLORS[i % PIE_COLORS.length] }}
                    />
                    {c.name}
                  </span>
                  <span className="font-mono text-ink-800">{c.value.toLocaleString()}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Ingest trend */}
          <div className="lg:col-span-2 bg-white border border-ink/10 rounded-lg p-4">
            <h2 className="font-display font-semibold text-ink-800 mb-3">Weekly Parcel Ingest</h2>
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={weeklyIngestTrend}>
                <defs>
                  <linearGradient id="fillIngest" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#3E7C7C" stopOpacity={0.35} />
                    <stop offset="100%" stopColor="#3E7C7C" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="day" tick={{ fontSize: 12, fill: "#26385A" }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12, fill: "#26385A" }} axisLine={false} tickLine={false} width={40} />
                <Tooltip />
                <Area type="monotone" dataKey="parcels" stroke="#3E7C7C" strokeWidth={2} fill="url(#fillIngest)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Activity feed */}
          <div className="bg-white border border-ink/10 rounded-lg p-4">
            <h2 className="font-display font-semibold text-ink-800 mb-3">Recent Activity</h2>
            <ul className="space-y-3">
              {activityFeed.map((a) => (
                <li key={a.id} className="flex gap-2.5 text-sm">
                  <span className={`mt-1.5 w-1.5 h-1.5 rounded-full shrink-0 ${ACTIVITY_DOT[a.kind]}`} />
                  <div>
                    <p className="text-ink-800 leading-snug">{a.text}</p>
                    <p className="text-xs text-ink-600/50 font-mono">{a.time}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Source status strip */}
        <div className="bg-white border border-ink/10 rounded-lg p-4">
          <h2 className="font-display font-semibold text-ink-800 mb-3">Connected Sources</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-3">
            {dataSources.map((s) => (
              <div key={s.id} className="border border-ink/10 rounded-md p-3">
                <p className="text-xs font-mono text-ink-600/50">{s.format}</p>
                <p className="text-sm font-medium text-ink-800 leading-snug mt-0.5">{s.name}</p>
                <p className="text-xs text-ink-600/60 mt-1">{s.records.toLocaleString()} records</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
