#!/usr/bin/env python3
"""
Sports Market Simulation Demo
Quick demonstration of all three algorithms
"""

from sports_market import SportsMarket
from base_price_algorithm import BasePriceAlgorithm
from intragame_algorithm import IntragameAlgorithm
from timeframe_algorithm import TimeframeAlgorithm

def main():
    print("🏀 SPORTS MARKET SIMULATION DEMO 🏀")
    print("=" * 50)
    
    # Initialize all components
    sm = SportsMarket()
    bpa = BasePriceAlgorithm()
    iga = IntragameAlgorithm()
    tfa = TimeframeAlgorithm()
    
    # Demo 1: Base Price for Malik Monk
    print("\n📊 DEMO 1: Base Price Calculation")
    print("-" * 30)
    
    monk_data = sm.get_player_data("Malik Monk")
    season_avg = monk_data["season_avg_2023"]
    
    base_result = bpa.calculate_base_price(
        player_stats=(season_avg[0], season_avg[1], season_avg[2], season_avg[3], season_avg[4], season_avg[6]),
        is_rookie=False
    )
    
    print(f"Player: Malik Monk")
    print(f"2023-2024 Season Averages: PTS={season_avg[0]:.1f}, REB={season_avg[1]:.1f}, AST={season_avg[2]:.1f}")
    print(f"Base Price: ${base_result['base_price']:.2f}")
    print(f"PRS Score: {base_result['prs']:.3f}")
    
    # Demo 2: Intragame Simulation for Devin Booker
    print("\n🎯 DEMO 2: Intragame Simulation")
    print("-" * 30)
    
    booker_data = sm.get_player_data("Devin Booker")
    games = booker_data["games"]
    last_game = sm.get_random_game_stats("Devin Booker")  # Random game
    season_avg = booker_data["season_avg_2024"]
    last_5_avg = sm.calculate_last_n_averages(games, 5)
    
    intragame_result = iga.simulate_intragame(
        actual_stats=last_game,
        season_avg=season_avg,
        last_5_avg=last_5_avg,
        old_price=35.0
    )
    
    print(f"Player: Devin Booker")
    print(f"Last Game: PTS={last_game[0]}, REB={last_game[1]}, AST={last_game[2]}, TO={last_game[3]}, STOCKS={last_game[4]}, 3PM={last_game[5]}, TS%={last_game[6]:.3f}")
    print(f"Old Price: ${intragame_result['old_price']:.2f}")
    print(f"New Price: ${intragame_result['new_price']:.2f}")
    print(f"Price Change: {intragame_result['price_change_pct']:+.2f}%")
    print(f"PPS: {intragame_result['pps']:.3f}")
    
    # Demo 3: Timeframe Simulation for Miles McBride
    print("\n📅 DEMO 3: Weekly Timeframe Simulation")
    print("-" * 30)
    
    mcbride_data = sm.get_player_data("Miles McBride")
    games = mcbride_data["games"]
    season_avg = mcbride_data["season_avg_2024"]
    
    # Get random 4 games for weekly simulation
    import random
    last_4_games = random.sample(games, min(4, len(games)))
    recent_avg = sm.calculate_last_n_averages(games, len(last_4_games))
    
    # Calculate totals over random 4 games
    actual_totals = [0] * 7
    for game in last_4_games:
        for i in range(7):
            actual_totals[i] += game[i]
    
    timeframe_result = tfa.simulate_timeframe(
        actual_totals=tuple(actual_totals),
        num_games=len(last_4_games),
        season_avg=season_avg,
        recent_avg=recent_avg,
        old_price=15.0,
        timeframe="weekly"
    )
    
    print(f"Player: Miles McBride")
    print(f"Timeframe: Weekly ({len(last_4_games)} games)")
    print(f"Actual Totals: PTS={actual_totals[0]}, REB={actual_totals[1]}, AST={actual_totals[2]}, TO={actual_totals[3]}, STOCKS={actual_totals[4]}, 3PM={actual_totals[5]}, TS%={actual_totals[6]:.3f}")
    print(f"Old Price: ${timeframe_result['old_price']:.2f}")
    print(f"New Price: ${timeframe_result['new_price']:.2f}")
    print(f"Price Change: {timeframe_result['price_change_pct']:+.2f}%")
    print(f"PPS: {timeframe_result['pps']:.3f}")
    
    # Demo 4: Rookie Base Price
    print("\n🏆 DEMO 4: Rookie Base Price")
    print("-" * 30)
    
    # Simulate different draft picks
    draft_picks = [1, 10, 30, 60]
    for pick in draft_picks:
        rookie_result = bpa.calculate_base_price(draft_pick=pick, is_rookie=True)
        print(f"Draft Pick #{pick}: ${rookie_result['base_price']:.2f} (DRS: {rookie_result['drs']:.3f})")
    
    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETE!")
    print("Run 'python3 main.py' to use the full interactive system.")
    print("=" * 50)

if __name__ == "__main__":
    main() 