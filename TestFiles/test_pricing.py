import pytest
from pytest import approx
from pricing_engine import get_base_price, calculate_dynamic_price

def test_get_base_price_yoga():
    # Güncel fiyat listesine göre 200
    assert get_base_price("Yoga") == 200

def test_get_base_price_fitness():
    assert get_base_price("Fitness") == 80

def test_get_base_price_invalid():
    # Geçersiz ders varsayılan 100 döner
    assert get_base_price("Tekwando") == 100

def test_price_morning_discount():
    # Yoga(200) * Sabah(0.8) * Standard(1.0) = 160
    assert calculate_dynamic_price("Yoga", 8, "Standard") == 160

def test_price_standard_hours():
    # Yoga(200) * Öğlen(1.0) * Standard(1.0) = 200
    assert calculate_dynamic_price("Yoga", 14, "Standard") == 200

def test_price_evening_surge():
    # Yoga(200) * Akşam(1.1) * Standard(1.0) = 220
    # Not: Parametrik testler akşam zammını %10 (1.1) bekliyor.
    assert calculate_dynamic_price("Yoga", 19, "Standard") == approx(220.0)
