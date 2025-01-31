# src/publichost/utils.py
import string
import random

# Common reserved words and system terms
RESERVED_WORDS = {
    # System and admin paths
    'admin', 'administrator', 'root', 'system', 'dashboard', 'console',
    'api', 'auth', 'login', 'dev', 'test', 'staging', 'prod', 'production',
    'internal', 'app', 'host', 'server', 'database', 'db', 'mail', 'smtp',
    'ftp', 'ssh', 'dns', 'mx', 'ns', 'ns1', 'ns2', 'web', 'www', 'control',
    
    # Common service names
    'grafana', 'prometheus', 'kibana', 'jenkins', 'gitlab', 'github', 
    'bitbucket', 'jira', 'confluence', 'wiki', 'docs', 'registry',
    
    # Security related
    'security', 'secure', 'ssl', 'tls', 'vpn', 'firewall', 'proxy',
    'sysadmin', 'webmaster', 'postmaster', 'hostmaster',
    
    # Common subdomains
    'blog', 'shop', 'store', 'support', 'help', 'status', 'metrics',
    'monitor', 'stats', 'analytics', 'cdn', 'assets', 'static', 'media',
    
    # Special terms
    'localhost', 'example', 'test', 'invalid', 'undefined', 'null'
}

def generate_subdomain(length: int = 5) -> str:
    """
    Generate a random subdomain that's not in the reserved list.
    
    Args:
        length (int): Length of the subdomain to generate
        
    Returns:
        str: A safe random subdomain
    """
    while True:
        chars = string.ascii_lowercase + string.digits
        subdomain = ''.join(random.choice(chars) for _ in range(length))
        if subdomain not in RESERVED_WORDS:
            return subdomain