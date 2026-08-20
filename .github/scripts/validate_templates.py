import re
from pathlib import Path
import sys

TEMPLATES_DIR = Path("templates")

REQUIRED_SOURCE = "registry.abcxyz.com/abcxyz/dnsciz/aws"

# Only treat REQUIRED_SOURCE as present if it appears as a Terraform `source = "..."` line.
REQUIRED_SOURCE_RE = re.compile(
    r'^\s*source\s*=\s*"' + re.escape(REQUIRED_SOURCE) + r'"\s*$',
    re.MULTILINE,
)

# Version pin check: version = "x.y.z"
VERSION_RE = re.compile(r'^\s*version\s*=\s*"\d+\.\d+\.\d+"\s*$', re.MULTILINE)

# Disallow local module sources like source = "./..."
LOCAL_SOURCE_RE = re.compile(r'^\s*source\s*=\s*"\./', re.MULTILINE)

# Disallow public registry module sources like source = "...registry.terraform.io..."
PUBLIC_REGISTRY_SOURCE_RE = re.compile(
    r'^\s*source\s*=\s*".*registry\.terraform\.io.*"\s*$',
    re.MULTILINE,
)

def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)

def main() -> None:
    if not TEMPLATES_DIR.exists():
        fail("templates/ directory not found")

    tf_files = list(TEMPLATES_DIR.rglob("*.tf"))
    if not tf_files:
        fail("No .tf files found under templates/")

    source_hits = 0
    unpinned = []

    for tf in tf_files:
        text = tf.read_text(encoding="utf-8", errors="replace")

        has_required_source = bool(REQUIRED_SOURCE_RE.search(text))
        if has_required_source:
            source_hits += 1

        # If a file references the required module source, it must pin version = "x.y.z".
        if has_required_source and not VERSION_RE.search(text):
            unpinned.append(str(tf))

        # Guardrail: prevent accidentally publishing module code or local module sources in templates.
        if LOCAL_SOURCE_RE.search(text):
            fail(
                f"Local module source found (./...) in {tf}. "
                f"Templates should reference the abcxyz registry."
            )

        # allowed for providers, but not as module source; conservative guardrail
        if PUBLIC_REGISTRY_SOURCE_RE.search(text):
            fail(
                f"Public registry module source found in {tf}. "
                f"Expected abcxyz private registry module source."
            )

    if source_hits == 0:
        fail(f"No template references '{REQUIRED_SOURCE}'. Did the module source change?")

    if unpinned:
        fail(
            'Some templates reference the Pro module but do not pin version = "x.y.z":\n'
            + "\n".join(unpinned)
        )

    print("OK: templates look consistent (registry source + pinned version + no local module sources).")

if __name__ == "__main__":
    main()
