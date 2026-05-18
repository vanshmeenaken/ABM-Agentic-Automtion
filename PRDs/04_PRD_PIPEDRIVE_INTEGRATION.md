# 04 — Pipedrive Integration

**Phase:** 4  
**Inputs from:** Phase 2 (prospect + campaign models)  
**Outputs to:** Phase 5 (governance uses Pipedrive DNC state), Phase 9+ (channel phases log to Pipedrive)

---

## 1. Phase purpose
Build the full Pipedrive API integration: fetch persons/organisations/leads, create leads, update labels, create activities, add notes, detect manual intervention, mark replied, mark DNC, mark meeting booked.

## 2. Pipedrive is source of truth
The Django platform syncs TO and FROM Pipedrive but never overwrites Pipedrive state without explicit workflow validation. Pipedrive wins on conflict for: lead status, owner, DNC flag, manual activity detection.

---

## 3. Integration operations

### Read operations
- `GET /persons/{id}` — fetch person record
- `GET /organizations/{id}` — fetch org record
- `GET /leads/{id}` — fetch lead record
- `GET /activities?person_id=` — detect manual sales activity

### Write operations
- `POST /leads` — create new lead from prospect
- `PUT /persons/{id}` — update label/field
- `POST /activities` — log touchpoint or handoff activity
- `POST /notes` — add handoff brief as note

### Sync events
- Prospect created in platform → create person + lead in Pipedrive
- Sequence stopped → update lead label to `automation_stopped`
- Reply detected → update label to `replied`, log activity
- Handoff created → add note + activity assigned to owner
- Meeting booked → create meeting activity in Pipedrive
- DNC marked → add `do_not_contact` label permanently

---

## 4. Manual intervention detection
Poll Pipedrive activities for each active prospect every 15 minutes via Celery Beat. If a sales owner has logged a call, email, or meeting manually → trigger stop automation for that prospect.

---

## 5. Pipedrive field mapping
| Pipedrive field | Platform field |
|-----------------|----------------|
| Person name | Prospect first_name + last_name |
| Email | Prospect email |
| Phone | Prospect phone |
| Organization | Account company_name |
| Label | Sequence status + automation state |
| Owner | Campaign owner |

---

## 6. Acceptance criteria
- [ ] Prospect created in platform → appears in Pipedrive as person + lead
- [ ] Manual Pipedrive activity → stops automation in platform within 15 min
- [ ] Reply detected → Pipedrive label updated within 5 min
- [ ] DNC marked in Pipedrive → prospect blocked in platform within sync cycle
- [ ] Handoff note appears in Pipedrive lead timeline
