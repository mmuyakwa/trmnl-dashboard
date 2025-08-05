from flask import Flask, render_template, jsonify, redirect, abort, Response
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
TRMNL_API_KEY = os.getenv('TRMNL_API_KEY')
TRMNL_DEVICE_ID = os.getenv('TRMNL_DEVICE_ID', 'XX:XX:XX:XX:XX:XX')
TRMNL_BASE_URL = os.getenv('TRMNL_BASE_URL', 'https://trmnl.app/api')

class TRMNLClient:
    """Client for TRMNL API interactions"""
    
    def __init__(self, api_key, device_id, base_url):
        self.api_key = api_key
        self.device_id = device_id
        self.base_url = base_url
        
    def get_display_content(self):
        """Fetch current display content from TRMNL API"""
        try:
            headers = {
                'ID': self.device_id,
                'Access-Token': self.api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/display",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f'API Error: {response.status_code}',
                    'message': response.text,
                    'timestamp': datetime.now().isoformat()
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': 'Connection Error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Initialize TRMNL client
trmnl_client = TRMNLClient(TRMNL_API_KEY, TRMNL_DEVICE_ID, TRMNL_BASE_URL)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         device_id=TRMNL_DEVICE_ID,
                         api_configured=bool(TRMNL_API_KEY))

@app.route('/api/status')
def api_status():
    """API endpoint to get current TRMNL status"""
    if not TRMNL_API_KEY:
        return jsonify({
            'success': False,
            'error': 'Configuration Error',
            'message': 'TRMNL API key not configured'
        }), 500
    
    result = trmnl_client.get_display_content()
    return jsonify(result)

@app.route('/api/refresh')
def api_refresh():
    """API endpoint to force refresh TRMNL content"""
    return api_status()  # Same as status for now

@app.route('/image')
def image():
    """Display the current TRMNL image in fullscreen view"""
    if not TRMNL_API_KEY:
        abort(500)
    
    result = trmnl_client.get_display_content()
    
    if result.get('success') and result.get('data') and result['data'].get('image_url'):
        image_url = result['data']['image_url']
        filename = result['data'].get('filename', 'TRMNL Display')
        return render_template('image.html', 
                             image_url=image_url,
                             filename=filename,
                             device_id=TRMNL_DEVICE_ID)
    else:
        abort(404)

@app.route('/image/proxy')
def image_proxy():
    """Proxy the TRMNL image to avoid CORS issues"""
    if not TRMNL_API_KEY:
        abort(500)
    
    result = trmnl_client.get_display_content()
    
    if result.get('success') and result.get('data') and result['data'].get('image_url'):
        try:
            image_response = requests.get(result['data']['image_url'], timeout=10)
            if image_response.status_code == 200:
                return Response(
                    image_response.content,
                    mimetype=image_response.headers.get('content-type', 'image/png')
                )
        except requests.exceptions.RequestException:
            pass
    
    abort(404)

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error="Internal server error"), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=debug)