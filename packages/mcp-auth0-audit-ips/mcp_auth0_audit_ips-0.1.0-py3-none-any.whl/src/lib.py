import requests
import time
from typing import List

def make_request_with_retry(url: str, method: str = "get", max_retries: int = 3, initial_delay: int = 1, **kwargs):
    """Make a request with retry logic for 429 errors"""
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code != 429:  # If not a rate limit error
                return response
            
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                delay = initial_delay * (2 ** attempt)
                time.sleep(delay)
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            delay = initial_delay * (2 ** attempt)
            time.sleep(delay)
    
    return response

def get_suspicious_ips(tinybird_token: str, tinybird_url: str, date_from: str, date_to: str, min_failures: int = 5, limit: int = 100) -> str:
    """Fetch suspicious IPs from Tinybird"""
    params = {
        'date_from': date_from,
        'date_to': date_to,
        'min_failures': min_failures,
        'limit': limit,
        'token': tinybird_token
    }
    
    try:
        response = make_request_with_retry(tinybird_url, params=params)
        response.raise_for_status()
        return str(response.json())
    except Exception as e:
        return str(e)

def get_ip_details(ipquery_url: str, ips: List[str]) -> str:
    """Get IP details from ipquery.io"""
    ip_list = ','.join(ips)
    try:
        response = make_request_with_retry(f"{ipquery_url}/{ip_list}")
        response.raise_for_status()
        return str(response.json())
    except Exception as e:
        return str(e)

def check_ip_reputation(abuseipdb_key: str, vt_key: str, ips: List[str]) -> str:
    """Check IP reputation using various services"""
    if not ips:
        return {"error": "No IP provided"}
    
    results = {}
    for ip in ips:
        abuse_url = f"https://api.abuseipdb.com/api/v2/check"
        headers = {"Key": abuseipdb_key, "Accept": "application/json"}
        params = {"ipAddress": ip, "maxAgeInDays": 90}
        try:
            response = make_request_with_retry(abuse_url, headers=headers, params=params)
            results["abuseipdb"] = response.json()
        except Exception as e:
            results["abuseipdb"] = {"error": str(e)}

        vt_url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"x-apikey": vt_key}
        try:
            response = make_request_with_retry(vt_url, headers=headers)
            results["virustotal"] = response.json()
        except Exception as e:
            results["virustotal"] = {"error": str(e)}

    return str(results)
