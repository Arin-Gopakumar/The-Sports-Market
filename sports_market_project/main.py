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
        print("7. Exit")
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
                    tuple(actual_totals), len(sampled_games), season_avg_2023, recent_avg, investment, timeframe, use_2023_stats=True
                )
            else:
                result = self.timeframe_algo.simulate_timeframe(
                    tuple(actual_totals), len(sampled_games), season_avg, recent_avg, investment, timeframe
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
                            tuple(actual_totals), len(sampled_games), season_avg_2023, recent_avg, investment_amount, algorithm, use_2023_stats=True
                        )
                    else:
                        result = self.timeframe_algo.simulate_timeframe(
                            tuple(actual_totals), len(sampled_games), season_avg, recent_avg, investment_amount, algorithm
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
                    tuple(actual_totals), len(sampled_games), season_avg_2023, recent_avg, old_price, timeframe, use_2023_stats=True
                )
            else:
                result = self.timeframe_algo.simulate_timeframe(
                    tuple(actual_totals), len(sampled_games), season_avg, recent_avg, old_price, timeframe
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
                actual_totals, num_games, season_avg, recent_avg, old_price, timeframe
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
    
    def run(self):
        """Main run loop"""
        while True:
            self.print_welcome()
            
            choice = input("\nEnter your choice (1-7): ")
            
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
                print("\nThank you for using Sports Market Simulation!")
                break
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    simulator = SportsMarketSimulator()
    simulator.run() 