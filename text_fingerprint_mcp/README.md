# text-fingerprint-mcp

Small MCP server that produces stable fingerprints for text: cryptographic hashes, per-line digests, and optional whitespace normalization.

## Tools

- `hash_text(text, algo="sha256", normalize="none")` → hex digest
- `hash_lines(text, algo="sha256", normalize="rstrip")` → newline-separated `line_number<TAB>digest`
- `fingerprint_bundle(text)` → a short multi-hash bundle (sha256 + blake2b)

See `usage.md` for example calls.
