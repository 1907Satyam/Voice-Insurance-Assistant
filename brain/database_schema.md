# Relational Database Schema

The implementation uses SQLAlchemy models in `backend/app/db/models.py`. SQLite
is used by default; set `DATABASE_URL` to a PostgreSQL SQLAlchemy URL in deployed
environments.

## `users`

| Column | Type | Constraints / purpose |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `name` | String(120) | Required display name |
| `phone` | String(20) | Unique, indexed contact number |
| `preferred_language` | String(40) | Defaults to `hi` |
| `created_at` | DateTime | UTC creation timestamp |

One user may have multiple policies and claims.

## `policies`

| Column | Type | Constraints / purpose |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `policy_number` | String(40) | Unique, indexed policy reference |
| `user_id` | Integer | Nullable foreign key to `users.id` |
| `type` | String(40) | Indexed insurance category such as `motor` or `health` |
| `name`, `insurer` | String | Display names |
| `premium_inr`, `sum_insured_inr` | Float | Amounts in INR |
| `start_date`, `end_date` | String(10) | ISO `YYYY-MM-DD` dates |
| `coverage`, `exclusions` | JSON | Lists of plain-language clauses |
| `description` | Text | Short policy summary |

## `claims`

| Column | Type | Constraints / purpose |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `reference_id` | String(24) | Unique, indexed claim reference |
| `user_id`, `policy_id` | Integer | Nullable foreign keys to user and policy |
| `incident_type` | String(60) | Required category |
| `incident_date`, `incident_location` | String | Incident details |
| `description` | Text | Required incident description |
| `status` | String(40) | Indexed workflow status |
| `status_message` | Text | Plain-language status explanation |
| `created_at` | DateTime | UTC creation timestamp |

The seed script creates a demo user, motor and health policies, and example
claim `CLM-9842`. Seeded data is for demonstration and must be replaced with
appropriately protected customer data before production use.

## `claim_documents`

| Column | Type | Constraints / purpose |
| --- | --- | --- |
| `id` | Integer | Primary key |
| `claim_id` | Integer | Required foreign key to `claims.id` |
| `filename` | String(255) | Original display filename |
| `content_type` | String(100) | Allowed PDF/JPEG/PNG/WebP MIME type |
| `storage_name` | String(80) | Random server-side filename, unique |
| `size_bytes` | Integer | File size after upload validation |
| `uploaded_at` | DateTime | UTC upload timestamp |

Files are stored under `UPLOAD_DIR` (default `backend/uploads`) and metadata is
associated with the claim.