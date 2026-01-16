import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Box,
  Paper,
  Typography,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Grid,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { scansApi } from "../../api/scans";
import type { ScanResponse } from "../../types";

const ResultsViewer: React.FC = () => {
  const { runId } = useParams<{ runId: string }>();
  const [scan, setScan] = useState<ScanResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (runId) {
      loadScan();
    }
  }, [runId]);

  const loadScan = async () => {
    if (!runId) return;

    setLoading(true);
    try {
      const data = await scansApi.getScan(runId);
      setScan(data);
    } catch (err: any) {
      setError(err.message || "Failed to load scan results");
    } finally {
      setLoading(false);
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

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !scan) {
    return (
      <Alert severity="error">
        {error || "Scan not found"}
      </Alert>
    );
  }

  const scoreData = [
    { name: "Security Score", value: scan.score.security_score },
    { name: "Remaining Risk", value: 100 - scan.score.security_score },
  ];

  const COLORS = ["#4caf50", "#ff9800"];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Scan Results
      </Typography>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: "center" }}>
            <Typography variant="h6" gutterBottom>
              Security Score
            </Typography>
            <Typography variant="h3" color="primary">
              {scan.score.security_score.toFixed(2)}
            </Typography>
            <Chip
              label={scan.score.verdict}
              color={getVerdictColor(scan.score.verdict) as any}
              sx={{ mt: 2 }}
            />
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Score Breakdown
            </Typography>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={scoreData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value.toFixed(1)}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {scoreData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Metrics
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Jailbreak Success Rate
            </Typography>
            <Typography variant="h6">
              {(scan.score.jailbreak_success_rate * 100).toFixed(1)}%
            </Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Injection Success Rate
            </Typography>
            <Typography variant="h6">
              {(scan.score.prompt_injection_success_rate * 100).toFixed(1)}%
            </Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              PII Leak Rate
            </Typography>
            <Typography variant="h6">
              {(scan.score.pii_leak_rate * 100).toFixed(1)}%
            </Typography>
          </Grid>
          <Grid item xs={6} md={3}>
            <Typography variant="body2" color="text.secondary">
              Toxicity Severity
            </Typography>
            <Typography variant="h6">
              {scan.score.toxicity_severity.toFixed(2)}
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Attack Results ({scan.attacks.length})
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Category</TableCell>
                <TableCell>Prompt</TableCell>
                <TableCell>Blocked</TableCell>
                <TableCell>Jailbreak</TableCell>
                <TableCell>Injection</TableCell>
                <TableCell>PII Leak</TableCell>
                <TableCell>Details</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {scan.attacks.map((attack) => (
                <TableRow key={attack.attack_id}>
                  <TableCell>{attack.category}</TableCell>
                  <TableCell sx={{ maxWidth: 300 }}>
                    {attack.prompt.substring(0, 50)}...
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={attack.response.blocked ? "Yes" : "No"}
                      color={attack.response.blocked ? "success" : "default"}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {attack.judge.jailbreak_success ? "✓" : "✗"}
                  </TableCell>
                  <TableCell>
                    {attack.judge.prompt_injection_success ? "✓" : "✗"}
                  </TableCell>
                  <TableCell>
                    {attack.judge.pii_leak ? "✓" : "✗"}
                  </TableCell>
                  <TableCell>
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        View Details
                      </AccordionSummary>
                      <AccordionDetails>
                        <Box>
                          <Typography variant="subtitle2">Full Prompt:</Typography>
                          <Typography variant="body2" sx={{ mb: 2 }}>
                            {attack.prompt}
                          </Typography>
                          <Typography variant="subtitle2">Response:</Typography>
                          <Typography variant="body2" sx={{ mb: 2 }}>
                            {attack.response.content}
                          </Typography>
                          <Typography variant="subtitle2">Judge Notes:</Typography>
                          <Typography variant="body2">
                            {attack.judge.notes.join(", ") || "None"}
                          </Typography>
                        </Box>
                      </AccordionDetails>
                    </Accordion>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default ResultsViewer;

