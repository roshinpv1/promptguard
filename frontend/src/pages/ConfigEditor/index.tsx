import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Paper,
  Typography,
  Alert,
  CircularProgress,
} from "@mui/material";
// SyntaxHighlighter removed for now - using plain textarea
import { configApi } from "../../api/config";

const ConfigEditor: React.FC = () => {
  const [configYaml, setConfigYaml] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [validationResult, setValidationResult] = useState<{
    valid: boolean;
    error?: string;
  } | null>(null);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    setLoading(true);
    try {
      const response = await configApi.getConfig();
      // Convert config to YAML (simple version)
      const yaml = JSON.stringify(response.config, null, 2);
      setConfigYaml(yaml);
    } catch (err: any) {
      setError(err.message || "Failed to load config");
    } finally {
      setLoading(false);
    }
  };

  const handleValidate = async () => {
    setValidationResult(null);
    try {
      const result = await configApi.validateConfig(configYaml);
      setValidationResult(result);
      if (!result.valid) {
        setError(result.error || "Invalid configuration");
      } else {
        setSuccess("Configuration is valid!");
      }
    } catch (err: any) {
      setValidationResult({ valid: false, error: err.message });
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccess(null);

    try {
      // Parse YAML to JSON
      const config = JSON.parse(configYaml);
      await configApi.updateConfig({ config });
      setSuccess("Configuration saved successfully!");
    } catch (err: any) {
      setError(err.message || "Failed to save config");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Configuration Editor
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {validationResult && (
        <Alert
          severity={validationResult.valid ? "success" : "error"}
          sx={{ mb: 2 }}
        >
          {validationResult.valid
            ? "Configuration is valid"
            : `Validation failed: ${validationResult.error}`}
        </Alert>
      )}

      <Paper sx={{ p: 3, mb: 2 }}>
        <Box sx={{ mb: 2, display: "flex", gap: 2 }}>
          <Button variant="outlined" onClick={handleValidate}>
            Validate
          </Button>
          <Button
            variant="contained"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? <CircularProgress size={24} /> : "Save"}
          </Button>
          <Button variant="outlined" onClick={loadConfig}>
            Reload
          </Button>
        </Box>

        <textarea
          value={configYaml}
          onChange={(e) => setConfigYaml(e.target.value)}
          style={{
            width: "100%",
            minHeight: "500px",
            fontFamily: "monospace",
            padding: "12px",
            border: "1px solid #ccc",
            borderRadius: "4px",
          }}
        />
      </Paper>
    </Box>
  );
};

export default ConfigEditor;

