# Usage

Tools exposed by this server:

- `uuid_v4()` → generate a random UUID (v4)
- `uuid_v5(namespace, name)` → generate a deterministic UUID (v5)
  - `namespace` can be one of: `dns`, `url`, `oid`, `x500`
  - or a UUID string
- `uuid_validate(value)` → returns `ok` or an error message
- `uuid_inspect(value)` → returns normalized UUID + version/variant info

Notes:
- UUID parsing is strict (must be a valid UUID string).
- No fetching or external lookups are performed.
