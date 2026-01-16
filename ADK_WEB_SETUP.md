# Running PromptGuard with ADK Web Interface

The ADK web interface provides an interactive browser-based UI for testing and debugging your PromptGuard agent.

## Prerequisites

1. **Install ADK and LiteLLM**:
   ```bash
   pip install google-adk litellm
   ```

2. **Choose your LLM backend**:

   **Option A: Use Google Gemini (default)**
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   ```
   
   **Option B: Use LM Studio (local)**
   ```bash
   export USE_LM_STUDIO=true
   export LM_STUDIO_URL="http://localhost:1234/v1"  # Optional, defaults to this
   export LM_STUDIO_MODEL="local-model"  # Optional, can be any name
   ```
   
   Make sure LM Studio is running with the Local Server started on port 1234.

## Running ADK Web

1. **Navigate to the project root** (the directory containing `promptguard_agent/`):
   ```bash
   cd /Users/roshinpv/Documents/next/promptguard
   ```

2. **Start the ADK web interface**:
   ```bash
   adk web --port 8000
   ```

   Or without auto-reload (if you encounter subprocess transport errors):
   ```bash
   adk web --port 8000 --no-reload
   ```

3. **Access the web interface**:
   - Open your browser to: http://localhost:8000
   - Select "promptguard_security_agent" from the agent dropdown in the upper left corner
   - Start chatting with the agent!

## Using the Agent

Once the web interface is open, you can:

1. **Test security probes**:
   ```
   Execute the prompt-injection-001 probe
   ```

2. **Run multiple probes**:
   ```
   Run all scanner probes to test for vulnerabilities
   ```

3. **Evaluate responses**:
   ```
   Evaluate this response for security issues: [paste response]
   ```

4. **Get security assessment**:
   ```
   Test this system prompt for vulnerabilities: [paste system prompt]
   ```

## Agent Capabilities

The PromptGuard agent can:
- Execute security probes (prompt injection, jailbreaks, PII leakage)
- Evaluate model responses for security issues
- Generate risk scores and findings
- Provide remediation recommendations

## Troubleshooting

### Error: "Module not found: promptguard"
- Make sure you've installed the package: `pip install -e .`

### Error: "GOOGLE_API_KEY not found" (when using Gemini)
- Set the environment variable: `export GOOGLE_API_KEY="your-key"`
- Or if using LM Studio, set: `export USE_LM_STUDIO=true`

### Error: "Cannot connect to LM Studio"
- Make sure LM Studio is running and Local Server is started
- Check that the server is on port 1234 (or set `LM_STUDIO_URL` accordingly)
- Verify connection: `curl http://localhost:1234/v1/models`
- In LM Studio, enable "Serve on Local Network" if needed

### Error: "_make_subprocess_transport NotImplementedError"
- Use `--no-reload` flag: `adk web --port 8000 --no-reload`

### Agent not showing in dropdown
- Make sure you're running from the parent directory (not inside `promptguard_agent/`)
- Check that `promptguard_agent/agent.py` exists and defines `root_agent`

## Development Tips

- The web interface auto-reloads when you change `agent.py` (unless `--no-reload` is used)
- You can inspect agent execution steps and tool calls in the UI
- Use the chat interface to test different security scenarios
- Check the browser console for detailed logs

## Next Steps

- Customize probes in `promptguard_agent/agent.py`
- Add more tools for advanced security testing
- Integrate with your actual LLM targets
- Add policy enforcement capabilities

