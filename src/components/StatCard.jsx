export default function StatCard({ label, value, unit, accent = "ink", note }) {
  const accentClass = {
    ink: "text-ink-800",
    contour: "text-contour",
    seal: "text-seal-dark",
    alert: "text-alert",
  }[accent];

  return (
    <div className="bg-white border border-ink/10 rounded-lg px-5 py-4 flex flex-col gap-1">
      <p className="text-xs uppercase tracking-wide text-ink-600/60 font-medium">{label}</p>
      <p className={`font-display text-3xl font-semibold ${accentClass}`}>
        {value}
        {unit && <span className="text-base font-body text-ink-600/50 ml-1">{unit}</span>}
      </p>
      {note && <p className="text-xs text-ink-600/50 mt-0.5">{note}</p>}
    </div>
  );
}
