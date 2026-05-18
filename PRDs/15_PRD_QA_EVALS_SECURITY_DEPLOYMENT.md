# 15 — QA, Evals, Security, and Deployment

**Phase:** 15  
**Inputs from:** All prior phases  
**Outputs to:** Production deployment

---

## 1. Phase purpose
Add evaluation suites for all agents, test strategy, security controls, environment management, production deployment configuration, monitoring, backup, webhook retry queues, and error handling.

---

## 2. Eval suites (per agent)
| Agent | Eval dimensions |
|-------|----------------|
| Persona Classifier | Accuracy on 50 designation samples, edge cases, ambiguous titles |
| Message Compliance | True positive rate on blocked content, false positive rate on valid content |
| Email Copy | Persona alignment score, compliance pass rate, human approval rate |
| WhatsApp Copy | Format compliance, length compliance, opt-out language present |
| Reply Classifier | Intent accuracy on 100 reply samples across all categories |
| Sales Handoff | Brief completeness, suggested response quality |

---

## 3. Security controls
- All API endpoints authenticated (JWT)
- Webhook endpoints validate HMAC signature
- Sensitive fields (email, phone) encrypted at rest
- PII access logged in AuditLog
- Admin panel restricted to admin role
- Rate limiting on all public-facing endpoints
- No raw LLM output written to Pipedrive without validation

---

## 4. Environment management
| Environment | Purpose |
|-------------|---------|
| Local | Development and architecture validation |
| Staging | Integration testing, eval runs, UAT |
| Production | Live platform |

---

## 5. Monitoring
- Django health check endpoint polled every 60 sec
- Celery task failure rate alerted if > 5% in 1 hour
- Pipedrive sync lag alerted if > 30 min
- Stop automation delay alerted if > 10 min from reply

---

## 6. Backup
- PostgreSQL daily backup with 30-day retention
- AuditLog exported to cold storage monthly

---

## 7. Acceptance criteria
- [ ] All 6 agent eval suites pass minimum thresholds
- [ ] Staging environment mirrors production config
- [ ] Security scan passes with no critical findings
- [ ] Monitoring alerts fire correctly on simulated failures
- [ ] Backup and restore tested
