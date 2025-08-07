import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Ensure the application module can be imported when tests run from any path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app import validate_csv_structure


def test_valid_csv(monkeypatch):
    errors = []
    warnings = []
    monkeypatch.setattr(st, "error", lambda msg: errors.append(msg))
    monkeypatch.setattr(st, "warning", lambda msg: warnings.append(msg))

    df = pd.DataFrame({"Ingredient": ["Flour"], "Unit Cost": [1.5]})

    assert validate_csv_structure(df, ["Ingredient", "Unit Cost"], "Ingredient Info CSV")
    assert errors == []
    assert warnings == []


def test_invalid_numeric(monkeypatch):
    captured = []
    monkeypatch.setattr(st, "error", lambda msg: captured.append(msg))
    monkeypatch.setattr(st, "warning", lambda msg: None)

    df = pd.DataFrame({"Ingredient": ["Flour"], "Unit Cost": ["abc"]})

    assert not validate_csv_structure(df, ["Ingredient", "Unit Cost"], "Ingredient Info CSV")
    assert len(captured) == 1


def test_missing_column(monkeypatch):
    captured = []
    monkeypatch.setattr(st, "error", lambda msg: captured.append(msg))
    monkeypatch.setattr(st, "warning", lambda msg: None)

    df = pd.DataFrame({"Ingredient": ["Flour"]})

    assert not validate_csv_structure(df, ["Ingredient", "Unit Cost"], "Ingredient Info CSV")
    assert len(captured) == 1


def test_extra_column_warns(monkeypatch):
    errors = []
    warnings = []
    monkeypatch.setattr(st, "error", lambda msg: errors.append(msg))
    monkeypatch.setattr(st, "warning", lambda msg: warnings.append(msg))

    df = pd.DataFrame({"Ingredient": ["Flour"], "Unit Cost": [1.5], "Notes": ["something"]})

    assert validate_csv_structure(df, ["Ingredient", "Unit Cost"], "Ingredient Info CSV")
    assert errors == []
    assert len(warnings) == 1
