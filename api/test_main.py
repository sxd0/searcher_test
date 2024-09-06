from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

#важно!!! выбрать существующие данные, либо в pytest выйдет ошибка
def test_delete_document():
    delete_response = client.delete("/documents/5")
    assert delete_response.status_code == 204

    get_response = client.get("/documents/1")
    assert get_response.status_code == 404


def test_search_documents():
    response = client.get("/search/?query=поиск")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_document():
    get_response = client.get("/documents/10")
    assert get_response.status_code == 200
    assert "text" in get_response.json()


def test_import_csv():
    csv_data = """rubrics,text,created_date
test,Импортированный документ,2024-09-01 12:00:00
"""
    response = client.post("/import-csv/", files={"file": ("test.csv", csv_data, "text/csv")})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_test_db():
    response = client.get("/test-db/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


