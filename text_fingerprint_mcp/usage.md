# Usage

## Run

```bash
text-fingerprint-mcp
```

## Tool examples

### Hash a blob of text

- `hash_text(text="hello", algo="sha256")`
- `hash_text(text="hello\n", algo="sha256", normalize="rstrip")`

### Hash each line (useful for quick diff anchors)

- `hash_lines(text="a\nb\n", algo="sha256", normalize="rstrip")`

### Get a small bundle

- `fingerprint_bundle(text="...large...text...")`
