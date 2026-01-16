# ADK + LM Studio Integration Issue

## Problem

ADK's Python `Agent` class doesn't support custom model strings like `openai/local-model`. It only recognizes Gemini model names. When you try to use LM Studio, ADK still tries to use Gemini and requires a valid `GOOGLE_API_KEY`.

## Solutions

### Option 1: Use Gemini (Recommended for ADK)

If you want to use ADK web interface, use Gemini:

1. **Set in `.env` file**:
   ```bash
   USE_LM_STUDIO=false
   GOOGLE_API_KEY=your-actual-gemini-api-key
   ```

2. **Get API key**: https://aistudio.google.com/app/apikey

### Option 2: Use LiteLLM Proxy (For LM Studio)

Run LiteLLM as a proxy server that ADK can connect to:

1. **Install LiteLLM**:
   ```bash
   pip install litellm
   ```

2. **Create LiteLLM config** (`litellm_config.yaml`):
   ```yaml
   model_list:
     - model_name: local-model
       litellm_params:
         model: openai/local-model
         api_base: http://localhost:1234/v1
         api_key: lm-studio
   ```

3. **Start LiteLLM proxy**:
   ```bash
   litellm --config litellm_config.yaml --port 4000
   ```

4. **Update `.env`** to point to LiteLLM proxy:
   ```bash
   USE_LM_STUDIO=true
   LM_STUDIO_URL=http://localhost:4000/v1
   ```

5. **Update ADK to use the proxy** (requires custom BaseLlm implementation)

### Option 3: Use PromptGuard CLI (Not ADK Web)

Instead of ADK web, use the PromptGuard CLI which supports LM Studio directly:

```bash
# This works with LM Studio
promptguard assess --config promptshield.yaml --policy policy.example.yaml
```

The CLI uses the full PromptGuard runner which supports custom targets including LM Studio.

## Current Status

The agent code currently:
- Detects `USE_LM_STUDIO=true`
- Configures LiteLLM
- But falls back to Gemini because ADK doesn't support custom models

**To use LM Studio with ADK web, you need Option 2 (LiteLLM proxy) or use the CLI instead.**

## Quick Fix for Now

If you just want ADK web to work:

1. **Edit `promptguard_agent/.env`**:
   ```bash
   USE_LM_STUDIO=false
   GOOGLE_API_KEY=your-gemini-api-key-here
   ```

2. **Restart ADK web**:
   ```bash
   adk web --port 8000
   ```

This will use Gemini instead of LM Studio, but ADK web will work.

