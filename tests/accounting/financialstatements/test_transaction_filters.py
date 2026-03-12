#!/usr/bin/env python3
"""Unit tests for query.transaction_filters module."""

import pandas as pd

from investment.accounting.transaction_filters import (
    find_cash_infusion,
    find_all_stock_tradings_by_symbol,
    find_dividend_payments,
    find_expenses,
    find_service_charges,
)


def test_find_dividend_payments():
    df = pd.DataFrame({
        "Selitys": ["Arvopaperit", "Palvelumaksu", "ARVOPAPERIT"],
    })
    result = find_dividend_payments(df)
    assert len(result) == 2
    assert list(result["Selitys"]) == ["Arvopaperit", "ARVOPAPERIT"]


def test_find_service_charges():
    df = pd.DataFrame({
        "Selitys": ["Palvelumaksu", "Arvopaperit", "PALVELUMAKSU"],
    })
    result = find_service_charges(df)
    assert len(result) == 2
    assert list(result["Selitys"]) == ["Palvelumaksu", "PALVELUMAKSU"]


def test_find_all_stock_tradings_by_symbol():
    df = pd.DataFrame({
        "Laji": [700, 700, 700, 710],
        "Viesti": ["O:AAPL US /10", "M:AAPL US /5", "O:MSFT /3", "tilisiirto"],
        "Selitys": ["NOSTO", "PANO", "NOSTO", "tilisiirto"],
        "Määrä EUROA": ["-100,00", "50,00", "-200,00", "1000,00"],
    })
    result = find_all_stock_tradings_by_symbol(df)
    assert set(result.keys()) == {"AAPL", "MSFT"}
    assert len(result["AAPL"]) == 2
    assert len(result["MSFT"]) == 1


def test_find_cash_infusion():
    df = pd.DataFrame({
        "Laji": [710, 710, 700],
        "Selitys": ["Tilisiirto", "NOSTO", "Tilisiirto"],
        "Määrä EUROA": ["1000,00", "500,00", "200,00"],
        "Viesti": ["", "", ""],
    })
    result = find_cash_infusion(df)
    assert len(result) == 1
    assert result.iloc[0]["Selitys"] == "Tilisiirto"


def test_find_expenses():
    df = pd.DataFrame({
        "Määrä EUROA": ["-15,49", "-625,7"],
        "Laji": [700, 700],
        "Selitys": ["TILISIIRTO", "NOSTO"],
        "Viesti": ["", "O:PFE US /30"]
    })
    result = find_expenses(df)
    assert len(result) == 1
    assert result.iloc[0]["Määrä EUROA"] == "-15,49"


