import os

os.system(
    "python main.py CSP2023提高 NOIP2023 --dpi=120 --alpha=0.2 --save=samples/CSP2023提高_vs_NOIP2023.png --no-show"
)
os.system(
    "python main.py CSP2024提高 NOIP2024 --dpi=120 --alpha=0.2 --save=samples/CSP2024提高_vs_NOIP2024.png --no-show"
)
os.system(
    "python main.py CSP2025提高 NOIP2025 --dpi=120 --alpha=0.2 --save=samples/CSP2025提高_vs_NOIP2025.png --no-show"
)
os.system(
    "python main.py CSP2025提高 NOIP2025 --dpi=120 --alpha=0.1 --save=samples/CSP2025提高_vs_NOIP2025_alpha01.png --no-show"
)
os.system(
    "python main.py NOIP2024 NOIP2025 --dpi=120 --save=samples/NOIP2024_vs_NOIP2025.png --no-show"
)
