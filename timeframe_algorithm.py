import numpy as np
import math

class TimeframeAlgorithm:
    def __init__(self):
        pass
    
    def calculate_projected_stats(self, season_avg, recent_avg, timeframe, use_2023_stats=False, player_archetype=None):
        """
        Calculate projected stats per game based on timeframe
        
        Args:
            season_avg: tuple of season averages (2024-2025)
            recent_avg: tuple of recent averages
            timeframe: str, 'weekly', 'monthly', or 'season'
            use_2023_stats: bool, if True, use 2023-2024 stats for season projections
            player_archetype: str, player archetype for projection adjustments
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
            
            # Apply archetype-specific monthly projection adjustments
            if player_archetype == "Superstars":
                projected = [stat * 1.0212 for stat in projected]
            elif player_archetype == "Elite Shooters":
                projected = [stat * 1.002 for stat in projected]
            elif player_archetype == "Elite Defenders":
                projected = [stat * 0.99685 for stat in projected]
            elif player_archetype == "Elite Playmakers":
                projected = [stat * 1.02 for stat in projected]
            elif player_archetype == "Rebounding Machines":
                projected = [stat * 0.999 for stat in projected]
            elif player_archetype == "Turnover Prone":
                projected = [stat * 0.9885 for stat in projected]
            elif player_archetype == "One Dimensional":
                projected = [stat * 1.008 for stat in projected]
            elif player_archetype == "Versatile":
                projected = [stat * 1.0325 for stat in projected]
            elif player_archetype == "Role Players":
                projected = [stat * 1.0035 for stat in projected]
            elif player_archetype == "High Volume Scorers":
                projected = [stat * 1.001 for stat in projected]
            elif player_archetype == "High Efficiency":
                projected = [stat * 1.0008 for stat in projected]
        elif timeframe == "season":
            if use_2023_stats:
                # Season: Use 2023-2024 season averages as baseline
                projected = list(season_avg)  # season_avg will be 2023-2024 stats
            else:
                # Season: Use 2024-2025 season averages
                projected = list(season_avg)
        else:
            raise ValueError("Invalid timeframe. Use 'weekly', 'monthly', or 'season'")
        
        # Apply archetype-specific projection multiplier
        if player_archetype == "Superstars" and timeframe == "weekly":
            # Boost weekly superstar projections by 3.25%
            projected = [stat * 1.035 for stat in projected]
        elif player_archetype == "Elite Playmakers" and timeframe == "weekly":
            # Boost weekly elite playmaker projections by 3.25% (2.5% + 0.75%)
            projected = [stat * 1.035 for stat in projected]
        elif player_archetype == "Versatile" and timeframe == "weekly":
            # Boost weekly versatile projections by 4.25% (3% + 1% + 0.5% - 0.25%)
            projected = [stat * 1.045 for stat in projected]
        elif player_archetype == "One Dimensional" and timeframe == "weekly":
            # Boost weekly one dimensional projections by 0.5%
            projected = [stat * 1.0105 for stat in projected]
        elif player_archetype == "Role Players" and timeframe == "weekly":
            # Boost weekly role player projections by 0.55% (0.3% + 0.25%)
            projected = [stat * 1.01 for stat in projected]
        elif player_archetype == "Turnover Prone" and timeframe == "weekly":
            # Reduce weekly turnover prone projections by 2%
            projected = [stat * 0.98 for stat in projected]
        elif player_archetype == "Rebounding Machines" and timeframe == "weekly":
            # Reduce weekly rebounding machine projections by 1.3%
            projected = [stat * 0.985 for stat in projected]
        elif player_archetype == "High Volume Scorers" and timeframe == "weekly":
            # Reduce weekly high volume scorer projections by 1.3%
            projected = [stat * 0.995 for stat in projected]
        elif player_archetype == "Bench Warmers" and timeframe == "weekly":
            # Reduce weekly high volume scorer projections by 1.3%
            projected = [stat * 1.003 for stat in projected]
        elif player_archetype == "Elite Shooters" and timeframe == "weekly":
            # Reduce weekly high volume scorer projections by 1.3%
            projected = [stat * 0.9975 for stat in projected]
        
        return tuple(projected)
    
    def calculate_standard_deviations(self, projected_stats, timeframe, player_archetype=None):
        """
        Calculate standard deviations using timeframe-specific alpha values
        """
        pts, reb, ast, to, stocks, threepm, ts_pct = projected_stats
        
        # Define alpha values for each timeframe
        if timeframe == "weekly":
            alphas = self._get_weekly_alphas(player_archetype, projected_stats)
        elif timeframe == "monthly":
            alphas = self._get_monthly_alphas(player_archetype)
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
    
    def _get_weekly_alphas(self, player_archetype, projected_stats):
        """
        Get archetype-specific weekly alpha values
        """
        # Default weekly alphas
        default_alphas = {
            'pts': 1.418,
            'reb': 0.945,
            'ast': 0.945,
            'to': 0.958,
            'stocks': 0.958,
            'threepm': 0.958,
            'ts%': 0.07
        }
        
        if not player_archetype:
            return default_alphas
        
        # Archetype-specific alpha values
        if player_archetype == "Superstars":
            return {
                'pts': 1.6,      # +12.8%
                'reb': 1.1,      # +16.4%
                'ast': 1.1,      # +16.4%
                'to': 0.958,     # unchanged
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "Versatile":
            return {
                'pts': 1.702,    # +20%
                'reb': 1.134,    # +20%
                'ast': 1.134,    # +20%
                'to': 1.150,     # +20%
                'stocks': 1.150, # +20%
                'threepm': 1.150, # +20%
                'ts%': 0.084     # +20%
            }
        elif player_archetype == "Elite Playmakers":
            return {
                'pts': 1.418,    # unchanged
                'reb': 0.945,    # unchanged
                'ast': 1.2,      # +27.0%
                'to': 0.958,     # unchanged
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "High Volume Scorers":
            return {
                'pts': 1.3,      # -8.3%
                'reb': 0.945,    # unchanged
                'ast': 0.945,    # unchanged
                'to': 0.958,     # unchanged
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "Rebounding Machines":
            return {
                'pts': 1.418,    # unchanged
                'reb': 0.85,     # -10.1%
                'ast': 0.945,    # unchanged
                'to': 0.958,     # unchanged
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "Bench Warmers":
            return {
                'pts': 1.021,    # -10% from 1.134 (additional 10% decrease)
                'reb': 0.680,    # -10% from 0.756 (additional 10% decrease)
                'ast': 0.680,    # -10% from 0.756 (additional 10% decrease)
                'to': 0.689,     # -10% from 0.766 (additional 10% decrease)
                'stocks': 0.689, # -10% from 0.766 (additional 10% decrease)
                'threepm': 0.689, # -10% from 0.766 (additional 10% decrease)
                'ts%': 0.050     # -10% from 0.056 (additional 10% decrease)
            }
        elif player_archetype == "Turnover Prone":
            return {
                'pts': 1.418,    # unchanged
                'reb': 0.945,    # unchanged
                'ast': 0.945,    # unchanged
                'to': 1.1,       # +14.8%
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "One Dimensional":
            # Find signature stat (highest stat excluding ts%)
            pts, reb, ast, to, stocks, threepm, ts_pct = projected_stats
            stats = [pts, reb, ast, to, stocks, threepm]
            stat_names = ['pts', 'reb', 'ast', 'to', 'stocks', 'threepm']
            max_index = stats.index(max(stats))
            signature_stat = stat_names[max_index]
            
            # Start with default alphas
            alphas = default_alphas.copy()
            # Raise signature stat by 8%
            alphas[signature_stat] *= 1.08
            return alphas
        elif player_archetype == "Role Players":
            return {
                'pts': 1.489,    # +5%
                'reb': 0.992,    # +5%
                'ast': 0.992,    # +5%
                'to': 1.006,     # +5%
                'stocks': 1.006, # +5%
                'threepm': 1.006, # +5%
                'ts%': 0.074     # +5%
            }
        else:
            # Default for Elite Shooters, Elite Defenders, High Efficiency
            return default_alphas
    
    def _get_monthly_alphas(self, player_archetype):
        """
        Get archetype-specific monthly alpha values
        """
        # Default monthly alphas
        default_alphas = {
            'pts': 0.809,
            'reb': 0.539,
            'ast': 0.539,
            'to': 0.547,
            'stocks': 0.547,
            'threepm': 0.547,
            'ts%': 0.07
        }
        
        if not player_archetype:
            return default_alphas
        
        # Archetype-specific monthly alpha values
        if player_archetype == "Superstars":
            return {
                'pts': 1.011,    # +25% from 0.809
                'reb': 0.674,    # +25% from 0.539
                'ast': 0.674,    # +25% from 0.539
                'to': 0.684,     # +25% from 0.547
                'stocks': 0.684, # +25% from 0.547
                'threepm': 0.684, # +25% from 0.547
                'ts%': 0.088     # +25% from 0.07
            }
        elif player_archetype == "Elite Shooters":
            return {
                'pts': 0.833,    # +3% from 0.809
                'reb': 0.555,    # +3% from 0.539
                'ast': 0.555,    # +3% from 0.539
                'to': 0.563,     # +3% from 0.547
                'stocks': 0.563, # +3% from 0.547
                'threepm': 0.563, # +3% from 0.547
                'ts%': 0.072     # +3% from 0.07
            }
        elif player_archetype == "Elite Playmakers":
            return {
                'pts': 0.971,    # +20% from 0.809
                'reb': 0.647,    # +20% from 0.539
                'ast': 0.647,    # +20% from 0.539
                'to': 0.656,     # +20% from 0.547
                'stocks': 0.656, # +20% from 0.547
                'threepm': 0.656, # +20% from 0.547
                'ts%': 0.084     # +20% from 0.07
            }
        elif player_archetype == "Turnover Prone":
            return {
                'pts': 0.769,    # -5% from 0.809
                'reb': 0.512,    # -5% from 0.539
                'ast': 0.512,    # -5% from 0.539
                'to': 0.520,     # -5% from 0.547
                'stocks': 0.520, # -5% from 0.547
                'threepm': 0.520, # -5% from 0.547
                'ts%': 0.067     # -5% from 0.07
            }
        elif player_archetype == "One Dimensional":
            return {
                'pts': 0.890,    # +10% from 0.809
                'reb': 0.593,    # +10% from 0.539
                'ast': 0.593,    # +10% from 0.539
                'to': 0.602,     # +10% from 0.547
                'stocks': 0.602, # +10% from 0.547
                'threepm': 0.602, # +10% from 0.547
                'ts%': 0.077     # +10% from 0.07
            }
        elif player_archetype == "Versatile":
            return {
                'pts': 1.011,    # +25% from 0.809
                'reb': 0.674,    # +25% from 0.539
                'ast': 0.674,    # +25% from 0.539
                'to': 0.684,     # +25% from 0.547
                'stocks': 0.684, # +25% from 0.547
                'threepm': 0.684, # +25% from 0.547
                'ts%': 0.088     # +25% from 0.07
            }
        elif player_archetype == "Role Players":
            return {
                'pts': 0.849,    # +5% from 0.809
                'reb': 0.566,    # +5% from 0.539
                'ast': 0.566,    # +5% from 0.539
                'to': 0.574,     # +5% from 0.547
                'stocks': 0.574, # +5% from 0.547
                'threepm': 0.574, # +5% from 0.547
                'ts%': 0.074     # +5% from 0.07
            }
        else:
            # Default for other archetypes
            return default_alphas
        
        if not player_archetype:
            return default_alphas
        
        # Archetype-specific alpha values
        if player_archetype == "Superstars":
            return {
                'pts': 1.6,      # +12.8%
                'reb': 1.1,      # +16.4%
                'ast': 1.1,      # +16.4%
                'to': 0.958,     # unchanged
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "Versatile":
            return {
                'pts': 1.702,    # +20%
                'reb': 1.134,    # +20%
                'ast': 1.134,    # +20%
                'to': 1.150,     # +20%
                'stocks': 1.150, # +20%
                'threepm': 1.150, # +20%
                'ts%': 0.084     # +20%
            }
        elif player_archetype == "Elite Playmakers":
            return {
                'pts': 1.418,    # unchanged
                'reb': 0.945,    # unchanged
                'ast': 1.2,      # +27.0%
                'to': 0.958,     # unchanged
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "High Volume Scorers":
            return {
                'pts': 1.3,      # -8.3%
                'reb': 0.945,    # unchanged
                'ast': 0.945,    # unchanged
                'to': 0.958,     # unchanged
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "Rebounding Machines":
            return {
                'pts': 1.418,    # unchanged
                'reb': 0.85,     # -10.1%
                'ast': 0.945,    # unchanged
                'to': 0.958,     # unchanged
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "Bench Warmers":
            return {
                'pts': 1.021,    # -10% from 1.134 (additional 10% decrease)
                'reb': 0.680,    # -10% from 0.756 (additional 10% decrease)
                'ast': 0.680,    # -10% from 0.756 (additional 10% decrease)
                'to': 0.689,     # -10% from 0.766 (additional 10% decrease)
                'stocks': 0.689, # -10% from 0.766 (additional 10% decrease)
                'threepm': 0.689, # -10% from 0.766 (additional 10% decrease)
                'ts%': 0.050     # -10% from 0.056 (additional 10% decrease)
            }
        elif player_archetype == "Turnover Prone":
            return {
                'pts': 1.418,    # unchanged
                'reb': 0.945,    # unchanged
                'ast': 0.945,    # unchanged
                'to': 1.1,       # +14.8%
                'stocks': 0.958, # unchanged
                'threepm': 0.958, # unchanged
                'ts%': 0.07      # unchanged
            }
        elif player_archetype == "One Dimensional":
            # Find signature stat (highest stat excluding ts%)
            pts, reb, ast, to, stocks, threepm, ts_pct = projected_stats
            stats = [pts, reb, ast, to, stocks, threepm]
            stat_names = ['pts', 'reb', 'ast', 'to', 'stocks', 'threepm']
            max_index = stats.index(max(stats))
            signature_stat = stat_names[max_index]
            
            # Start with default alphas
            alphas = default_alphas.copy()
            # Raise signature stat by 8%
            alphas[signature_stat] *= 1.08
            return alphas
        elif player_archetype == "Role Players":
            return {
                'pts': 1.489,    # +5%
                'reb': 0.992,    # +5%
                'ast': 0.992,    # +5%
                'to': 1.006,     # +5%
                'stocks': 1.006, # +5%
                'threepm': 1.006, # +5%
                'ts%': 0.074     # +5%
            }
        else:
            # Default for Elite Shooters, Elite Defenders, High Efficiency
            return default_alphas
    
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
    
    def calculate_pps(self, z_scores, player_archetype=None):
        """
        Calculate PPS (Performance Points Score) with archetype-specific weightings
        """
        # Default weights
        default_weights = {
            'pts': 0.45,
            'reb': 0.15,
            'ast': 0.15,
            'to': 0.05,
            'stocks': 0.10,
            'threepm': 0.05,
            'ts%': 0.05
        }
        
        if not player_archetype:
            weights = default_weights
        else:
            weights = self._get_archetype_weights(player_archetype)
        
        # Calculate PPS
        pps = sum(weights[stat] * z_scores[stat] for stat in weights.keys())
        
        return pps
    
    def _get_archetype_weights(self, player_archetype):
        """
        Get archetype-specific PPS weights for weekly, monthly, and season algorithms
        """
        if player_archetype == "Superstars":
            return {
                'pts': 0.35,
                'reb': 0.125,
                'ast': 0.125,
                'to': 0.075,
                'stocks': 0.125,
                'threepm': 0.10,
                'ts%': 0.10
            }
        elif player_archetype == "Elite Shooters":
            return {
                'pts': 0.45,
                'reb': 0.15,
                'ast': 0.15,
                'to': 0.05,
                'stocks': 0.10,
                'threepm': 0.05,
                'ts%': 0.05
            }
        elif player_archetype == "Elite Defenders":
            return {
                'pts': 0.45,
                'reb': 0.15,
                'ast': 0.15,
                'to': 0.05,
                'stocks': 0.10,
                'threepm': 0.05,
                'ts%': 0.05
            }
        elif player_archetype == "High Volume Scorers":
            return {
                'pts': 0.425,
                'reb': 0.125,
                'ast': 0.125,
                'to': 0.05,
                'stocks': 0.075,
                'threepm': 0.10,
                'ts%': 0.10
            }
        elif player_archetype == "Elite Playmakers":
            return {
                'pts': 0.375,
                'reb': 0.15,
                'ast': 0.225,
                'to': 0.05,
                'stocks': 0.10,
                'threepm': 0.05,
                'ts%': 0.05
            }
        elif player_archetype == "Rebounding Machines":
            return {
                'pts': 0.375,
                'reb': 0.15,
                'ast': 0.225,
                'to': 0.05,
                'stocks': 0.10,
                'threepm': 0.05,
                'ts%': 0.05
            }
        elif player_archetype == "Bench Warmers":
            return {
                'pts': 0.20,
                'reb': 0.175,
                'ast': 0.175,
                'to': 0.05,
                'stocks': 0.15,
                'threepm': 0.10,
                'ts%': 0.15
            }
        elif player_archetype == "High Efficiency":
            return {
                'pts': 0.45,
                'reb': 0.125,
                'ast': 0.15,
                'to': 0.05,
                'stocks': 0.10,
                'threepm': 0.05,
                'ts%': 0.075
            }
        elif player_archetype == "Turnover Prone":
            return {
                'pts': 0.45,
                'reb': 0.15,
                'ast': 0.15,
                'to': 0.025,
                'stocks': 0.10,
                'threepm': 0.05,
                'ts%': 0.075
            }
        elif player_archetype == "One Dimensional":
            return {
                'pts': 0.35,
                'reb': 0.175,
                'ast': 0.175,
                'to': 0.05,
                'stocks': 0.125,
                'threepm': 0.03,
                'ts%': 0.095
            }
        elif player_archetype == "Versatile":
            return {
                'pts': 0.35,
                'reb': 0.125,
                'ast': 0.125,
                'to': 0.075,
                'stocks': 0.125,
                'threepm': 0.10,
                'ts%': 0.10
            }
        elif player_archetype == "Role Players":
            return {
                'pts': 0.425,
                'reb': 0.175,
                'ast': 0.175,
                'to': 0.05,
                'stocks': 0.075,
                'threepm': 0.05,
                'ts%': 0.05
            }
        else:
            # Default weights for unknown archetypes
            return {
                'pts': 0.45,
                'reb': 0.15,
                'ast': 0.15,
                'to': 0.05,
                'stocks': 0.10,
                'threepm': 0.05,
                'ts%': 0.05
            }
    
    def calculate_dis(self, pps, player_archetype=None):
        """
        Calculate Demand Imbalance Score (DIS)
        """
        buy_adj = 15 * pps
        sell_adj = -15 * pps
        
        buys = 50 + buy_adj + 2
        sells = 50 + sell_adj - 2
        
        dis = (buys - sells) / (buys + sells)
        return dis
    
    def calculate_raw_delta(self, pps, dis, player_archetype=None):
        """
        Calculate raw delta
        """
        return 0.8 * pps + 0.2 * dis
    
    def apply_dampening(self, raw_delta, timeframe, player_archetype=None):
        """
        Apply dampening with special rules for season timeframe and archetype-specific dampening
        """
        if raw_delta >= 0:
            # Upside dampening
            if timeframe in ["weekly", "monthly"]:
                if player_archetype == "Superstars":
                    # More aggressive upside dampening for superstars
                    dampened = min(raw_delta / math.sqrt(max(1 - 0.5 * raw_delta**2, 0.001)), 10)
                elif player_archetype == "One Dimensional":
                    # Less aggressive upside dampening for One Dimensional
                    dampened = min(raw_delta / math.sqrt(max(1 - 0.5 * raw_delta**2, 0.001)), 10)
                elif player_archetype == "Bench Warmers":
                    if timeframe == "weekly":
                        # Weekly dampening for Bench Warmers
                        dampened = min(raw_delta / math.sqrt(max(1 - 0.1 * raw_delta**2, 0.001)), 10)
                    else:  # monthly
                        # Monthly dampening for Bench Warmers
                        dampened = min(raw_delta / math.sqrt(max(1 - 0.05 * raw_delta**2, 0.001)), 10)
                elif player_archetype == "Versatile":
                    if timeframe == "weekly":
                        # Weekly dampening for Versatile
                        dampened = min(raw_delta / math.sqrt(max(1 - 0.8 * raw_delta**2, 0.001)), 10)
                    else:  # monthly
                        # Monthly dampening for Versatile
                        dampened = min(raw_delta / math.sqrt(max(1 - 0.1 * raw_delta**2, 0.001)), 10)
                elif player_archetype == "Rebounding Machines":
                    # Standard dampening for Rebounding Machines
                    dampened = min(raw_delta / math.sqrt(max(1 - 0.8 * raw_delta**2, 0.001)), 10)
                else:
                    # Standard dampening for other archetypes
                    dampened = min(raw_delta / math.sqrt(max(1 - 0.5 * raw_delta**2, 0.001)), 10)
            else:  # season
                dampened = min(raw_delta / math.sqrt(max(1 - 0.1 * raw_delta**2, 0.001)), 50)
        else:
            # Downside dampening
            dampened = -1 * (abs(raw_delta)**2 / (abs(raw_delta)**2 + 0.18))
        
        return dampened
    
    def calculate_new_price(self, old_price, dampened_delta):
        """
        Calculate new price and price change percentage
        """
        new_price = old_price * (1 + dampened_delta)
        price_change_pct = dampened_delta * 100
        
        return new_price, price_change_pct
    
    def simulate_timeframe(self, actual_totals, num_games, season_avg, recent_avg, old_price, timeframe, use_2023_stats=False, player_archetype=None):
        """
        Complete timeframe simulation
        
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
        projected_stats = self.calculate_projected_stats(season_avg, recent_avg, timeframe, use_2023_stats, player_archetype)
        
        # Step 2: Calculate standard deviations
        std_devs = self.calculate_standard_deviations(projected_stats, timeframe, player_archetype)
        
        # Step 3: Calculate actual per-game averages
        actual_avg = self.calculate_actual_averages(actual_totals, num_games)
        
        # Step 4: Calculate z-scores
        z_scores = self.calculate_z_scores(actual_avg, projected_stats, std_devs)
        
        # Step 5: Calculate PPS
        pps = self.calculate_pps(z_scores, player_archetype)
        
        # Step 6: Calculate DIS
        dis = self.calculate_dis(pps, player_archetype)
        
        # Step 7: Calculate raw delta
        raw_delta = self.calculate_raw_delta(pps, dis, player_archetype)
        
        # Step 8: Apply dampening
        dampened_delta = self.apply_dampening(raw_delta, timeframe, player_archetype)
        
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