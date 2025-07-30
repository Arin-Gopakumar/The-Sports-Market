import numpy as np
import math

class TimeframeTestAlgorithm:
    def __init__(self):
        pass
    
    def calculate_projected_stats(self, season_avg, recent_avg, timeframe, use_2023_stats=False):
        """
        Calculate projected stats per game based on timeframe (no archetype adjustments)
        
        Args:
            season_avg: tuple of season averages (2024-2025)
            recent_avg: tuple of recent averages
            timeframe: str, 'weekly', 'monthly', or 'season'
            use_2023_stats: bool, if True, use 2023-2024 stats for season projections
        """
        if timeframe == "weekly":
            # Weekly: 0.5 × Season Avg + 0.5 × Last 4 Games Avg
            projected = []
            for i in range(len(season_avg)):
                projected.append(0.5 * season_avg[i] + 0.5 * recent_avg[i])
        elif timeframe == "monthly":
            # Monthly: 0.5 × Season Avg + 0.5 × Last 12 Games Avg
            projected = []
            for i in range(len(season_avg)):
                projected.append(0.5 * season_avg[i] + 0.5 * recent_avg[i])
        elif timeframe == "season":
            if use_2023_stats:
                # Season: Use 2023-2024 season averages as baseline
                projected = list(season_avg)  # season_avg will be 2023-2024 stats
            else:
                # Season: Use 2024-2025 season averages
                projected = list(season_avg)
        else:
            raise ValueError("Invalid timeframe. Use 'weekly', 'monthly', or 'season'")
        
        return tuple(projected)
    
    def calculate_standard_deviations(self, projected_stats, timeframe):
        """
        Calculate standard deviations using timeframe-specific alpha values (no archetype adjustments)
        """
        pts, reb, ast, to, stocks, threepm, ts_pct = projected_stats
        
        # Define alpha values for each timeframe (same for all players)
        if timeframe == "weekly":
            alphas = {
                'pts': 1.418,
                'reb': 0.945,
                'ast': 0.945,
                'to': 0.958,
                'stocks': 0.958,
                'threepm': 0.958,
                'ts%': 0.07
            }
        elif timeframe == "monthly":
            alphas = {
                'pts': 0.809,
                'reb': 0.539,
                'ast': 0.539,
                'to': 0.547,
                'stocks': 0.547,
                'threepm': 0.547,
                'ts%': 0.07
            }
        else:  # season
            alphas = {
                'pts': 0.794,
                'reb': 0.529,
                'ast': 0.529,
                'to': 0.537,
                'stocks': 0.537,
                'threepm': 0.537,
                'ts%': 0.07
            }
        
        std_devs = {
            'pts': alphas['pts'] * math.sqrt(max(pts, 0.1)),
            'reb': alphas['reb'] * math.sqrt(max(reb, 0.1)),
            'ast': alphas['ast'] * math.sqrt(max(ast, 0.1)),
            'to': alphas['to'] * math.sqrt(max(to, 0.1)),
            'stocks': alphas['stocks'] * math.sqrt(max(stocks, 0.1)),
            'threepm': alphas['threepm'] * math.sqrt(max(threepm, 0.1)),
            'ts%': alphas['ts%']  # fixed
        }
        
        return std_devs
    
    def calculate_actual_averages(self, actual_totals, num_games):
        """
        Calculate actual per-game averages from totals
        """
        actual_avg = []
        for total in actual_totals:
            actual_avg.append(total / num_games)
        return tuple(actual_avg)
    
    def calculate_z_scores(self, actual_avg, projected_stats, std_devs):
        """
        Calculate z-scores for each stat
        Note: TO uses (projected - actual) / std dev
        """
        pts, reb, ast, to, stocks, threepm, ts_pct = actual_avg
        proj_pts, proj_reb, proj_ast, proj_to, proj_stocks, proj_threepm, proj_ts_pct = projected_stats
        
        z_scores = {
            'pts': (pts - proj_pts) / std_devs['pts'],
            'reb': (reb - proj_reb) / std_devs['reb'],
            'ast': (ast - proj_ast) / std_devs['ast'],
            'to': (proj_to - to) / std_devs['to'],  # inverted for TO
            'stocks': (stocks - proj_stocks) / std_devs['stocks'],
            'threepm': (threepm - proj_threepm) / std_devs['threepm'],
            'ts%': (ts_pct - proj_ts_pct) / std_devs['ts%']
        }
        
        return z_scores
    
    def calculate_pps(self, z_scores):
        """
        Calculate PPS (Performance Points Score) with default weightings
        """
        # Default weights (same for all players)
        weights = {
            'pts': 0.45,
            'reb': 0.15,
            'ast': 0.15,
            'to': 0.05,
            'stocks': 0.10,
            'threepm': 0.05,
            'ts%': 0.05
        }
        
        pps = sum(weights[stat] * z_scores[stat] for stat in weights.keys())
        return pps
    
    def calculate_dis(self, pps):
        """
        Calculate Demand Imbalance Score (DIS)
        """
        buy_adj = 15 * pps
        sell_adj = -15 * pps
        
        buys = 50 + buy_adj + 2
        sells = 50 + sell_adj - 2
        
        dis = (buys - sells) / (buys + sells)
        return dis
    
    def calculate_raw_delta(self, pps, dis):
        """
        Calculate raw delta
        """
        return 0.8 * pps + 0.2 * dis
    
    def apply_dampening(self, raw_delta, timeframe):
        """
        Apply dampening with timeframe-specific rules (no archetype adjustments)
        """
        if raw_delta >= 0:
            # Upside dampening
            if timeframe == "weekly":
                dampened = min(raw_delta / math.sqrt(max(1 - 0.1 * raw_delta**2, 0.001)), 10)
            elif timeframe == "monthly":
                dampened = min(raw_delta / math.sqrt(max(1 - 0.1 * raw_delta**2, 0.001)), 10)
            else:  # season
                dampened = min(raw_delta / math.sqrt(max(1 - 0.1 * raw_delta**2, 0.001)), 50)
        else:
            # Downside dampening (same for all timeframes)
            dampened = -1 * (abs(raw_delta)**2 / (abs(raw_delta)**2 + 0.18))
        
        return dampened
    
    def calculate_new_price(self, old_price, dampened_delta):
        """
        Calculate new price and price change percentage
        """
        new_price = old_price * (1 + dampened_delta)
        price_change_pct = dampened_delta * 100
        
        return new_price, price_change_pct
    
    def simulate_timeframe(self, actual_totals, num_games, season_avg, recent_avg, old_price, timeframe, use_2023_stats=False):
        """
        Complete timeframe simulation without archetype adjustments
        
        Args:
            actual_totals: tuple of total stats over timeframe
            num_games: int, number of games in timeframe
            season_avg: tuple of season averages
            recent_avg: tuple of recent games averages (4, 12, or season)
            old_price: float, current stock price
            timeframe: str, 'weekly', 'monthly', or 'season'
            use_2023_stats: bool, if True, use 2023-2024 stats for season projections
        
        Returns:
            dict with all calculations and results
        """
        # Step 1: Calculate projected stats per game
        projected_stats = self.calculate_projected_stats(season_avg, recent_avg, timeframe, use_2023_stats)
        
        # Step 2: Calculate standard deviations
        std_devs = self.calculate_standard_deviations(projected_stats, timeframe)
        
        # Step 3: Calculate actual per-game averages
        actual_avg = self.calculate_actual_averages(actual_totals, num_games)
        
        # Step 4: Calculate z-scores
        z_scores = self.calculate_z_scores(actual_avg, projected_stats, std_devs)
        
        # Step 5: Calculate PPS
        pps = self.calculate_pps(z_scores)
        
        # Step 6: Calculate DIS
        dis = self.calculate_dis(pps)
        
        # Step 7: Calculate raw delta
        raw_delta = self.calculate_raw_delta(pps, dis)
        
        # Step 8: Apply dampening
        dampened_delta = self.apply_dampening(raw_delta, timeframe)
        
        # Step 9: Calculate new price
        new_price, price_change_pct = self.calculate_new_price(old_price, dampened_delta)
        
        return {
            'projected_stats': projected_stats,
            'standard_deviations': std_devs,
            'actual_averages': actual_avg,
            'z_scores': z_scores,
            'pps': pps,
            'dis': dis,
            'raw_delta': raw_delta,
            'dampened_delta': dampened_delta,
            'new_price': new_price,
            'price_change_pct': price_change_pct,
            'old_price': old_price,
            'timeframe': timeframe,
            'num_games': num_games
        } 