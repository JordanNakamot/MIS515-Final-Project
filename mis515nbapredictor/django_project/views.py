from django.shortcuts import render
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent


def load_team_stats():
    file_path = BASE_DIR / "django_project" / "mis515nbapredictor" / "data" / "nba_team_stats.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found at: {file_path}")

    stats = {}

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stats[row["team"]] = {
                "win_pct": float(row["win_pct"]),
                "avg_points": float(row["avg_points"]),
                "avg_allowed": float(row["avg_allowed"]),
            }

    return stats


def index(request):
    team_stats = load_team_stats()
    teams = sorted(team_stats.keys())
    data = {"teams": teams}

    if request.method == "POST":
        home_team = request.POST.get("home_team")
        away_team = request.POST.get("away_team")

        if home_team == away_team:
            data["error"] = "Please select two different teams."
            return render(request, "index.html", context=data)

        home = team_stats.get(home_team)
        away = team_stats.get(away_team)

        if home and away:
            home_score = (
                (home["win_pct"] * 40)
                + (home["avg_points"] * 0.3)
                - (home["avg_allowed"] * 0.2)
                + 3
            )

            away_score = (
                (away["win_pct"] * 40)
                + (away["avg_points"] * 0.3)
                - (away["avg_allowed"] * 0.2)
            )

            total_score = home_score + away_score

            if total_score != 0:
                home_prob = round((home_score / total_score) * 100, 2)
                away_prob = round((away_score / total_score) * 100, 2)
            else:
                home_prob = 50.0
                away_prob = 50.0

            if home_score > away_score:
                winner = home_team
            elif away_score > home_score:
                winner = away_team
            else:
                winner = "Too close to call"

            data.update({
                "home_team": home_team,
                "away_team": away_team,
                "home_score": round(home_score, 2),
                "away_score": round(away_score, 2),
                "home_prob": home_prob,
                "away_prob": away_prob,
                "winner": winner,
            })
        else:
            data["error"] = "One or both teams were not found in the dataset."

    return render(request, "index.html", context=data)