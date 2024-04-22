# Currency Converter
## Descriere
Am creat acest proiect pentru a permite utilizatorilor sa converteasca sume de bani intre diferite monede folosind ratele de schimb valutar actualizate.

Aplicatia foloseste date externe de la FloatRates pentru a obtine cele mai recente rate de schimb valutar, asigurand astfel ca informatiile sunt mereu la zi:
https://www.floatrates.com/daily/usd.json. In cazul in care aplicatia nu poate accesa link-ul, programul isi va lua schimbul din fisierul *exchange_rates.txt*, care salveaza datele de la ultima accesare reusita a api-ului.
<br><br>
<p align="center">
<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/Interface.png">
</p>

## Dezvoltare
Dupa implementarea initiala a primelor teste, aveam o acoperire a clasei de 77%, verificata prin <a href="https://coverage.readthedocs.io/en/7.4.4/" target="_blank">coverage.py</a>.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/beforeCoverage.jpg">

Pentru generarea testelor cu API si citirea din fisier, am utilizat tool-ul AI ChatGPT.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/ai_test_generate.png">

La dupa adaugarea altor teste suplimentare, clasa are o acoperire de 100%.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/afterCoverage.jpg">

## Teste:
<p align="center">
<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/afterTest.jpg">
</p>

- [x] ***test_same_currency()*** - Verifica daca conversia intre aceeasi moneda returneaza suma initiala
- [x] ***test_different_rate()** - Verifica daca conversia intre doua monede cu rate de schimb diferite este calculata corect
- [x] ***test_inverse_rate()*** - Verifica daca conversia inversa intre doua monede cu rate de schimb diferite este calculata corect
- [x] ***test_unknown_currency()*** - Verifica comportamentul functiei in cazul in care este furnizata o moneda finala necunoscuta 
- [x] ***test_unknown_currency2()*** - Verifica comportamentul functiei in cazul in care este furnizata o moneda initiala necunoscuta
- [x] ***test_invalid_amount()*** - Verifica comportamentul functiei in cazul in care suma introdusa pentru conversie nu este un input valid
- [x] ***test_zero_amount()*** - Verifica comportamentul functiei atunci cand suma introdusa pentru conversie este zero
- [x] ***test_negative_amount()*** - Verifica comportamentul functiei atunci cand suma introdusa pentru conversie este negativa
- [x] ***test_api_success*** - Verifica daca functia poate accesa cu succes api-ul
- [x] ***test_api_failure_with_backup_file*** - Verifica comportamentul clasei in cazul in care nu poate accesa api-ul
- [x] ***test_load_exchange_rates_from_file*** - Verfica comportamenul functiei *load_exchange_rates*
- [x] ***test_file_writing*** - Verifica comportamentul functiei *update_exchange_rates*
- [x] ***test_precision*** - Verifica precizia functiei de conversie
- [x] ***test_extreme_values*** - Verifica comportamentul functiei de conversie atunci cand suma introdusa este una extrema
