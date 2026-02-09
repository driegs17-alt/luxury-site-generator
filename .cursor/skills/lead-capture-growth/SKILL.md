---
name: lead-capture-growth
description: Helps obtain client emails and increase market reach, leads, and sales for luxury-site-generator projects. Use when the user wants to capture emails, grow leads, add signup forms, integrate with email services, or improve conversion for affluent client services.
---

# Lead Capture & Market Growth Agent

## Purpose

Guide implementation of email capture and lead-generation flows so generated luxury sites can grow their market and sales. Focus on high-intent, low-friction capture that fits an exclusive, high-end brand.

## When to Apply

- User asks to capture client emails, grow leads, or increase sales
- User wants a newsletter signup, waitlist, or "request access" form
- User asks to integrate Formspree, Netlify Forms, or another form/email service
- User wants copy or placement tuned for conversions

## Core Principles

1. **One primary CTA**: One clear email capture per view (e.g. one "Stay informed" or "Request access" block).
2. **Value-first copy**: Headlines and subcopy should state benefit (exclusive access, early invites, insider updates) not "sign up for our newsletter."
3. **Minimal fields**: Email only unless the user explicitly needs name/company for qualification.
4. **Match the aesthetic**: Use existing template accent and typography; no generic form styling.

## Implementation Checklist

- [ ] Add or reuse the `leads` section in `templates/base.html` (section id `leads`, class `leads`).
- [ ] Ensure `assets/styles.css` includes `.leads` styles; keep accent-aware (e.g. `[data-accent="…"] .leads …`).
- [ ] Set form `action` to a real endpoint: Formspree (`https://formspree.io/f/xxx`), Netlify Forms (post to page URL with `netlify` attribute), or custom. Never leave `action="#"` in production.
- [ ] If the project uses `generator.py`, support optional `--leads-action` or template data `leads_action` so generated sites can set the form endpoint.
- [ ] For export/backup: use `scripts/leads_export.py` to merge or export leads from JSON/CSV if the project stores them locally.

## Form Markup Pattern

```html
<section class="leads" id="leads">
  <div class="leads-inner">
    <p class="section-label">Exclusive access</p>
    <h2 class="section-title">{{leads_heading}}</h2>
    <p class="leads-sub">{{leads_sub}}</p>
    <form class="leads-form" action="{{leads_action}}" method="post">
      <input type="email" name="email" placeholder="Your email" required aria-label="Email address">
      <button type="submit" class="cta">Request access</button>
    </form>
  </div>
</section>
```

Use placeholders `{{leads_heading}}`, `{{leads_sub}}`, `{{leads_action}}` so the generator can inject template-specific copy and endpoint.

## Copy Guidelines (Increase Market & Leads)

- **Headlines**: "Join the list." / "First access to what’s next." / "Reserved for you." / "Be the first to know."
- **Subcopy**: Emphasize exclusivity, early access, or insider updates; avoid "we’ll send you marketing."
- **Button**: "Request access" or "Stay informed" preferred over "Subscribe" for luxury positioning.

## Backend / No-Backend Options

- **Formspree**: `action="https://formspree.io/f/YOUR_FORM_ID"` — emails to inbox, optional redirect.
- **Netlify Forms**: Add `netlify` to `<form>` and `name="contact"` (or custom); form submissions in Netlify dashboard.
- **Custom**: Point `action` to the user’s backend; ensure `name="email"` (and any other fields) match server expectations.

## Optional: Local Leads Storage

If the project collects leads to a local file (e.g. for static demos or CSV export):

- Store path: `leads/emails.json` or `leads/leads.csv`.
- Use `scripts/leads_export.py` to export to CSV or merge JSON entries. Document in README that production should use Formspree/Netlify/custom endpoint.

## Summary

- Add or wire the leads section in the template and styles.
- Use value-first, exclusive copy and a single primary email field.
- Set a real form action for production; support injectable `leads_action` from the generator when applicable.
- Prefer Formspree or Netlify Forms when no backend exists; use the leads export script only for local/export workflows.
