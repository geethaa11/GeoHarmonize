// Mock data layer.
// Replace these functions with real API calls once the backend team exposes endpoints.
// Keeping all "fake network" data in one file means swapping to real fetch() calls
// later only touches this file, not every component.

export const dataSources = [
  {
    id: "src-01",
    name: "State Revenue Dept. — Bhu-Naksha",
    type: "Cadastral Map (Shapefile)",
    format: "SHP",
    status: "harmonized",
    records: 18420,
    lastSync: "2026-08-24T09:12:00Z",
    coordSystem: "EPSG:32644 (UTM 44N)"
  },
  {
    id: "src-02",
    name: "Survey of India Topo Sheets",
    type: "Raster Topographic Sheet",
    format: "GeoTIFF",
    status: "harmonized",
    records: 6210,
    lastSync: "2026-08-23T14:40:00Z",
    coordSystem: "EPSG:4326 (WGS 84)"
  },
  {
    id: "src-03",
    name: "Municipal Property Tax Records",
    type: "Tabular Address Data",
    format: "CSV",
    status: "conflict",
    records: 41120,
    lastSync: "2026-08-25T07:05:00Z",
    coordSystem: "No CRS (address-only)"
  },
  {
    id: "src-04",
    name: "Drone Survey — Ward 12 Resurvey",
    type: "Orthophoto + Parcel Vector",
    format: "GeoJSON",
    status: "processing",
    records: 3040,
    lastSync: "2026-08-25T11:20:00Z",
    coordSystem: "EPSG:32644 (UTM 44N)"
  },
  {
    id: "src-05",
    name: "Registration Dept. Sale Deeds",
    type: "Tabular Transaction Data",
    format: "XML",
    status: "conflict",
    records: 27890,
    lastSync: "2026-08-22T18:00:00Z",
    coordSystem: "No CRS (parcel ID linked)"
  }
];

export const harmonizationStats = {
  totalParcels: 96680,
  harmonizedParcels: 61150,
  conflictParcels: 8420,
  pendingParcels: 27110,
  sourcesConnected: 5,
  avgConfidence: 87
};

export const weeklyIngestTrend = [
  { day: "Mon", parcels: 4200 },
  { day: "Tue", parcels: 5100 },
  { day: "Wed", parcels: 4800 },
  { day: "Thu", parcels: 6300 },
  { day: "Fri", parcels: 7100 },
  { day: "Sat", parcels: 3900 },
  { day: "Sun", parcels: 2600 }
];

export const conflictBreakdown = [
  { name: "Boundary mismatch", value: 3620 },
  { name: "Owner name mismatch", value: 2140 },
  { name: "Duplicate parcel ID", value: 1580 },
  { name: "CRS misalignment", value: 1080 }
];

// Sample harmonized parcel records for the map + table views.
// lat/lng are illustrative points, not real cadastral coordinates.
export const landRecords = [
  {
    id: "PCL-100234",
    village: "Anna Nagar West",
    surveyNo: "112/4A",
    owner: "R. Kannan",
    areaSqm: 1240,
    status: "harmonized",
    confidence: 96,
    lat: 13.0878,
    lng: 80.2101,
    sources: ["Bhu-Naksha", "Property Tax"]
  },
  {
    id: "PCL-100235",
    village: "Anna Nagar West",
    surveyNo: "112/4B",
    owner: "S. Meenakshi",
    areaSqm: 980,
    status: "harmonized",
    confidence: 91,
    lat: 13.0885,
    lng: 80.2112,
    sources: ["Bhu-Naksha", "Sale Deeds"]
  },
  {
    id: "PCL-100311",
    village: "Kolathur",
    surveyNo: "44/2",
    owner: "M. Suresh Babu",
    areaSqm: 2100,
    status: "conflict",
    confidence: 54,
    lat: 13.1210,
    lng: 80.2185,
    sources: ["Property Tax", "Sale Deeds"],
    conflictReason: "Boundary shifted 4.2m against SoI topo sheet"
  },
  {
    id: "PCL-100312",
    village: "Kolathur",
    surveyNo: "44/3",
    owner: "P. Iyer",
    areaSqm: 1560,
    status: "processing",
    confidence: 0,
    lat: 13.1225,
    lng: 80.2199,
    sources: ["Drone Survey Ward 12"]
  },
  {
    id: "PCL-100450",
    village: "Villivakkam",
    surveyNo: "78/1C",
    owner: "K. Devaraj",
    areaSqm: 860,
    status: "conflict",
    confidence: 61,
    lat: 13.1064,
    lng: 80.1998,
    sources: ["Bhu-Naksha", "Property Tax"],
    conflictReason: "Owner name mismatch across two registers"
  },
  {
    id: "PCL-100451",
    village: "Villivakkam",
    surveyNo: "78/1D",
    owner: "N. Bhavani",
    areaSqm: 1120,
    status: "harmonized",
    confidence: 98,
    lat: 13.1072,
    lng: 80.2005,
    sources: ["Bhu-Naksha", "SoI Topo", "Sale Deeds"]
  }
];

export const activityFeed = [
  { id: 1, text: "Drone Survey — Ward 12 batch ingested (3,040 parcels)", time: "12 min ago", kind: "info" },
  { id: 2, text: "Boundary conflict flagged on PCL-100311 (Kolathur)", time: "48 min ago", kind: "conflict" },
  { id: 3, text: "Municipal Property Tax Records re-synced", time: "2 hr ago", kind: "info" },
  { id: 4, text: "241 parcels auto-harmonized in Anna Nagar West", time: "5 hr ago", kind: "success" },
  { id: 5, text: "CRS misalignment resolved for Bhu-Naksha batch #18", time: "1 day ago", kind: "success" }
];
