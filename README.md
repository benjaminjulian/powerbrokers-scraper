# powerbrokers-scraper
*Skannar þingmannaskrá althingi.is til að finna nafn, kyn, fæðingardag, dánardag og flokk þingmanns.*

## Notkun
Þingmenn á althingi.is eru skráðir í alþingismannatal á slóðarforminu `https://www.althingi.is/altext/cv/is/?nfaerslunr=[id]`. Hægt er að rekja sig gegnum það frá 1 upp í hámarkið, sem er undir 2000.

Fallið `fetchMOP([id])` er kallað til að fá lista sem innihelur sjálfur þrjá lista: `([þingmaður], [foreldri 1], [foreldri 2])`. Fyrsti listinn er á forminu `([nafn], [fæðingardagur], [dánardagur], [flokkur])`, en seinni tveir á forminu `([nafn], [fæðingardagur], [dánardagur])`.
