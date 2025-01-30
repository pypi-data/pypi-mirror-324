import urllib.parse
from onelink.utils import validate_config, shorten_url

class DeeplinkGenerator:
    def __init__(self, config):
        """
        Initializes the DeeplinkGenerator with a configuration.
        """
        self.config = config
        self.validate_config()

    def validate_config(self):
        """
        Validates the configuration provided during initialization.
        """
        validate_config(self.config)

    def generate_deeplink(self):
        """
        Generates the deep link based on the configuration.
        """
        base_url = self.config["redirect_url"]
        parameters = self.config["parameters"]
        platforms = self.config["platforms"]
        event = self.config["event"]
        
        android = platforms.get("android", {})
        ios = platforms.get("ios", {})
        
        query_parameters = {
            "android": f"{android.get('package', '')}://{event}?{urllib.parse.urlencode(parameters)}&fallback_url={urllib.parse.quote(android.get('fallback_url', ''))}",
            "ios": f"{ios.get('package', '')}://{event}?{urllib.parse.urlencode(parameters)}&fallback_url={urllib.parse.quote(ios.get('fallback_url', ''))}"
        }
        
        deeplink = f"{base_url}?{urllib.parse.urlencode(query_parameters)}"
        return deeplink

    def create_deeplink(self):
        """
        Creates the deep link and shortens it.
        """
        try:
            deep_link = self.generate_deeplink()
            short_link = shorten_url(deep_link)
            return short_link
        except ValueError as e:
            print(f"Validation Error: {e}")
            return None
