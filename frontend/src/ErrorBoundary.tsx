import React, { Component, ErrorInfo, ReactNode } from "react";
import { Box, Typography, Alert } from "@mui/material";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <Box sx={{ p: 4 }}>
          <Alert severity="error">
            <Typography variant="h6">Something went wrong</Typography>
            <Typography variant="body2">
              {this.state.error?.message || "Unknown error"}
            </Typography>
            <Typography variant="body2" sx={{ mt: 2 }}>
              Check the browser console for more details.
            </Typography>
          </Alert>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

