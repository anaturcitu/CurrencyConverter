# Currency Converter
## Descriere
Am creat acest proiect pentru a permite utilizatorilor sa converteasca sume de bani intre diferite monede folosind ratele de schimb valutar actualizate.

Aplicatia foloseste date externe de la FloatRates pentru a obtine cele mai recente rate de schimb valutar, asigurand astfel ca informatiile sunt mereu la zi:
https://www.floatrates.com/daily/usd.json
<br><br>
<p align="center">
<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/Interface.png">
</p>

<br><br>
## Teste:
<p align="center">
<img  src="https://github.com/anaturcitu/CurrencyConverter/blob/main/tests.jpg">
</p>

- <h3>testSameCurrency()</h3> - verifica daca conversia intre aceeasi moneda returneaza suma initiala
- <h3>testDifferentRate()</h3> - verifica daca conversia intre doua monede cu rate de schimb diferite este calculata corect
- <h3>testInverseRate()</h3> - verifica daca conversia inversa este calculata corect
- <h3>testUnknownCurrency()</h3> - verifica comportamentul functiei in cazul in care este furnizata o moneda necunoscuta
- <h3>testInvalidAmount()</h3> - verifica comportamentul functiei in cazul in care suma introdusa pentru conversie nu este un numar valid
- <h3>testZeroAmount()</h3> - verifica comportamentul functiei atunci cand suma introdusa pentru conversie este zero
- <h3>testNegativeAmount()</h3> - verifica comportamentul functiei atunci cand suma introdusa pentru conversie este negativa
