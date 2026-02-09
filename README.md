# Luxury Site Generator

A program that creates high-end websites for affluent client services—concierge, private aviation, luxury real estate, art advisory, family offices, and executive wellness.

## Quick Start

```bash
# List available templates
python3 generator.py -l

# Generate a concierge site (default output: ./output)
python3 generator.py concierge

# Generate with custom output directory
python3 generator.py aviation -o ./my-jet-site

# Customize business name and tagline
python3 generator.py estate --name "Monte Vista Estates" --tagline "Exceptional properties for exceptional lives"
```

## Templates

| Template | Use Case | Aesthetic |
|----------|----------|-----------|
| `concierge` | Lifestyle management, 24/7 concierge | Champagne & ivory |
| `aviation` | Private jet charter, air travel | Obsidian & dark |
| `estate` | Luxury real estate, off-market properties | Forest greens |
| `art` | Art advisory, collection management | Gallery cream & gold |
| `wealth` | Family office, wealth orchestration | Banker navy & gold |
| `wellness` | Executive health, longevity, biohacking | Sage & organic |

## Lead capture (market & sales growth)

Generated sites include an **email capture** section to grow leads and sales:

- **Section**: "Exclusive access" with headline and one email field; copy is template-specific.
- **Form action**: Default `#` (no backend). For production, use `--leads-action` with a Formspree or Netlify Forms URL:
  ```bash
  python3 generator.py concierge --leads-action "https://formspree.io/f/YOUR_FORM_ID"
  ```
- **Local endpoint**: Run the included server to capture leads into `leads/emails.json`:
  ```bash
  python3 generator.py concierge -o output --leads-action "http://127.0.0.1:8080/submit"
  python3 server.py -d output -p 8080
  ```
  Then open http://127.0.0.1:8080 — form submissions go to `/submit` and are stored locally.
- **Export leads**: Export stored emails to CSV:
  ```bash
  python3 scripts/leads_export.py -o leads.csv
  ```

The project includes a **Cursor skill** (`.cursor/skills/lead-capture-growth/`) so the agent can help with email capture, copy, and integration.

## Output

Each run produces a complete static site:
- `index.html` — Single-page layout with hero, services, leads section, footer
- `assets/styles.css` — Premium design system (Cormorant Garamond + Inter)

Open `output/index.html` in a browser to preview.

## Requirements

Python 3.7+. No external dependencies.
