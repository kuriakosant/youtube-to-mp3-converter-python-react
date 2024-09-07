import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_convert(client):
    # Test invalid request
    response = client.post('/convert', json={})
    assert response.status_code == 400

    # Test valid request
    valid_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Replace with an actual video ID
    response = client.post('/convert', json={'url': valid_url})
    assert response.status_code == 200
