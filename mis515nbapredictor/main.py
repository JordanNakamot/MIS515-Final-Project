def predict_winner(home_team, away_team, home_win_pct, away_win_pct,
                   home_avg_points, away_avg_points,
                   home_avg_allowed, away_avg_allowed):
    
    home_score = (home_win_pct * 0.4) + (home_avg_points * 0.3) - (home_avg_allowed * 0.3)
    away_score = (away_win_pct * 0.4) + (away_avg_points * 0.3) - (away_avg_allowed * 0.3)

    print("\n--- NBA Matchup Analysis ---")
    print(f"Home Team: {home_team}")
    print(f"Away Team: {away_team}")
    print(f"{home_team} Score: {home_score:.2f}")
    print(f"{away_team} Score: {away_score:.2f}")

    if home_score > away_score:
        print(f"Predicted Winner: {home_team}")
    elif away_score > home_score:
        print(f"Predicted Winner: {away_team}")
    else:
        print("Predicted Winner: Too close to call")


if __name__ == "__main__":
    home_team = input("Enter home team: ")
    away_team = input("Enter away team: ")

    home_win_pct = float(input(f"Enter {home_team} win percentage: "))
    away_win_pct = float(input(f"Enter {away_team} win percentage: "))

    home_avg_points = float(input(f"Enter {home_team} average points scored: "))
    away_avg_points = float(input(f"Enter {away_team} average points scored: "))

    home_avg_allowed = float(input(f"Enter {home_team} average points allowed: "))
    away_avg_allowed = float(input(f"Enter {away_team} average points allowed: "))

    predict_winner(
        home_team, away_team,
        home_win_pct, away_win_pct,
        home_avg_points, away_avg_points,
        home_avg_allowed, away_avg_allowed
    )