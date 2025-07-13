import os
import sys
import re

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def adjust_qss_urls(qss_text):
    """Adjust URLs in QSS text to use absolute paths."""
    
    pattern = r'url\((["\']?)(.*?)\1\)'

    def replacer(match):
        quote, relative_path = match.groups()
        full_path = resource_path(relative_path)
        qt_path = full_path.replace("\\", "/")  
        return f'url("{qt_path}")'

    return re.sub(pattern, replacer, qss_text)