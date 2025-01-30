import urllib.parse
import requests

def validate_config(config):
    """
    Validates the configuration dictionary to ensure required keys and correct data structure.
    """
    required_keys = ["redirect_url", "parameters", "platforms"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key: {key}")
    
    if "platforms" not in config or not isinstance(config["platforms"], dict):
        raise ValueError("platforms configuration must be a dictionary containing 'android' and 'ios' settings")
    
    if "android" not in config["platforms"] or "ios" not in config["platforms"]:
        raise ValueError("Both android and ios platforms configurations are required")
    
    return True

def shorten_url(long_url):
    """
    Shortens a URL using the is.gd service.
    """
    try:
        response = requests.get(f"https://is.gd/create.php?format=simple&url={urllib.parse.quote(long_url)}")
        if response.status_code == 200:
            return response.text
        else:
            return long_url
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return long_url
