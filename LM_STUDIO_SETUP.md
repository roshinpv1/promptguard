# Using LM Studio with PromptGuard ADK Agent

This guide shows you how to use LM Studio (running locally) instead of Google Gemini with the PromptGuard ADK agent.

## Prerequisites

1. **Install LiteLLM**:
   ```bash
   pip install litellm
   ```

2. **Start LM Studio**:
   - Open LM Studio
   - Load a model
   - Go to the "Local Server" tab (↔ icon)
   - Click "Start Server"
   - The server will run on `http://localhost:1234` by default

3. **Verify LM Studio is running**:
   ```bash
   curl http://localhost:1234/v1/models
   ```
   You should see a JSON response with available models.

## Configuration

### Option 1: Environment Variables (Recommended)

Set these environment variables before running `adk web`:

```bash
export USE_LM_STUDIO=true
export LM_STUDIO_URL="http://localhost:1234/v1"  # Optional, defaults to this
export LM_STUDIO_MODEL="local-model"  # Optional, can be any name
```

Then run:
```bash
adk web --port 8000
```

### Option 2: Modify agent.py

You can also directly edit `promptguard_agent/agent.py` and change:

```python
USE_LM_STUDIO = True  # Change from False to True
LM_STUDIO_URL = "http://localhost:1234/v1"
LM_STUDIO_MODEL = "your-model-name"
```

## How It Works

1. **LiteLLM Integration**: The agent uses LiteLLM to connect to LM Studio's OpenAI-compatible API
2. **Environment Variables**: LiteLLM reads `OPENAI_API_BASE` and `OPENAI_API_KEY` to configure the connection
3. **Model String**: ADK uses the model string `openai/{model_name}` which LiteLLM intercepts and routes to LM Studio

## Troubleshooting

### Connection Issues

**Problem**: "Cannot connect to LM Studio"

**Solutions**:
1. Make sure LM Studio is running and the Local Server is started
2. Check the port: `curl http://localhost:1234/v1/models`
3. In LM Studio, enable "Serve on Local Network" if needed
4. Verify the URL matches: `echo $LM_STUDIO_URL`

**Problem**: "LiteLLM not installed"

**Solution**:
```bash
pip install litellm
```

### Model Not Found

**Problem**: Agent can't find the model

**Solutions**:
1. The model name in `LM_STUDIO_MODEL` can be any string - it's just an identifier
2. LM Studio will use whatever model you have loaded
3. Try using a simple name like "local-model" or "lm-studio"

### ADK Compatibility

**Note**: ADK's Python API may have limited support for custom models. If you encounter issues:

1. **Check ADK version**: Make sure you have the latest version
   ```bash
   pip install --upgrade google-adk
   ```

2. **Use LiteLLM proxy mode**: You can run LiteLLM as a proxy server:
   ```bash
   litellm --port 4000 --config config.yaml
   ```
   Then configure ADK to use `http://localhost:4000` as the model endpoint

3. **Fallback to Gemini**: If LM Studio doesn't work, the agent will automatically fall back to Gemini (if `GOOGLE_API_KEY` is set)

## Example Session

Once configured, start the ADK web interface:

```bash
export USE_LM_STUDIO=true
adk web --port 8000
```

Then in the browser:
1. Open http://localhost:8000
2. Select "promptguard_security_agent" from the dropdown
3. Start chatting - it will use your local LM Studio model!

## Switching Back to Gemini

To switch back to Gemini:

```bash
unset USE_LM_STUDIO
export GOOGLE_API_KEY="your-api-key"
adk web --port 8000
```

Or simply don't set `USE_LM_STUDIO` and ensure `GOOGLE_API_KEY` is set.

## Advanced Configuration

### Custom Port

If LM Studio is running on a different port:

```bash
export LM_STUDIO_URL="http://localhost:8080/v1"
```

### Network Access

If you want to access LM Studio from another machine:

1. In LM Studio, enable "Serve on Local Network"
2. Use your machine's IP address:
   ```bash
   export LM_STUDIO_URL="http://192.168.1.100:1234/v1"
   ```

### Multiple Models

You can switch between models by changing `LM_STUDIO_MODEL`:

```bash
export LM_STUDIO_MODEL="llama-3-8b"
# or
export LM_STUDIO_MODEL="mistral-7b"
```

The actual model used is whatever is loaded in LM Studio.

