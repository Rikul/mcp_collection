#!/usr/bin/env bash
set -euo pipefail

# CI/local validation + smoke run for all servers.
# - validates repo structure
# - builds a fresh venv
# - installs each server editable
# - runs each console_script briefly (timeout)
#
# Exit codes:
# 0 = all good
# 1 = problems

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIMEOUT_SECS="${MCP_SMOKE_TIMEOUT:-2}"
VENV_DIR="${MCP_VALIDATE_VENV_DIR:-/tmp/mcp_collection_venv}"

cd "$ROOT"

python3 scripts/validate_collection.py --format text

echo "---"
echo "Creating venv: $VENV_DIR"
rm -rf "$VENV_DIR"
python3 -m venv "$VENV_DIR"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
python -m pip install -U pip >/dev/null

tmp_db=""
make_tmp_sqlite_db() {
  tmp_db="$(python - <<'PY'
import sqlite3, tempfile
p=tempfile.NamedTemporaryFile(suffix='.db', delete=False)
p.close()
conn=sqlite3.connect(p.name)
conn.execute('create table t(x int)')
conn.execute('insert into t(x) values (1)')
conn.commit(); conn.close()
print(p.name)
PY
)"
}
make_tmp_sqlite_db

fail=0
fails=""

for d in */pyproject.toml; do
  srv=${d%%/*}
  echo ""
  echo "== $srv =="

  python -m pip install -e "$ROOT/$srv" >/dev/null || {
    echo "pip install -e failed"
    fail=1
    fails+="$srv:install\n"
    continue
  }

  # If the server has unit tests, run them. Keep them basic + fast.
  if [ -d "$ROOT/$srv/tests" ]; then
    python -m pip install -U pytest >/dev/null
    echo "pytest: $srv"
    if ! pytest -q "$ROOT/$srv/tests"; then
      fail=1
      fails+="$srv:pytest\n"
    fi
  fi

  scripts=$(python - "$srv" <<'PY'
import sys, tomllib, pathlib
srv=sys.argv[1]
obj=tomllib.loads((pathlib.Path(srv)/'pyproject.toml').read_text())
print(' '.join(sorted(obj.get('project',{}).get('scripts',{}).keys())))
PY
)

  if [ -z "$scripts" ]; then
    echo "NO_SCRIPTS"
    fail=1
    fails+="$srv:NO_SCRIPTS\n"
    continue
  fi

  for s in $scripts; do
    echo "run: $s"

    code=0
    if [ "$s" = "sqlite-read-server-mcp" ]; then
      timeout "${TIMEOUT_SECS}s" "$s" --database "$tmp_db" >/dev/null 2>&1 || code=$?
    else
      timeout "${TIMEOUT_SECS}s" "$s" >/dev/null 2>&1 || code=$?
    fi

    # timeout returns 124
    if [ "$code" = "0" ] || [ "$code" = "124" ]; then
      echo "ok (code $code)"
    else
      echo "FAIL (code $code)"
      fail=1
      fails+="$srv:$s:$code\n"
    fi
  done
done

rm -f "$tmp_db" 2>/dev/null || true

echo "---"
if [ "$fail" -eq 0 ]; then
  echo "ALL_OK"
  exit 0
else
  echo -e "FAILURES:\n$fails"
  exit 1
fi
