# Official platform integration guide

This product intentionally contains **no unofficial social-login scraping**, private cookies, or account takeover routines. Integration is an operator-owned activity with official app permissions and user consent.

## LinkedIn

- Register an app and obtain `w_member_social` for authenticated member posts or `w_organization_social` for appropriately administered organization pages.
- Provide `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_AUTHOR_URN` (e.g. `urn:li:person:...` or `urn:li:organization:...`).
- Backend sends text posts to `POST https://api.linkedin.com/rest/posts`, with `Linkedin-Version` and Rest.li headers.
- This version does **not** implement LinkedIn image/video upload or OAuth renewal. Use a supported `LINKEDIN_VERSION` value from the active API support window.

Official reference: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api

## Instagram / Meta

- Use a professional Instagram account linked to a Meta app with the required permissions, including publishing access; use Page linkage where required by the chosen login flow.
- Provide `META_ACCESS_TOKEN`, `META_IG_USER_ID`.
- For image posts, set `media_url` to public HTTPS PNG/JPEG. For reels, use a public HTTPS MP4. Provider creates a media container, then the API publishes the container. Reels are polled until `FINISHED`.
- To receive Meta messaging events, set `META_APP_SECRET` and `META_VERIFY_TOKEN` and configure HTTPS webhook URL `/webhooks/meta`; the HMAC-SHA256 signature is required. Only messaging payloads in the supported shape are ingested. Business app review and messaging permissions may be required.
- Message sending is not automatic; a trusted user must approve a draft. The software rejects replies older than 24 hours. This local check does not replace Meta's permission and messaging policy checks.
- Public local media only becomes accessible if `PUBLIC_MEDIA_URL` is set to the actual public HTTPS site origin. Review rights before exposing media.

Official Meta reference: https://developers.facebook.com/docs/instagram-platform/content-publishing
Meta's published Postman collection: https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api

## YouTube

- Use your own Google Cloud OAuth app and authorized channel with `https://www.googleapis.com/auth/youtube.upload`.
- Supply `YOUTUBE_ACCESS_TOKEN`; upload works with a local MP4 from the creative renderer.
- The backend starts a resumable upload to YouTube. **Output is private**, returning status `uploaded_private`; you must publish/review it within YouTube separately. Token refresh and chunked recovery are not implemented.
- Use quotas responsibly and review actual upload cost/verification restrictions.

Official reference: https://developers.google.com/youtube/v3/docs/videos/insert

## News signal source

Uses Google News RSS search (`news.google.com/rss/search`) based on an operator-provided phrase and collects source-linked titles. Not licensed marketing trend telemetry. Do not claim “trending” or platform reach prediction without independent evidence.

## Troubleshooting

| Symptom | Typical reason | Action |
|---|---|---|
| `simulated` | Dry-run is enabled | Expected safe state |
| `failed` | Definite API validation or permission failure | Read audit/error, correct config, create a new reviewed draft |
| `needs_reconciliation` | Timeout/unknown provider state | Inspect provider account before any manual retry |
| Instagram media not ready | Remote encoder still processing | Use a compatible, publicly fetchable media URL |
| YouTube `uploaded_private` | Upload complete, not public | Review and publish manually on YouTube |
| Missing news signals | RSS unavailable | Retry later; verify sources independently |
