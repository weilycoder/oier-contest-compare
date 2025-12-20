import os

from scour.scour import scourString, sanitizeOptions

commands = [
    "CSP2023提高 NOIP2023 --alpha=0.2 --save=samples/CSP2023提高_vs_NOIP2023.svg --no-show",
    "CSP2024提高 NOIP2024 --alpha=0.2 --save=samples/CSP2024提高_vs_NOIP2024.svg --no-show",
    "CSP2025提高 NOIP2025 --alpha=0.2 --save=samples/CSP2025提高_vs_NOIP2025.svg --no-show",
    "CSP2025提高 NOIP2025 --alpha=0.1 --save=samples/CSP2025提高_vs_NOIP2025_alpha01.svg --no-show",
    "NOIP2024 NOIP2025 --save=samples/NOIP2024_vs_NOIP2025.svg --no-show",
    "CSP2025提高 NOIP2025 --alpha=0.1 --save=samples/CSP2025提高_vs_NOIP2025_fit.svg --no-show --polyfit=2",
]

for cmd in commands:
    os.system("python main.py " + cmd)


options = sanitizeOptions()

options.strip_comments = True
options.remove_descriptive_elements = True

options.strip_ids = True
options.shorten_ids = True

options.newlines = False
options.indent_type = "none"

for filename in os.listdir("samples"):
    if filename.endswith(".svg"):
        with open(os.path.join("samples", filename), "r", encoding="utf-8") as f:
            svg_content = f.read()
        optimized_svg = scourString(svg_content, options=options)
        with open(os.path.join("samples", filename), "w", encoding="utf-8") as f:
            f.write(optimized_svg)
