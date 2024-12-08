# hAppy Apka 🎵

Aplikacja do losowego odtwarzania krótkich klipów wideo YouTube w określonych interwałach czasowych.

## Funkcjonalności 🎯

### Podstawowe sterowanie
- **🎲 hAppy shot** - losuje i odtwarza nowy klip wideo
- **🔄 hAppy continuum** - automatycznie odtwarza kolejne klipy w wybranym interwale czasowym

### Wyświetlanie wideo
- Automatyczne odtwarzanie wideo po uruchomieniu
- Wyświetlanie miniaturki filmu po zatrzymaniu
- Regulowany czas odtwarzania (5-10 sekund)
- Pasek postępu i licznik pozostałego czasu

### Menu kontroli
- Ukryte domyślnie (dostępne po kliknięciu w ikonę menu)
- Ustawienia czasu odtwarzania
- Informacje o aktualnym wideo
- Kopiowanie linku do aktualnego wideo
- Status ostatniego odświeżenia bazy

## Wymagania techniczne 🛠️

### Wymagane biblioteki Python
```bash
streamlit
sqlite3 (wbudowana)
```

### Baza danych
- SQLite - plik `clips.db`
- Wymagana tabela `clips` z kolumną `clip_url` zawierającą linki do YouTube

## Instalacja i uruchomienie 🚀

1. Sklonuj repozytorium lub pobierz kod źródłowy

2. Zainstaluj wymagane zależności:
```bash
pip install streamlit
```

3. Upewnij się, że masz przygotowaną bazę danych `clips.db` z odpowiednią strukturą

4. Uruchom aplikację:
```bash
streamlit run happy_app.py
```

## Struktura bazy danych 📁

Wymagana tabela w bazie SQLite (`clips.db`):
```sql
CREATE TABLE clips (
    clip_url TEXT NOT NULL
);
```

## Obsługa aplikacji 📱

1. **Uruchamianie nowego wideo**
   - Kliknij "🎲 hAppy shot" aby wylosować i odtworzyć nowy klip
   - Film zatrzyma się automatycznie po upływie ustawionego czasu

2. **Tryb automatyczny**
   - Zaznacz "🔄 hAppy continuum" aby włączyć automatyczne odtwarzanie
   - Aplikacja będzie automatycznie losować i odtwarzać kolejne klipy

3. **Ustawienia czasu**
   - Otwórz menu kontroli (ikona w lewym górnym rogu)
   - Użyj suwaka do ustawienia czasu odtwarzania (5-10 sekund)

4. **Kopiowanie linku**
   - W menu kontroli znajdź sekcję "Link do filmu"
   - Użyj przycisku "📋 Kopiuj link" aby skopiować link do schowka

## Konfiguracja 🔧

Aplikacja korzysta z domyślnych ustawień:
- Domyślny czas odtwarzania: 6 sekund
- Tryb ciemny
- Menu kontroli domyślnie ukryte
- Automatyczne odtworzenie pierwszego wideo po uruchomieniu

## Wsparcie 💡

W razie problemów:
1. Sprawdź połączenie z bazą danych
2. Upewnij się, że linki w bazie są poprawnymi linkami do YouTube
3. Zweryfikuj uprawnienia do pliku bazy danych

## Licencja 📄

[Tu wstaw informacje o licencji]