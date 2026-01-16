import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  TextField,
  Paper,
  Typography,
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
} from "@mui/material";
import { useScanStore } from "../../store/scanStore";
import { useNavigate } from "react-router-dom";

const ScanDashboard: React.FC = () => {
  const navigate = useNavigate();
  const { scanHistory, loading, error, createScan, fetchScans } = useScanStore();
  const [systemPrompt, setSystemPrompt] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchScans();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSubmit = async () => {
    if (!systemPrompt.trim()) {
      return;
    }

    setSubmitting(true);
    try {
      const scan = await createScan({
        system_prompt: systemPrompt,
      });
      navigate(`/results/${scan.run_id}`);
    } catch (err) {
      // Error handled by store
    } finally {
      setSubmitting(false);
    }
  };

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case "PASS":
        return "success";
      case "WARN":
        return "warning";
      case "FAIL":
        return "error";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Scan Dashboard
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => {}}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          New Scan
        </Typography>
        <TextField
          fullWidth
          multiline
          rows={6}
          label="System Prompt"
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          placeholder="Enter your system prompt here..."
          sx={{ mb: 2 }}
        />
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={submitting || !systemPrompt.trim()}
        >
          {submitting ? <CircularProgress size={24} /> : "Run Scan"}
        </Button>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Scan History
        </Typography>
        {loading ? (
          <CircularProgress />
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Run ID</TableCell>
                  <TableCell>Model</TableCell>
                  <TableCell>Verdict</TableCell>
                  <TableCell>Score</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {scanHistory.map((scan) => (
                  <TableRow key={scan.run_id}>
                    <TableCell>{scan.run_id.substring(0, 8)}...</TableCell>
                    <TableCell>{scan.model_id}</TableCell>
                    <TableCell>
                      <Chip
                        label={scan.verdict}
                        color={getVerdictColor(scan.verdict) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{scan.security_score.toFixed(2)}</TableCell>
                    <TableCell>
                      {new Date(scan.created_at).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        onClick={() => navigate(`/results/${scan.run_id}`)}
                      >
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Paper>
    </Box>
  );
};

export default ScanDashboard;

