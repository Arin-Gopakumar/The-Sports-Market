#!/usr/bin/env python3
"""
Archetype Analysis Script
Comprehensive analysis of each player archetype's performance across all key metrics
"""

from sports_market import SportsMarket
from base_price_algorithm import BasePriceAlgorithm
from intragame_algorithm import IntragameAlgorithm
from timeframe_algorithm import TimeframeAlgorithm
import numpy as np
import random

def analyze_archetype_metrics():
    """Analyze each player archetype's performance across all key metrics"""
    sm = SportsMarket()
    base_algo = BasePriceAlgorithm()
    intragame_algo = IntragameAlgorithm()
    timeframe_algo = TimeframeAlgorithm()
    
    print("🏀 PLAYER ARCHETYPE METRICS ANALYSIS")
    print("=" * 60)
    print("Analyzing 197 players across 12 archetypes...")
    print()
    
    # Define archetypes and their criteria
    archetypes = {
        'Superstars': {'pts': (25, 35), 'ast': (6, 12), 'reb': (6, 12), 'description': 'Elite all-around players'},
        'Elite Shooters': {'threepm': (3, 6), 'ts_pct': (0.60, 0.70), 'description': 'High volume, high efficiency 3PT'},
        'Elite Defenders': {'stocks': (2.5, 4.0), 'pts': (6, 14), 'description': 'High stocks, lower scoring'},
        'High Volume Scorers': {'pts': (20, 30), 'ts_pct': (0.45, 0.55), 'description': 'High points, lower efficiency'},
        'Elite Playmakers': {'ast': (8, 12), 'description': 'Very high assists'},
        'Rebounding Machines': {'reb': (10, 15), 'description': 'Very high rebounds'},
        'Bench Warmers': {'pts': (2, 6), 'description': 'Very low stats'},
        'High Efficiency': {'ts_pct': (0.62, 0.72), 'description': 'High efficiency role players'},
        'Turnover Prone': {'to': (4, 6), 'description': 'High turnover rates'},
        'One Dimensional': {'pts': (18, 28), 'reb': (1, 3), 'ast': (1, 3), 'description': 'High scoring, low everything else'},
        'Versatile': {'pts': (10, 18), 'reb': (3, 7), 'ast': (3, 6), 'description': 'Moderate everything'},
        'Role Players': {'description': 'Balanced, moderate stats'}
    }
    
    # Categorize players
    player_categories = categorize_players(sm, archetypes)
    
    # Analyze each archetype
    archetype_results = {}
    
    for archetype, players_list in player_categories.items():
        if not players_list:
            continue
            
        print(f"\n📊 {archetype.upper()} ANALYSIS")
        print("-" * 50)
        print(f"Players: {len(players_list)}")
        print(f"Description: {archetypes[archetype]['description']}")
        
        # Run comprehensive analysis
        results = analyze_archetype_comprehensive(archetype, players_list, sm, base_algo, intragame_algo, timeframe_algo)
        archetype_results[archetype] = results
        
        # Display results
        display_archetype_metrics(archetype, results, players_list)
    
    # Generate comprehensive report
    generate_archetype_report(archetype_results, player_categories)

def categorize_players(sm, archetypes):
    """Categorize all players into archetypes"""
    players = sm.list_players()
    player_categories = {archetype: [] for archetype in archetypes.keys()}
    
    for player_name in players:
        player_data = sm.get_player_data(player_name)
        season_avg = player_data["season_avg_2024"]
        pts, reb, ast, to, stocks, threepm, ts_pct = season_avg
        
        # Categorize based on archetype criteria
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
    
    return player_categories

def analyze_archetype_comprehensive(archetype, players_list, sm, base_algo, intragame_algo, timeframe_algo):
    """Comprehensive analysis of an archetype across all metrics"""
    results = {
        'base_price': {'prices': [], 'prs_scores': [], 'z_scores': [], 'percentiles': []},
        'intragame': {'z_scores': [], 'pps_scores': [], 'dis_scores': [], 'price_changes': [], 'buyers_sellers': []},
        'timeframe': {'weekly': [], 'monthly': [], 'season': []},
        'statistics': {'avg_stats': [], 'std_stats': []}
    }
    
    # Sample size for analysis (to avoid too much computation)
    sample_size = min(20, len(players_list))
    sampled_players = random.sample(players_list, sample_size)
    
    for player_name, season_avg in sampled_players:
        player_data = sm.get_player_data(player_name)
        
        # Base Price Analysis
        pts, reb, ast, to, stocks, threepm, ts_pct = season_avg
        base_result = base_algo.calculate_base_price(
            player_stats=(pts, reb, ast, to, stocks, ts_pct),
            is_rookie=False
        )
        
        results['base_price']['prices'].append(base_result['base_price'])
        results['base_price']['prs_scores'].append(base_result['prs'])
        results['base_price']['z_scores'].append(base_result['z_scores'])
        results['base_price']['percentiles'].append(base_result['percentiles'])
        
        # Intragame Analysis (run multiple simulations)
        for _ in range(5):  # 5 simulations per player
            actual_stats = sm.get_random_game_stats(player_name)
            season_avg_2024 = player_data["season_avg_2024"]
            last_5_avg = sm.calculate_random_recent_averages(player_data["games"], 5, pool_size=10)
            
            intragame_result = intragame_algo.simulate_intragame(
                actual_stats, season_avg_2024, last_5_avg, 100  # $100 investment
            )
            
            results['intragame']['z_scores'].append(intragame_result['z_scores'])
            results['intragame']['pps_scores'].append(intragame_result['pps'])
            results['intragame']['dis_scores'].append(intragame_result['dis'])
            results['intragame']['price_changes'].append(intragame_result['price_change_pct'])
            
            # Calculate buyers/sellers
            pps = intragame_result['pps']
            buy_adj = 15 * pps
            sell_adj = -15 * pps
            buys = 50 + buy_adj + 2
            sells = 50 + sell_adj - 2
            results['intragame']['buyers_sellers'].append((buys, sells))
        
        # Timeframe Analysis
        for timeframe in ['weekly', 'monthly', 'season']:
            games = player_data["games"]
            season_avg_2024 = player_data["season_avg_2024"]
            
            # Sample games based on timeframe
            if timeframe == "weekly":
                sampled_games = random.sample(games, min(4, len(games)))
            elif timeframe == "monthly":
                sampled_games = random.sample(games, min(12, len(games)))
            else:  # season
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
                    100, timeframe, use_2023_stats=True
                )
            else:
                timeframe_result = timeframe_algo.simulate_timeframe(
                    tuple(actual_totals), len(sampled_games), season_avg_2024, recent_avg, 
                    100, timeframe
                )
            
            results['timeframe'][timeframe].append({
                'z_scores': timeframe_result['z_scores'],
                'pps': timeframe_result['pps'],
                'dis': timeframe_result['dis'],
                'price_change': timeframe_result['price_change_pct']
            })
        
        # Statistical summary
        results['statistics']['avg_stats'].append(season_avg)
        results['statistics']['std_stats'].append(season_avg)  # For simplicity
    
    return results

def display_archetype_metrics(archetype, results, players_list):
    """Display comprehensive metrics for an archetype"""
    print(f"\n📈 {archetype.upper()} METRICS:")
    print("-" * 40)
    
    # Base Price Metrics
    base_prices = results['base_price']['prices']
    prs_scores = results['base_price']['prs_scores']
    
    print(f"💰 BASE PRICE ANALYSIS:")
    print(f"  Average Base Price: ${np.mean(base_prices):.2f} ± ${np.std(base_prices):.2f}")
    print(f"  Price Range: ${min(base_prices):.2f} - ${max(base_prices):.2f}")
    print(f"  Average PRS Score: {np.mean(prs_scores):.3f} ± {np.std(prs_scores):.3f}")
    
    # Intragame Metrics
    pps_scores = results['intragame']['pps_scores']
    dis_scores = results['intragame']['dis_scores']
    price_changes = results['intragame']['price_changes']
    buyers_sellers = results['intragame']['buyers_sellers']
    
    print(f"\n🎯 INTRAGAME ANALYSIS:")
    print(f"  Average PPS: {np.mean(pps_scores):.3f} ± {np.std(pps_scores):.3f}")
    print(f"  Average DIS: {np.mean(dis_scores):.3f} ± {np.std(dis_scores):.3f}")
    print(f"  Average Price Change: {np.mean(price_changes):+.2f}% ± {np.std(price_changes):.2f}%")
    
    # Buyers/Sellers Analysis
    avg_buyers = np.mean([bs[0] for bs in buyers_sellers])
    avg_sellers = np.mean([bs[1] for bs in buyers_sellers])
    print(f"  Average Buyers: {avg_buyers:.1f}")
    print(f"  Average Sellers: {avg_sellers:.1f}")
    print(f"  Buy/Sell Ratio: {avg_buyers/avg_sellers:.2f}")
    
    # Z-Score Analysis
    all_z_scores = []
    for z_dict in results['intragame']['z_scores']:
        all_z_scores.extend(list(z_dict.values()))
    
    print(f"\n📊 Z-SCORE ANALYSIS:")
    print(f"  Z-Score Mean: {np.mean(all_z_scores):.3f}")
    print(f"  Z-Score Std Dev: {np.std(all_z_scores):.3f}")
    print(f"  Z-Score Range: {min(all_z_scores):.3f} to {max(all_z_scores):.3f}")
    
    # P&L per Trade Analysis
    print(f"\n💰 P&L PER TRADE ANALYSIS:")
    print(f"  Total Trades: {len(pps_scores)}")
    
    # Calculate P&L per trade (assuming $100 investment and 1% fee)
    pnl_per_trade = []
    for i, price_change in enumerate(price_changes):
        investment = 100  # $100 per trade
        user_pnl = investment * (price_change / 100)
        fee = investment * 0.01  # 1% fee
        bank_pnl = fee - user_pnl
        pnl_per_trade.append(bank_pnl)
    
    if pnl_per_trade:
        avg_pnl = np.mean(pnl_per_trade)
        median_pnl = np.median(pnl_per_trade)
        std_pnl = np.std(pnl_per_trade)
        positive_trades = [pnl for pnl in pnl_per_trade if pnl > 0]
        negative_trades = [pnl for pnl in pnl_per_trade if pnl < 0]
        
        print(f"  Average P&L per Trade: ${avg_pnl:+.2f}")
        print(f"  Median P&L per Trade: ${median_pnl:+.2f}")
        print(f"  P&L per Trade Std Dev: ${std_pnl:.2f}")
        print(f"  P&L per Trade Range: ${min(pnl_per_trade):+.2f} to ${max(pnl_per_trade):+.2f}")
        
        if positive_trades:
            print(f"  Average Winning Trade: ${np.mean(positive_trades):+.2f}")
        if negative_trades:
            print(f"  Average Losing Trade: ${np.mean(negative_trades):+.2f}")
        
        win_rate = (len(positive_trades) / len(pnl_per_trade)) * 100
        print(f"  Win Rate: {win_rate:.1f}%")
        print(f"  Wins: {len(positive_trades)}/{len(pnl_per_trade)}")
    
    # Timeframe Analysis
    for timeframe in ['weekly', 'monthly', 'season']:
        if results['timeframe'][timeframe]:
            timeframe_pps = [r['pps'] for r in results['timeframe'][timeframe]]
            timeframe_price_changes = [r['price_change'] for r in results['timeframe'][timeframe]]
            
            print(f"\n📅 {timeframe.upper()} ANALYSIS:")
            print(f"  Average PPS: {np.mean(timeframe_pps):.3f} ± {np.std(timeframe_pps):.3f}")
            print(f"  Average Price Change: {np.mean(timeframe_price_changes):+.2f}% ± {np.std(timeframe_price_changes):.2f}%")

def generate_archetype_report(archetype_results, player_categories):
    """Generate comprehensive archetype comparison report"""
    print(f"\n📊 COMPREHENSIVE ARCHETYPE COMPARISON")
    print("=" * 80)
    
    # Summary table
    print(f"{'Archetype':<20} {'Players':<8} {'Avg Base Price':<15} {'Avg PPS':<12} {'Avg DIS':<12} {'Avg Price Change':<15} {'Buy/Sell Ratio':<15}")
    print("-" * 100)
    
    for archetype, results in archetype_results.items():
        if not results:
            continue
            
        num_players = len(player_categories[archetype])
        avg_base_price = f"${np.mean(results['base_price']['prices']):.1f}"
        avg_pps = f"{np.mean(results['intragame']['pps_scores']):.3f}"
        avg_dis = f"{np.mean(results['intragame']['dis_scores']):.3f}"
        avg_price_change = f"{np.mean(results['intragame']['price_changes']):+.1f}%"
        
        # Calculate buy/sell ratio
        buyers_sellers = results['intragame']['buyers_sellers']
        avg_buyers = np.mean([bs[0] for bs in buyers_sellers])
        avg_sellers = np.mean([bs[1] for bs in buyers_sellers])
        buy_sell_ratio = f"{avg_buyers/avg_sellers:.2f}"
        
        print(f"{archetype:<20} {num_players:<8} {avg_base_price:<15} {avg_pps:<12} {avg_dis:<12} {avg_price_change:<15} {buy_sell_ratio:<15}")
    
    print(f"\n📈 KEY INSIGHTS:")
    print("=" * 40)
    
    # Find best/worst performers
    base_prices = [(archetype, np.mean(results['base_price']['prices'])) 
                   for archetype, results in archetype_results.items() if results]
    pps_scores = [(archetype, np.mean(results['intragame']['pps_scores'])) 
                  for archetype, results in archetype_results.items() if results]
    price_changes = [(archetype, np.mean(results['intragame']['price_changes'])) 
                     for archetype, results in archetype_results.items() if results]
    
    best_base_price = max(base_prices, key=lambda x: x[1])
    worst_base_price = min(base_prices, key=lambda x: x[1])
    best_pps = max(pps_scores, key=lambda x: x[1])
    worst_pps = min(pps_scores, key=lambda x: x[1])
    best_price_change = max(price_changes, key=lambda x: x[1])
    worst_price_change = min(price_changes, key=lambda x: x[1])
    
    print(f"  Highest Base Price: {best_base_price[0]} (${best_base_price[1]:.1f})")
    print(f"  Lowest Base Price: {worst_base_price[0]} (${worst_base_price[1]:.1f})")
    print(f"  Highest PPS: {best_pps[0]} ({best_pps[1]:.3f})")
    print(f"  Lowest PPS: {worst_pps[0]} ({worst_pps[1]:.3f})")
    print(f"  Most Volatile: {best_price_change[0]} ({best_price_change[1]:+.1f}%)")
    print(f"  Least Volatile: {worst_price_change[0]} ({worst_price_change[1]:+.1f}%)")

if __name__ == "__main__":
    analyze_archetype_metrics() 