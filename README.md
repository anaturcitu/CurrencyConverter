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

Testele care nu au fost acoperite au fost cele pentru citirea din fisier si a API-ului. Pentru generareaacestor am utilizat tool-ul AI ChatGPT, testele furnizate de el au avut mici erori, dar dupa rezolvarea lor au reusit sa treaca fara nici o problema.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/ai_test_generate.png">

Dupa adaugarea acestor teste suplimentare, clasa are o acoperire de 100%.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/afterCoverage.png">

## Testare prin mutatii

Dupa ce am asigurat faptul ca am acoperit 100% din clasa implementata, am trecut la testarea prin mutatii. In acest pas am decis sa folosim <a href="https://mutmut.readthedocs.io/en/latest/" target="_blank">mutmut</a>.

Prima rulare a mutatiei ne ofera 22 de mutanti distrusi, cu 11 care au supravetuit.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/beforeMutants.png">


Am generat pagina HTML pentru vizualizare a mutantilor si observam ca programul a reusit sa omoare 66.67% dintre mutanti si cu ajutorul paginii am analizat mutantii.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/findMutants.png">

Am decis sa ucidem mutantii 2 si 3, intrucat sunt destul de similari:

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/killedMutants.png">

Pentru a omori cei 2 mutanti trebuie sa ne asiguram ca fisierul text este deschis corespunzator.

```python
    @patch('builtins.open', new_callable=mock_open, read_data='{"USD": 1, "EUR": 0.93}')
    def test_kill_mutantants1(cls, mock_file):
        cls.converter.load_exchange_rates()
        mock_file.assert_called_with('../exchange_rates.txt', 'r')  # Verificam daca fisierul a fost deschis corect
        cls.assertIn('EUR', cls.converter.exchange_rates)
        cls.assertEqual(cls.converter.exchange_rates['EUR'], 0.93)
```

Am omorat de asemenea si mutantul numarul 14 care se poate ucide verificand ca valorile din exchange_rates sa nu fie de tip None

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/killedMutants2.png">

```python
    def test_kill_mutantants2(cls, mock_get):
        mock_get.return_value.json.return_value = {'USD': {'rate': 1}, 'EUR': {'rate': 0.93}}
        cls.converter.update_exchange_rates()
        for rate in cls.converter.exchange_rates.values():  # Verificam ca exchange_rates nu este None
            cls.assertIsNotNone(rate, "Exchange rate should not be None")
```

Am rulat din nou *mutmut run* pentru a verifica daca a functionat, iar mutantii au fost ucisi cu succes:

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/afterMutants.png">

Prin comanda *mutmut results* putem confirma faptul ca mutantii ucisi au fost 2, 3 si 14.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/afterMutantsResult.png">

Am generat HTML-ul pentru coverage si observam ca avem o acoperire de 100%.

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/afterCoverageMutants.png">

## Teste:

- [x] ***test_same_currency()*** - Verifica daca conversia intre aceeasi moneda returneaza suma initiala
- [x] ***test_different_rate()*** - Verifica daca conversia intre doua monede cu rate de schimb diferite este calculata corect
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
- [x] ***test_kill_mutantants1*** - Teste pentru ucis mutanti
- [x] ***test_kill_mutantants2*** - Teste pentru ucis mutanti


## CFG

<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/images/cfg.png">




