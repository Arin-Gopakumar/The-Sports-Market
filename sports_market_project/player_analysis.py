#!/usr/bin/env python3
"""
Player Analysis Script
Analyzes the diversity of the enhanced player pool and runs targeted simulations
"""

from sports_market import SportsMarket
import numpy as np
from base_price_algorithm import BasePriceAlgorithm
from intragame_algorithm import IntragameAlgorithm
from timeframe_algorithm import TimeframeAlgorithm
import random

def analyze_player_pool():
    """Analyze the enhanced player pool"""
    sm = SportsMarket()
    players = sm.list_players()
    
    print("🏀 ENHANCED PLAYER POOL ANALYSIS")
    print("=" * 50)
    print(f"Total Players: {len(players)}")
    print()
    
    # Analyze player types by their stats
    player_categories = {
        'Superstars': [],
        'Elite Shooters': [],
        'Elite Defenders': [],
        'High Volume Scorers': [],
        'Elite Playmakers': [],
        'Rebounding Machines': [],
        'Bench Warmers': [],
        'High Efficiency': [],
        'Turnover Prone': [],
        'One Dimensional': [],
        'Versatile': [],
        'Role Players': []
    }
    
    for player_name in players:
        player_data = sm.get_player_data(player_name)
        season_avg = player_data["season_avg_2024"]
        pts, reb, ast, to, stocks, threepm, ts_pct = season_avg
        
        # Categorize players based on their stats
        if pts >= 25 and ast >= 6 and reb >= 6:
            player_categories['Superstars'].append((player_name, season_avg))
        elif threepm >= 3 and ts_pct >= 0.60:
            player_categories['Elite Shooters'].append((player_name, season_avg))
        elif stocks >= 2.5 and pts <= 14:
            player_categories['Elite Defenders'].append((player_name, season_avg))
        elif pts >= 20 and ts_pct <= 0.55:
            player_categories['High Volume Scorers'].append((player_name, season_avg))
        elif ast >= 8:
            player_categories['Elite Playmakers'].append((player_name, season_avg))
        elif reb >= 10:
            player_categories['Rebounding Machines'].append((player_name, season_avg))
        elif pts <= 6:
            player_categories['Bench Warmers'].append((player_name, season_avg))
        elif ts_pct >= 0.62:
            player_categories['High Efficiency'].append((player_name, season_avg))
        elif to >= 4:
            player_categories['Turnover Prone'].append((player_name, season_avg))
        elif pts >= 18 and (reb <= 3 or ast <= 3):
            player_categories['One Dimensional'].append((player_name, season_avg))
        elif 10 <= pts <= 18 and 3 <= reb <= 7 and 3 <= ast <= 6:
            player_categories['Versatile'].append((player_name, season_avg))
        else:
            player_categories['Role Players'].append((player_name, season_avg))
    
    # Display results
    for category, players_list in player_categories.items():
        if players_list:
            print(f"\n📊 {category.upper()}: {len(players_list)} players")
            print("-" * 40)
            
            # Show top 3 examples
            for i, (name, stats) in enumerate(players_list[:3]):
                pts, reb, ast, to, stocks, threepm, ts_pct = stats
                print(f"  {i+1}. {name}: {pts:.1f}pts, {reb:.1f}reb, {ast:.1f}ast, {stocks:.1f}stocks, {threepm:.1f}3PM, {ts_pct:.3f}TS%")
            
            if len(players_list) > 3:
                print(f"  ... and {len(players_list) - 3} more")
    
    # Show overall statistics
    print(f"\n📈 OVERALL STATISTICS")
    print("=" * 30)
    
    all_stats = []
    for player_name in players:
        player_data = sm.get_player_data(player_name)
        all_stats.append(player_data["season_avg_2024"])
    
    all_stats = np.array(all_stats)
    
    print(f"Points: {all_stats[:, 0].mean():.1f} ± {all_stats[:, 0].std():.1f} (range: {all_stats[:, 0].min():.1f}-{all_stats[:, 0].max():.1f})")
    print(f"Rebounds: {all_stats[:, 1].mean():.1f} ± {all_stats[:, 1].std():.1f} (range: {all_stats[:, 1].min():.1f}-{all_stats[:, 1].max():.1f})")
    print(f"Assists: {all_stats[:, 2].mean():.1f} ± {all_stats[:, 2].std():.1f} (range: {all_stats[:, 2].min():.1f}-{all_stats[:, 2].max():.1f})")
    print(f"Turnovers: {all_stats[:, 3].mean():.1f} ± {all_stats[:, 3].std():.1f} (range: {all_stats[:, 3].min():.1f}-{all_stats[:, 3].max():.1f})")
    print(f"Stocks: {all_stats[:, 4].mean():.1f} ± {all_stats[:, 4].std():.1f} (range: {all_stats[:, 4].min():.1f}-{all_stats[:, 4].max():.1f})")
    print(f"3PM: {all_stats[:, 5].mean():.1f} ± {all_stats[:, 5].std():.1f} (range: {all_stats[:, 5].min():.1f}-{all_stats[:, 5].max():.1f})")
    print(f"TS%: {all_stats[:, 6].mean():.3f} ± {all_stats[:, 6].std():.3f} (range: {all_stats[:, 6].min():.3f}-{all_stats[:, 6].max():.3f})")
    
    return player_categories

def test_algorithm_diversity():
    """Test how algorithms handle different player types"""
    sm = SportsMarket()
    base_algo = BasePriceAlgorithm()
    
    print(f"\n🧪 ALGORITHM DIVERSITY TESTING")
    print("=" * 50)
    
    # Find players from different categories
    players = sm.list_players()
    
    # Find examples of different player types
    superstar = None
    elite_shooter = None
    bench_warmer = None
    elite_defender = None
    high_volume = None
    
    for player_name in players:
        player_data = sm.get_player_data(player_name)
        season_avg = player_data["season_avg_2024"]
        pts, reb, ast, to, stocks, threepm, ts_pct = season_avg
        
        if superstar is None and pts >= 25 and ast >= 6 and reb >= 6:
            superstar = (player_name, season_avg)
        elif elite_shooter is None and threepm >= 3 and ts_pct >= 0.60:
            elite_shooter = (player_name, season_avg)
        elif bench_warmer is None and pts <= 6:
            bench_warmer = (player_name, season_avg)
        elif elite_defender is None and stocks >= 2.5 and pts <= 14:
            elite_defender = (player_name, season_avg)
        elif high_volume is None and pts >= 20 and ts_pct <= 0.55:
            high_volume = (player_name, season_avg)
        
        if all([superstar, elite_shooter, bench_warmer, elite_defender, high_volume]):
            break
    
    # Test base prices for different player types
    test_players = [
        ("Superstar", superstar),
        ("Elite Shooter", elite_shooter),
        ("Bench Warmer", bench_warmer),
        ("Elite Defender", elite_defender),
        ("High Volume Scorer", high_volume)
    ]
    
    for player_type, (player_name, stats) in test_players:
        if stats is None:
            continue
            
        pts, reb, ast, to, stocks, threepm, ts_pct = stats
        result = base_algo.calculate_base_price(
            player_stats=(pts, reb, ast, to, stocks, ts_pct),
            is_rookie=False
        )
        
        print(f"\n{player_type} ({player_name}):")
        print(f"  Stats: {pts:.1f}pts, {reb:.1f}reb, {ast:.1f}ast, {to:.1f}to, {stocks:.1f}stocks, {ts_pct:.3f}TS%")
        print(f"  Base Price: ${result['base_price']:.2f}")
        print(f"  PRS Score: {result['prs']:.3f}")

def run_player_type_simulations():
    """Run simulations for specific player types or all types"""
    sm = SportsMarket()
    base_algo = BasePriceAlgorithm()
    intragame_algo = IntragameAlgorithm()
    timeframe_algo = TimeframeAlgorithm()
    
    # Get player categories
    player_categories = analyze_player_pool()
    
    print(f"\n🎯 PLAYER TYPE SIMULATION MENU")
    print("=" * 50)
    print("Available player types:")
    
    category_list = []
    for i, (category, players_list) in enumerate(player_categories.items(), 1):
        if players_list:
            print(f"{i}. {category} ({len(players_list)} players)")
            category_list.append((category, players_list))
    
    print(f"{len(category_list) + 1}. ALL PLAYER TYPES")
    print(f"{len(category_list) + 2}. EXIT")
    
    try:
        choice = int(input(f"\nSelect player type (1-{len(category_list) + 2}): "))
        
        if choice == len(category_list) + 1:
            # Run simulations for all player types
            run_all_player_type_simulations(player_categories, sm, base_algo, intragame_algo, timeframe_algo)
        elif choice == len(category_list) + 2:
            return
        elif 1 <= choice <= len(category_list):
            # Run simulations for specific player type
            category, players_list = category_list[choice - 1]
            run_single_player_type_simulations(category, players_list, sm, base_algo, intragame_algo, timeframe_algo)
        else:
            print("Invalid choice.")
            
    except ValueError:
        print("Invalid input. Please enter a number.")

def run_single_player_type_simulations(category, players_list, sm, base_algo, intragame_algo, timeframe_algo):
    """Run simulations for a specific player type"""
    print(f"\n🎯 {category.upper()} SIMULATIONS")
    print("=" * 50)
    print(f"Testing {len(players_list)} {category} players")
    
    # Get simulation parameters
    try:
        num_simulations = int(input("Number of simulations per player (e.g., 10): "))
        investment_amount = float(input("Investment amount per trade ($): "))
        
        print(f"\nSelect algorithms to test:")
        print("1. Base Price only")
        print("2. Intragame only")
        print("3. Weekly only")
        print("4. Monthly only")
        print("5. Season only")
        print("6. All algorithms")
        
        algorithm_choice = int(input("Select option (1-6): "))
        
        if algorithm_choice == 1:
            algorithms = ["base_price"]
        elif algorithm_choice == 2:
            algorithms = ["intragame"]
        elif algorithm_choice == 3:
            algorithms = ["weekly"]
        elif algorithm_choice == 4:
            algorithms = ["monthly"]
        elif algorithm_choice == 5:
            algorithms = ["season"]
        elif algorithm_choice == 6:
            algorithms = ["base_price", "intragame", "weekly", "monthly", "season"]
        else:
            print("Invalid choice. Using all algorithms.")
            algorithms = ["base_price", "intragame", "weekly", "monthly", "season"]
        
        # Run simulations
        results = run_player_type_simulations_core(
            category, players_list, sm, base_algo, intragame_algo, timeframe_algo,
            num_simulations, investment_amount, algorithms
        )
        
        # Display results
        display_player_type_results(category, results, algorithms)
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")

def run_all_player_type_simulations(player_categories, sm, base_algo, intragame_algo, timeframe_algo):
    """Run simulations for all player types"""
    print(f"\n🎯 ALL PLAYER TYPES SIMULATIONS")
    print("=" * 50)
    
    try:
        num_simulations = int(input("Number of simulations per player type (e.g., 5): "))
        investment_amount = float(input("Investment amount per trade ($): "))
        
        print(f"\nSelect algorithms to test:")
        print("1. Base Price only")
        print("2. Intragame only")
        print("3. Weekly only")
        print("4. Monthly only")
        print("5. Season only")
        print("6. All algorithms")
        
        algorithm_choice = int(input("Select option (1-6): "))
        
        if algorithm_choice == 1:
            algorithms = ["base_price"]
        elif algorithm_choice == 2:
            algorithms = ["intragame"]
        elif algorithm_choice == 3:
            algorithms = ["weekly"]
        elif algorithm_choice == 4:
            algorithms = ["monthly"]
        elif algorithm_choice == 5:
            algorithms = ["season"]
        elif algorithm_choice == 6:
            algorithms = ["base_price", "intragame", "weekly", "monthly", "season"]
        else:
            print("Invalid choice. Using all algorithms.")
            algorithms = ["base_price", "intragame", "weekly", "monthly", "season"]
        
        # Run simulations for each category
        all_results = {}
        total_categories = len([cat for cat, players in player_categories.items() if players])
        current_category = 0
        
        for category, players_list in player_categories.items():
            if players_list:
                current_category += 1
                print(f"\n📊 Testing {category} ({current_category}/{total_categories})...")
                
                results = run_player_type_simulations_core(
                    category, players_list, sm, base_algo, intragame_algo, timeframe_algo,
                    num_simulations, investment_amount, algorithms
                )
                
                all_results[category] = results
        
        # Display comprehensive results
        display_all_player_type_results(all_results, algorithms)
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")

def run_player_type_simulations_core(category, players_list, sm, base_algo, intragame_algo, timeframe_algo, 
                                   num_simulations, investment_amount, algorithms):
    """Core simulation logic for player types"""
    results = {
        'base_price': {'prices': [], 'prs_scores': []},
        'intragame': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
        'weekly': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
        'monthly': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
        'season': {'trades': [], 'total_pnl': 0, 'win_rate': 0}
    }
    
    for player_name, season_avg in players_list:
        player_data = sm.get_player_data(player_name)
        
        for sim in range(num_simulations):
            # Base Price Simulation
            if "base_price" in algorithms:
                pts, reb, ast, to, stocks, threepm, ts_pct = season_avg
                base_result = base_algo.calculate_base_price(
                    player_stats=(pts, reb, ast, to, stocks, ts_pct),
                    is_rookie=False
                )
                results['base_price']['prices'].append(base_result['base_price'])
                results['base_price']['prs_scores'].append(base_result['prs'])
            
            # Intragame Simulation
            if "intragame" in algorithms:
                actual_stats = sm.get_random_game_stats(player_name)
                season_avg_2024 = player_data["season_avg_2024"]
                last_5_avg = sm.calculate_random_recent_averages(player_data["games"], 5, pool_size=10)
                
                intragame_result = intragame_algo.simulate_intragame(
                    actual_stats, season_avg_2024, last_5_avg, investment_amount
                )
                
                # Calculate P&L with 1% fee
                price_change_pct = intragame_result['price_change_pct'] / 100
                user_pnl = investment_amount * price_change_pct
                fee = investment_amount * 0.01
                bank_pnl = fee - user_pnl
                
                trade = {
                    'player': player_name,
                    'bank_pnl': bank_pnl,
                    'price_change_pct': intragame_result['price_change_pct'],
                    'pps': intragame_result['pps']
                }
                
                results['intragame']['trades'].append(trade)
                results['intragame']['total_pnl'] += bank_pnl
            
            # Timeframe Simulations
            for timeframe in ["weekly", "monthly", "season"]:
                if timeframe in algorithms:
                    games = player_data["games"]
                    season_avg_2024 = player_data["season_avg_2024"]
                    
                    # Determine number of games based on timeframe
                    if timeframe == "weekly":
                        num_games = 4
                        sampled_games = random.sample(games, min(4, len(games)))
                    elif timeframe == "monthly":
                        num_games = 12
                        sampled_games = random.sample(games, min(12, len(games)))
                    else:  # season
                        num_games = len(games)
                        sampled_games = games
                    
                    recent_avg = sm.calculate_last_n_averages(games, len(sampled_games))
                    
                    # Calculate actual totals
                    actual_totals = [0] * 7
                    for game in sampled_games:
                        for i in range(7):
                            actual_totals[i] += game[i]
                    
                    # Run simulation
                    if timeframe == "season":
                        season_avg_2023 = player_data["season_avg_2023"]
                        timeframe_result = timeframe_algo.simulate_timeframe(
                            tuple(actual_totals), len(sampled_games), season_avg_2023, recent_avg, 
                            investment_amount, timeframe, use_2023_stats=True
                        )
                    else:
                        timeframe_result = timeframe_algo.simulate_timeframe(
                            tuple(actual_totals), len(sampled_games), season_avg_2024, recent_avg, 
                            investment_amount, timeframe
                        )
                    
                    # Calculate P&L with 1% fee
                    price_change_pct = timeframe_result['price_change_pct'] / 100
                    user_pnl = investment_amount * price_change_pct
                    fee = investment_amount * 0.01
                    bank_pnl = fee - user_pnl
                    
                    trade = {
                        'player': player_name,
                        'bank_pnl': bank_pnl,
                        'price_change_pct': timeframe_result['price_change_pct'],
                        'pps': timeframe_result['pps']
                    }
                    
                    results[timeframe]['trades'].append(trade)
                    results[timeframe]['total_pnl'] += bank_pnl
    
    # Calculate win rates
    for algorithm in algorithms:
        if algorithm in ['intragame', 'weekly', 'monthly', 'season']:
            trades = results[algorithm]['trades']
            if trades:
                wins = sum(1 for trade in trades if trade['bank_pnl'] > 0)
                results[algorithm]['win_rate'] = (wins / len(trades)) * 100
    
    return results

def display_player_type_results(category, results, algorithms):
    """Display results for a specific player type"""
    print(f"\n📊 {category.upper()} SIMULATION RESULTS")
    print("=" * 50)
    
    for algorithm in algorithms:
        if algorithm == "base_price":
            prices = results['base_price']['prices']
            prs_scores = results['base_price']['prs_scores']
            
            print(f"\n💰 BASE PRICE RESULTS:")
            print(f"  Average Base Price: ${np.mean(prices):.2f}")
            print(f"  Price Range: ${min(prices):.2f} - ${max(prices):.2f}")
            print(f"  Average PRS Score: {np.mean(prs_scores):.3f}")
            print(f"  PRS Range: {min(prs_scores):.3f} - {max(prs_scores):.3f}")
            
        elif algorithm in ['intragame', 'weekly', 'monthly', 'season']:
            trades = results[algorithm]['trades']
            total_pnl = results[algorithm]['total_pnl']
            win_rate = results[algorithm]['win_rate']
            
            if trades:
                avg_pnl = total_pnl / len(trades)
                print(f"\n📈 {algorithm.upper()} RESULTS:")
                print(f"  Total Trades: {len(trades)}")
                print(f"  Total Bank P&L: ${total_pnl:+.2f}")
                print(f"  Average Bank P&L per Trade: ${avg_pnl:+.2f}")
                print(f"  Bank Win Rate: {win_rate:.1f}%")
                print(f"  Bank Wins: {int(win_rate * len(trades) / 100)}/{len(trades)}")

def display_all_player_type_results(all_results, algorithms):
    """Display comprehensive results for all player types"""
    print(f"\n📊 COMPREHENSIVE PLAYER TYPE RESULTS")
    print("=" * 60)
    
    # Summary table
    print(f"{'Player Type':<20} {'Players':<8} {'Base Price':<12} {'Intragame':<12} {'Weekly':<12} {'Monthly':<12} {'Season':<12}")
    print("-" * 80)
    
    for category, results in all_results.items():
        if not results:
            continue
            
        # Count players (assuming all algorithms have same number of trades)
        num_players = len(results.get('intragame', {}).get('trades', [])) // 10 if 'intragame' in algorithms else 0
        
        # Base price average
        base_price_avg = f"${np.mean(results['base_price']['prices']):.1f}" if 'base_price' in algorithms else "N/A"
        
        # P&L for each algorithm
        intragame_pnl = f"${results['intragame']['total_pnl']:+.1f}" if 'intragame' in algorithms else "N/A"
        weekly_pnl = f"${results['weekly']['total_pnl']:+.1f}" if 'weekly' in algorithms else "N/A"
        monthly_pnl = f"${results['monthly']['total_pnl']:+.1f}" if 'monthly' in algorithms else "N/A"
        season_pnl = f"${results['season']['total_pnl']:+.1f}" if 'season' in algorithms else "N/A"
        
        print(f"{category:<20} {num_players:<8} {base_price_avg:<12} {intragame_pnl:<12} {weekly_pnl:<12} {monthly_pnl:<12} {season_pnl:<12}")
    
    # Overall summary
    print("\n📈 OVERALL SUMMARY:")
    total_pnl = sum(results.get('intragame', {}).get('total_pnl', 0) for results in all_results.values())
    print(f"  Total P&L across all player types: ${total_pnl:+.2f}")

def main_menu():
    """Main menu for player analysis"""
    while True:
        print(f"\n🎯 PLAYER ANALYSIS MENU")
        print("=" * 40)
        print("1. Analyze Player Pool")
        print("2. Test Algorithm Diversity")
        print("3. Run Player Type Simulations")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == "1":
            analyze_player_pool()
        elif choice == "2":
            test_algorithm_diversity()
        elif choice == "3":
            run_player_type_simulations()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu() 