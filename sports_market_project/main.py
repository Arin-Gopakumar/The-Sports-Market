#!/usr/bin/env python3
"""
Sports Market Simulation System
Main interface for running simulations with all three algorithms
"""

from sports_market import SportsMarket
from base_price_algorithm import BasePriceAlgorithm
from intragame_algorithm import IntragameAlgorithm
from timeframe_algorithm import TimeframeAlgorithm

class SportsMarketSimulator:
    def __init__(self):
        self.sports_market = SportsMarket()
        self.base_price_algo = BasePriceAlgorithm()
        self.intragame_algo = IntragameAlgorithm()
        self.timeframe_algo = TimeframeAlgorithm()
    
    def print_welcome(self):
        """Print welcome message and available options"""
        print("🏀 SPORTS MARKET SIMULATION SYSTEM 🏀")
        print("=" * 50)
        print("Available Players:")
        for i, player in enumerate(self.sports_market.list_players(), 1):
            print(f"{i}. {player}")
        print("\nAlgorithms:")
        print("1. Base Price (Rookie/Non-Rookie)")
        print("2. Intragame Simulation")
        print("3. Timeframe/Season Simulation")
        print("4. Custom Input")
        print("5. Calculate Base Prices for All Players")
        print("6. Profitability Testing Mode")
        print("7. Player Type Analysis & Simulations")
        print("8. Exit")
        print("=" * 50)
    
    def run_base_price_simulation(self):
        """Run base price simulation"""
        print("\n📊 BASE PRICE ALGORITHM")
        print("-" * 30)
        
        # Choose player or custom input
        choice = input("Use stored player data? (y/n): ").lower()
        
        if choice == 'y':
            print("\nAvailable players:")
            players = self.sports_market.list_players()
            for i, player in enumerate(players, 1):
                print(f"{i}. {player}")
            
            try:
                player_idx = int(input("Select player (number): ")) - 1
                player_name = players[player_idx]
                player_data = self.sports_market.get_player_data(player_name)
                
                # Use 2023 season averages for base price calculation
                season_avg = player_data["season_avg_2023"]
                
                print(f"\nUsing {player_name} 2023-2024 season averages:")
                print(f"PTS: {season_avg[0]:.1f}, REB: {season_avg[1]:.1f}, AST: {season_avg[2]:.1f}")
                print(f"TO: {season_avg[3]:.1f}, STOCKS: {season_avg[4]:.1f}, 3PM: {season_avg[5]:.1f}, TS%: {season_avg[6]:.3f}")
                
                # Calculate base price (non-rookie)
                result = self.base_price_algo.calculate_base_price(
                    player_stats=(season_avg[0], season_avg[1], season_avg[2], season_avg[3], season_avg[4], season_avg[6]),
                    is_rookie=False
                )
                
            except (ValueError, IndexError):
                print("Invalid selection. Using custom input.")
                return self.run_base_price_custom()
        else:
            return self.run_base_price_custom()
        
        # Display results
        print(f"\n📈 RESULTS:")
        print(f"Base Price: ${result['base_price']:.2f}")
        print(f"PRS Score: {result['prs']:.3f}")
        print(f"Z-Scores: {result['z_scores']}")
        print(f"Percentiles: {result['percentiles']}")
        
        return result
    
    def run_base_price_custom(self):
        """Run base price with custom input"""
        print("\nEnter player stats (2023-2024 season averages):")
        try:
            pts = float(input("Points per game: "))
            reb = float(input("Rebounds per game: "))
            ast = float(input("Assists per game: "))
            to = float(input("Turnovers per game: "))
            stocks = float(input("Steals + Blocks per game: "))
            ts_pct = float(input("True Shooting % (0.0-1.0): "))
            
            result = self.base_price_algo.calculate_base_price(
                player_stats=(pts, reb, ast, to, stocks, ts_pct),
                is_rookie=False
            )
            
            print(f"\n📈 RESULTS:")
            print(f"Base Price: ${result['base_price']:.2f}")
            print(f"PRS Score: {result['prs']:.3f}")
            
            return result
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return None
    
    def run_intragame_simulation(self):
        """Run intragame simulation"""
        print("\n🎯 INTRAGAME SIMULATION")
        print("-" * 30)
        
        # Choose player or custom input
        choice = input("Use stored player data? (y/n): ").lower()
        
        if choice == 'y':
            return self.run_intragame_with_player()
        else:
            return self.run_intragame_custom()
    
    def run_intragame_with_player(self):
        """Run intragame simulation with stored player data"""
        print("\nAvailable players:")
        players = self.sports_market.list_players()
        for i, player in enumerate(players, 1):
            print(f"{i}. {player}")
        
        try:
            player_idx = int(input("Select player (number): ")) - 1
            player_name = players[player_idx]
            player_data = self.sports_market.get_player_data(player_name)
            
            # Get random game as actual stats
            games = player_data["games"]
            if len(games) < 1:
                print("Not enough game data available.")
                return None
            
            actual_stats = self.sports_market.get_random_game_stats(player_name)
            season_avg = player_data["season_avg_2024"]
            last_5_games = games[-5:] if len(games) >= 5 else games
            last_5_avg = self.sports_market.calculate_random_recent_averages(games, 5, pool_size=10)
            
            print(f"\nUsing {player_name} data:")
            print(f"Actual Game: PTS={actual_stats[0]}, REB={actual_stats[1]}, AST={actual_stats[2]}, TO={actual_stats[3]}, STOCKS={actual_stats[4]}, 3PM={actual_stats[5]}, TS%={actual_stats[6]:.3f}")
            
            # Get old price
            old_price = float(input("Enter current stock price: $"))
            
            # Run simulation
            result = self.intragame_algo.simulate_intragame(
                actual_stats, season_avg, last_5_avg, old_price
            )
            
            self.display_intragame_results(result)
            return result
            
        except (ValueError, IndexError):
            print("Invalid selection.")
            return None
    
    def run_intragame_custom(self):
        """Run intragame simulation with custom input"""
        print("\nEnter actual game stats:")
        try:
            pts = float(input("Points: "))
            reb = float(input("Rebounds: "))
            ast = float(input("Assists: "))
            to = float(input("Turnovers: "))
            stocks = float(input("Steals + Blocks: "))
            threepm = float(input("3-Pointers Made: "))
            ts_pct = float(input("True Shooting % (0.0-1.0): "))
            
            actual_stats = (pts, reb, ast, to, stocks, threepm, ts_pct)
            
            print("\nEnter season averages:")
            season_pts = float(input("Points per game: "))
            season_reb = float(input("Rebounds per game: "))
            season_ast = float(input("Assists per game: "))
            season_to = float(input("Turnovers per game: "))
            season_stocks = float(input("Steals + Blocks per game: "))
            season_threepm = float(input("3-Pointers per game: "))
            season_ts_pct = float(input("True Shooting %: "))
            
            season_avg = (season_pts, season_reb, season_ast, season_to, season_stocks, season_threepm, season_ts_pct)
            
            print("\nEnter last 5 games averages:")
            last5_pts = float(input("Points per game: "))
            last5_reb = float(input("Rebounds per game: "))
            last5_ast = float(input("Assists per game: "))
            last5_to = float(input("Turnovers per game: "))
            last5_stocks = float(input("Steals + Blocks per game: "))
            last5_threepm = float(input("3-Pointers per game: "))
            last5_ts_pct = float(input("True Shooting %: "))
            
            last_5_avg = (last5_pts, last5_reb, last5_ast, last5_to, last5_stocks, last5_threepm, last5_ts_pct)
            
            old_price = float(input("Enter current stock price: $"))
            
            result = self.intragame_algo.simulate_intragame(
                actual_stats, season_avg, last_5_avg, old_price
            )
            
            self.display_intragame_results(result)
            return result
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return None
    
    def display_intragame_results(self, result):
        """Display intragame simulation results"""
        print(f"\n📊 INTRAGAME SIMULATION RESULTS:")
        print(f"Projected Stats: {result['projected_stats']}")
        print(f"Standard Deviations: {result['standard_deviations']}")
        print(f"Z-Scores: {result['z_scores']}")
        print(f"PPS: {result['pps']:.3f}")
        print(f"DIS: {result['dis']:.3f}")
        print(f"Raw Delta: {result['raw_delta']:.3f}")
        print(f"Dampened Delta: {result['dampened_delta']:.3f}")
        print(f"Old Price: ${result['old_price']:.2f}")
        print(f"New Price: ${result['new_price']:.2f}")
        print(f"Price Change: {result['price_change_pct']:+.2f}%")
    
    def calculate_all_base_prices(self):
        """Calculate base prices for all stored players"""
        print("\n📊 CALCULATING BASE PRICES FOR ALL PLAYERS")
        print("-" * 50)
        
        results = {}
        for player_name in self.sports_market.list_players():
            player_data = self.sports_market.get_player_data(player_name)
            season_avg = player_data["season_avg_2023"]
            
            print(f"\n📈 {player_name}:")
            print(f"2023-2024 Season Averages: PTS={season_avg[0]:.1f}, REB={season_avg[1]:.1f}, AST={season_avg[2]:.1f}")
            print(f"TO={season_avg[3]:.1f}, STOCKS={season_avg[4]:.1f}, 3PM={season_avg[5]:.1f}, TS%={season_avg[6]:.3f}")
            
            result = self.base_price_algo.calculate_base_price(
                player_stats=(season_avg[0], season_avg[1], season_avg[2], season_avg[3], season_avg[4], season_avg[6]),
                is_rookie=False
            )
            
            print(f"Base Price: ${result['base_price']:.2f}")
            print(f"PRS Score: {result['prs']:.3f}")
            print(f"Z-Scores: {result['z_scores']}")
            print(f"Percentiles: {result['percentiles']}")
            
            results[player_name] = result
        
        print(f"\n✅ Base prices calculated for all {len(results)} players.")
        return results
    
    def run_profitability_testing(self):
        """Run profitability testing mode"""
        print("\n💰 PROFITABILITY TESTING MODE")
        print("=" * 50)
        print("This mode helps you test algorithm profitability manually.")
        print("You can run multiple simulations and track your results.")
        print()
        
        # Initialize tracking
        self.test_results = {
            'intragame': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'weekly': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'monthly': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'season': {'trades': [], 'total_pnl': 0, 'win_rate': 0}
        }
        
        while True:
            print("\n📊 TESTING OPTIONS:")
            print("1. Run Intragame Simulation")
            print("2. Run Weekly Simulation")
            print("3. Run Monthly Simulation")
            print("4. Run Season Simulation")
            print("5. View Current Results")
            print("6. Reset Results")
            print("7. Export Results")
            print("8. Automated Testing")
            print("9. Back to Main Menu")
            
            test_choice = input("\nSelect option (1-9): ")
            
            if test_choice == "1":
                self.run_test_intragame()
            elif test_choice == "2":
                self.run_test_timeframe("weekly")
            elif test_choice == "3":
                self.run_test_timeframe("monthly")
            elif test_choice == "4":
                self.run_test_timeframe("season")
            elif test_choice == "5":
                self.display_test_results()
            elif test_choice == "6":
                self.reset_test_results()
            elif test_choice == "7":
                self.export_test_results()
            elif test_choice == "8":
                self.run_automated_testing()
            elif test_choice == "9":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def run_test_intragame(self):
        """Run intragame simulation for testing"""
        print("\n🎯 INTRAGAME TESTING")
        print("-" * 30)
        
        # Select player
        players = self.sports_market.list_players()
        print("Available players:")
        for i, player in enumerate(players, 1):
            print(f"{i}. {player}")
        
        try:
            player_idx = int(input("Select player (number): ")) - 1
            player_name = players[player_idx]
            player_data = self.sports_market.get_player_data(player_name)
            
            # Get random game stats
            actual_stats = self.sports_market.get_random_game_stats(player_name)
            season_avg = player_data["season_avg_2024"]
            last_5_avg = self.sports_market.calculate_random_recent_averages(player_data["games"], 5, pool_size=10)
            
            print(f"\n📈 {player_name} - Random Game:")
            print(f"Stats: PTS={actual_stats[0]}, REB={actual_stats[1]}, AST={actual_stats[2]}, TO={actual_stats[3]}, STOCKS={actual_stats[4]}, 3PM={actual_stats[5]}, TS%={actual_stats[6]:.3f}")
            
            # Get investment amount
            investment = float(input("Enter investment amount ($): "))
            
            # Run simulation
            result = self.intragame_algo.simulate_intragame(
                actual_stats, season_avg, last_5_avg, investment
            )
            
            # Calculate P&L with 1% fee (bank perspective)
            price_change_pct = result['price_change_pct'] / 100
            user_pnl = investment * price_change_pct
            fee = investment * 0.01  # 1% fee
            bank_pnl = fee - user_pnl  # Bank profits from fee, loses from user gains
            new_value = investment + user_pnl - fee
            
            # Store result
            trade = {
                'player': player_name,
                'old_price': result['old_price'],
                'new_price': result['new_price'],
                'price_change_pct': result['price_change_pct'],
                'investment': investment,
                'user_pnl': user_pnl,
                'fee': fee,
                'bank_pnl': bank_pnl,
                'new_value': new_value,
                'pps': result['pps'],
                'timestamp': len(self.test_results['intragame']['trades']) + 1
            }
            
            self.test_results['intragame']['trades'].append(trade)
            self.test_results['intragame']['total_pnl'] += bank_pnl
            
            # Display result
            print(f"\n💰 TRADE RESULT:")
            print(f"Old Price: ${result['old_price']:.2f}")
            print(f"New Price: ${result['new_price']:.2f}")
            print(f"Price Change: {result['price_change_pct']:+.2f}%")
            print(f"Investment: ${investment:.2f}")
            print(f"Bank P&L: ${bank_pnl:+.2f}")
            print(f"New Value: ${new_value:.2f}")
            print(f"PPS: {result['pps']:.3f}")
            
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
    
    def run_test_timeframe(self, timeframe):
        """Run timeframe simulation for testing"""
        print(f"\n📅 {timeframe.upper()} TESTING")
        print("-" * 30)
        
        # Select player
        players = self.sports_market.list_players()
        print("Available players:")
        for i, player in enumerate(players, 1):
            print(f"{i}. {player}")
        
        try:
            player_idx = int(input("Select player (number): ")) - 1
            player_name = players[player_idx]
            player_data = self.sports_market.get_player_data(player_name)
            
            games = player_data["games"]
            season_avg = player_data["season_avg_2024"]
            
            # Determine number of games and recent averages
            if timeframe == "weekly":
                num_games = 4
                recent_games = games[-4:] if len(games) >= 4 else games
            elif timeframe == "monthly":
                num_games = 12
                recent_games = games[-12:] if len(games) >= 12 else games
            else:  # season
                num_games = len(games)
                recent_games = games
            
            recent_avg = self.sports_market.calculate_last_n_averages(games, len(recent_games))
            
            # Calculate actual totals from random game samples
            import random
            if timeframe == "weekly":
                sampled_games = random.sample(games, min(4, len(games)))
            elif timeframe == "monthly":
                sampled_games = random.sample(games, min(12, len(games)))
            else:  # season
                sampled_games = games
            
            actual_totals = [0] * 7
            for game in sampled_games:
                for i in range(7):
                    actual_totals[i] += game[i]
            
            print(f"\n📈 {player_name} - {timeframe.title()} Performance:")
            print(f"Games: {len(sampled_games)}")
            print(f"Actual Totals: PTS={actual_totals[0]}, REB={actual_totals[1]}, AST={actual_totals[2]}, TO={actual_totals[3]}, STOCKS={actual_totals[4]}, 3PM={actual_totals[5]}, TS%={actual_totals[6]:.3f}")
            
            # Get investment amount
            investment = float(input("Enter investment amount ($): "))
            
            # Run simulation
            if timeframe == "season":
                season_avg_2023 = player_data["season_avg_2023"]
                result = self.timeframe_algo.simulate_timeframe(
                    tuple(actual_totals), len(sampled_games), season_avg_2023, recent_avg, investment, timeframe, use_2023_stats=True, player_archetype=None
                )
            else:
                result = self.timeframe_algo.simulate_timeframe(
                    tuple(actual_totals), len(sampled_games), season_avg, recent_avg, investment, timeframe, player_archetype=None
                )
            
            # Calculate P&L with 1% fee (bank perspective)
            price_change_pct = result['price_change_pct'] / 100
            user_pnl = investment * price_change_pct
            fee = investment * 0.01  # 1% fee
            bank_pnl = fee - user_pnl  # Bank profits from fee, loses from user gains
            new_value = investment + user_pnl - fee
            
            # Store result
            trade = {
                'player': player_name,
                'old_price': result['old_price'],
                'new_price': result['new_price'],
                'price_change_pct': result['price_change_pct'],
                'investment': investment,
                'user_pnl': user_pnl,
                'fee': fee,
                'bank_pnl': bank_pnl,
                'new_value': new_value,
                'pps': result['pps'],
                'timeframe': timeframe,
                'timestamp': len(self.test_results[timeframe]['trades']) + 1
            }
            
            self.test_results[timeframe]['trades'].append(trade)
            self.test_results[timeframe]['total_pnl'] += bank_pnl
            
            # Display result
            print(f"\n💰 TRADE RESULT:")
            print(f"Old Price: ${result['old_price']:.2f}")
            print(f"New Price: ${result['new_price']:.2f}")
            print(f"Price Change: {result['price_change_pct']:+.2f}%")
            print(f"Investment: ${investment:.2f}")
            print(f"Bank P&L: ${bank_pnl:+.2f}")
            print(f"New Value: ${new_value:.2f}")
            print(f"PPS: {result['pps']:.3f}")
            
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
    
    def display_test_results(self):
        """Display current testing results"""
        print("\n📊 CURRENT TESTING RESULTS")
        print("=" * 50)
        
        for algorithm, data in self.test_results.items():
            trades = data['trades']
            total_pnl = data['total_pnl']
            
            if trades:
                wins = sum(1 for trade in trades if trade['bank_pnl'] > 0)
                win_rate = (wins / len(trades)) * 100
                avg_pnl = total_pnl / len(trades)
                
                print(f"\n{algorithm.upper()}:")
                print(f"  Total Trades: {len(trades)}")
                print(f"  Total Bank P&L: ${total_pnl:+.2f}")
                print(f"  Average Bank P&L per Trade: ${avg_pnl:+.2f}")
                print(f"  Bank Win Rate: {win_rate:.1f}%")
                print(f"  Bank Wins: {wins}/{len(trades)}")
                
                # Show recent trades
                print(f"  Recent Trades:")
                for trade in trades[-3:]:  # Last 3 trades
                    print(f"    {trade['player']}: Bank ${trade['bank_pnl']:+.2f} (User ${trade['user_pnl']:+.2f}, Fee ${trade['fee']:.2f})")
            else:
                print(f"\n{algorithm.upper()}: No trades yet")
        
        # Overall summary
        total_trades = sum(len(data['trades']) for data in self.test_results.values())
        total_pnl = sum(data['total_pnl'] for data in self.test_results.values())
        
        if total_trades > 0:
            print(f"\n📈 OVERALL SUMMARY:")
            print(f"  Total Trades: {total_trades}")
            print(f"  Total Bank P&L: ${total_pnl:+.2f}")
            print(f"  Average Bank P&L per Trade: ${total_pnl/total_trades:+.2f}")
    
    def reset_test_results(self):
        """Reset all testing results"""
        self.test_results = {
            'intragame': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'weekly': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'monthly': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'season': {'trades': [], 'total_pnl': 0, 'win_rate': 0}
        }
        print("✅ All testing results have been reset.")
    
    def export_test_results(self):
        """Export testing results to a file"""
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"profitability_test_results_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("SPORTS MARKET PROFITABILITY TEST RESULTS\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for algorithm, data in self.test_results.items():
                trades = data['trades']
                total_pnl = data['total_pnl']
                
                f.write(f"{algorithm.upper()} RESULTS:\n")
                f.write("-" * 30 + "\n")
                
                if trades:
                    wins = sum(1 for trade in trades if trade['bank_pnl'] > 0)
                    win_rate = (wins / len(trades)) * 100
                    avg_pnl = total_pnl / len(trades)
                    
                    f.write(f"Total Trades: {len(trades)}\n")
                    f.write(f"Total Bank P&L: ${total_pnl:+.2f}\n")
                    f.write(f"Average Bank P&L per Trade: ${avg_pnl:+.2f}\n")
                    f.write(f"Bank Win Rate: {win_rate:.1f}%\n")
                    f.write(f"Bank Wins: {wins}/{len(trades)}\n\n")
                    
                    f.write("Individual Trades:\n")
                    for trade in trades:
                        f.write(f"  {trade['timestamp']}. {trade['player']}: Bank ${trade['bank_pnl']:+.2f} (User ${trade['user_pnl']:+.2f}, Fee ${trade['fee']:.2f})\n")
                else:
                    f.write("No trades yet\n")
                
                f.write("\n")
        
        print(f"✅ Results exported to {filename}")
    
    def run_automated_testing(self):
        """Run automated testing with multiple simulations"""
        print("\n🤖 AUTOMATED TESTING")
        print("=" * 50)
        print("This will run multiple simulations automatically.")
        print()
        
        # Get testing parameters
        try:
            num_simulations = int(input("Number of simulations to run (e.g., 100): "))
            investment_amount = float(input("Investment amount per trade ($): "))
            
            print("\nSelect algorithms to test:")
            print("1. Intragame only")
            print("2. Weekly only")
            print("3. Monthly only")
            print("4. Season only")
            print("5. All algorithms")
            
            algorithm_choice = input("Select option (1-5): ")
            
            if algorithm_choice == "1":
                algorithms = ["intragame"]
            elif algorithm_choice == "2":
                algorithms = ["weekly"]
            elif algorithm_choice == "3":
                algorithms = ["monthly"]
            elif algorithm_choice == "4":
                algorithms = ["season"]
            elif algorithm_choice == "5":
                algorithms = ["intragame", "weekly", "monthly", "season"]
            else:
                print("Invalid choice. Using all algorithms.")
                algorithms = ["intragame", "weekly", "monthly", "season"]
            
            print(f"\n🚀 Starting automated testing...")
            print(f"Simulations: {num_simulations}")
            print(f"Investment per trade: ${investment_amount}")
            print(f"Algorithms: {', '.join(algorithms)}")
            print()
            
            # Run automated simulations
            self.run_automated_simulations(num_simulations, investment_amount, algorithms)
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
    
    def run_automated_simulations(self, num_simulations, investment_amount, algorithms):
        """Run automated simulations"""
        import random
        import time
        
        players = self.sports_market.list_players()
        total_simulations = num_simulations * len(algorithms)
        completed = 0
        
        print("Progress: ", end="", flush=True)
        
        for algorithm in algorithms:
            for i in range(num_simulations):
                # Select random player
                player_name = random.choice(players)
                player_data = self.sports_market.get_player_data(player_name)
                
                if algorithm == "intragame":
                    # Run intragame simulation
                    actual_stats = self.sports_market.get_random_game_stats(player_name)
                    season_avg = player_data["season_avg_2024"]
                    last_5_avg = self.sports_market.calculate_random_recent_averages(player_data["games"], 5, pool_size=10)
                    
                    result = self.intragame_algo.simulate_intragame(
                        actual_stats, season_avg, last_5_avg, investment_amount
                    )
                    
                    # Calculate P&L with 1% fee (bank perspective)
                    price_change_pct = result['price_change_pct'] / 100
                    user_pnl = investment_amount * price_change_pct
                    fee = investment_amount * 0.01  # 1% fee
                    bank_pnl = fee - user_pnl  # Bank profits from fee, loses from user gains
                    
                    # Store result
                    trade = {
                        'player': player_name,
                        'old_price': result['old_price'],
                        'new_price': result['new_price'],
                        'price_change_pct': result['price_change_pct'],
                        'investment': investment_amount,
                        'user_pnl': user_pnl,
                        'fee': fee,
                        'bank_pnl': bank_pnl,
                        'new_value': investment_amount + user_pnl - fee,
                        'pps': result['pps'],
                        'timestamp': len(self.test_results['intragame']['trades']) + 1
                    }
                    
                    self.test_results['intragame']['trades'].append(trade)
                    self.test_results['intragame']['total_pnl'] += bank_pnl
                    
                else:
                    # Run timeframe simulation
                    games = player_data["games"]
                    season_avg = player_data["season_avg_2024"]
                    
                    # Determine number of games based on timeframe
                    if algorithm == "weekly":
                        num_games = 4
                        sampled_games = random.sample(games, min(4, len(games)))
                    elif algorithm == "monthly":
                        num_games = 12
                        sampled_games = random.sample(games, min(12, len(games)))
                    else:  # season
                        num_games = len(games)
                        sampled_games = games
                    
                    recent_avg = self.sports_market.calculate_last_n_averages(games, len(sampled_games))
                    
                    # Calculate actual totals
                    actual_totals = [0] * 7
                    for game in sampled_games:
                        for i in range(7):
                            actual_totals[i] += game[i]
                    
                    # Run simulation
                    if algorithm == "season":
                        season_avg_2023 = player_data["season_avg_2023"]
                        result = self.timeframe_algo.simulate_timeframe(
                            tuple(actual_totals), len(sampled_games), season_avg_2023, recent_avg, investment_amount, algorithm, use_2023_stats=True, player_archetype=None
                        )
                    else:
                        result = self.timeframe_algo.simulate_timeframe(
                            tuple(actual_totals), len(sampled_games), season_avg, recent_avg, investment_amount, algorithm, player_archetype=None
                        )
                    
                    # Calculate P&L with 1% fee (bank perspective)
                    price_change_pct = result['price_change_pct'] / 100
                    user_pnl = investment_amount * price_change_pct
                    fee = investment_amount * 0.01  # 1% fee
                    bank_pnl = fee - user_pnl  # Bank profits from fee, loses from user gains
                    
                    # Store result
                    trade = {
                        'player': player_name,
                        'old_price': result['old_price'],
                        'new_price': result['new_price'],
                        'price_change_pct': result['price_change_pct'],
                        'investment': investment_amount,
                        'user_pnl': user_pnl,
                        'fee': fee,
                        'bank_pnl': bank_pnl,
                        'new_value': investment_amount + user_pnl - fee,
                        'pps': result['pps'],
                        'timeframe': algorithm,
                        'timestamp': len(self.test_results[algorithm]['trades']) + 1
                    }
                    
                    self.test_results[algorithm]['trades'].append(trade)
                    self.test_results[algorithm]['total_pnl'] += bank_pnl
                
                completed += 1
                
                # Show progress every 10 simulations
                if completed % 10 == 0:
                    progress = (completed / total_simulations) * 100
                    print(f"{progress:.0f}% ", end="", flush=True)
        
        print("\n✅ Automated testing completed!")
        print(f"Total simulations run: {completed}")
        
        # Display results
        self.display_test_results()
        
        # Ask if user wants to export results
        export_choice = input("\nExport results to file? (y/n): ").lower()
        if export_choice == 'y':
            self.export_test_results()
    
    def run_timeframe_simulation(self):
        """Run timeframe simulation"""
        print("\n📅 TIMEFRAME/SEASON SIMULATION")
        print("-" * 30)
        
        # Choose timeframe
        print("Select timeframe:")
        print("1. Weekly (4 games)")
        print("2. Monthly (12 games)")
        print("3. Season")
        
        timeframe_choice = input("Enter choice (1-3): ")
        timeframe_map = {"1": "weekly", "2": "monthly", "3": "season"}
        timeframe = timeframe_map.get(timeframe_choice)
        
        if not timeframe:
            print("Invalid choice.")
            return None
        
        # Choose player or custom input
        choice = input("Use stored player data? (y/n): ").lower()
        
        if choice == 'y':
            return self.run_timeframe_with_player(timeframe)
        else:
            return self.run_timeframe_custom(timeframe)
    
    def run_timeframe_with_player(self, timeframe):
        """Run timeframe simulation with stored player data"""
        print("\nAvailable players:")
        players = self.sports_market.list_players()
        for i, player in enumerate(players, 1):
            print(f"{i}. {player}")
        
        try:
            player_idx = int(input("Select player (number): ")) - 1
            player_name = players[player_idx]
            player_data = self.sports_market.get_player_data(player_name)
            
            games = player_data["games"]
            season_avg = player_data["season_avg_2024"]
            
            # Determine number of games and recent averages based on timeframe
            if timeframe == "weekly":
                num_games = 4
                recent_games = games[-4:] if len(games) >= 4 else games
            elif timeframe == "monthly":
                num_games = 12
                recent_games = games[-12:] if len(games) >= 12 else games
            else:  # season
                num_games = len(games)
                recent_games = games
            
            recent_avg = self.sports_market.calculate_last_n_averages(games, len(recent_games))
            
            # Calculate actual totals from random game samples
            import random
            if timeframe == "weekly":
                sampled_games = random.sample(games, min(4, len(games)))
            elif timeframe == "monthly":
                sampled_games = random.sample(games, min(12, len(games)))
            else:  # season
                sampled_games = games
            
            actual_totals = [0] * 7
            for game in sampled_games:
                for i in range(7):
                    actual_totals[i] += game[i]
            
            print(f"\nUsing {player_name} {timeframe} data:")
            print(f"Games: {len(sampled_games)}")
            print(f"Actual Totals: PTS={actual_totals[0]}, REB={actual_totals[1]}, AST={actual_totals[2]}, TO={actual_totals[3]}, STOCKS={actual_totals[4]}, 3PM={actual_totals[5]}, TS%={actual_totals[6]:.3f}")
            
            old_price = float(input("Enter current stock price: $"))
            
            # For season simulations, use 2023-2024 stats as baseline
            if timeframe == "season":
                season_avg_2023 = player_data["season_avg_2023"]
                result = self.timeframe_algo.simulate_timeframe(
                    tuple(actual_totals), len(sampled_games), season_avg_2023, recent_avg, old_price, timeframe, use_2023_stats=True, player_archetype=None
                )
            else:
                result = self.timeframe_algo.simulate_timeframe(
                    tuple(actual_totals), len(sampled_games), season_avg, recent_avg, old_price, timeframe, player_archetype=None
                )
            
            self.display_timeframe_results(result)
            return result
            
        except (ValueError, IndexError):
            print("Invalid selection.")
            return None
    
    def run_timeframe_custom(self, timeframe):
        """Run timeframe simulation with custom input"""
        print(f"\nEnter {timeframe} totals:")
        try:
            total_pts = float(input("Total Points: "))
            total_reb = float(input("Total Rebounds: "))
            total_ast = float(input("Total Assists: "))
            total_to = float(input("Total Turnovers: "))
            total_stocks = float(input("Total Steals + Blocks: "))
            total_threepm = float(input("Total 3-Pointers: "))
            total_ts_pct = float(input("Average True Shooting %: "))
            
            actual_totals = (total_pts, total_reb, total_ast, total_to, total_stocks, total_threepm, total_ts_pct)
            
            num_games = int(input(f"Number of games in {timeframe}: "))
            
            print("\nEnter season averages:")
            season_pts = float(input("Points per game: "))
            season_reb = float(input("Rebounds per game: "))
            season_ast = float(input("Assists per game: "))
            season_to = float(input("Turnovers per game: "))
            season_stocks = float(input("Steals + Blocks per game: "))
            season_threepm = float(input("3-Pointers per game: "))
            season_ts_pct = float(input("True Shooting %: "))
            
            season_avg = (season_pts, season_reb, season_ast, season_to, season_stocks, season_threepm, season_ts_pct)
            
            print(f"\nEnter recent {timeframe} averages:")
            recent_pts = float(input("Points per game: "))
            recent_reb = float(input("Rebounds per game: "))
            recent_ast = float(input("Assists per game: "))
            recent_to = float(input("Turnovers per game: "))
            recent_stocks = float(input("Steals + Blocks per game: "))
            recent_threepm = float(input("3-Pointers per game: "))
            recent_ts_pct = float(input("True Shooting %: "))
            
            recent_avg = (recent_pts, recent_reb, recent_ast, recent_to, recent_stocks, recent_threepm, recent_ts_pct)
            
            old_price = float(input("Enter current stock price: $"))
            
            result = self.timeframe_algo.simulate_timeframe(
                actual_totals, num_games, season_avg, recent_avg, old_price, timeframe, player_archetype=None
            )
            
            self.display_timeframe_results(result)
            return result
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return None
    
    def display_timeframe_results(self, result):
        """Display timeframe simulation results"""
        print(f"\n📊 {result['timeframe'].upper()} SIMULATION RESULTS:")
        print(f"Projected Stats: {result['projected_stats']}")
        print(f"Standard Deviations: {result['standard_deviations']}")
        print(f"Actual Averages: {result['actual_averages']}")
        print(f"Z-Scores: {result['z_scores']}")
        print(f"PPS: {result['pps']:.3f}")
        print(f"DIS: {result['dis']:.3f}")
        print(f"Raw Delta: {result['raw_delta']:.3f}")
        print(f"Dampened Delta: {result['dampened_delta']:.3f}")
        print(f"Old Price: ${result['old_price']:.2f}")
        print(f"New Price: ${result['new_price']:.2f}")
        print(f"Price Change: {result['price_change_pct']:+.2f}%")
    
    def analyze_player_pool(self):
        """Analyze the enhanced player pool"""
        players = self.sports_market.list_players()
        
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
            player_data = self.sports_market.get_player_data(player_name)
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
        
        import numpy as np
        all_stats = []
        for player_name in players:
            player_data = self.sports_market.get_player_data(player_name)
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
    
    def run_player_type_simulations(self):
        """Run simulations for specific player types or all types"""
        # Get player categories
        player_categories = self.analyze_player_pool()
        
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
                self.run_all_player_type_simulations(player_categories)
            elif choice == len(category_list) + 2:
                return
            elif 1 <= choice <= len(category_list):
                # Run simulations for specific player type
                category, players_list = category_list[choice - 1]
                self.run_single_player_type_simulations(category, players_list)
            else:
                print("Invalid choice.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def run_single_player_type_simulations(self, category, players_list):
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
            results = self.run_player_type_simulations_core(
                category, players_list, num_simulations, investment_amount, algorithms
            )
            
            # Display results
            self.display_player_type_results(category, results, algorithms)
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
    
    def run_all_player_type_simulations(self, player_categories):
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
                    
                    results = self.run_player_type_simulations_core(
                        category, players_list, num_simulations, investment_amount, algorithms
                    )
                    
                    all_results[category] = results
            
            # Display comprehensive results
            self.display_all_player_type_results(all_results, algorithms, num_simulations)
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
    
    def run_player_type_simulations_core(self, category, players_list, num_simulations, investment_amount, algorithms):
        """Core simulation logic for player types"""
        import random
        import numpy as np
        
        results = {
            'base_price': {'prices': [], 'prs_scores': []},
            'intragame': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'weekly': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'monthly': {'trades': [], 'total_pnl': 0, 'win_rate': 0},
            'season': {'trades': [], 'total_pnl': 0, 'win_rate': 0}
        }
        
        for player_name, season_avg in players_list:
            player_data = self.sports_market.get_player_data(player_name)
            
            for sim in range(num_simulations):
                # Base Price Simulation
                if "base_price" in algorithms:
                    pts, reb, ast, to, stocks, threepm, ts_pct = season_avg
                    base_result = self.base_price_algo.calculate_base_price(
                        player_stats=(pts, reb, ast, to, stocks, ts_pct),
                        is_rookie=False
                    )
                    results['base_price']['prices'].append(base_result['base_price'])
                    results['base_price']['prs_scores'].append(base_result['prs'])
                
                # Intragame Simulation
                if "intragame" in algorithms:
                    actual_stats = self.sports_market.get_random_game_stats(player_name)
                    season_avg_2024 = player_data["season_avg_2024"]
                    last_5_avg = self.sports_market.calculate_random_recent_averages(player_data["games"], 5, pool_size=10)
                    
                    intragame_result = self.intragame_algo.simulate_intragame(
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
                        
                        recent_avg = self.sports_market.calculate_last_n_averages(games, len(sampled_games))
                        
                        # Calculate actual totals
                        actual_totals = [0] * 7
                        for game in sampled_games:
                            for i in range(7):
                                actual_totals[i] += game[i]
                        
                        # Run simulation
                        if timeframe == "season":
                            season_avg_2023 = player_data["season_avg_2023"]
                            timeframe_result = self.timeframe_algo.simulate_timeframe(
                                tuple(actual_totals), len(sampled_games), season_avg_2023, recent_avg, 
                                investment_amount, timeframe, use_2023_stats=True, player_archetype=category
                            )
                        else:
                            timeframe_result = self.timeframe_algo.simulate_timeframe(
                                tuple(actual_totals), len(sampled_games), season_avg_2024, recent_avg, 
                                investment_amount, timeframe, player_archetype=category
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
    
    def display_player_type_results(self, category, results, algorithms):
        """Display results for a specific player type"""
        import numpy as np
        
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
                    
                    # Calculate P&L per trade statistics
                    pnl_per_trade = [trade['bank_pnl'] for trade in trades]
                    positive_trades = [pnl for pnl in pnl_per_trade if pnl > 0]
                    negative_trades = [pnl for pnl in pnl_per_trade if pnl < 0]
                    
                    print(f"\n📈 {algorithm.upper()} RESULTS:")
                    print(f"  Total Trades: {len(trades)}")
                    print(f"  Average P&L per Trade: ${avg_pnl:+.2f}")
                    print(f"  Median P&L per Trade: ${np.median(pnl_per_trade):+.2f}")
                    print(f"  P&L per Trade Range: ${min(pnl_per_trade):+.2f} to ${max(pnl_per_trade):+.2f}")
                    print(f"  P&L per Trade Std Dev: ${np.std(pnl_per_trade):.2f}")
                    
                    if positive_trades:
                        print(f"  Average Winning Trade: ${np.mean(positive_trades):+.2f}")
                    if negative_trades:
                        print(f"  Average Losing Trade: ${np.mean(negative_trades):+.2f}")
                    
                    print(f"  Bank Win Rate: {win_rate:.1f}%")
                    print(f"  Bank Wins: {int(win_rate * len(trades) / 100)}/{len(trades)}")
                    
                    # Show top 3 best and worst trades
                    sorted_trades = sorted(trades, key=lambda x: x['bank_pnl'], reverse=True)
                    best_trades = [f"${trade['bank_pnl']:+.2f}" for trade in sorted_trades[:3]]
                    worst_trades = [f"${trade['bank_pnl']:+.2f}" for trade in sorted_trades[-3:]]
                    print(f"  Best 3 Trades: {', '.join(best_trades)}")
                    print(f"  Worst 3 Trades: {', '.join(worst_trades)}")
    
    def display_all_player_type_results(self, all_results, algorithms, num_simulations=10):
        """Display comprehensive results for all player types"""
        import numpy as np
        
        print(f"\n📊 COMPREHENSIVE PLAYER TYPE RESULTS")
        print("=" * 80)
        
        # Summary table
        print(f"{'Player Type':<20} {'Players':<8} {'Base Price':<12} {'Avg P&L/Trade':<15} {'Win Rate':<10} {'Best Trade':<12} {'Worst Trade':<12}")
        print("-" * 90)
        
        for category, results in all_results.items():
            if not results:
                continue
            
            # Count players - check all algorithm types for trades
            num_players = 0
            for algo in ['intragame', 'weekly', 'monthly', 'season']:
                if algo in algorithms and results.get(algo, {}).get('trades'):
                    trades = results[algo]['trades']
                    if trades:
                        num_players = len(trades) // num_simulations
                    break
            
            # Base price average
            base_price_avg = f"${np.mean(results['base_price']['prices']):.1f}" if 'base_price' in algorithms else "N/A"
            
            # P&L per trade statistics - check all algorithm types
            avg_pnl_str = "N/A"
            win_rate_str = "N/A"
            best_trade_str = "N/A"
            worst_trade_str = "N/A"
            
            # Check intragame first
            if 'intragame' in algorithms and results.get('intragame', {}).get('trades'):
                trades = results['intragame']['trades']
                avg_pnl_per_trade = np.mean([trade['bank_pnl'] for trade in trades])
                win_rate = results['intragame']['win_rate']
                best_trade = max([trade['bank_pnl'] for trade in trades])
                worst_trade = min([trade['bank_pnl'] for trade in trades])
                
                avg_pnl_str = f"${avg_pnl_per_trade:+.2f}"
                win_rate_str = f"{win_rate:.1f}%"
                best_trade_str = f"${best_trade:+.1f}"
                worst_trade_str = f"${worst_trade:+.1f}"
            
            # Check timeframe algorithms if intragame not available
            elif any(algo in algorithms for algo in ['weekly', 'monthly', 'season']):
                # Find the first available timeframe algorithm
                for algo in ['weekly', 'monthly', 'season']:
                    if algo in algorithms and results.get(algo, {}).get('trades'):
                        trades = results[algo]['trades']
                        avg_pnl_per_trade = np.mean([trade['bank_pnl'] for trade in trades])
                        win_rate = results[algo]['win_rate']
                        best_trade = max([trade['bank_pnl'] for trade in trades])
                        worst_trade = min([trade['bank_pnl'] for trade in trades])
                        
                        avg_pnl_str = f"${avg_pnl_per_trade:+.2f}"
                        win_rate_str = f"{win_rate:.1f}%"
                        best_trade_str = f"${best_trade:+.1f}"
                        worst_trade_str = f"${worst_trade:+.1f}"
                        break
            
            print(f"{category:<20} {num_players:<8} {base_price_avg:<12} {avg_pnl_str:<15} {win_rate_str:<10} {best_trade_str:<12} {worst_trade_str:<12}")
        
        # Overall summary
        print("\n📈 OVERALL SUMMARY:")
        total_pnl = 0
        total_trades = 0
        
        # Sum across all algorithm types
        for results in all_results.values():
            for algo in ['intragame', 'weekly', 'monthly', 'season']:
                if algo in results and results[algo]['trades']:
                    total_pnl += results[algo]['total_pnl']
                    total_trades += len(results[algo]['trades'])
        
        if total_trades > 0:
            overall_avg_pnl = total_pnl / total_trades
            print(f"  Total Trades: {total_trades}")
            print(f"  Average P&L per Trade: ${overall_avg_pnl:+.2f}")
            print(f"  Total P&L across all player types: ${total_pnl:+.2f}")
    
    def run(self):
        """Main run loop"""
        while True:
            self.print_welcome()
            
            choice = input("\nEnter your choice (1-8): ")
            
            if choice == "1":
                self.run_base_price_simulation()
            elif choice == "2":
                self.run_intragame_simulation()
            elif choice == "3":
                self.run_timeframe_simulation()
            elif choice == "4":
                print("\nCustom input options:")
                print("1. Base Price")
                print("2. Intragame")
                print("3. Timeframe")
                custom_choice = input("Select algorithm (1-3): ")
                if custom_choice == "1":
                    self.run_base_price_custom()
                elif custom_choice == "2":
                    self.run_intragame_custom()
                elif custom_choice == "3":
                    self.run_timeframe_simulation()
                else:
                    print("Invalid choice.")
            elif choice == "5":
                self.calculate_all_base_prices()
            elif choice == "6":
                self.run_profitability_testing()
            elif choice == "7":
                self.run_player_type_simulations()
            elif choice == "8":
                print("\nThank you for using Sports Market Simulation!")
                break
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    simulator = SportsMarketSimulator()
    simulator.run() 