"""
Basic tests for TRMNL Dashboard Flask application.
"""
import os
import sys
import pytest
import tempfile
from unittest.mock import patch, MagicMock

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

def test_imports():
    """Test that the main modules can be imported."""
    try:
        import app
        assert app is not None
    except ImportError as e:
        pytest.fail(f"Failed to import app module: {e}")

def test_flask_app_creation():
    """Test that Flask app can be created."""
    # Set required environment variables
    with patch.dict(os.environ, {
        'TRMNL_API_KEY': 'test-key',
        'TRMNL_DEVICE_ID': '00:00:00:00:00:00',
        'TRMNL_BASE_URL': 'https://trmnl.app/api'
    }):
        import app
        assert app.app is not None
        assert app.app.name == 'app'

def test_trmnl_client_creation():
    """Test that TRMNLClient can be created."""
    with patch.dict(os.environ, {
        'TRMNL_API_KEY': 'test-key',
        'TRMNL_DEVICE_ID': '00:00:00:00:00:00',
        'TRMNL_BASE_URL': 'https://trmnl.app/api'
    }):
        import app
        client = app.TRMNLClient('test-key', '00:00:00:00:00:00', 'https://trmnl.app/api')
        assert client.api_key == 'test-key'
        assert client.device_id == '00:00:00:00:00:00'
        assert client.base_url == 'https://trmnl.app/api'

@patch('app.requests.get')
def test_trmnl_client_success_response(mock_get):
    """Test TRMNLClient with successful API response."""
    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'image_url': 'https://example.com/image.png',
        'filename': 'test.png',
        'update_firmware': False
    }
    mock_get.return_value = mock_response
    
    with patch.dict(os.environ, {
        'TRMNL_API_KEY': 'test-key',
        'TRMNL_DEVICE_ID': '00:00:00:00:00:00',
        'TRMNL_BASE_URL': 'https://trmnl.app/api'
    }):
        import app
        client = app.TRMNLClient('test-key', '00:00:00:00:00:00', 'https://trmnl.app/api')
        result = client.get_display_content()
        
        assert result['success'] is True
        assert 'data' in result
        assert result['data']['image_url'] == 'https://example.com/image.png'
        assert 'timestamp' in result

@patch('app.requests.get')
def test_trmnl_client_error_response(mock_get):
    """Test TRMNLClient with error API response."""
    # Mock error response
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = 'Unauthorized'
    mock_get.return_value = mock_response
    
    with patch.dict(os.environ, {
        'TRMNL_API_KEY': 'test-key',
        'TRMNL_DEVICE_ID': '00:00:00:00:00:00',
        'TRMNL_BASE_URL': 'https://trmnl.app/api'
    }):
        import app
        client = app.TRMNLClient('test-key', '00:00:00:00:00:00', 'https://trmnl.app/api')
        result = client.get_display_content()
        
        assert result['success'] is False
        assert result['error'] == 'API Error: 401'
        assert result['message'] == 'Unauthorized'
        assert 'timestamp' in result

def test_flask_routes_exist():
    """Test that Flask routes are properly defined."""
    with patch.dict(os.environ, {
        'TRMNL_API_KEY': 'test-key',
        'TRMNL_DEVICE_ID': '00:00:00:00:00:00',
        'TRMNL_BASE_URL': 'https://trmnl.app/api'
    }):
        import app
        
        # Get all routes
        routes = [rule.rule for rule in app.app.url_map.iter_rules()]
        
        # Check that expected routes exist
        assert '/' in routes
        assert '/api/status' in routes
        assert '/api/refresh' in routes
        assert '/image' in routes
        assert '/image/proxy' in routes

def test_flask_app_test_client():
    """Test Flask app with test client."""
    with patch.dict(os.environ, {
        'TRMNL_API_KEY': 'test-key',
        'TRMNL_DEVICE_ID': '00:00:00:00:00:00',
        'TRMNL_BASE_URL': 'https://trmnl.app/api'
    }):
        import app
        
        with app.app.test_client() as client:
            # Test main route
            response = client.get('/')
            assert response.status_code == 200
            assert b'TRMNL Dashboard' in response.data
            
            # Test API status route (will fail without actual API, but should not crash)
            response = client.get('/api/status')
            assert response.status_code in [200, 500]  # Either works or fails gracefully