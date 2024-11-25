from urllib.parse import urlparse, parse_qs

def extract_node_ids():
    return '0:1'

def extract_file_key(figma_link):

    parts = figma_link.split('/')
    if len(parts) >= 5:
        return parts[4]
    else:
        return None
    
