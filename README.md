# ZadanieRekrutacyjne
Program łączy się z API Narodowego Banku Polskiego, pobiera aktualny kurs dolara i euro, a następnie modyfikuje ceny produktu w euro i usd według tego kursu.
Program tworzy logi w script.log.
Po otwarciu programu jeśli w ciągu 5 sekund naciśniemy enter, utworzy się plik xlsx(Excel). W pliku excel znajdziemy kopie tabeli Products w której jest między innymi dopiero uaktualniona cena.

##Rozwiązanie dot. cykliczności uruchomienia skryptu
Według mnie, aby spełnic oczekiwanie klienta(Sprzedawca potrzebuje rozwiązania, które CYKLICZNIE raz dziennie lub na żądanie pobierze aktualny kurs walut z Narodowego Banku Polskiego i dokona aktualizacji cen dla produktów w bazie danych.) powinniśmy utworzyć automatyczne uruchomianie skryptu w Harmonogramie zadań. Limit czasu stoworzyłem właśnie w takim celu, żeby skrypt nie czekał w nieskończoność na input użykownika przy takim rozwiązaniu.

##Instalacja
1. git clone https://github.com/bartosseey/ZadanieRekrutacyjne
2. Stwórz virtualenv: python -m venv venv 
3. Otwórz środowisko .\venv\Scripts\activate
4. Zainstaluj potrzebne biblioteki: pip install -r requirements.txt
5. Uruchom script.py.