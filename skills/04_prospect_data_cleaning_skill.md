# Skill: Prospect Data Cleaning

**Used by:** Data Quality Agent  
**Domain:** Contact record normalisation

---

## Purpose
Normalises raw prospect fields: email, phone, company name, and designation strings into clean, consistent formats ready for platform storage and Pipedrive sync.

---

## When to use
On every raw prospect record imported from CSV or external source.

---

## Input schema
```
raw_email: string
raw_phone: string
raw_company_name: string
raw_designation: string
raw_first_name: string
raw_last_name: string
region: string (for phone country code resolution)
```

---

## Output schema
```
email: string (normalised)
phone: string (E.164 format)
company_name: string (display format)
company_name_normalised: string (for dedup matching)
designation: string (cleaned)
first_name: string
last_name: string
corrections_log: list
```

---

## Domain logic

### Email normalisation
- Lowercase entire string
- Trim leading/trailing whitespace
- Remove display name if present (`"John Doe <john@company.com>"` → `john@company.com`)
- Validate format (must contain @ and valid domain)
- Flag if disposable email domain detected

### Phone normalisation
- Strip spaces, dashes, brackets, dots
- Add country code from region if missing (India default: +91)
- Convert to E.164 format: `+91XXXXXXXXXX`
- Flag if digit count invalid for country code

### Company name cleaning
- Remove legal suffixes for dedup matching (Ltd, Pvt, Inc, Corp, LLP, GmbH)
- Preserve original for display
- Title case normalisation

### Designation cleaning
Common replacements:
- "MD" → "Managing Director"
- "VP Mktg" → "VP Marketing"
- "BDM" → "Business Development Manager"
- "AVP" → "Associate Vice President"

---

## Rules
- Log every correction made — never silently overwrite
- Never discard a record — only flag it
- Empty fields are flagged, not errored

---

## Failure cases
- Email with no @ sign → flag as invalid_email
- Phone with < 7 digits after stripping → flag as invalid_phone
- Company name is a single character or blank → flag as incomplete_company
