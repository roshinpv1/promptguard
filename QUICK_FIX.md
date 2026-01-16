# Quick Fix: ADK Web API Key Error

## The Problem

You're seeing this error:
```
API key not valid. Please pass a valid API key.
```

This happens because:
1. ADK web **only supports Google Gemini models** (not LM Studio directly)
2. Your `.env` file has a placeholder API key: `GOOGLE_API_KEY=your-google-api-key-here`

## Solution

### Option 1: Use Gemini with ADK Web (Recommended)

1. **Get a Gemini API key**:
   - Go to: https://aistudio.google.com/app/apikey
   - Create a new API key
   - Copy it

2. **Update `.env` file**:
   ```bash
   # Edit promptguard_agent/.env
   USE_LM_STUDIO=false
   GOOGLE_API_KEY=AIzaSy...your-actual-key-here
   ```

3. **Restart ADK web**:
   ```bash
   adk web --port 8000
   ```

### Option 2: Use LM Studio with PromptGuard CLI

If you want to use LM Studio, **don't use ADK web**. Use the PromptGuard CLI instead:

1. **Update `.env`**:
   ```bash
   USE_LM_STUDIO=true
   LM_STUDIO_URL=http://localhost:1234/v1
   ```

2. **Make sure LM Studio is running** (Local Server started)

3. **Use CLI instead**:
   ```bash
   promptguard assess --config promptshield.yaml --policy policy.example.yaml
   ```

## Why ADK Web Doesn't Support LM Studio

ADK's `Agent` class only accepts Gemini model names (like `gemini-3-flash-preview`). It doesn't support custom model strings like `openai/local-model` that LiteLLM uses.

## Summary

- **ADK Web** → Requires Gemini API key
- **PromptGuard CLI** → Supports both Gemini and LM Studio

Choose the option that fits your needs!

