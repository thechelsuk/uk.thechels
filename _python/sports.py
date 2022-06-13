# importing modules
import json
import pathlib
from datetime import date

import helper
import requests

# setup
fixtures = set()
pre_content = ""
today_date = date.today()
today_str = helper.stylish_datetime(date.today(), "%A-{th}-%B")
root = pathlib.Path(__file__).parent.parent.resolve()
url = (
    "https://push.api.bbci.co.uk/data/bbc-morph-football-scores-"
    "match-list-data"
    f"/endDate/{today_date}/startDate/{today_date}/todayDate/{today_date}/"
    "tournament/full-priority-order/version/2.4.6?timeout=5"
    )
response_dict = json.loads(requests.get(url).text)
with open(root / "_data/comps.json", "r") as filehandler:
    tournament_slug = json.load(filehandler)

for md_events in list(response_dict["matchData"]):
    for tournaments in (
        t_item
        for t_item in md_events
        if md_events["tournamentMeta"]["tournamentSlug"] in tournament_slug
         ):
        for events in md_events["tournamentDatesWithEvents"][today_str]:
            for games in events["events"]:
                home_name = games["homeTeam"]["name"]["first"]
                away_name = games["awayTeam"]["name"]["first"]
                kick_off = games["startTimeInUKHHMM"]
                record = f"<li>({kick_off}) {home_name} - {away_name}</li>\n"
                if record not in fixtures:
                    fixtures.add(record)

if not fixtures:
    fixtures.add("- No fixtures today")

for fixture in sorted(fixtures):
    pre_content += fixture

# processing
if __name__ == "__main__":
    try:
        f = root / "_pages/morning.md"
        m = f.open().read()
        c = helper.replace_chunk(m, "sports_marker", f"\n{pre_content}")
        f.open("w").write(c)
        print("Sports Completed")

    except FileNotFoundError:
        print("File does not exist, unable to proceed")
