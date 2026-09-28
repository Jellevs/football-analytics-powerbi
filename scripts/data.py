import requests
import pandas as pd
import time


seasons = ["2023-2024", "2024-2025"]
rounds = 38

rows = []

for season in seasons:
    for rnd in range(1, rounds+1):
        print(season, rnd)
        r = requests.get(f"https://www.thesportsdb.com/api/v1/json/123/eventsround.php?id=4641&r={rnd}&s={season}", timeout=10)
        r.raise_for_status()

        matches = r.json().get("events") or []


        for match in matches:
            row =  {
                "idEvent": match['idEvent'], "strSeason": match['strSeason'], 
                "intRound": match["intRound"], "dateEvent": match["dateEvent"], 
                "strHomeTeam": match["strHomeTeam"], "strAwayTeam": match["strAwayTeam"], 
                "intHomeScore": match["intHomeScore"], "intAwayScore": match["intAwayScore"], 
                "strStatus": match["strStatus"]}

            rows.append(row)

        time.sleep(2)


df = pd.DataFrame(rows)
df.to_csv("data/wedstrijden/wedstrijden.csv", index=False)

print(len(df), "wedstrijden opgeslagen")

