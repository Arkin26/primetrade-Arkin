#!/bin/sh
set -e

# #region agent log
_log() {
  msg="$1"
  hid="$2"
  ts=$(date +%s000)
  echo "{\"sessionId\":\"f40fa8\",\"runId\":\"entrypoint\",\"hypothesisId\":\"$hid\",\"location\":\"docker-entrypoint.sh\",\"message\":\"$msg\",\"data\":{\"port\":\"${PORT:-8000}\",\"alembic\":\"$(command -v alembic 2>/dev/null || echo missing)\"},\"timestamp\":$ts}" >&2
}
# #endregion

PORT="${PORT:-8000}"

# #region agent log
_log "entrypoint_start" "H1"
# #endregion

# #region agent log
_log "running_alembic" "H4"
# #endregion
alembic upgrade head

# #region agent log
_log "alembic_done_starting_uvicorn" "H4"
# #endregion
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
