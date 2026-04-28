from django.shortcuts import render

def index(request):
    data = {}

    if request.method == "POST":
        home_team = request.POST.get("home_team")
        away_team = request.POST.get("away_team")

        home_win_pct = float(request.POST.get("home_win_pct"))
        away_win_pct = float(request.POST.get("away_win_pct"))

        home_avg_points = float(request.POST.get("home_avg_points"))
        away_avg_points = float(request.POST.get("away_avg_points"))

        home_avg_allowed = float(request.POST.get("home_avg_allowed"))
        away_avg_allowed = float(request.POST.get("away_avg_allowed"))

        home_score = (home_win_pct * 40) + (home_avg_points * 0.3) - (home_avg_allowed * 0.2) + 3
        away_score = (away_win_pct * 40) + (away_avg_points * 0.3) - (away_avg_allowed * 0.2)

        total_score = home_score + away_score
        home_prob = round((home_score / total_score) * 100, 2)
        away_prob = round((away_score / total_score) * 100, 2)

        if home_score > away_score:
            winner = home_team
        elif away_score > home_score:
            winner = away_team
        else:
            winner = "Too close to call"

        data = {
            "home_team": home_team,
            "away_team": away_team,
            "home_score": round(home_score, 2),
            "away_score": round(away_score, 2),
            "home_prob": home_prob,
            "away_prob": away_prob,
            "winner": winner,
        }

    return render(request, "index.html", context=data)