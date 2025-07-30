# shared_utils/text_utils.py

import re
from datetime import datetime

def clean_transaction_value(value_str):
    """Clean and parse transaction value string"""
    if not value_str:
        return 0.0
    
    try:
        # Remove currency symbols and spaces
        cleaned = re.sub(r'[^\d.,]', '', str(value_str))
        
        # Handle Indonesian number format (1.000.000,00)
        if ',' in cleaned and '.' in cleaned:
            if cleaned.rfind(',') > cleaned.rfind('.'):
                # Indonesian format
                cleaned = cleaned.replace('.', '').replace(',', '.')
            else:
                # US format
                cleaned = cleaned.replace(',', '')
        elif ',' in cleaned:
            # Check if comma is decimal separator
            if len(cleaned.split(',')[-1]) <= 2:
                cleaned = cleaned.replace(',', '.')
            else:
                cleaned = cleaned.replace(',', '')
        
        return float(cleaned)
        
    except:
        return 0.0

def fuzzy_month_match(text_blocks):
    """Find month from text blocks using fuzzy matching"""
    month_map = {
        'januari': 'January', 'februari': 'February', 'maret': 'March', 
        'april': 'April', 'mei': 'May', 'juni': 'June',
        'juli': 'July', 'agustus': 'August', 'september': 'September', 
        'oktober': 'October', 'november': 'November', 'desember': 'December'
    }
    
    for block in text_blocks:
        text_lower = block.lower()
        for indo_month, eng_month in month_map.items():
            if indo_month in text_lower:
                return eng_month
    
    return None

def clean_number(number_str):
    """Clean and parse number string"""
    try:
        # Remove non-numeric characters except decimal separators
        cleaned = re.sub(r'[^\d.,]', '', str(number_str))
        
        # Handle different decimal formats
        if ',' in cleaned and '.' in cleaned:
            if cleaned.rfind(',') > cleaned.rfind('.'):
                # Indonesian format: 1.000.000,00
                cleaned = cleaned.replace('.', '').replace(',', '.')
            else:
                # US format: 1,000,000.00
                cleaned = cleaned.replace(',', '')
        elif ',' in cleaned:
            # Check if comma is decimal separator
            if len(cleaned.split(',')[-1]) <= 2:
                cleaned = cleaned.replace(',', '.')
            else:
                cleaned = cleaned.replace(',', '')
        
        return float(cleaned)
        
    except:
        return 0.0

def clean_string(text):
    """Clean string for processing"""
    if not text:
        return ""
    
    # Remove extra whitespace and special characters
    cleaned = re.sub(r'\s+', ' ', str(text).strip())
    cleaned = re.sub(r'[^\w\s.,;:\-()]', '', cleaned)
    
    return cleaned
