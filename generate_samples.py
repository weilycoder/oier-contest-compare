import os
import subprocess

from scour.scour import scourString, sanitizeOptions


def compress_svg(filename: str) -> None:
    options = sanitizeOptions()

    options.strip_comments = True
    options.remove_descriptive_elements = True

    options.strip_ids = True
    options.shorten_ids = True

    options.newlines = False
    options.indent_type = "none"

    with open(os.path.join("samples", filename), "r", encoding="utf-8") as f:
        svg_content = f.read()
    optimized_svg = scourString(svg_content, options=options)
    with open(os.path.join("samples", filename), "w", encoding="utf-8") as f:
        f.write(optimized_svg)


commands = [
    [["CSP2023提高", "NOIP2023", "--alpha=0.2", "--no-show"], "samples/CSP2023提高_vs_NOIP2023.svg"],
    [["CSP2024提高", "NOIP2024", "--alpha=0.2", "--no-show"], "samples/CSP2024提高_vs_NOIP2024.svg"],
    [["CSP2025提高", "NOIP2025", "--alpha=0.2", "--no-show"], "samples/CSP2025提高_vs_NOIP2025.svg"],
    [["CSP2025提高", "NOIP2025", "--alpha=0.1", "--no-show"], "samples/CSP2025提高_vs_NOIP2025_alpha01.svg"],
    [["NOIP2024", "NOIP2025", "--no-show"], "samples/NOIP2024_vs_NOIP2025.svg"],
    [["CSP2025提高", "NOIP2025", "--alpha=0.1", "--polyfit=2", "--no-show"], "samples/CSP2025提高_vs_NOIP2025_fit.svg"],
]

for cmd in commands:
    args, output_file = cmd
    if os.path.exists(output_file):
        print(f"Skipping {output_file} (already exists)")
    else:
        print(f"Generating {output_file}...")
        subprocess.run(["python", "main.py", f"--save={output_file}"] + args, check=True)
        print(f"Generated {output_file}, compressing...")
        compress_svg(output_file)
        print(f"Compressed {output_file}")
