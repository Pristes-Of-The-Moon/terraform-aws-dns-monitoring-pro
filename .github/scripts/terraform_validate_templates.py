#!/usr/bin/env python3
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

TEMPLATES_DIR = Path("templates")

# Must match your existing conventions script
REQUIRED_SOURCE = "registry.abcxyz.com/abcxyz/dnsciz/aws"

MODULE_START_RE = re.compile(r'^\s*module\s+"([^"]+)"\s*{')
KEY_ASSIGN_RE = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=')
MODULE_REF_RE = re.compile(r'\bmodule\.([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\b')

RESERVED_KEYS = {"source", "version", "providers", "depends_on", "for_each", "count"}

def run(cmd, cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True)

def collect_inputs_and_patch_sources(root: Path):
    """
    In-place (on a TEMP COPY ONLY):
      - replace REQUIRED_SOURCE with ./_stub_pro_module
      - remove version lines inside those module blocks
      - collect input variable names passed into that module block
      - collect module output attribute references (module.<name>.<attr>)
    """
    all_inputs = set()
    referenced_outputs = set()  # (module_name, attr)
    stubbed_module_names = set()

    for tf in root.rglob("*.tf"):
        text = tf.read_text(encoding="utf-8", errors="replace")
        referenced_outputs |= set(MODULE_REF_RE.findall(text))

        lines = text.splitlines(keepends=True)
        out = []

        in_module = False
        module_name = None
        brace_depth = 0
        rel_depth = 0
        is_target_module = False

        for line in lines:
            m = MODULE_START_RE.match(line)
            if not in_module and m:
                in_module = True
                module_name = m.group(1)
                brace_depth = line.count("{") - line.count("}")
                rel_depth = brace_depth
                is_target_module = False
                out.append(line)
                continue

            if in_module:
                current_rel_depth = rel_depth

                # If this module block references the private registry source, stub it
                if "source" in line and REQUIRED_SOURCE in line:
                    is_target_module = True
                    stubbed_module_names.add(module_name)
                    line = line.replace(REQUIRED_SOURCE, "./_stub_pro_module")

                # If this is the stubbed module, drop version lines
                if is_target_module and re.match(r'^\s*version\s*=\s*".*"\s*$', line):
                    pass
                else:
                    # Collect top-level inputs inside module block (depth == 1)
                    if is_target_module and current_rel_depth == 1:
                        km = KEY_ASSIGN_RE.match(line)
                        if km:
                            key = km.group(1)
                            if key not in RESERVED_KEYS:
                                all_inputs.add(key)

                    out.append(line)

                # update depth counters
                delta = line.count("{") - line.count("}")
                brace_depth += delta
                rel_depth += delta

                if brace_depth <= 0:
                    in_module = False
                    module_name = None
                    brace_depth = 0
                    rel_depth = 0
                    is_target_module = False

                continue

            out.append(line)

        tf.write_text("".join(out), encoding="utf-8")

    # Only need outputs referenced from modules we stubbed
    output_attrs = {attr for (mname, attr) in referenced_outputs if mname in stubbed_module_names}
    return all_inputs, output_attrs, stubbed_module_names

def write_stub_module(stub_dir: Path, input_vars: set, output_names: set):
    stub_dir.mkdir(parents=True, exist_ok=True)

    variables_tf = []
    for v in sorted(input_vars):
        variables_tf.append(f'variable "{v}" {{\n  type = any\n}}\n')

    outputs_tf = []
    for o in sorted(output_names):
        outputs_tf.append(f'output "{o}" {{\n  value = null\n}}\n')

    (stub_dir / "variables.tf").write_text("\n".join(variables_tf) + "\n", encoding="utf-8")
    (stub_dir / "outputs.tf").write_text("\n".join(outputs_tf) + "\n", encoding="utf-8")

def iter_cases(templates_dir: Path):
    # templates/<case>/*.tf  OR templates/*.tf
    subdirs = [p for p in templates_dir.iterdir() if p.is_dir()]
    if subdirs:
        for d in sorted(subdirs):
            if any(d.rglob("*.tf")):
                yield d
    else:
        if any(templates_dir.rglob("*.tf")):
            yield templates_dir

def main():
    if not TEMPLATES_DIR.exists():
        raise SystemExit("templates/ directory not found")

    cases = list(iter_cases(TEMPLATES_DIR))
    if not cases:
        raise SystemExit("No .tf files found under templates/")

    failures = []
    for case_dir in cases:
        with tempfile.TemporaryDirectory(prefix=f"tf-validate-{case_dir.name}-") as tmp:
            tmp_root = Path(tmp) / "case"
            shutil.copytree(case_dir, tmp_root, dirs_exist_ok=True)

            inputs, outputs, stubbed = collect_inputs_and_patch_sources(tmp_root)
            if not stubbed:
                failures.append(f"{case_dir}: no module source matched {REQUIRED_SOURCE}")
                continue

            write_stub_module(tmp_root / "_stub_pro_module", inputs, outputs)

            try:
                run(["terraform", "init", "-backend=false", "-input=false", "-no-color"], cwd=tmp_root)
                run(["terraform", "validate", "-no-color"], cwd=tmp_root)
            except subprocess.CalledProcessError:
                failures.append(str(case_dir))

    if failures:
        print("FAILED cases:")
        for f in failures:
            print(f" - {f}")
        raise SystemExit(1)

    print("OK: terraform validate succeeded for all template cases (stubbed module).")

if __name__ == "__main__":
    main()
