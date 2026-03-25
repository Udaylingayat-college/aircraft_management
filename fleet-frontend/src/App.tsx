import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Dashboard } from "./pages/Dashboard";
import { Units } from "./pages/Units";
import { Hangars } from "./pages/Hangars";
import { AircraftPage } from "./pages/AircraftPage";
import { Assets } from "./pages/Assets";
import { Transactions } from "./pages/Transactions";
import { Inspections } from "./pages/Inspections";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/units" element={<Units />} />
          <Route path="/hangars" element={<Hangars />} />
          <Route path="/aircraft" element={<AircraftPage />} />
          <Route path="/assets" element={<Assets />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/inspections" element={<Inspections />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
