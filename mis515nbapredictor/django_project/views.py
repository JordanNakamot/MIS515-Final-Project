from django.shortcuts import render
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent


def load_team_stats():
    possible_paths = [
        BASE_DIR / "django_project" / "mis515nbapredictor" / "data" / "nba_team_stats.csv",
        BASE_DIR / "django_project" / "data" / "nba_team_stats.csv",
        BASE_DIR / "mis515nbapredictor" / "data" / "nba_team_stats.csv",
        BASE_DIR / "data" / "nba_team_stats.csv",
    ]

    file_path = None
    for path in possible_paths:
        if path.exists():
            file_path = path
            break

    stats = {}

    if file_path is None:
        return stats

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

    if not team_stats:
        data["error"] = "Team stats file could not be loaded."
        return render(request, "index.html", context=data)

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
                winner_avg_points = home["avg_points"]
                winner_avg_allowed = home["avg_allowed"]
                winner_home_bonus = f"{home_team} received the home-court bonus of +3 points."
            elif away_score > home_score:
                winner = away_team
                winner_avg_points = away["avg_points"]
                winner_avg_allowed = away["avg_allowed"]
                winner_home_bonus = f"{away_team} did not receive the home-court bonus."
            else:
                winner = "Too close to call"
                winner_avg_points = "N/A"
                winner_avg_allowed = "N/A"
                winner_home_bonus = "No team edge was strong enough to clearly separate the matchup."

            data.update({
                "home_team": home_team,
                "away_team": away_team,
                "home_score": round(home_score, 2),
                "away_score": round(away_score, 2),
                "home_prob": home_prob,
                "away_prob": away_prob,
                "winner": winner,
                "home_win_pct": home["win_pct"],
                "away_win_pct": away["win_pct"],
                "home_avg_points": home["avg_points"],
                "away_avg_points": away["avg_points"],
                "home_avg_allowed": home["avg_allowed"],
                "away_avg_allowed": away["avg_allowed"],
                "winner_avg_points": winner_avg_points,
                "winner_avg_allowed": winner_avg_allowed,
                "winner_home_bonus": winner_home_bonus,
            })
        else:
            data["error"] = "One or both teams were not found in the dataset."

    return render(request, "index.html", context=data)