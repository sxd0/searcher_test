from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# def test_create_document():
#     # Создаем документ без полей title и content
#     response = client.post("/documents/", json={"text": "Тестовый документ", "rubrics": ["test"]})
#     assert response.status_code == 201
#     assert "id" in response.json()
#     assert response.json()["text"] == "Тестовый документ"

def delete_document():
    # Создаем документ
    response = client.post("/documents/", json={"text": "Удаляемый документ", "rubrics": ["test"]})
    assert response.status_code == 201
    document_id = response.json()["id"]

    # Удаляем документ
    delete_response = client.delete(f"/documents/{document_id}")
    assert delete_response.status_code == 204

    # Проверяем, что документ удален
    get_response = client.get(f"/documents/{document_id}")
    assert get_response.status_code == 404

def search_documents():
    # Создаем документ для поиска
    client.post("/documents/", json={"text": "Документ для поиска", "rubrics": ["test"]})

    # Выполняем поиск
    response = client.get("/search/?query=поиск")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["text"] == "Документ для поиска"

def import_csv():
    # Данные для импорта CSV (без title и content)
    csv_data = """rubrics,text,created_date
test,Импортированный документ,2024-09-01 12:00:00
"""
    response = client.post("/import-csv/", files={"file": ("test.csv", csv_data, "text/csv")})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_db():
    # Проверка подключения к базе данных
    response = client.get("/test-db/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def get_document():
    # Создаем документ для получения по ID
    response = client.post("/documents/", json={"text": "Документ для получения", "rubrics": ["test"]})
    assert response.status_code == 201
    document_id = response.json()["id"]

    # Получаем документ по ID
    get_response = client.get(f"/documents/{document_id}")
    assert get_response.status_code == 200
    assert get_response.json()["text"] == "Документ для получения"
