# Keystroke Dynamics - Analiza wzorców pisania

Projekt do zbierania i analizy danych z klawiatury w celu badania behawioralnych wzorców pisania użytkownika (Keystroke Dynamics).

## Wymagania
- Python 3.8 lub nowszy
- Wymagane biblioteki:
  ```bash
  pip install pynput pandas openpyxl matplotlib scikit-learn
  ```

## Pliki
- "keystroke_collector.py": Skrypt do zbierania danych z klawiatury.
- "analyze_keystrokes.py": Analiza i wizualizacja danych.
- "keystroke_data.csv": Dane zebrane po uruchomieniu skryptu.

## Uruchomienie
1. Uruchom "keystroke_collector.py", pisz coś na klawiaturze i zakończ `ESC`.
2. Następnie uruchom `analyze_keystrokes.py` aby wyświetlić wykresy i analizę danych.
