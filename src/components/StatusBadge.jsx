const STYLES = {
  harmonized: "bg-contour/10 text-contour border-contour/30",
  conflict: "bg-alert/10 text-alert border-alert/30",
  processing: "bg-seal/10 text-seal-dark border-seal/30",
};

const LABELS = {
  harmonized: "Harmonized",
  conflict: "Conflict",
  processing: "Processing",
};

export default function StatusBadge({ status }) {
  const style = STYLES[status] || STYLES.processing;
  const label = LABELS[status] || status;
  return (
    <span
      className={`inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full border ${style}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      {label}
    </span>
  );
}
