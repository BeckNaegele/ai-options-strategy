# Database & Privacy Compliance Documentation

## Overview

This application implements a comprehensive SQL database system to track legal disclaimer acceptances while maintaining full GDPR and CCPA compliance.

---

## Database Schema

### Tables

#### 1. `acceptances` Table
Stores user acceptance records with associated data.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Auto-incrementing record ID |
| `session_id` | TEXT | Unique session identifier |
| `timestamp` | TIMESTAMP | Date/time of acceptance |
| `ip_address` | TEXT | User's IP address |
| `geographic_location` | TEXT | City, Region, Country |
| `country_code` | TEXT | ISO 2-letter country code |
| `browser_info` | TEXT | Browser name and version |
| `device_info` | TEXT | Device type (Desktop/Mobile/Tablet) |
| `user_agent` | TEXT | Full user agent string |
| `terms_version` | TEXT | Version of terms accepted |
| `consent_analytics` | INTEGER | 1 if user consented to analytics, 0 otherwise |
| `consent_functional` | INTEGER | Always 1 (required for app functionality) |
| `created_at` | TIMESTAMP | Record creation timestamp |

#### 2. `data_requests` Table
Tracks GDPR/CCPA data rights requests.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Auto-incrementing request ID |
| `session_id` | TEXT | Session ID making the request |
| `request_type` | TEXT | Type: access, deletion, export, opt-out |
| `request_timestamp` | TIMESTAMP | When request was made |
| `status` | TEXT | pending, completed, rejected |
| `completed_timestamp` | TIMESTAMP | When request was completed |
| `notes` | TEXT | Additional information |

#### 3. `terms_versions` Table
Tracks different versions of terms and conditions.

| Column | Type | Description |
|--------|------|-------------|
| `version` | TEXT PRIMARY KEY | Version identifier (e.g., "1.0") |
| `effective_date` | TIMESTAMP | When version became effective |
| `description` | TEXT | Description of changes |
| `full_text` | TEXT | Full text of terms (optional) |

---

## Data Collected

### Required Data (Collected Automatically)
- **Session ID**: Unique identifier for the user's session
- **Timestamp**: When terms were accepted
- **IP Address**: User's internet protocol address
- **Geographic Location**: Approximate location (City, Region, Country)
- **Country Code**: ISO 2-letter code (for GDPR/CCPA detection)
- **Browser Information**: Browser name and version
- **Device Information**: Desktop, Mobile, or Tablet
- **User Agent**: Technical browser/OS information
- **Terms Version**: Which version was accepted

### Optional Data (Requires Consent)
- **Analytics Consent**: Whether user agreed to analytics tracking

### Data NOT Collected
- Name, email, phone number
- Payment information
- Social security numbers
- Financial account numbers
- Browsing history on other sites

---

## GDPR Compliance

### Legal Basis for Processing
1. **Consent**: User provides explicit consent via checkbox
2. **Legal Obligation**: Maintaining audit trail for legal defense
3. **Legitimate Interests**: Security and fraud prevention

### User Rights Implemented

#### 1. Right to Access (Article 15)
Users can view all data stored about them.

**How to Exercise:**
- Footer → "Your Data Rights" → "Access My Data"
- Enter Session ID
- System displays all records

#### 2. Right to Erasure (Article 17 - "Right to be Forgotten")
Users can request deletion of their data.

**How to Exercise:**
- Footer → "Your Data Rights" → "Delete My Data"
- Enter Session ID
- System permanently deletes all records

#### 3. Right to Data Portability (Article 20)
Users can export their data in machine-readable format.

**How to Exercise:**
- Footer → "Your Data Rights" → "Export My Data"
- Enter Session ID
- Download JSON file with all data

#### 4. Right to Object (Article 21)
Users can opt-out of analytics tracking.

**How to Exercise:**
- Footer → "Your Data Rights" → "Opt-Out of Analytics"
- System stops analytics tracking

#### 5. Right to Information (Articles 13-14)
Comprehensive Privacy Policy provided before data collection.

**How to Access:**
- Legal Disclaimer → "Privacy Policy" expandable section
- Footer → "View Full Privacy Policy" button

### Data Retention
- **Retention Period**: 3 years from acceptance date
- **Reason**: Legal compliance and audit requirements
- **Early Deletion**: Available upon request

### Data Breach Notification
- **Notification Timeline**: Within 72 hours
- **Scope**: Users and relevant authorities
- **Method**: Application notification and email (if available)

---

## CCPA Compliance

### Consumer Rights Implemented

#### 1. Right to Know (§1798.100)
Users can know what personal information is collected.

**Disclosure Location:**
- Legal Disclaimer → Section 12: "Data Collection and Privacy"
- Privacy Policy → Section 2: "Information We Collect"

#### 2. Right to Delete (§1798.105)
Users can request deletion of their data.

**How to Exercise:**
- Same as GDPR Right to Erasure (see above)

#### 3. Right to Opt-Out (§1798.120)
**Note:** We do NOT sell personal information.
- Users can opt-out of analytics tracking
- No sale of data occurs

#### 4. Right to Non-Discrimination (§1798.125)
Users exercising privacy rights are NOT discriminated against.
- Full application access maintained
- No price differences
- No service level differences

### CCPA Notices

**"Do Not Sell My Personal Information"**
- We do NOT sell personal information
- Stated clearly in Privacy Policy Section 5.1
- No opt-out required (no sale occurs)

**At Collection Notice**
- Provided in Legal Disclaimer Section 12
- Provided in Privacy Policy
- Provided before "Accept" button clicked

---

## Database Operations

### Initialization
```python
from database import DisclaimerDatabase

db = DisclaimerDatabase()
# Creates database and tables if they don't exist
```

### Recording Acceptance
```python
from user_tracking import UserDataCollector

# Collect user data
user_data = UserDataCollector.collect_all_data()
user_data['consent_analytics'] = True  # or False

# Store in database
record_id = db.record_acceptance(**user_data)
```

### Accessing User Data
```python
# Get all records for a session
data = db.get_user_data(session_id="abc123")

# Export as JSON
json_data = db.export_user_data_json(session_id="abc123")
```

### Deleting User Data
```python
# Delete all records for a session
deleted_count = db.delete_user_data(session_id="abc123")
```

### Logging Data Requests
```python
# Log GDPR/CCPA request
db.log_data_request(
    session_id="abc123",
    request_type="access",  # access, deletion, export, opt-out
    notes="User requested data access"
)
```

### Getting Statistics
```python
# Get anonymized statistics
stats = db.get_statistics()
# Returns: total_acceptances, by_country, by_version, analytics_consent_rate
```

---

## Security Measures

### Data Protection
1. **Database Encryption**: SQLite database stored securely
2. **Access Control**: Limited to application server
3. **No Third-Party Access**: Data NOT sold or shared (except legal requirements)
4. **Session-Based Identification**: No personally identifiable names/emails collected
5. **IP Anonymization**: Optional (can be implemented)

### Security Best Practices
- Regular database backups
- Access logging for all database operations
- Secure server configuration
- HTTPS encryption for data transmission
- No sensitive data stored (no passwords, payment info, etc.)

---

## Deployment Considerations

### Streamlit Cloud

**Important Note:** Streamlit Cloud apps reset on deployment, which means the SQLite database will be lost.

**Solutions:**

#### Option 1: SQLite with Persistent Volume (Local/Self-Hosted)
```bash
# Mount persistent volume
docker run -v /path/to/data:/app/data streamlit_app
```

#### Option 2: PostgreSQL (Recommended for Production)
```python
# Update database.py to use PostgreSQL instead of SQLite
import psycopg2
# Use environment variables for connection
DATABASE_URL = os.getenv('DATABASE_URL')
```

**Streamlit Cloud Environment Variables:**
```
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Option 3: Cloud Database
- AWS RDS (PostgreSQL/MySQL)
- Google Cloud SQL
- Azure Database
- Heroku Postgres

### Environment Variables
Create `.streamlit/secrets.toml`:
```toml
[database]
url = "postgresql://user:password@host:port/database"
type = "postgresql"
```

Access in code:
```python
import streamlit as st
db_url = st.secrets["database"]["url"]
```

---

## Testing

### Test Database Operations
```python
# Test acceptance recording
user_data = {
    'session_id': 'test_123',
    'ip_address': '127.0.0.1',
    'geographic_location': 'Test City, Test State, Test Country',
    'country_code': 'US',
    'browser_info': 'Chrome 96',
    'device_info': 'Desktop',
    'user_agent': 'Mozilla/5.0...',
    'terms_version': '1.0',
    'consent_analytics': True
}

record_id = db.record_acceptance(**user_data)
print(f"Record ID: {record_id}")

# Test data retrieval
data = db.get_user_data('test_123')
print(f"Found {len(data)} records")

# Test deletion
deleted = db.delete_user_data('test_123')
print(f"Deleted {deleted} records")
```

---

## Legal Disclaimers

### For Application Administrators

**You must:**
1. Review Privacy Policy with legal counsel
2. Customize contact information
3. Ensure data security measures are in place
4. Respond to data requests within legal timeframes (30-45 days)
5. Maintain data request logs
6. Notify users of data breaches within 72 hours

**Recommended:**
- Appoint a Data Protection Officer (DPO) if required
- Conduct Data Protection Impact Assessment (DPIA)
- Maintain records of processing activities
- Regular security audits

---

## Support & Contact

For questions about database implementation or privacy compliance:
- Review this documentation
- Check Privacy Policy (privacy_policy.py)
- Consult legal counsel for specific legal questions

---

## Version History

- **v1.0** (2025-10-30): Initial implementation
  - SQLite database
  - GDPR & CCPA compliance
  - User data rights interface
  - Privacy Policy integration

---

## License & Disclaimer

This database system is provided for educational and informational purposes. The developer is NOT a lawyer and this does NOT constitute legal advice. Consult with qualified legal counsel to ensure compliance with applicable laws in your jurisdiction.

