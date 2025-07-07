# utils/security.py
from flask import redirect, request
from urllib.parse import urlparse

def is_safe_url(target):
    if not target:
        return False
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def safe_redirect(target, fallback):
    if target and is_safe_url(target):
        return redirect(target)
    return redirect(fallback)