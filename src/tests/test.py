from src.main import app
from fastapi.testclient import TestClient


client = TestClient(app)




class RootTest:
    @staticmethod
    def test_head():

        response =  client.head('/check_db')
        assert response.status_code == 200


class TestTasks:
    @staticmethod
    def all_tasks():
        response = client.get('/all_tasks')
        assert response.status_code == 200

    @staticmethod
    def test_connect():
        response = client.get('/ping')
        assert response.status_code == 200
        assert response.text == 'pong'

