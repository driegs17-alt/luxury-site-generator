#!/usr/bin/env python3
"""
Luxury Website Generator
Creates high-end websites for affluent client services.
"""

import argparse
import json
import os
from pathlib import Path

TEMPLATES = {
    "concierge": {
        "name": "Elite Concierge",
        "tagline": "Life, handled.",
        "problem": "Your time is worth more than the mundane.",
        "services": [
            "24/7 lifestyle management",
            "Exclusive access coordination",
            "Private event curation",
            "Global reservation privileges",
            "White-glove relocation"
        ],
        "accent": "champagne",
        "leads_heading": "First access to what's next.",
        "leads_sub": "Join the list for exclusive invitations and priority booking.",
        "leads_action": "#"
    },
    "aviation": {
        "name": "Apex Air",
        "tagline": "The sky, yours alone.",
        "problem": "Commercial travel diminishes those who've transcended it.",
        "services": [
            "Fully crewed private aircraft",
            "Empty-leg optimization",
            "Global FBO network access",
            "Helicopter transfer coordination",
            "Discretion at every altitude"
        ],
        "accent": "obsidian",
        "leads_heading": "Reserved for you.",
        "leads_sub": "Be the first to receive availability and member-only offers.",
        "leads_action": "#"
    },
    "estate": {
        "name": "Vestry Estates",
        "tagline": "Where legacy meets landscape.",
        "problem": "Your next residence deserves more than a listing.",
        "services": [
            "Off-market property access",
            "Confidential acquisition advisory",
            "Estate valuation & structuring",
            "Cross-border property coordination",
            "Legacy planning integration"
        ],
        "accent": "forest",
        "leads_heading": "Off-market opportunities, first.",
        "leads_sub": "Get early access to exclusive properties and private viewings.",
        "leads_action": "#"
    },
    "art": {
        "name": "Atelier Advisory",
        "tagline": "Collecting with intention.",
        "problem": "The art market rewards those with the right counsel.",
        "services": [
            "Primary market placement",
            "Provenance research & authentication",
            "Collection strategy development",
            "Private sale facilitation",
            "Estate planning for collections"
        ],
        "accent": "gallery",
        "leads_heading": "Join the list.",
        "leads_sub": "Receive priority access to private sales and acquisition opportunities.",
        "leads_action": "#"
    },
    "wealth": {
        "name": "Meridian Family Office",
        "tagline": "Wealth orchestrated.",
        "problem": "Complexity demands a single, trusted hand.",
        "services": [
            "Unified wealth architecture",
            "Multi-generational structuring",
            "Philanthropic strategy",
            "Concierge tax & legal coordination",
            "Next-generation preparation"
        ],
        "accent": "banker",
        "leads_heading": "A conversation, when you're ready.",
        "leads_sub": "Express interest and we'll reach out to schedule a confidential introduction.",
        "leads_action": "#"
    },
    "wellness": {
        "name": "Apex Longevity",
        "tagline": "Years, not days.",
        "problem": "Peak performance requires more than a gym membership.",
        "services": [
            "Executive health optimization",
            "Biohacking & longevity protocols",
            "Private medical concierge",
            "Regenerative medicine access",
            "Discretion-first care"
        ],
        "accent": "sage",
        "leads_heading": "Be the first to know.",
        "leads_sub": "Early access to new protocols, member openings, and insider briefings.",
        "leads_action": "#"
    }
}


def load_template_html() -> str:
    """Load the base HTML template."""
    base = Path(__file__).parent
    template_path = base / "templates" / "base.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text()


def generate_site(template_name: str, output_dir: str, custom_data: dict = None) -> str:
    """Generate a complete website for the given template."""
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}. Choose from: {list(TEMPLATES.keys())}")
    
    data = {**TEMPLATES[template_name], **(custom_data or {})}
    html = load_template_html()
    
    # Apply template variables
    for key, value in data.items():
        if isinstance(value, list):
            value = "\n          ".join(f"<li>{item}</li>" for item in value)
        placeholder = "{{" + key + "}}"
        html = html.replace(placeholder, str(value))
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Write HTML
    (output_path / "index.html").write_text(html)
    
    # Copy assets (skip if output is project root - assets already in place)
    base = Path(__file__).parent
    assets_src = base / "assets"
    assets_dst = output_path.resolve() / "assets"
    if assets_src.exists() and assets_src.resolve() != assets_dst:
        import shutil
        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)
    
    return str(output_path / "index.html")


def list_templates() -> None:
    """Print available templates."""
    print("\nAvailable luxury website templates:\n")
    for key, data in TEMPLATES.items():
        print(f"  {key:12} — {data['name']}: {data['tagline']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Generate luxury websites for affluent client services")
    parser.add_argument("template", nargs="?", help="Template to generate (concierge, aviation, estate, art, wealth, wellness)")
    parser.add_argument("-o", "--output", default=".", help="Output directory (use . for project root)")
    parser.add_argument("-l", "--list", action="store_true", help="List available templates")
    parser.add_argument("--name", help="Custom business name")
    parser.add_argument("--tagline", help="Custom tagline")
    parser.add_argument("--leads-action", help="Form action URL for lead capture (e.g. Formspree or Netlify Forms endpoint)")
    
    args = parser.parse_args()
    
    if args.list or not args.template:
        list_templates()
        if not args.template:
            return
    
    custom = {}
    if args.name:
        custom["name"] = args.name
    if args.tagline:
        custom["tagline"] = args.tagline
    if args.leads_action:
        custom["leads_action"] = args.leads_action
    
    try:
        path = generate_site(args.template, args.output, custom or None)
        print(f"✓ Generated: {path}")
        print(f"  Open in browser to preview.\n")
    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
