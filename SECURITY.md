# GS420 AI Security

Phase 20 adds defense-in-depth controls.

## Input and files
- Upload extensions are allow-listed.
- Upload size is capped by GS420_MAX_UPLOAD_MB.
- Uploaded names are reduced to a safe basename; generated UUID prefixes prevent collisions.
- Search limits are bounded.
- Pydantic request models enforce request lengths.

## Tools and execution
- Calculator uses a restricted expression evaluator.
- Python execution uses isolated mode, temporary working directories, timeouts, output limits and AST checks for dangerous imports/calls.
- This is **not** a perfect OS security boundary. Never expose arbitrary code execution to untrusted users without container/VM isolation.

## Secrets
Keep tokens and credentials in deployment environment variables or platform secret stores. Never commit them.

## Network and CORS
Production deployments should replace wildcard CORS with the exact frontend origin(s). Rate limiting and authentication should be enabled at the deployment gateway before exposing the service publicly.

## Model safety
Model output is untrusted data. Do not automatically execute model-generated shell commands or tool calls without explicit permission checks.
