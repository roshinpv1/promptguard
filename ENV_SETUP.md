# Environment Variables Setup

This guide shows you how to set up environment variables for PromptGuard ADK Agent.

## Quick Setup

### Option 1: Create .env file (Recommended)

1. **Copy the example file**:
   ```bash
   cp promptguard_agent/.env.example promptguard_agent/.env
   ```

2. **Edit the .env file** with your values:
   ```bash
   # For Gemini
   GOOGLE_API_KEY=your-actual-api-key-here
   USE_LM_STUDIO=false

   # OR for LM Studio
   USE_LM_STUDIO=true
   LM_STUDIO_URL=http://localhost:1234/v1
   LM_STUDIO_MODEL=local-model
   ```

3. **The agent will automatically load** the .env file when it starts.

### Option 2: Set environment variables directly

```bash
# For Gemini
export GOOGLE_API_KEY="your-api-key"
export USE_LM_STUDIO=false

# OR for LM Studio
export USE_LM_STUDIO=true
export LM_STUDIO_URL="http://localhost:1234/v1"
export LM_STUDIO_MODEL="local-model"
```

## Environment Variables

### `USE_LM_STUDIO`
- **Type**: boolean (true/false)
- **Default**: false
- **Description**: Set to `true` to use LM Studio (local), `false` to use Google Gemini (cloud)

### `GOOGLE_API_KEY`
- **Type**: string
- **Required when**: `USE_LM_STUDIO=false`
- **Description**: Your Google Gemini API key
- **Get it from**: https://aistudio.google.com/app/apikey

### `LM_STUDIO_URL`
- **Type**: string (URL)
- **Default**: `http://localhost:1234/v1`
- **Required when**: `USE_LM_STUDIO=true`
- **Description**: Base URL for LM Studio API server

### `LM_STUDIO_MODEL`
- **Type**: string
- **Default**: `local-model`
- **Required when**: `USE_LM_STUDIO=true`
- **Description**: Model name identifier (can be any name, LM Studio uses the loaded model)

## File Locations

The agent looks for `.env` files in this order:
1. `promptguard_agent/.env` (preferred)
2. `.env` (project root)

## Example .env Files

### Using Google Gemini
```bash
USE_LM_STUDIO=false
GOOGLE_API_KEY=AIzaSy...your-actual-key
```

### Using LM Studio
```bash
USE_LM_STUDIO=true
LM_STUDIO_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=local-model
```

## Verification

After setting up your .env file, verify it's loaded:

```bash
# Start the agent
adk web --port 8000

# Check the console output - it should show:
# - "Using LM Studio at..." if USE_LM_STUDIO=true
# - Or use Gemini if USE_LM_STUDIO=false and GOOGLE_API_KEY is set
```

## Security Notes

- **Never commit .env files** to git (they're in .gitignore)
- **Use .env.example** as a template (this file is safe to commit)
- **Keep your API keys secret** - don't share them publicly

## Troubleshooting

### Variables not loading
- Make sure the .env file is in the correct location
- Check file permissions (should be readable)
- Verify the format is correct (KEY=value, no spaces around =)

### Wrong model being used
- Check `USE_LM_STUDIO` value (should be `true` or `false`, not `"true"` or `"false"`)
- Verify environment variables are set correctly
- Restart the agent after changing .env file

