# OneLink Generator

A Python package for generating platform-specific URLs for Android and iOS with support for custom parameters and fallback URLs.

## Features

- **Cross-Platform Support**: Generate deep links for both Android and iOS.
- **Custom Parameters**: Include user-specific parameters like email and invite tokens.
- **Fallback URLs**: Redirect users to app stores if the app is not installed.
- **Automatic Platform Detection**: Detects user platform and redirects accordingly.
- **Short Link Generation**: Creates short and shareable deep links.
- **Flask Integration**: Easily integrate with Flask-based web applications.
- **Error Handling**: Provides error messages for missing or invalid parameters.

## Installation

You can install the package via pip from PyPI:

```bash
pip install flask
pip install onelink
```

## Usage

### 1. Basic Setup
To generate OneLink-style URLs for Android and iOS, you need to set the App IDs for each platform and any other parameters you want to include.

### 2. Creating a Custom Link - Flask

```python
from flask import Flask, request, jsonify, render_template_string
import urllib.parse
from onelink.generator import DeeplinkGenerator

app = Flask(__name__)

@app.route('/create_deeplink', methods=['POST'])
def create_deeplink():
    try:
        config = request.json
        onelink = DeeplinkGenerator(config)
        short_link = onelink.create_deeplink()
        return jsonify({"short_link": short_link})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/redirect', methods=['GET'])
def redirect_user():
    android_deeplink = request.args.get('android')
    parsed_url = urllib.parse.urlparse(android_deeplink)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    android_fallback = query_params.get('fallback_url', [None])[0]

    ios_deeplink = request.args.get('ios')
    ios_parsed_url = urllib.parse.urlparse(ios_deeplink)
    ios_query_params = urllib.parse.parse_qs(ios_parsed_url.query)
    ios_fallback = ios_query_params.get('fallback_url', [None])[0]

    if not android_deeplink or not ios_deeplink or not android_fallback or not ios_fallback:
        return "Error: Missing platform deep links or fallback URLs", 400

    user_agent = request.headers.get('User-Agent', '').lower()

    html_content = """
    <html>
        <head>
            <script type="text/javascript">
                function redirectToApp(deepLink, fallbackUrl) {
                    var isAndroid = /android/i.test(navigator.userAgent);
                    var isIos = /iphone|ipod|ipad/i.test(navigator.userAgent);

                    window.location = deepLink;
                    setTimeout(function() {
                        window.location = fallbackUrl;
                    }, 2000);
                }
                redirectToApp("{{ deep_link }}", "{{ fallback_url }}");
            </script>
        </head>
        <body>
            <h1>Redirecting...</h1>
        </body>
    </html>
    """

    if 'android' in user_agent:
        deep_link = android_deeplink
        fallback_url = android_fallback
    elif 'iphone' in user_agent or 'ipad' in user_agent:
        deep_link = ios_deeplink
        fallback_url = ios_fallback
    else:
        deep_link = android_deeplink
        fallback_url = android_fallback

    return render_template_string(html_content, deep_link=deep_link, fallback_url=fallback_url)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
```

### Payload - create_deeplink

```json
{
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
```

### Generated Links - Production

```json
{
    "short_link": "https://is.gd/RyvDfA"
}
```

### Generated Links - Localhost

```json
{
    "short_link": "http://127.0.0.1:8080/redirect?android=com.abcandroid%3A%2F%2Finvite-email%3Femail%3Dabc%2540yopmail.com%26invite_code%3DABJGD867252JJHG%2525%2524%2523KLFJKLFG%26fallback_url%3Dhttps%253A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%253Fid%253Dcom.aiapp&ios=com.abcios%3A%2F%2Finvite-email%3Femail%3Dabc%2540yopmail.com%26invite_code%3DABJGD867252JJHG%2525%2524%2523KLFJKLFG%26fallback_url%3Dhttps%253A%2F%2Fapps.apple.com%2Fin%2Fapp%2Fapp-ai%2Fid6738657557"
}
```