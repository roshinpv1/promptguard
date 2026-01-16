import React, { useState } from "react";
import {
  Box,
  Button,
  TextField,
  Paper,
  Typography,
  Alert,
  CircularProgress,
  MenuItem,
  Grid,
} from "@mui/material";
import { testApi } from "../../api/testApi";
import { useNavigate } from "react-router-dom";

const APITester: React.FC = () => {
  const navigate = useNavigate();
  const [apiUrl, setApiUrl] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [modelId, setModelId] = useState("");
  const [systemPrompt, setSystemPrompt] = useState("");
  const [apiType, setApiType] = useState("openai");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!apiUrl || !modelId || !systemPrompt) {
      setError("Please fill in all required fields");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await testApi.testExternalAPI({
        api_url: apiUrl,
        api_key: apiKey || undefined,
        model_id: modelId,
        system_prompt: systemPrompt,
        api_type: apiType,
      });

      // Navigate to results (we'll create a temp result view)
      navigate(`/results/${response.run_id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || "Failed to test API");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Test External LLM API
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              select
              label="API Type"
              value={apiType}
              onChange={(e) => setApiType(e.target.value)}
            >
              <MenuItem value="openai">OpenAI</MenuItem>
              <MenuItem value="anthropic">Anthropic</MenuItem>
              <MenuItem value="azure">Azure OpenAI</MenuItem>
              <MenuItem value="custom">Custom</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="API Endpoint URL"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              placeholder="https://api.openai.com/v1/chat/completions"
              required
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="API Key"
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-..."
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Model ID"
              value={modelId}
              onChange={(e) => setModelId(e.target.value)}
              placeholder="gpt-4"
              required
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={6}
              label="System Prompt"
              value={systemPrompt}
              onChange={(e) => setSystemPrompt(e.target.value)}
              placeholder="Enter your system prompt here..."
              required
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              variant="contained"
              onClick={handleSubmit}
              disabled={loading || !apiUrl || !modelId || !systemPrompt}
              size="large"
            >
              {loading ? <CircularProgress size={24} /> : "Run Security Test"}
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default APITester;

