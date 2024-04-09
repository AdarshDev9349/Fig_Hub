from urllib.parse import urlparse, parse_qs

def extract_node_ids(figma_link):
    parsed_url = urlparse(figma_link)
    query_params = parse_qs(parsed_url.query)
    if 'node-id' in query_params:
        return query_params['node-id'][0]
    else:
        return None

def extract_file_key(figma_link):

    parts = figma_link.split('/')
    if len(parts) >= 5:
        return parts[4]
    else:
        return None
    
