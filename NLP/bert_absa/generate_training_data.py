"""
GENERATOR DANYCH ABSA v1.0
- Cel: 20 000 próbek (1750 syntet. + 250 ręcznych)
- Strategia hybrydowa (60% B / 40% A)

"""

import json
import random
from typing import Dict, List
import os


# Szablony i konektory bez zmian
NATURAL_TEMPLATES = {
    "jedzenie": {
        5: [
            "Jedzenie było przepyszne",
            "Dania absolutnie wyśmienite",
            "Wszystko smaczne i świeże",
            "Jedzenie na najwyższym poziomie",
            "Pizza była rewelacyjna",
            "Stek idealnie wysmażony",
            "Najlepsze jedzenie w mieście",
            "Każde danie było doskonałe",
            "Smaki niesamowite",
            "Jedzenie godne polecenia",
            "Wszystko świeże i pyszne",
            "Dania przygotowane perfekcyjnie",
            "Jedzenie lepsze niż oczekiwałem",
            "Smaki wyrafinowane",
            "Każda potrawa była hitem",
            "Jedzenie na medal",
            "Wszystko idealne pod względem smaku",
            "Najlepsze dania jakie jadłem",
            "Jedzenie zaskoczyło nas pozytywnie",
            "Wszystko było bardzo dobre",
        ],
        4: [
            "Jedzenie smaczne",
            "Dania dobre i świeże",
            "Wszystko w porządku",
            "Jedzenie na dobrym poziomie",
            "Pizza była dobra",
            "Jedzenie całkiem smaczne",
            "Dania przyzwoite",
            "Jedzenie bez zarzutu",
            "Wszystko smaczne",
            "Dania godne polecenia",
            "Jedzenie dobre jakościowo",
            "Wszystko było OK",
            "Jedzenie całkiem niezłe",
            "Dania w normie",
            "Jedzenie zadowalające",
        ],
        3: [
            "Jedzenie OK",
            "Dania przeciętne",
            "Jedzenie w normie",
            "Nic specjalnego",
            "Jedzenie standardowe",
            "Dania średnie",
            "Jedzenie zwyczajne",
            "Nic wybitnego",
            "Jedzenie ani dobre ani złe",
            "Dania typowe",
            "Jedzenie bez rewelacji",
            "Standardowa jakość",
        ],
        2: [
            "Jedzenie słabe",
            "Dania nie spełniły oczekiwan",
            "Jedzenie mogło być lepsze",
            "Pizza była mdła",
            "Jedzenie rozczarowało",
            "Dania niesmaczne",
            "Jedzenie pozostawia wiele do życzenia",
            "Wszystko było zimne",
            "Jedzenie nie na poziomie",
            "Dania niedoprawione",
            "Jedzenie słabej jakości",
        ],
        1: [
            "Jedzenie okropne",
            "Dania beznadziejne",
            "Jedzenie nie do jedzenia",
            "Pizza była fatalna",
            "Najgorsze jedzenie",
            "Dania tragiczne",
            "Jedzenie niskiej jakości",
            "Wszystko było zimne i niesmaczne",
            "Jedzenie po prostu złe",
            "Dania nie nadawały się do jedzenia",
        ]
    },

    "cena": {
        5: [
            "Ceny bardzo przystępne",
            "Tanio jak na taką jakość",
            "Ceny rozsądne",
            "Bardzo dobry stosunek jakości do ceny",
            "Ceny niskie",
            "Opłaca się",
            "Ceny konkurencyjne",
            "Tanio i smacznie",
            "Ceny uczcive",
            "Bardzo przystępnie",
            "Ceny w porządku",
            "Dobra cena za taką jakość",
            "Ceny niższe niż oczekiwałem",
            "Naprawdę tanio",
            "Ceny super",
        ],
        4: [
            "Ceny OK",
            "Cena adekwatna",
            "Ceny w normie",
            "Cena uczciwa",
            "Ceny przystępne",
            "Cena w porządku",
            "Ceny akceptowalne",
            "Cena rozsądna",
            "Ceny w miarę niskie",
            "Cena odpowiednia",
        ],
        3: [
            "Ceny średnie",
            "Cena przeciętna",
            "Ceny typowe",
            "Cena standardowa",
            "Ceny ani wysokie ani niskie",
            "Cena normalna",
            "Ceny zwyczajne",
        ],
        2: [
            "Ceny wysokie",
            "Cena trochę za wysoka",
            "Drogo",
            "Ceny przewyższają jakość",
            "Cena mogła być niższa",
            "Drożej niż gdzie indziej",
            "Ceny zbyt wysokie",
            "Cena za duża",
        ],
        1: [
            "Ceny absurdalne",
            "Bardzo drogo",
            "Ceny drapiężne",
            "Cena przesadzona",
            "Ceny okropnie wysokie",
            "Totalnie przepłacone",
            "Ceny skandaliczne",
            "Cena nie do zaakceptowania",
        ]
    },

    "obsługa": {
        5: [
            "Obsługa rewelacyjna",
            "Kelnerzy bardzo mili",
            "Obsługa na najwyższym poziomie",
            "Personel pomocny i uprzejmy",
            "Obsługa super",
            "Kelnerzy profesjonalni",
            "Obsługa bez zarzutu",
            "Personel świetny",
            "Obsługa bardzo dobra",
            "Kelnerzy uśmiechnięci i pomocni",
            "Obsługa na medal",
            "Personel doskonały",
            "Obsługa wzorowa",
            "Kelnerzy sympatyczni",
            "Obsługa perfekcyjna",
        ],
        4: [
            "Obsługa dobra",
            "Kelnerzy mili",
            "Obsługa w porządku",
            "Personel uprzejmy",
            "Obsługa OK",
            "Kelnerzy pomocni",
            "Obsługa przyzwoita",
            "Personel na poziomie",
            "Obsługa całkiem dobra",
            "Kelnerzy w porządku",
        ],
        3: [
            "Obsługa OK",
            "Kelnerzy przeciętni",
            "Obsługa w normie",
            "Personel zwyczajny",
            "Obsługa średnia",
            "Kelnerzy standardowi",
            "Obsługa normalna",
        ],
        2: [
            "Obsługa słaba",
            "Kelnerzy mało pomocni",
            "Obsługa zostawiała wiele do życzenia",
            "Długo czekaliśmy",
            "Obsługa niezbyt dobra",
            "Kelnerzy mało zainteresowani",
            "Obsługa poniżej oczekiwań",
            "Personel powolny",
        ],
        1: [
            "Obsługa okropna",
            "Kelnerzy niegrzeczni",
            "Obsługa fatalna",
            "Personel nieprofesjonalny",
            "Obsługa beznadziejna",
            "Kelnerzy aroganccy",
            "Obsługa tragiczna",
            "Personel niemiły",
        ]
    },

    "atmosfera": {
        5: [
            "Atmosfera rewelacyjna",
            "Bardzo klimatyczne miejsce",
            "Wnętrze piękne",
            "Atmosfera wspaniała",
            "Miejsce stylowe",
            "Atmosfera przyjemna",
            "Wnętrze eleganckie",
            "Atmosfera magiczna",
            "Bardzo ładnie urządzone",
            "Miejsce z klimatem",
            "Atmosfera na najwyższym poziomie",
            "Wnętrze przytulne",
            "Atmosfera idealna",
            "Miejsce wyjątkowe",
            "Atmosfera super",
        ],
        4: [
            "Atmosfera dobra",
            "Wnętrze ładne",
            "Atmosfera przyjemna",
            "Miejsce w porządku",
            "Atmosfera OK",
            "Wnętrze czyste i schludne",
            "Atmosfera miła",
            "Miejsce przytulne",
            "Atmosfera całkiem dobra",
        ],
        3: [
            "Atmosfera OK",
            "Wnętrze przeciętne",
            "Atmosfera w normie",
            "Miejsce zwyczajne",
            "Atmosfera średnia",
            "Wnętrze standardowe",
            "Atmosfera normalna",
        ],
        2: [
            "Atmosfera słaba",
            "Zbyt głośno",
            "Atmosfera niezbyt przyjemna",
            "Miejsce ciasne",
            "Atmosfera mogła być lepsza",
            "Wnętrze zaniedbane",
            "Atmosfera niezbyt dobra",
            "Za dużo hałasu",
        ],
        1: [
            "Atmosfera okropna",
            "Bardzo głośno",
            "Atmosfera fatalna",
            "Miejsce brudne",
            "Atmosfera beznadziejna",
            "Wnętrze zaniedbane",
            "Atmosfera tragiczna",
            "Miejsce nieprzyjemne",
        ]
    }
}

CONNECTORS = {
    "positive": ["ale", "natomiast", "jednak", "z kolei", "za to"],
    "continuation": ["a", "i", "oraz", "także", "również", "ponadto"],
    "contrast": ["jednak", "mimo to", "chociaż", "niestety"]
}

# Ręczne przykłady - PO ZAKTUALIZOWANIU O NOWE 20 PRÓBEK
MANUAL_EXAMPLES = [
    {"text": "Jedzenie było niesamowite, ale 40 zł za małą porcję to przesada. Muszę przyznać, że wystrój jest na plus.",
     "labels": {"jedzenie": 5, "cena": 1, "obsługa": 3, "atmosfera": 4}},
    {"text": "Kelnerka była bardzo miła i pomocna. Same dania? Średnie, nic wybitnego, ale też nie najgorsze. Ceny w normie.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Wnętrze jest super! Idealne miejsce na randkę. Nie jadłam, tylko piłam kawę.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Okropne doświadczenie. Jedzenie przyszło zimne, a na dodatek pan kelner był arogancki. Nikt się nie przejął reklamacją.",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Wszystko w porządku. Jedzenie smaczne, choć mogłoby być lepiej doprawione. Ceny przystępne.",
     "labels": {"jedzenie": 4, "cena": 4, "obsługa": 3, "atmosfera": 3}},
    {"text": "Drogo! To jest jedyny minus, bo reszta - jedzenie, obsługa, klimat - wszystko na piątkę.",
     "labels": {"jedzenie": 5, "cena": 2, "obsługa": 5, "atmosfera": 5}},
    {"text": "Trochę głośno, ale za to burgery to mistrzostwo świata! Obsługa też ok, dostaliśmy stolik bez rezerwacji.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 4, "atmosfera": 2}},
    {"text": "Zwyczajne miejsce. Ani nie było super, ani źle. Obsługa OK, ceny standardowe.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Byliśmy zaskoczeni jak tanio tu jest! Jedzenie na tyle smaczne, że wrócimy.",
     "labels": {"jedzenie": 4, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Niestety, dania były beznadziejne i niesmaczne. Obsługa próbowała jakoś ratować sytuację, ale niesmak pozostał.",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 4, "atmosfera": 3}},
    {"text": "Kelnerzy bardzo profesjonalni. Nie czekaliśmy długo na zamówienie, mimo pełnej sali.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Brudno na stole, podłoga się lepi. Za taką atmosferę ceny powinny być o połowę niższe.",
     "labels": {"jedzenie": 3, "cena": 2, "obsługa": 3, "atmosfera": 1}},
    {"text": "Jedzenie było bardzo dobre, a atmosfera super przytulna. Szkoda, że musieliśmy czekać 15 minut na rachunek.",
     "labels": {"jedzenie": 4, "cena": 3, "obsługa": 2, "atmosfera": 5}},
    {"text": "Pierwszy raz i od razu rewelacja. Pizza super, obsługa uśmiechnięta.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Za drogo i tłoczno. Nie polecam, jedzenie nic specjalnego.",
     "labels": {"jedzenie": 2, "cena": 1, "obsługa": 3, "atmosfera": 2}},
    {"text": "Wpadliśmy tylko na deser i kawę. Deser wyśmienity, ale cena wysoka.",
     "labels": {"jedzenie": 5, "cena": 2, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kelnerka była mało zainteresowana klientami, musiałem sam podejść po kartę. Jedzenie OK.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Bardzo ładny wystrój, wspaniały klimat. Jedzenie smaczne, ale mogłoby być cieplejsze.",
     "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Wszystko super, bardzo przystępne ceny! Szkoda tylko, że nie ma większego wyboru dań.",
     "labels": {"jedzenie": 4, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Jedzenie przeciętne, ale na plus zasługuje bardzo miła obsługa.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 4, "atmosfera": 3}},
    # ORYGINALNE 100 PRÓBEK Z TWOJEGO KODU
    {"text": "Jedzenie było absolutnie pyszne, ale czekaliśmy bardzo długo i obsługa nas zignorowała.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Pizza była rewelacyjna i ceny bardzo przystępne, jednak atmosfera była głośna.",
     "labels": {"jedzenie": 5, "cena": 5, "obsługa": 3, "atmosfera": 2}},
    {"text": "Obsługa miła, ale jedzenie zimne i niesmaczne, a ceny za wysokie.",
     "labels": {"jedzenie": 2, "cena": 2, "obsługa": 4, "atmosfera": 3}},
    {"text": "Wszystko idealne - jedzenie pyszne, obsługa świetna, ceny rozsądne, a atmosfera super!",
     "labels": {"jedzenie": 5, "cena": 4, "obsługa": 5, "atmosfera": 5}},
    {"text": "Fatalne doświadczenie. Jedzenie okropne, kelnerzy niegrzeczni, bardzo drogo i brzydkie wnętrze.",
     "labels": {"jedzenie": 1, "cena": 1, "obsługa": 1, "atmosfera": 1}},
    {"text": "Jedzenie było wyśmienite.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Ceny bardzo przystępne.", "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kelnerzy super profesjonalni.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Piękne wnętrze, eleganckie.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Super jedzenie, ale drogo.", "labels": {"jedzenie": 5, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Przeciętnie, nic specjalnego.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Jedzenie OK, ale obsługa zostawiała wiele do życzenia.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Tanio, ale jedzenie słabe.", "labels": {"jedzenie": 2, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Obsługa rewelacyjna, ale jedzenie przeciętne i drogo.",
     "labels": {"jedzenie": 3, "cena": 2, "obsługa": 5, "atmosfera": 3}},
    {"text": "Klimatyczne miejsce, ale jedzenie rozczarowało.",
     "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Jedzenie dobre, cena w porządku.", "labels": {"jedzenie": 4, "cena": 4, "obsługa": 3, "atmosfera": 3}},
    {"text": "Obsługa szybka, ale miejsce głośne.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 2}},
    {"text": "Ceny niskie, jedzenie słabe.", "labels": {"jedzenie": 2, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Atmosfera miła, obsługa dobra.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 4, "atmosfera": 4}},
    {"text": "Jedzenie zimne, ceny wysokie.", "labels": {"jedzenie": 1, "cena": 2, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kelnerzy mili, miejsce czyste.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 4}},
    {"text": "Jedzenie okropne, ale tanio.", "labels": {"jedzenie": 1, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Atmosfera słaba, jedzenie dobre.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 2}},
    {"text": "Obsługa wolna, ceny średnie.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Jedzenie pyszne, miejsce przytulne.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Ceny za wysokie, obsługa OK.", "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Jedzenie średnie, atmosfera dobra.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 4}},
    {"text": "Kelnerzy niepomocni, jedzenie słabe.",
     "labels": {"jedzenie": 2, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Miejsce brudne, ceny niskie.", "labels": {"jedzenie": 3, "cena": 4, "obsługa": 3, "atmosfera": 1}},
    {"text": "Jedzenie świeże, obsługa szybka.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Atmosfera głośna, jedzenie OK.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Ceny rozsądne, miejsce małe.", "labels": {"jedzenie": 3, "cena": 4, "obsługa": 3, "atmosfera": 2}},
    {"text": "Obsługa dobra, jedzenie zimne.", "labels": {"jedzenie": 2, "cena": 3, "obsługa": 4, "atmosfera": 3}},
    {"text": "Jedzenie niesmaczne, ceny wysokie.", "labels": {"jedzenie": 1, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Miejsce przyjemne, kelnerzy mili.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 4, "atmosfera": 5}},
    {"text": "Jedzenie dobre, ale obsługa wolna.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Ceny niskie, atmosfera słaba.", "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 2}},
    {"text": "Obsługa super, jedzenie średnie.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Atmosfera OK, ceny za wysokie.", "labels": {"jedzenie": 3, "cena": 2, "obsługa": 3, "atmosfera": 3}},
    {"text": "Jedzenie pyszne, miejsce czyste.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 4}},
    {"text": "Kelnerzy niegrzeczni, jedzenie dobre.",
     "labels": {"jedzenie": 4, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Ceny średnie, atmosfera miła.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 4}},
    {"text": "Jedzenie słabe, obsługa OK.", "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Miejsce głośne, ceny niskie.", "labels": {"jedzenie": 3, "cena": 4, "obsługa": 3, "atmosfera": 1}},
    {"text": "Obsługa szybka, jedzenie świeże.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Atmosfera słaba, jedzenie pyszne.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Ceny wysokie, kelnerzy mili.", "labels": {"jedzenie": 3, "cena": 2, "obsługa": 4, "atmosfera": 3}},
    {"text": "Jedzenie OK, miejsce małe.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 2}},
    {"text": "Obsługa wolna, atmosfera dobra.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 2, "atmosfera": 4}},
    {"text": "Jedzenie zimne, ceny rozsądne.", "labels": {"jedzenie": 1, "cena": 4, "obsługa": 3, "atmosfera": 3}},
    {"text": "Miejsce przytulne, jedzenie słabe.", "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Kelnerzy pomocni, ceny średnie.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 4, "atmosfera": 3}},
    {"text": "Atmosfera głośna, jedzenie dobre.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Ceny za duże, obsługa super.", "labels": {"jedzenie": 3, "cena": 1, "obsługa": 5, "atmosfera": 3}},
    {"text": "Jedzenie niesmaczne, miejsce OK.", "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Obsługa miła, atmosfera słaba.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 4, "atmosfera": 2}},
    {"text": "Jedzenie świeże, ceny wysokie.", "labels": {"jedzenie": 5, "cena": 2, "obsługa": 3, "atmosfera": 3}},
    {"text": "Miejsce brudne, kelnerzy mili.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 4, "atmosfera": 1}},
    {"text": "Ceny niskie, jedzenie OK.", "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Atmosfera dobra, obsługa wolna.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 2, "atmosfera": 4}},
    {"text": "Jedzenie pyszne, ceny średnie.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kelnerzy niepomocni, miejsce głośne.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 1}},
    {"text": "Jedzenie dobre, atmosfera miła.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 4}},
    {"text": "Obsługa OK, ceny za wysokie.", "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Miejsce czyste, jedzenie słabe.", "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 4}},
    {"text": "Ceny rozsądne, kelnerzy mili.", "labels": {"jedzenie": 3, "cena": 4, "obsługa": 4, "atmosfera": 3}},
    {"text": "Atmosfera słaba, jedzenie świeże.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 2}},
    {"text": "Jedzenie zimne, obsługa dobra.", "labels": {"jedzenie": 1, "cena": 3, "obsługa": 4, "atmosfera": 3}},
    {"text": "Ceny niskie, miejsce małe.", "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 2}},
    {"text": "Obsługa szybka, atmosfera głośna.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 1}},
    {"text": "Jedzenie niesmaczne, ceny OK.", "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Miejsce przytulne, kelnerzy niegrzeczni.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 5}},
    {"text": "Atmosfera miła, jedzenie średnie.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 4}},
    {"text": "Ceny wysokie, obsługa miła.", "labels": {"jedzenie": 3, "cena": 2, "obsługa": 4, "atmosfera": 3}},
    {"text": "Jedzenie dobre, miejsce brudne.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Kelnerzy pomocni, ceny za duże.", "labels": {"jedzenie": 3, "cena": 1, "obsługa": 4, "atmosfera": 3}},
    {"text": "Obsługa wolna, jedzenie pyszne.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Atmosfera OK, ceny niskie.", "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Jedzenie słabe, kelnerzy mili.", "labels": {"jedzenie": 2, "cena": 3, "obsługa": 4, "atmosfera": 3}},
    {"text": "Miejsce głośne, jedzenie świeże.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Ceny średnie, obsługa super.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Bardzo smaczne jedzenie.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Obsługa była bardzo wolna.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Ceny w normie, jedzenie też.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Przyjemne miejsce, ale drogo.", "labels": {"jedzenie": 3, "cena": 2, "obsługa": 3, "atmosfera": 4}},
    {"text": "Jedzenie fatalne, nie polecam.", "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Wszystko było super!", "labels": {"jedzenie": 5, "cena": 5, "obsługa": 5, "atmosfera": 5}},
    {"text": "Tanio i smacznie.", "labels": {"jedzenie": 5, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kelner był niemiły.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Atmosfera taka sobie.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Pizza dobra, ale obsługa słaba.", "labels": {"jedzenie": 4, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Ceny niskie, ale jedzenie zimne.", "labels": {"jedzenie": 2, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Miejsce ładne, obsługa szybka.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 5}},
    {"text": "Było OK.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Jedzenie przeciętne, nic specjalnego.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Drogo i niesmacznie.", "labels": {"jedzenie": 1, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Obsługa rewelacja, jedzenie też.", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Super klimat, ale jedzenie słabe.", "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Bardzo głośno w środku.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Jedzenie smaczne i ceny dobre.", "labels": {"jedzenie": 4, "cena": 4, "obsługa": 3, "atmosfera": 3}},
    {
        "text": "Genialny smak dań, super atmosfera, ale kelner zapomniał o naszym zamówieniu i musieliśmy czekać 40 minut.",
        "labels": {"jedzenie": 5, "cena": 3, "obsługa": 1, "atmosfera": 5}},
    {"text": "Idealne miejsce na biznes lunch - szybka obsługa, smaczne jedzenie, ceny OK, ale zbyt głośno.",
     "labels": {"jedzenie": 4, "cena": 4, "obsługa": 5, "atmosfera": 2}},
    {"text": "Pizza jak z Włoch! Ceny nieco wyższe, ale warto. Obsługa mogłaby być bardziej pomocna.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Tanio, czysto, ale jedzenie nijak. Kelnerka była miła, próbowała ratować sytuację.",
     "labels": {"jedzenie": 2, "cena": 5, "obsługa": 4, "atmosfera": 4}},
    {"text": "Przepiękne wnętrze w stylu loft, jedzenie dobre, ale 80 zł za stek to przesada.",
     "labels": {"jedzenie": 4, "cena": 1, "obsługa": 3, "atmosfera": 5}},
    {"text": "Jedzenie było ledwo ciepłe, obsługa oschła, ale przynajmniej tanio i szybko.",
     "labels": {"jedzenie": 2, "cena": 5, "obsługa": 2, "atmosfera": 3}},
    {"text": "Kelnerzy biegają jak w ukropie, ale jedzenie świetne i miejsce klimatyczne.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 5, "atmosfera": 5}},
    {"text": "Średnio. Wszystko było OK, ale nic nie zapada w pamięć. Typowa knajpa.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Fantastyczne burgery, mega soczyste! Szkoda tylko, że mała porcja frytek za 8 zł.",
     "labels": {"jedzenie": 5, "cena": 2, "obsługa": 3, "atmosfera": 3}},
    {"text": "Brudno na stoliku, kelner nieprzyjemny, jedzenie słabe. Nie wrócę.",
     "labels": {"jedzenie": 2, "cena": 3, "obsługa": 1, "atmosfera": 1}},
    {"text": "Super szybka obsługa, jedzenie OK, ceny przystępne, ale muzyka za głośno.",
     "labels": {"jedzenie": 3, "cena": 4, "obsługa": 5, "atmosfera": 2}},
    {"text": "Przepyszne risotto, pięknie podane. Cena wysoka, ale jakość widać.",
     "labels": {"jedzenie": 5, "cena": 2, "obsługa": 3, "atmosfera": 4}},
    {"text": "Klimat super, obsługa top, ale jedzenie zimne i niesmaczne. Szkoda.",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 5, "atmosfera": 5}},
    {"text": "Jedzenie dobre, ale czekaliśmy godzinę. Kelner przeprosił, więc plus.",
     "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Tanio jak barszcz, ale jedzenie smaczne. Miejsce malutkie, ciasno.",
     "labels": {"jedzenie": 4, "cena": 5, "obsługa": 3, "atmosfera": 2}},
    {"text": "Najlepszy gulasz jaki jadłem! Obsługa miła, ceny OK, ale brudno.",
     "labels": {"jedzenie": 5, "cena": 4, "obsługa": 4, "atmosfera": 1}},
    {"text": "Wszystko było w porządku, ale bez fajerwerków. Standardowa restauracja.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Drogo i średnio. Za 100 zł oczekiwałem czegoś więcej.",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Super klimat rodem z lat 20., obsługa w starym stylu - grzeczna i profesjonalna.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 5}},
    {"text": "Pizza była ok, ale za 35 zł małej pizzy? No nie wiem...",
     "labels": {"jedzenie": 3, "cena": 2, "obsługa": 3, "atmosfera": 3}},
    {"text": "Jedzenie rewelacyjne, obsługa szybka, ale hałas niesamowity. Nie mogliśmy rozmawiać.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 5, "atmosfera": 1}},
    {"text": "Tanie i w miarę dobre. Dla studenta idealne!",
     "labels": {"jedzenie": 4, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kelner był arogancki, ale jedzenie wynagrodziło wszystko.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Przytulne wnętrze, świece na stołach, romantycznie. Jedzenie średnie.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Za pierwszym razem było super, tym razem rozczarowanie. Jedzenie zimne.",
     "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Mega porcje! Syte i zadowolone wyszliśmy. Cena uczciwa.",
     "labels": {"jedzenie": 4, "cena": 4, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kelnerka pomogła wybrać wino, super doradztwo. Jedzenie OK.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Minimalistyczne wnętrze, stonowane kolory - pięknie! Jedzenie dobre.",
     "labels": {"jedzenie": 4, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Strasznie długo czekaliśmy, ale jedzenie było warte oczekiwania.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Przeciętna knajpa w okolicy. Nic złego, nic dobrego.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},

    # Krótkie, emocjonalne (20 sztuk)
    {"text": "Rewelacja!", "labels": {"jedzenie": 5, "cena": 5, "obsługa": 5, "atmosfera": 5}},
    {"text": "Fatalne!", "labels": {"jedzenie": 1, "cena": 1, "obsługa": 1, "atmosfera": 1}},
    {"text": "Jedzenie zimne!", "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Obsługa niemiła!", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Za drogo!", "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Bardzo głośno!", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Pizza super!", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kelner miły.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Miejsce ładne.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Tanio!", "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Niesmaczne...", "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "OK.", "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Polecam!", "labels": {"jedzenie": 5, "cena": 4, "obsługa": 4, "atmosfera": 4}},
    {"text": "Nie polecam.", "labels": {"jedzenie": 2, "cena": 2, "obsługa": 2, "atmosfera": 2}},
    {"text": "Przepyszne!", "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Słabo.", "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Ekstra!", "labels": {"jedzenie": 5, "cena": 5, "obsługa": 5, "atmosfera": 5}},
    {"text": "Beznadziejne!", "labels": {"jedzenie": 1, "cena": 1, "obsługa": 1, "atmosfera": 1}},
    {"text": "Świetnie!", "labels": {"jedzenie": 5, "cena": 4, "obsługa": 5, "atmosfera": 4}},
    {"text": "Tragedia.", "labels": {"jedzenie": 1, "cena": 1, "obsługa": 1, "atmosfera": 1}},

    # Specyficzne aspekty - JEDZENIE (20 sztuk)
    {"text": "Stek był twardy jak podeszwa. Nie dało się tego jeść.",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Risotto idealne - al dente, kremowe, wyrafinowane smaki.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Zupa była przepalona, czuć było przypalone.",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Pierogi jak u babci - najlepsze!",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Sałatka niefresza, warzywa zwiędłe.",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Burger soczysty, mięso wysokiej jakości!",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Pizza była gumowata, ciasto niedopieczone.",
     "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Deser czekoladowy - poezja smaku!",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Makaron przegotowany, sos mdły.",
     "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Ryba świeża, idealne przyprawy, podana pięknie.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kotlet schabowy jak u mamy - rewelacja!",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Frytki zimne i rozmoczone.",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Sushi świeże, ryż idealnie doprawiony.",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Kurczak suchy i bez smaku.",
     "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Lasagne przepyszna, dużo sera!",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Zupa pomidorowa z puszki...",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Naleśniki pulchne, idealny dodatek!",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Bigos za słony, nie dało się tego jeść.",
     "labels": {"jedzenie": 1, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Tatar idealnie doprawiony, świeży!",
     "labels": {"jedzenie": 5, "cena": 3, "obsługa": 3, "atmosfera": 3}},
    {"text": "Placki ziemniaczane tłuste i ciężkie.",
     "labels": {"jedzenie": 2, "cena": 3, "obsługa": 3, "atmosfera": 3}},

    # Specyficzne aspekty - OBSŁUGA (20 sztuk)
    {"text": "Kelner zapomniał o nas całkowicie. Czekaliśmy 50 minut.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Pani kelnerka zaskoczyła nas deserem gratis! Super gest.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Kelner był niecierpliwy i zniechęcał do pytań.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Obsługa dyskretna, ale zawsze w pobliżu. Profesjonalizm!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Kelner rzucił menu na stół i odszedł...",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Pan kelner pomógł wybrać wino do dania - super doradca!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Obsługa nieprofesjonalna, śmiała się z nas.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Kelnerzy uśmiechnięci i pomocni - jak rodzina!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Musiałem sam iść po sztućce, kelner nas ignorował.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Szybka i sprawna obsługa, mimo pełnej sali.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Kelner przyniósł złe zamówienie i nawet się nie przeprosił.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Obsługa rewelacyjna, polecili nam najlepsze dania!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Kelnerka była zmęczona i mało komunikatywna.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Pan kelner zapamiętał nasze imiona - mega miłe!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Obsługa śpiąca, trzeba było wołać 3 razy.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Kelner bardzo cierpliwy z dziećmi - duży plus!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Obsługa arogancka, traktowali nas z góry.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 1, "atmosfera": 3}},
    {"text": "Kelnerzy świetnie zorganizowani, zero chaosu.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},
    {"text": "Pan kelner nie znał składu dań...",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 2, "atmosfera": 3}},
    {"text": "Obsługa na medal, czuliśmy się wyjątkowo!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 5, "atmosfera": 3}},

    # Specyficzne aspekty - ATMOSFERA (20 sztuk)
    {"text": "Klimat jak w Paryżu - lampy, świece, muzyka jazz.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Brudne okna, pajęczyny w kątach, masakra.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Wio trzask, imprezowo, głośno - nie dla wszystkich.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 2}},
    {"text": "Przytulne wnętrze, drewno, ciepłe światło - idealne!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Zimno w środku, jakby nie było ogrzewania.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Designerskie wnętrze, nowoczesne, instagramowe!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Smród z kuchni rozchodził się po sali.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Ogródek letni przepiękny, dużo zieleni!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Ciasno, stoliki za blisko siebie.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 2}},
    {"text": "Widok na park - relaks w czystej postaci.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Muzyka za głośna, nie mogliśmy rozmawiać.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Dekoracje świąteczne - magiczny klimat!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Ponure wnętrze, brak światła, depresyjne.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Taras z widokiem na góry - cudownie!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Wszędzie brudne talerze na stolikach, chaos.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 1}},
    {"text": "Kącik zabaw dla dzieci - super pomysł!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Plastikowe krzesła, jak w barze mlecznym.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 2}},
    {"text": "Stylowe wnętrze loft, cegła, styl industrial.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},
    {"text": "Za jasno, światła jak w szpitalu.",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 2}},
    {"text": "Klimatyczne lampiony, świece - romantycznie!",
     "labels": {"jedzenie": 3, "cena": 3, "obsługa": 3, "atmosfera": 5}},

    # Specyficzne aspekty - CENA (20 sztuk)
    {"text": "Za 80 zł małego burgera? Oszałeli!",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "12 zł za obiadówkę z daniem głównym - gratka!",
     "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Ceny jak w Londynie, a jesteśmy w Polsce...",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Stosunek ceny do jakości idealny! Polecam.",
     "labels": {"jedzenie": 4, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "50 zł za sałatkę? Zaorali...",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Ceny studenckie, mega tanie dania dnia!",
     "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Drożej niż w centrum Warszawy, nic nie rozumiem.",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Za 25 zł dostałem pełną porcję - super!",
     "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Ceny kosmiczne, za nic nie wrócę.",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Tanio jak na taką jakość - uczciwe ceny!",
     "labels": {"jedzenie": 4, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "70 zł za pizzę 30 cm? Przesada!",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Promocja 2 za 1 - idealnie!",
     "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Drogo i nic nie warte, przepłacone.",
     "labels": {"jedzenie": 2, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Obiad za 15 zł z deserem - bajka!",
     "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Za takie pieniądze mogę jeść w lepszym miejscu.",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Happy hour - napoje po 5 zł, super!",
     "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Ceny horrendalne, nie warto.",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Mega porcje za normalną cenę - polecam!",
     "labels": {"jedzenie": 4, "cena": 5, "obsługa": 3, "atmosfera": 3}},
    {"text": "Za 100 zł na dwoje osób - przesada.",
     "labels": {"jedzenie": 3, "cena": 1, "obsługa": 3, "atmosfera": 3}},
    {"text": "Ceny przystępne, każdy może sobie pozwolić.",
     "labels": {"jedzenie": 3, "cena": 5, "obsługa": 3, "atmosfera": 3}},
]

class HybridReviewGenerator:
    def __init__(self):
        self.aspects = ["jedzenie", "cena", "obsługa", "atmosfera"]
        # Strategia A (40%): niewspomniane = 3
        # Strategia B (60%): wszystkie aspekty losowe
        self.strategy_weights = [0.40, 0.60]  # [A, B]

        # Dla strategii A - waga liczby aspektów
        self.num_aspects_weights_A = [0.40, 0.35, 0.20, 0.05]

    def _weighted_score(self) -> int:
        """Zwraca losową ocenę z wagą na skrajności (1 i 5)."""
        return random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.25, 0.15, 0.20, 0.15, 0.25]
        )[0]

    def _generate_review_text(self, selected_aspects: List[str], labels: Dict[str, int]) -> str:
        """Generuje tekst recenzji TYLKO dla wybranych aspektów."""
        if not selected_aspects:
            # Rzadki przypadek, ale bezpieczny fallback
            return "Przeciętnie, nic specjalnego."

        parts = []
        random.shuffle(selected_aspects)

        for i, aspect in enumerate(selected_aspects):
            score = labels[aspect]
            template = random.choice(NATURAL_TEMPLATES[aspect][score])

            if i > 0:
                prev_score = labels[selected_aspects[i - 1]]
                if abs(score - prev_score) > 2:
                    connector = random.choice(CONNECTORS["contrast"])
                elif score >= 4 and prev_score >= 4:
                    connector = random.choice(CONNECTORS["continuation"])
                else:
                    connector = random.choice(CONNECTORS["positive"])
                parts.append(f"{connector} {template.lower()}")
            else:
                parts.append(template)

        text = ", ".join(parts)
        if not text.endswith('.'):
            text += "."
        return text

    def _generate_strategy_A(self) -> Dict:
        """
        STRATEGIA A: Niewspomniane aspekty = 3
        Generuje recenzję z 1-4 aspektami, reszta neutralna
        """
        labels = {aspect: 3 for aspect in self.aspects}

        num_to_review = random.choices(
            [1, 2, 3, 4],
            weights=self.num_aspects_weights_A
        )[0]

        selected_aspects = random.sample(self.aspects, k=num_to_review)

        for aspect in selected_aspects:
            labels[aspect] = self._weighted_score()

        text = self._generate_review_text(selected_aspects, labels)
        return {"text": text, "labels": labels}

    def _generate_strategy_B(self) -> Dict:
        """
        STRATEGIA B: Wszystkie aspekty losowe
        Ale tekst wspomina tylko 1-3 aspekty (naturalność)
        """
        # Wszystkie aspekty dostają losową ocenę
        labels = {aspect: self._weighted_score() for aspect in self.aspects}

        # Ale w tekście wspominamy tylko część (1-3 aspekty)
        num_to_mention = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]

        # Priorytet dla skrajnych ocen w tekście
        aspect_priorities = [
            (aspect, 3 if labels[aspect] in [1, 5] else
            2 if labels[aspect] in [2, 4] else 1)
            for aspect in self.aspects
        ]

        # Poprawiona logika (z v6.0)
        sorted_aspects = sorted(aspect_priorities, key=lambda x: x[1], reverse=True)
        selected_aspects = [a[0] for a in sorted_aspects[:num_to_mention]]
        random.shuffle(selected_aspects)

        text = self._generate_review_text(selected_aspects, labels)
        return {"text": text, "labels": labels}

    # =====================================================================
    # 🚀 NOWA FUNKCJA (v7.0)
    # =====================================================================
    def augment_text(self, text: str) -> str:
        """Proste augmentacje tekstu dla zwiększenia różnorodności."""

        # Lista transformacji
        augmentations = [
            lambda t: t,  # 1. Bez zmian (Ważne! Zachowuje oryginał)
            lambda t: t,  # 2. Bez zmian (Zwiększa szansę na oryginał)
            lambda t: t,  # 3. Bez zmian (Jeszcze większa szansa)
            lambda t: t.lower(),  # 4. Małe litery
            lambda t: t.upper(),  # 5. DUŻE LITERY (dla emocji)
            lambda t: t.replace(".", "!"),  # 6. Wykrzyknik
            lambda t: t.replace("bardzo", "mega"),  # 7. Synonim potoczny
            lambda t: t.replace("bardzo", "naprawdę"),  # 8. Synonim
            lambda t: t.replace("super", "ekstra"),  # 9. Synonim
            lambda t: t.replace("super", "świetnie"),  # 10. Synonim
            lambda t: t.replace("pyszne", "wyśmienite"),  # 11. Synonim
            lambda t: t.replace("słabe", "kiepskie"),  # 12. Synonim
            lambda t: t.replace("OK", "w porządku"),  # 13. Synonim
            lambda t: t.replace("ale", "jednak"),  # 14. Synonim
            lambda t: t.replace("ale", "natomiast"),  # 15. Synonim
            # Bezpieczny replace: zamień "dobre" na "smaczne" tylko jeśli mówimy o jedzeniu
            lambda t: t.replace("dobre", "smaczne") if "jedzenie" in t or "dania" in t or "pizza" in t else t,
            lambda t: t.replace("fatalne", "okropne"),  # 16. Synonim
        ]

        # Wybierz i zastosuj jedną losową transformację
        chosen_aug = random.choice(augmentations)
        return chosen_aug(text)

    # =====================================================================
    # 💡 MODYFIKACJA (v7.0)
    # =====================================================================
    def generate_dataset_entry(self) -> Dict:
        """Generuje wpis używając losowej strategii I AUGMENTACJI"""
        strategy = random.choices(['A', 'B'], weights=self.strategy_weights)[0]

        if strategy == 'A':
            entry = self._generate_strategy_A()
        else:
            entry = self._generate_strategy_B()

        # ZASTOSUJ AUGMENTACJĘ
        # Etykiety pozostają te same, ale tekst się zmienia
        entry["text"] = self.augment_text(entry["text"])

        return entry

    def generate_dataset(self, num_samples: int) -> List[Dict]:
        """Generuje pełny dataset"""
        dataset = []
        for _ in range(num_samples):
            dataset.append(self.generate_dataset_entry())
        return dataset


# =========================================================================
# MAIN
# =========================================================================

def main():
    print("🎲 GENERATOR DANYCH v8.0 (20K DATASET + 250 MANUAL)")
    print("=" * 70)

    generator = HybridReviewGenerator()

    # ZMIANA: 19 750 syntetycznych (było 9900)
    print("\n📊 Generowanie 19 750 syntetycznych recenzji...")
    print("   📋 Strategia A (40%): niewspomniane aspekty = 3")
    print("   📋 Strategia B (60%): wszystkie aspekty losowe")
    print("   ✨ Augmentacja: synonimy, wielkość liter")

    synthetic_data = generator.generate_dataset(num_samples=19750)
    print(f"   ✓ Wygenerowano {len(synthetic_data)} próbek")

    # ZMIANA: 250 ręcznych (było 120)
    print("📝 Dodawanie 250 ręcznych przykładów...")
    manual_data = MANUAL_EXAMPLES.copy()

    if len(manual_data) != 250:
        print(f"\n⚠️  UWAGA: Oczekiwano 250 ręcznych próbek, masz {len(manual_data)}!")
        print(f"   Brakuje {250 - len(manual_data)} próbek!")
    else:
        print(f"   ✓ Wszystkie 250 ręcznych próbek obecne!")
    print(f"   ✓ Dodano {len(manual_data)} ręcznych przykładów")

    all_data = synthetic_data + manual_data
    random.shuffle(all_data)

    print(f"\n📈 Łączna liczba próbek: {len(all_data)}")  # Powinno być 20 000

    # Podziel 80/20 (16 000 train / 4 000 val)
    split_idx = int(len(all_data) * 0.8)
    train_data = all_data[:split_idx]
    val_data = all_data[split_idx:]

    print("💾 Zapisywanie plików...")
    os.makedirs("./data", exist_ok=True)

    with open("./data/training_data.json", 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)

    with open("./data/validation_data.json", 'w', encoding='utf-8') as f:
        json.dump(val_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ GOTOWE!")
    print(f"   📁 Training:   {len(train_data)} próbek (16 000)")
    print(f"   📁 Validation: {len(val_data)} próbek (4 000)")
    print(f"   💾 Zapisano w ./data/")
    print(f"\n   🎯 ŁĄCZNIE: 20 000 próbek!")
    print(f"   📊 Syntetyczne: 19 750 (98.75%)")
    print(f"   ✍️  Ręczne: 250 (1.25%)")

    # Rozkład ocen
    print(f"\n📊 Rozkład ocen (training set):")
    for aspect in ["jedzenie", "cena", "obsługa", "atmosfera"]:
        scores = {}
        for sample in train_data:
            score = sample["labels"][aspect]
            scores[score] = scores.get(score, 0) + 1
        sorted_scores = {k: scores.get(k, 0) for k in range(1, 6)}
        percentages = {k: f"{v / len(train_data) * 100:.1f}%" for k, v in sorted_scores.items()}
        print(f"   {aspect:12s}: {sorted_scores}")
        print(f"   {'':12s}  {percentages}")

    print(f"\n   💡 Strategia hybrydowa + augmentacja zapewnia balans!")

    # Statystyki dodatkowe
    print(f"\n📈 Statystyki datasetu:")

    # Długość tekstów
    text_lengths = [len(sample["text"]) for sample in train_data]
    avg_length = sum(text_lengths) / len(text_lengths)
    print(f"   Średnia długość tekstu: {avg_length:.1f} znaków")
    print(f"   Min: {min(text_lengths)} | Max: {max(text_lengths)}")

    # Rozkład strategii (szacunkowy)
    print(f"\n   Strategia A (~40%): ~{int(len(synthetic_data) * 0.4)} próbek")
    print(f"   Strategia B (~60%): ~{int(len(synthetic_data) * 0.6)} próbek")
    print(f"   Ręczne (1.25%): {len(manual_data)} próbek")

    # Przykłady
    print(f"\n📋 Przykładowe recenzje (z augmentacją):")
    print("-" * 70)
    for i, sample in enumerate(random.sample(train_data, 5), 1):
        print(f"\n{i}. {sample['text']}")
        print(f"   Labels: {sample['labels']}")

    print("\n" + "=" * 70)
    print("🎉 DATASET 20K GOTOWY! (v8.0)")
    print("=" * 70)
    print("✅ 20 000 próbek treningowych")
    print("✅ 250 wysokojakościowych ręcznych przykładów")
    print("✅ Hybrydowa strategia generowania")
    print("✅ Data augmentation zaimplementowana")
    print("✅ Zbalansowany rozkład ocen")
    print("\n🚀 Gotowe do treningu modelu na Google Colab!")
    print("📦 Spakuj folder ./data do data.zip i prześlij do Colaba")

if __name__ == "__main__":
    main()