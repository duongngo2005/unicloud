from pathlib import Path
import os
import secrets

root = Path(__file__).resolve().parent.parent

example = root / ".env.example"
target = root / ".env"

if target.exists():
    raise SystemExit(
        ".env exists; refusing to overwrite it."
    )

content = example.read_text(encoding="utf-8")

if content.count("GENERATE_ME") != 2:
    raise SystemExit(
        "Unexpected .env.example placeholders."
    )

content = content.replace(
    "DB_PASSWORD=GENERATE_ME",
    "DB_PASSWORD=" + secrets.token_urlsafe(32)
)

content = content.replace(
    "NC_ADMIN_PASSWORD=GENERATE_ME",
    "NC_ADMIN_PASSWORD=" + secrets.token_urlsafe(32)
)

old_umask = os.umask(0o077)

try:
    with target.open("x", encoding="utf-8") as f:
        f.write(content)
finally:
    os.umask(old_umask)

print("Created .env securely.")
