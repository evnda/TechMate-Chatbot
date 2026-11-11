"""Uji integrasi route Flask menggunakan test client."""
import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def test_halaman_utama_menampilkan_techmate(client):
    res = client.get("/")
    assert res.status_code == 200
    assert "Bantuan Permasalahan Laptop" in res.get_data(as_text=True)


def test_halaman_chat_techmate(client):
    res = client.get("/chat/techmate")
    assert res.status_code == 200
    assert "TechMate" in res.get_data(as_text=True)


def test_tema_tidak_ada_404(client):
    assert client.get("/chat/tidak-ada").status_code == 404


def test_api_themes(client):
    data = client.get("/api/themes").get_json()
    assert len(data) == 1
    assert data[0]["id"] == "techmate"


def test_api_chat_berhasil(client):
    res = client.post("/api/chat", json={"message": "laptop saya lemot", "theme": "techmate"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["intent"] == "diagnosis_laptop_lemot"
    assert data["reply"]


@pytest.mark.parametrize("payload", [
    {"message": "", "theme": "techmate"},
    {"message": "halo", "theme": "salah"},
    {"message": "a" * 501, "theme": "techmate"},
    {},
])
def test_api_chat_input_tidak_valid(client, payload):
    assert client.post("/api/chat", json=payload).status_code == 400


def test_riwayat_tersimpan_dan_bisa_dihapus(client):
    client.post("/api/chat", json={"message": "halo", "theme": "techmate"})
    riwayat = client.get("/api/history/techmate").get_json()
    assert [r["sender"] for r in riwayat] == ["user", "bot"]
    client.delete("/api/history/techmate")
    assert client.get("/api/history/techmate").get_json() == []


def test_statistik_intent(client):
    client.post("/api/chat", json={"message": "halo", "theme": "techmate"})
    stats = client.get("/api/stats/techmate").get_json()
    assert stats[0]["intent"] == "salam"


def test_api_explain(client):
    data = client.post("/api/explain", json={"message": "laptop saya lemot", "theme": "techmate"}).get_json()
    assert data["threshold"] == 0.45
    assert data["candidates"][0]["intent"] == "diagnosis_laptop_lemot"


def test_admin_menampilkan_pertanyaan_tak_dikenali(client):
    client.post("/api/chat", json={"message": "harga tiket kereta", "theme": "techmate"})
    html = client.get("/admin/techmate").get_data(as_text=True)
    assert "harga tiket kereta" in html
    assert "tidak dikenali" in html
