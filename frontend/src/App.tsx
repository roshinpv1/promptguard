import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Layout from "./components/Layout";
import ScanDashboard from "./pages/ScanDashboard";
import APITester from "./pages/APITester";
import ResultsViewer from "./pages/ResultsViewer";
import ConfigEditor from "./pages/ConfigEditor";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#dc004e",
    },
  },
});

function App() {
  console.log("App component rendering");
  
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Navigate to="/scans" replace />} />
            <Route path="/scans" element={<ScanDashboard />} />
            <Route path="/test-api" element={<APITester />} />
            <Route path="/results/:runId" element={<ResultsViewer />} />
            <Route path="/config" element={<ConfigEditor />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;

