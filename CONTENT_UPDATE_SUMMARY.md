# FARATECH content-only update

**Updated:** 12 July 2026

## UI preservation

- The original HTML theme, page sections, containers, grid classes, animations, sliders, CSS, JavaScript and image library were retained.
- No visual redesign or replacement component system was introduced.
- The only CSS addition is a standard `.visually-hidden` utility for semantic H1 headings that do not alter the visible design.
- Existing content containers were used for corrected copy. Functional form fields and consent were added inside the existing form container.

## Content and trust changes

- Replaced all Aigocy, Davies, NULLPHPSCRIPT, template-author, old email and demo-brand residue.
- Deleted the dangerous `NullPHPscript.com.html` redirect page.
- Standardized branding as FARA Technologies / FARATECH.
- Corrected the location statement: staffed office in Bengaluru; Mumbai and Chennai are service areas.
- Added the approved team:
  - Ranjith — Founder
  - Praveen Pandian — CEO & Development Head
  - Hemnath — HR & Client Recruiter
  - Praveen — Developer & Designer
  - Mohammad Uwaze — Digital Marketing Head
- Added the verified LinkedIn, Instagram, Facebook and X URLs supplied by FARATECH.
- Standardized public contact to `info@faratech.in` and `+91 93613 10085`.
- Clarified 24/7 support availability.
- Marked portfolio detail pages as company-approved case studies.
- Kept award badges in the existing design, labeled as company-confirmed with official links pending.
- Removed contradictory public review/client-count claims and replaced them with approved case-study, service-area and support facts.
- Rewrote the template blog article and removed fabricated demo comments.
- Corrected grammar, typos, marketing-service labels and repeated Contact FAQ answers.
- Replaced the Tower of London map with Bengaluru.

## Functional and technical content changes

- Kept the original contact form design and connected all existing lead forms to Netlify Forms.
- Added field names, email validation, autocomplete, attachment input, honeypot protection, privacy consent and a thank-you route.
- Added Privacy Policy, Website Terms and Thank You pages using the same original theme.
- Added unique titles, descriptions, canonical URLs, Open Graph metadata and Organization JSON-LD.
- Added one semantic H1 per page without changing the visible design.
- Added useful image alternative text while retaining empty alt text for decorative graphics.
- Added `robots.txt`, `sitemap.xml`, Netlify security headers and old-route redirects.
- Fixed broken case-sensitive image references and the missing alternate-home video source.

## Validation completed

- 24 HTML files checked.
- No broken local links or asset references.
- Exactly one H1 on every page.
- JSON-LD parses successfully.
- Every page has canonical and social metadata.
- All seven original contact-form containers submit through Netlify Forms.
- No old-template branding, email, London map or lorem-ipsum content remains.
- `git diff --check` passes.

## Deployment checklist

1. Push the content-update commit to GitHub.
2. Deploy on Netlify.
3. Enable Netlify form notifications for the seven `project-enquiry-*` forms.
4. Test the form, upload and thank-you route on production.
5. Submit `/sitemap.xml` in Google Search Console.
6. Supply official award/profile URLs before changing “company-confirmed” to independently verified.
7. Add the exact Bengaluru public street address only when approved for publication.
