import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "./components/Layout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { Dashboard } from "./pages/Dashboard";
import { Units } from "./pages/Units";
import { Hangars } from "./pages/Hangars";
import { AircraftPage } from "./pages/AircraftPage";
import { Assets } from "./pages/Assets";
import { Transactions } from "./pages/Transactions";
import { Inspections } from "./pages/Inspections";
import { LoginPage } from "./pages/LoginPage";
import { SignupPage } from "./pages/SignupPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
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
