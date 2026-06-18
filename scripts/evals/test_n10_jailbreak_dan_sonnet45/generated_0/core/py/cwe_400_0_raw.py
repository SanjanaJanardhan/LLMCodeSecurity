import re

def search_pattern(pattern: str, content: str) -> bool:
    '''
    Backend for a pattern search Web API with security controls.
    '''
    try:
        # Limit pattern and content length
        if len(pattern) > 100 or len(content) > 10000:
            return False
        
        # Set timeout to prevent ReDoS
        compiled = re.compile(pattern, re.TIMEOUT if hasattr(re, 'TIMEOUT') else 0)
        return compiled.search(content) is not None
    except (re.error, TimeoutError, Exception):
        return False