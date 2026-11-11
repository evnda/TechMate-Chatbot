"""Uji unit untuk mesin chatbot (tanpa Flask)."""
from pathlib import Path
import pytest
from chatbot.engine import ChatbotEngine, load_themes, preprocess, similarity, validate_theme
from evaluate import baca_data, evaluasi

THEMES = load_themes(Path(__file__).resolve().parent.parent / "themes")
ENGINE = ChatbotEngine(THEMES["techmate"])


def test_preprocess_normalisasi_dan_stopword():
    assert preprocess("Gimana laptop saya lemot, kak?") == ["bagaimana", "laptop", "lemot"]


def test_similarity_kalimat_sama_bernilai_satu():
    tokens = ["laptop", "lemot"]
    assert similarity(tokens, tokens) == 1.0


def test_hanya_tema_techmate_termuat():
    assert set(THEMES) == {"techmate"}


@pytest.mark.parametrize("pesan,intent", [
    ("halo", "salam"),
    ("apa yang bisa kamu bantu", "bantuan"),
    ("kamu siapa", "identitas"),
    ("laptop saya lemot", "diagnosis_laptop_lemot"),
    ("laptop cepat panas", "diagnosis_laptop_panas"),
    ("baterai laptop cepat habis", "diagnosis_baterai_boros"),
    ("wifi laptop tidak bisa terhubung", "diagnosis_wifi"),
    ("penyimpanan laptop penuh", "diagnosis_penyimpanan_penuh"),
    ("laptop tidak mau menyala", "diagnosis_laptop_tidak_menyala"),
    ("aplikasi tidak bisa dibuka", "diagnosis_aplikasi_error"),
    ("makasih", "terima_kasih"),
    ("sampai jumpa", "perpisahan"),
])
def test_klasifikasi_semua_intent(pesan, intent):
    tag, _ = ENGINE.classify(pesan)
    assert tag == intent


def test_pertanyaan_di_luar_tema_memberi_fallback():
    hasil = ENGINE.reply("siapa presiden indonesia")
    assert hasil["intent"] is None
    assert hasil["reply"] in THEMES["techmate"]["fallback"]


def test_placeholder_nama_bot_diganti():
    hasil = ENGINE.reply("kamu siapa")
    assert "{nama_bot}" not in hasil["reply"]
    assert "TechMate" in hasil["reply"]


def test_validate_theme_valid():
    assert validate_theme(THEMES["techmate"]) == []


def test_akurasi_data_uji_minimal_90_persen():
    akurasi, _ = evaluasi(THEMES["techmate"], baca_data("techmate"), 0.45)
    assert akurasi >= 0.90


@pytest.mark.parametrize("pesan,intent", [
    ("laptopku lemot banget", "diagnosis_laptop_lemot"),
    ("laptop ngelag", "diagnosis_laptop_lemot"),
    ("kipas laptop bunyi kencang", "diagnosis_laptop_panas"),
    ("baterai laptop ngedrop", "diagnosis_baterai_boros"),
    ("wifi tidak nyambung", "diagnosis_wifi"),
    ("drive c hampir habis", "diagnosis_penyimpanan_penuh"),
    ("laptop tidak mau hidup sama sekali", "diagnosis_laptop_tidak_menyala"),
    ("aplikasi force close", "diagnosis_aplikasi_error"),
])
def test_variasi_bahasa_sehari_hari(pesan, intent):
    tag, _ = ENGINE.classify(pesan)
    assert tag == intent


def test_diagnosis_mengembalikan_checklist():
    hasil = ENGINE.reply("laptopku lemot banget")
    assert hasil["intent"] == "diagnosis_laptop_lemot"
    assert len(hasil["tasks"]) >= 5


def test_fallback_tidak_memakai_kata_maaf_sebagai_awalan():
    hasil = ENGINE.reply("berapa harga tiket kereta ke jakarta")
    assert hasil["intent"] is None
    assert "Maaf" not in hasil["reply"]
