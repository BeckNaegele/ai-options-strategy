"""
Database Management for Legal Disclaimer Acceptances
Stores user acceptance records with GDPR/CCPA compliance
"""
import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, List
import json

class DisclaimerDatabase:
    """Manages SQLite database for storing legal disclaimer acceptances"""
    
    def __init__(self, db_path: str = "disclaimer_acceptances.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create acceptances table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS acceptances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        
        # Create data_requests table for GDPR/CCPA compliance
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            request_type TEXT NOT NULL,
            request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            completed_timestamp TIMESTAMP,
            notes TEXT
        )
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
        INSERT OR IGNORE INTO terms_versions (version, effective_date, description)
        VALUES ('1.0', ?, 'Initial version with GDPR/CCPA compliance')
        """, (datetime.now(),))
        
        conn.commit()
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO acceptances (
            session_id, timestamp, ip_address, geographic_location, country_code,
            browser_info, device_info, user_agent, terms_version, consent_analytics
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def get_user_data(self, session_id: str) -> List[Dict]:
        """
        Retrieve all data for a specific session ID (GDPR right to access)
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM acceptances WHERE session_id = ?
        ORDER BY timestamp DESC
        """, (session_id,))
        
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        
        conn.close()
        return data
    
    def delete_user_data(self, session_id: str) -> int:
        """
        Delete all data for a specific session ID (GDPR right to erasure)
        Returns number of records deleted
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Log the deletion request first
        cursor.execute("""
        INSERT INTO data_requests (session_id, request_type, status)
        VALUES (?, 'deletion', 'completed')
        """, (session_id,))
        
        # Delete the data
        cursor.execute("DELETE FROM acceptances WHERE session_id = ?", (session_id,))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def log_data_request(self, session_id: str, request_type: str, notes: Optional[str] = None):
        """
        Log a data request (access, deletion, portability, etc.)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO data_requests (session_id, request_type, notes)
        VALUES (?, ?, ?)
        """, (session_id, request_type, notes))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self) -> Dict:
        """
        Get anonymized statistics about acceptances
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        by_country = cursor.fetchall()
        
        # Acceptances by terms version
        cursor.execute("""
        SELECT terms_version, COUNT(*) as count 
        FROM acceptances 
        GROUP BY terms_version
        """)
        by_version = cursor.fetchall()
        
        # Analytics consent rate
        cursor.execute("""
        SELECT 
            SUM(consent_analytics) as consented,
            COUNT(*) as total
        FROM acceptances
        """)
        analytics_consent = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_acceptances': total_acceptances,
            'by_country': dict(by_country),
            'by_version': dict(by_version),
            'analytics_consent_rate': analytics_consent[0] / analytics_consent[1] if analytics_consent[1] > 0 else 0
        }
    
    def export_user_data_json(self, session_id: str) -> str:
        """
        Export user data as JSON (GDPR right to data portability)
        """
        data = self.get_user_data(session_id)
        
        # Convert datetime objects to strings
        for record in data:
            if 'timestamp' in record:
                record['timestamp'] = str(record['timestamp'])
            if 'created_at' in record:
                record['created_at'] = str(record['created_at'])
        
        return json.dumps(data, indent=2)
    
    def close(self):
        """Close database connection (if needed for cleanup)"""
        pass

