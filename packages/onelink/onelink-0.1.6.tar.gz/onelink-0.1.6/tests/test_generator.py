import unittest
from onelink.generator import DeeplinkGenerator
from onelink.utils import validate_config, shorten_url

class TestDeeplinkPackage(unittest.TestCase):
    
    def setUp(self):
        self.config = {
            "redirect_url": "http://app.in/redirect",
            "event": "invite_email",
            "parameters": {
                "user_email": "abc@yopmail.com",
                "invite_token": "ABJGD867252JJHG%$#KLFJKLFG"
            },
            "platforms": {
                "android": {
                    "app_package": "com.abcandroid",
                    "fallback_link": "https://play.google.com/store/apps/details?id=com.aistyleapp"
                },
                "ios": {
                    "app_package": "com.abcios",
                    "fallback_link": "https://apps.apple.com/in/app/styleapp-ai/id6738657557"
                }
            }
        }
        self.deeplink_generator = DeeplinkGenerator(self.config)

    def test_validate_config_valid(self):
        try:
            self.deeplink_generator.validate_config()
        except ValueError:
            self.fail("validate_config raised ValueError unexpectedly!")

    def test_generate_deeplink(self):
        deeplink = self.deeplink_generator.generate_deeplink()
        self.assertIn("http://app.in/redirect?", deeplink)
    
    def test_shorten_url(self):
        long_url = "https://example.com"
        short_url = shorten_url(long_url)
        self.assertTrue(short_url.startswith("http"))
        
    def test_create_deeplink(self):
        short_link = self.deeplink_generator.create_deeplink()
        self.assertTrue(short_link.startswith("http"))

if __name__ == '__main__':
    unittest.main()
