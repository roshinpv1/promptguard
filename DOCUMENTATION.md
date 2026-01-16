# PromptGuard Documentation

## Quick Start

- **ADK Web Setup**: See `ADK_WEB_SETUP.md`
- **Environment Variables**: See `ENV_SETUP.md`
- **LM Studio Setup**: See `LM_STUDIO_SETUP.md`
- **Migration Guide**: See `MIGRATION_GUIDE.md`

## Troubleshooting

### API Key Issues
- **Missing API Key**: Set `GOOGLE_API_KEY` in `.env` or use `USE_LM_STUDIO=true`
- **Invalid API Key**: Get a valid key from https://aistudio.google.com/app/apikey

### LM Studio Issues
- **Connection Failed**: Make sure LM Studio Local Server is running on port 1234
- **ADK Web Doesn't Support LM Studio**: Use `promptguard assess` CLI instead

### Expected Behavior
- **Probes Blocked**: This is good! It means guards are working
- **Risk Score 0.0**: No vulnerability found (attack blocked or target refused safely)
- **Risk Score > 0.0**: Vulnerability found (attack succeeded)

See `promptguard_agent/EXPECTED_BEHAVIOR.md` for details.
