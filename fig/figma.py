def extract_node_ids():
    # Assuming '0:1' is the default node ID you need
    return '0:1'

def extract_file_key(figma_link):
    parts = figma_link.split('/')
    try:
        if '/file/' in figma_link:
            return parts[4] 
        else:
            return None
    except IndexError:
        return None
