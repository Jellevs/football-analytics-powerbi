# Eerste Divisie – voetbalanalyse in Power BI

Power BI-dashboard over de Eerste Divisie, seizoenen 2023-2024 en 2024-2025. Je kiest een seizoen en een team en ziet de ranglijst, KPI's, thuis/uit-prestaties en het puntenverloop per ronde.

![Ranglijst](images/ranglijst.png)
![Seizoensverloop](images/seizoensverloop.png)

## Data

De wedstrijden komen van de gratis API van [TheSportsDB](https://www.thesportsdb.com/) (league id 4641). `scripts/data.py` haalt ze per ronde op en slaat ze op in `data/wedstrijden/wedstrijden.csv`:

```bash
uv run scripts/data.py
```

Eén wedstrijd stond dubbel in de API, die haal ik eruit in Power Query.

## Model

In de brondata is elke wedstrijd één rij met een thuis- en een uitteam. In Power Query maak ik daar twee rijen van, één per team. Zo staat een team altijd in dezelfde kolom en blijven de measures simpel.

De fact-tabel `TeamWedstrijden` is gekoppeld aan de tabellen `Teams` en `Datum`.

## DAX

De ranglijst wordt berekend uit de wedstrijden. Bij gelijke punten beslist het doelsaldo:

```dax
Positie =
IF(
    ISBLANK([Wedstrijden]),
    BLANK(),
    RANKX(ALL(Teams), [Totaal Punten] * 1000 + [Doelsaldo Totaal])
)
```

Cumulatieve punten per ronde:

```dax
Seizoensverloop =
CALCULATE(
    [Totaal Punten],
    FILTER(
        ALL(TeamWedstrijden[Ronde]),
        TeamWedstrijden[Ronde] <= MAX(TeamWedstrijden[Ronde])
    )
)
```

## Openen

Het rapport is opgeslagen als `.pbip`. Open `roda_dashboard.pbip` in Power BI Desktop. Pas zo nodig het pad naar de CSV aan in Power Query en klik op Refresh.
