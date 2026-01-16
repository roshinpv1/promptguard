# Fix: Missing API Key Error

## The Error

```
Missing key inputs argument! To use the Google AI API, provide (`api_key`) arguments.
```

## The Problem

Your `.env` file has a **placeholder** API key:
```
GOOGLE_API_KEY=your-google-api-key-here
```

ADK needs a **real** API key to work.

## Solution

### Step 1: Get a Gemini API Key

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIzaSy...`)

### Step 2: Update .env File

Edit `promptguard_agent/.env`:

```bash
USE_LM_STUDIO=false
GOOGLE_API_KEY=AIzaSy...your-actual-key-here
```

**Replace** `your-google-api-key-here` with your actual key.

### Step 3: Restart ADK Web

```bash
adk web --port 8000
```

## Alternative: Use LM Studio with CLI

If you don't want to use Gemini, use LM Studio with the CLI instead:

1. **Update `.env`**:
   ```bash
   USE_LM_STUDIO=true
   LM_STUDIO_URL=http://localhost:1234/v1
   ```

2. **Use CLI** (not ADK web):
   ```bash
   promptguard assess --config promptshield.yaml
   ```

## Why This Happens

ADK web **only works with Gemini**. It requires a valid `GOOGLE_API_KEY` environment variable. The code now validates this and shows a clear error if the key is missing or invalid.

