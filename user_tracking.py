"""
User Tracking and Data Collection Module
Collects user information for compliance and analytics purposes
GDPR/CCPA Compliant - Only with explicit consent
"""
import streamlit as st
import requests
import json
from typing import Dict, Optional
from datetime import datetime
import hashlib

class UserDataCollector:
    """Collects user data for legal compliance and analytics"""
    
    @staticmethod
    def get_session_id() -> str:
        """
        Get or create a unique session ID for the user
        Uses Streamlit's session state
        """
        if 'user_session_id' not in st.session_state:
            # Create a unique session ID
            timestamp = datetime.now().isoformat()
            # Generate a hash-based session ID
            session_id = hashlib.sha256(timestamp.encode()).hexdigest()[:16]
            st.session_state.user_session_id = session_id
        
        return st.session_state.user_session_id
    
    @staticmethod
    def get_ip_address() -> Optional[str]:
        """
        Get user's IP address
        Note: This is tricky in Streamlit Cloud. We'll try multiple methods.
        """
        try:
            # Try to get from Streamlit context (may not always work)
            from streamlit.web.server.websocket_headers import _get_websocket_headers
            headers = _get_websocket_headers()
            if headers and 'X-Forwarded-For' in headers:
                return headers['X-Forwarded-For'].split(',')[0].strip()
        except:
            pass
        
        try:
            # Fallback: Use external service (be cautious with rate limits)
            response = requests.get('https://api.ipify.org?format=json', timeout=2)
            if response.status_code == 200:
                return response.json().get('ip')
        except:
            pass
        
        return None
    
    @staticmethod
    def get_geolocation(ip_address: Optional[str] = None) -> Dict[str, Optional[str]]:
        """
        Get geographic location based on IP address
        Returns: {location: str, country_code: str}
        """
        if not ip_address:
            return {'location': None, 'country_code': None}
        
        try:
            # Using ip-api.com (free, no API key needed, but rate limited)
            response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    location = f"{data.get('city', 'Unknown')}, {data.get('regionName', 'Unknown')}, {data.get('country', 'Unknown')}"
                    country_code = data.get('countryCode', 'XX')
                    return {
                        'location': location,
                        'country_code': country_code
                    }
        except Exception as e:
            print(f"Geolocation error: {e}")
        
        return {'location': 'Unknown', 'country_code': 'XX'}
    
    @staticmethod
    def get_browser_info() -> Dict[str, str]:
        """
        Get browser and device information
        Uses JavaScript to collect client-side info
        """
        # This will be collected via JavaScript in the Streamlit app
        # and stored in session state
        
        if 'browser_info' in st.session_state:
            return st.session_state.browser_info
        
        return {
            'browser': 'Unknown',
            'device': 'Unknown',
            'user_agent': 'Unknown'
        }
    
    @staticmethod
    def inject_browser_detection_script():
        """
        Inject JavaScript to detect browser and device information
        """
        st.markdown("""
        <script>
        // Detect browser information
        function detectBrowser() {
            var userAgent = navigator.userAgent;
            var browser = "Unknown";
            var device = "Unknown";
            
            // Browser detection
            if (userAgent.indexOf("Firefox") > -1) {
                browser = "Firefox";
            } else if (userAgent.indexOf("Chrome") > -1 && userAgent.indexOf("Edg") === -1) {
                browser = "Chrome";
            } else if (userAgent.indexOf("Safari") > -1 && userAgent.indexOf("Chrome") === -1) {
                browser = "Safari";
            } else if (userAgent.indexOf("Edg") > -1) {
                browser = "Edge";
            } else if (userAgent.indexOf("Opera") > -1 || userAgent.indexOf("OPR") > -1) {
                browser = "Opera";
            } else if (userAgent.indexOf("Trident") > -1) {
                browser = "Internet Explorer";
            }
            
            // Device detection
            if (/Mobile|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent)) {
                device = "Mobile";
                if (/iPad/i.test(userAgent)) {
                    device = "Tablet (iPad)";
                } else if (/Android/i.test(userAgent) && !/Mobile/i.test(userAgent)) {
                    device = "Tablet (Android)";
                } else if (/iPhone/i.test(userAgent)) {
                    device = "Mobile (iPhone)";
                } else if (/Android/i.test(userAgent)) {
                    device = "Mobile (Android)";
                }
            } else {
                device = "Desktop";
            }
            
            // Store in session storage
            sessionStorage.setItem('browser', browser);
            sessionStorage.setItem('device', device);
            sessionStorage.setItem('userAgent', userAgent);
            
            return {browser: browser, device: device, userAgent: userAgent};
        }
        
        // Run detection
        detectBrowser();
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def collect_all_data() -> Dict[str, any]:
        """
        Collect all user data for database storage
        """
        session_id = UserDataCollector.get_session_id()
        ip_address = UserDataCollector.get_ip_address()
        
        # Get geolocation if IP is available
        geo_data = UserDataCollector.get_geolocation(ip_address)
        
        # Get browser info from session state (populated by JavaScript)
        browser_info = st.session_state.get('browser_name', 'Unknown')
        device_info = st.session_state.get('device_type', 'Unknown')
        user_agent = st.session_state.get('user_agent_string', 'Unknown')
        
        return {
            'session_id': session_id,
            'ip_address': ip_address,
            'geographic_location': geo_data.get('location'),
            'country_code': geo_data.get('country_code'),
            'browser_info': browser_info,
            'device_info': device_info,
            'user_agent': user_agent,
            'terms_version': '1.0'
        }
    
    @staticmethod
    def is_gdpr_region(country_code: Optional[str]) -> bool:
        """
        Check if user is from GDPR-regulated region (EU/EEA)
        """
        gdpr_countries = [
            'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
            'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL',
            'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'IS', 'LI', 'NO', 'GB'
        ]
        return country_code in gdpr_countries if country_code else False
    
    @staticmethod
    def is_ccpa_region(country_code: Optional[str]) -> bool:
        """
        Check if user is from California (CCPA-regulated region)
        Note: IP-based detection can't distinguish US states, but we can detect US
        """
        return country_code == 'US' if country_code else False

