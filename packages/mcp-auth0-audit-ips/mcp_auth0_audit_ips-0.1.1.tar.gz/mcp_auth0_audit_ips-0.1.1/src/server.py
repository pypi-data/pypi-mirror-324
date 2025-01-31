from mcp.server.fastmcp import FastMCP
from lib import get_suspicious_ips, get_ip_details, check_ip_reputation
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()
TINYBIRD_TOKEN = os.getenv("TINYBIRD_TOKEN")
TINYBIRD_HOST = os.getenv("TINYBIRD_HOST")
TINYBIRD_URL = f"https://{TINYBIRD_HOST}/v0/pipes/auth0_suspicious_ips.json"
IPQUERY_URL = "https://api.ipquery.io"

ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY")
VT_KEY = os.getenv("VT_KEY")

mcp = FastMCP("auth0_suspicious_ips", dependencies=["requests"])

@mcp.tool()
def get_suspicious_ips_tool(date_from: str, date_to: str, min_failures: int = 5, limit: int = 100) -> str:
    return get_suspicious_ips(TINYBIRD_TOKEN, TINYBIRD_URL, date_from, date_to, min_failures, limit)

@mcp.tool()
def get_ip_details_tool(ips: List[str]) -> str:
    return get_ip_details(IPQUERY_URL, ips)

@mcp.tool()
def check_ip_reputation_tool(ips: List[str]) -> str:
    return check_ip_reputation(ABUSEIPDB_KEY, VT_KEY, ips)

@mcp.prompt()
def suspicious_auth0_ips_report() -> str:
    return """
    Use get_suspicious_ips_tool, get_ip_details_tool, and check_ip_reputation_tool to generate a security report. 
    Ask for a date range from the user.
    - get_suspicious_ips_tool returns failed ip logins from Auth0 log streams. use this format for datetimes YYYY-MM-DD HH:MM:SS.
    - get_ip_details_tool uses ipquery.io send the result from get_suspicious_ips_tool.
    - check_ip_reputation_tool uses abuseipdb and virustotal, send the result from get_suspicious_ips_tool.
    Skip errors if any of the tools fail.
    Once you do all requests, return a detailed report with the following sections: generated_at, summary, top_offenders, subnet_groups, geographic_distribution, risk_analysis, failed_attempts, first_attempt, last_attempt, user_agent, location, risk
    """
