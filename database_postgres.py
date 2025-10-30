"""
PostgreSQL Database Management for Legal Disclaimer Acceptances
Supabase-compatible version with persistent storage
GDPR/CCPA Compliant
"""
import os
from datetime import datetime
from typing import Optional, Dict, List
import json

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("Warning: psycopg2 not installed. Install with: pip install psycopg2-binary")

class DisclaimerDatabase:
    """Manages PostgreSQL database for storing legal disclaimer acceptances"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize database connection and create tables if needed
        
        Args:
            connection_string: PostgreSQL connection string
                              If None, will try to get from environment variable
        """
        if not POSTGRES_AVAILABLE:
            raise ImportError("psycopg2 is required for PostgreSQL. Install with: pip install psycopg2-binary")
        
        # Get connection string from parameter or environment
        self.connection_string = connection_string or os.getenv('DATABASE_URL')
        
        if not self.connection_string:
            raise ValueError(
                "Database connection string not provided. "
                "Set DATABASE_URL environment variable or pass connection_string parameter."
            )
        
        # Test connection
        try:
            conn = self.get_connection()
            conn.close()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}")
        
        # Initialize tables
        self.initialize_database()
    
    def get_connection(self):
        """Get a new database connection"""
        return psycopg2.connect(self.connection_string)
    
    def initialize_database(self):
        """Create tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Create acceptances table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS acceptances (
                id SERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                ip_address TEXT,
                geographic_location TEXT,
                country_code TEXT,
                browser_info TEXT,
                device_info TEXT,
                user_agent TEXT,
                terms_version TEXT NOT NULL,
                consent_analytics INTEGER DEFAULT 0,
                consent_functional INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create index on session_id for faster queries
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_acceptances_session_id 
            ON acceptances(session_id)
            """)
            
            # Create data_requests table for GDPR/CCPA compliance
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_requests (
                id SERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                request_type TEXT NOT NULL,
                request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                completed_timestamp TIMESTAMP,
                notes TEXT
            )
            """)
            
            # Create index on session_id for data_requests
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_data_requests_session_id 
            ON data_requests(session_id)
            """)
            
            # Create terms_versions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS terms_versions (
                version TEXT PRIMARY KEY,
                effective_date TIMESTAMP NOT NULL,
                description TEXT,
                full_text TEXT
            )
            """)
            
            # Insert current terms version if not exists
            cursor.execute("""
            INSERT INTO terms_versions (version, effective_date, description)
            VALUES (%s, %s, %s)
            ON CONFLICT (version) DO NOTHING
            """, ('1.0', datetime.now(), 'Initial version with GDPR/CCPA compliance'))
            
            conn.commit()
            print("✅ Database tables initialized successfully")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error initializing database: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def record_acceptance(self, 
                         session_id: str,
                         ip_address: Optional[str] = None,
                         geographic_location: Optional[str] = None,
                         country_code: Optional[str] = None,
                         browser_info: Optional[str] = None,
                         device_info: Optional[str] = None,
                         user_agent: Optional[str] = None,
                         terms_version: str = "1.0",
                         consent_analytics: bool = False) -> int:
        """
        Record a legal disclaimer acceptance
        Returns the record ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO acceptances (
                session_id, timestamp, ip_address, geographic_location, country_code,
                browser_info, device_info, user_agent, terms_version, consent_analytics
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """, (
                session_id,
                datetime.now(),
                ip_address,
                geographic_location,
                country_code,
                browser_info,
                device_info,
                user_agent,
                terms_version,
                1 if consent_analytics else 0
            ))
            
            record_id = cursor.fetchone()[0]
            conn.commit()
            print(f"✅ Acceptance recorded with ID: {record_id}")
            return record_id
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error recording acceptance: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def get_user_data(self, session_id: str) -> List[Dict]:
        """
        Retrieve all data for a specific session ID (GDPR right to access)
        """
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
            SELECT * FROM acceptances WHERE session_id = %s
            ORDER BY timestamp DESC
            """, (session_id,))
            
            rows = cursor.fetchall()
            data = [dict(row) for row in rows]
            
            return data
            
        except Exception as e:
            print(f"❌ Error retrieving user data: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def delete_user_data(self, session_id: str) -> int:
        """
        Delete all data for a specific session ID (GDPR right to erasure)
        Returns number of records deleted
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Log the deletion request first
            cursor.execute("""
            INSERT INTO data_requests (session_id, request_type, status)
            VALUES (%s, %s, %s)
            """, (session_id, 'deletion', 'completed'))
            
            # Delete the data
            cursor.execute("DELETE FROM acceptances WHERE session_id = %s", (session_id,))
            deleted_count = cursor.rowcount
            
            conn.commit()
            print(f"✅ Deleted {deleted_count} records for session: {session_id}")
            return deleted_count
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error deleting user data: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def log_data_request(self, session_id: str, request_type: str, notes: Optional[str] = None):
        """
        Log a data request (access, deletion, portability, etc.)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO data_requests (session_id, request_type, notes)
            VALUES (%s, %s, %s)
            """, (session_id, request_type, notes))
            
            conn.commit()
            print(f"✅ Data request logged: {request_type} for session {session_id}")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error logging data request: {e}")
        finally:
            cursor.close()
            conn.close()
    
    def get_statistics(self) -> Dict:
        """
        Get anonymized statistics about acceptances
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Total acceptances
            cursor.execute("SELECT COUNT(*) FROM acceptances")
            total_acceptances = cursor.fetchone()[0]
            
            # Acceptances by country
            cursor.execute("""
            SELECT country_code, COUNT(*) as count 
            FROM acceptances 
            WHERE country_code IS NOT NULL
            GROUP BY country_code 
            ORDER BY count DESC 
            LIMIT 10
            """)
            by_country = dict(cursor.fetchall())
            
            # Acceptances by terms version
            cursor.execute("""
            SELECT terms_version, COUNT(*) as count 
            FROM acceptances 
            GROUP BY terms_version
            """)
            by_version = dict(cursor.fetchall())
            
            # Analytics consent rate
            cursor.execute("""
            SELECT 
                SUM(consent_analytics) as consented,
                COUNT(*) as total
            FROM acceptances
            """)
            analytics_consent = cursor.fetchone()
            
            return {
                'total_acceptances': total_acceptances,
                'by_country': by_country,
                'by_version': by_version,
                'analytics_consent_rate': analytics_consent[0] / analytics_consent[1] if analytics_consent[1] > 0 else 0
            }
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {
                'total_acceptances': 0,
                'by_country': {},
                'by_version': {},
                'analytics_consent_rate': 0
            }
        finally:
            cursor.close()
            conn.close()
    
    def export_user_data_json(self, session_id: str) -> str:
        """
        Export user data as JSON (GDPR right to data portability)
        """
        data = self.get_user_data(session_id)
        
        # Convert datetime objects to strings
        for record in data:
            for key, value in record.items():
                if isinstance(value, datetime):
                    record[key] = value.isoformat()
        
        return json.dumps(data, indent=2, default=str)
    
    def close(self):
        """Close database connection (if needed for cleanup)"""
        pass
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] == 1
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

