# Why ADK Still Uses Google LLM Even With LM Studio Config

## The Core Problem

**ADK's `Agent` class does NOT support custom model strings.** It only recognizes Gemini model names like:
- `gemini-3-flash-preview`
- `gemini-2.5-flash`
- etc.

When you try to use `openai/local-model` or any custom string, ADK doesn't understand it and falls back to Gemini.

## What's Happening in the Code

Look at lines 173-179 in `agent.py`:

```python
if USE_LM_STUDIO:
    print("⚠ NOTE: ADK doesn't directly support custom models.")
    print("  Falling back to Gemini for now.")
    selected_model = "gemini-3-flash-preview"  # <-- Still using Gemini!
    USE_LM_STUDIO = False
```

Even when `USE_LM_STUDIO=true`, the code **intentionally falls back to Gemini** because ADK can't use custom models.

## Solutions

### Option 1: Use PromptGuard CLI (Supports LM Studio)

**Don't use ADK web** - use the CLI instead:

```bash
# Set in .env
USE_LM_STUDIO=true
LM_STUDIO_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=gemma3:27b

# Use CLI
promptguard assess --config promptshield.yaml --policy policy.example.yaml
```

The CLI uses the full PromptGuard runner which supports LM Studio directly.

### Option 2: Use Gemini with ADK Web

If you want to use ADK web, you **must** use Gemini:

```bash
# Set in .env
USE_LM_STUDIO=false
GOOGLE_API_KEY=your-actual-gemini-api-key
```

### Option 3: Create Custom BaseLlm (Advanced)

You could create a custom `BaseLlm` implementation for ADK, but this is complex and not officially supported.

## Why This Limitation Exists

ADK is designed by Google to work primarily with Gemini models. The Python API doesn't expose a clean way to use custom LLM backends through the `Agent` class.

## Recommendation

**For LM Studio**: Use `promptguard assess` (CLI)  
**For ADK Web**: Use Gemini with a valid API key

These are separate tools for different use cases!

