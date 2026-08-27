import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { landRecords } from "../data/mockData";

const STATUS_COLOR = {
  harmonized: "#3E7C7C",
  conflict: "#B5533C",
  processing: "#B08D3E",
};

export default function ParcelMap({ height = "420px", records = landRecords, center }) {
  const mapCenter = center || [
    records.reduce((s, r) => s + r.lat, 0) / records.length,
    records.reduce((s, r) => s + r.lng, 0) / records.length,
  ];

  return (
    <div style={{ height }} className="rounded-lg overflow-hidden border border-ink/10">
      <MapContainer center={mapCenter} zoom={13} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {records.map((r) => (
          <CircleMarker
            key={r.id}
            center={[r.lat, r.lng]}
            radius={9}
            pathOptions={{
              color: STATUS_COLOR[r.status],
              fillColor: STATUS_COLOR[r.status],
              fillOpacity: 0.55,
              weight: 2,
            }}
          >
            <Popup>
              <div className="font-body text-sm">
                <p className="font-semibold font-mono">{r.id}</p>
                <p>{r.village} · Survey {r.surveyNo}</p>
                <p className="text-ink-600/70">{r.owner} · {r.areaSqm} sqm</p>
                {r.conflictReason && (
                  <p className="text-alert text-xs mt-1">{r.conflictReason}</p>
                )}
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
