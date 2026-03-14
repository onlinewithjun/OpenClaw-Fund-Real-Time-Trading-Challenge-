# Secret Handling Rules

## Never write these to memory, docs, logs, or git-tracked files
- API keys
- Telegram bot tokens
- passwords
- session cookies
- bearer tokens
- private keys
- SSH keys
- webhook secrets

## Required behavior
1. If a secret appears in chat, config, logs, or files, redact it immediately before storing any summary.
2. In memory files, replace secrets with `[REDACTED - SECRET REMOVED]`.
3. Prefer describing configuration state, not literal credentials.
4. Before git commit/push, scan for common secret patterns.
5. If a secret ever reached git history or a public remote, treat it as compromised and rotate/revoke it.

## Memory-specific rule
- Daily memory may record that a token/key was configured successfully, but must never include the literal token/key value.
