# REST API quick reference

Authenticate all `/api/*` routes with `X-API-Key: <SOCIAL_API_KEY>`. `/health` and `/` are public; `/webhooks/meta` uses Meta signature verification. All JSON API requests must use `Content-Type: application/json`.

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Readiness status (no secrets) |
| GET | `/api/status` | Operator configuration readiness (booleans only) |
| GET, PUT | `/api/brand` | Brand profile |
| GET | `/api/signals?q=topic` | Google News RSS signal titles and sources |
| POST | `/api/drafts/generate` | Optional LLM/template copy |
| GET, POST | `/api/posts` | List and create immutable drafts |
| POST | `/api/posts/{id}/approve` | Draft → approved |
| POST | `/api/posts/{id}/schedule` | Approved → scheduled; timezone-aware `at` |
| POST | `/api/posts/{id}/publish` | Approved → publishing → result |
| POST | `/api/posts/{id}/cancel` | Scheduled → cancelled |
| POST | `/api/media/poster`, `/api/media/video` | Create PNG or MP4 |
| GET | `/api/media/{filename}` | Authenticated media download |
| GET | `/public/media/{filename}` | Only enabled with PUBLIC_MEDIA_URL |
| GET | `/api/inbox` | Review received messages |
| POST | `/api/inbox/ingest` | Operator-only test ingestion |
| POST | `/api/inbox/{id}/draft` | Draft suggested reply |
| PUT | `/api/inbox/{id}/reply` | Edit reviewable reply |
| POST | `/api/inbox/{id}/send` | Human-approved send / dry-run |
| GET | `/api/audit` | Last 200 local audit events |
| GET, POST | `/webhooks/meta` | Meta challenge and signed events |

### Example: create and approve a LinkedIn post

```bash
export KEY='your_random_key'
curl http://127.0.0.1:8050/api/posts \
  -H "X-API-Key: $KEY" -H 'Content-Type: application/json' \
  -d '{"title":"An idea worth sharing","body":"We are exploring practical AI workflows.","platform":"linkedin"}'
# Copy the id from the response; then:
curl -X POST http://127.0.0.1:8050/api/posts/REPLACE_ID/approve -H "X-API-Key: $KEY"
curl -X POST http://127.0.0.1:8050/api/posts/REPLACE_ID/publish -H "X-API-Key: $KEY"
```

With default `SOCIAL_DRY_RUN=true`, the final status must be `simulated`. `published` is only used for successful live Instagram or LinkedIn APIs. A YouTube upload becomes `uploaded_private`.

**Failure handling:** `409` means the transition is not allowed, `422` means input is invalid, `401` means authentication failed. External timeouts enter `needs_reconciliation` because the provider might have accepted the request; do not blindly retry.
