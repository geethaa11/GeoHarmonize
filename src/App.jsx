import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Overview from "./pages/Overview";
import MapExplorer from "./pages/MapExplorer";
import DataSources from "./pages/DataSources";
import LandRecords from "./pages/LandRecords";
import Conflicts from "./pages/Conflicts";

export default function App() {
  return (
    <div className="flex bg-contours">
      <Sidebar />
      <main className="flex-1 min-w-0">
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/map" element={<MapExplorer />} />
          <Route path="/sources" element={<DataSources />} />
          <Route path="/records" element={<LandRecords />} />
          <Route path="/conflicts" element={<Conflicts />} />
        </Routes>
      </main>
    </div>
  );
}
