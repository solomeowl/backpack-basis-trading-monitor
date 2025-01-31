from backpack_exchange_sdk.public import PublicClient
from datetime import datetime
import time
import pandas as pd
import numpy as np

class BackpackBasisTradingMonitor:
    def __init__(self):
        self.client = PublicClient()
        
    def calculate_backpack_basis_funding_stats(self, rates):
        """Calculate funding rate statistics"""
        try:
            # Convert funding rates to numerical values
            funding_rates = [float(rate['fundingRate']) for rate in rates]
            
            # Calculate 7-day metrics (21 intervals as funding rate is paid every 8 hours)
            seven_days = funding_rates[:21] if len(funding_rates) >= 21 else funding_rates
            positive_count = sum(1 for rate in seven_days if rate > 0)
            positive_percentage = (positive_count / len(seven_days)) * 100
            
            stats = {
                'current_rate': funding_rates[0],        # Latest funding rate
                'last_day': np.mean(funding_rates[:3]),  # Last 24h (3 intervals)
                'last_week': np.mean(seven_days),        # Last 7d
                'min_rate': min(seven_days),            # Min rate in 7 days
                'max_rate': max(seven_days),            # Max rate in 7 days
                'positive_count': positive_count,        # Count of positive rates
                'total_count': len(seven_days),         # Total number of rates
                'positive_percentage': positive_percentage # Percentage of positive rates
            }
            
            # Calculate annualized returns
            stats['annual_current'] = stats['current_rate'] * 1095 * 100  # Current APR
            stats['annual_day'] = stats['last_day'] * 1095 * 100         # 24h average APR
            stats['annual_week'] = stats['last_week'] * 1095 * 100       # 7d average APR
            
            return stats
        except Exception as e:
            print(f"Error calculating funding stats: {str(e)}")
            return None

    def monitor_backpack_basis_opportunities(self, min_annual_return=10):
        """Monitor arbitrage opportunities"""
        while True:
            try:
                print(f"\n🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 150)
                print("| Symbol  | Spot Price | Perp Price | Current FR | 24h Avg FR | 7d Avg FR | Current APR | 24h APR | 7d APR | Min FR 7d | Max FR 7d | Positive FR | Basis % |")
                print("| (Pair)  | (USDC)    | (USDC)     | (8h Rate)  | (Mean)     | (Mean)    | (Annual)    | (Mean)  | (Mean) | (7 days)  | (7 days)  | (7d Count) | (Spread)|")
                print("-" * 150)

                # Get all available markets
                markets = self.client.get_markets()
                # Filter for spot markets ending with USDC
                spot_markets = {market['symbol'].split('_')[0] for market in markets if market['symbol'].endswith('_USDC') and not market['symbol'].endswith('_PERP')}
                # Filter for perpetual markets
                perp_markets = {market['symbol'].split('_')[0] for market in markets if market['symbol'].endswith('_USDC_PERP')}
                # Find assets that have both spot and perpetual markets
                base_assets = spot_markets.intersection(perp_markets)

                for base in base_assets:
                    try:
                        spot_symbol = f"{base}_USDC"
                        perp_symbol = f"{base}_USDC_PERP"
                        
                        # Get spot price
                        spot_ticker = self.client.get_ticker(spot_symbol)
                        spot_price = float(spot_ticker['lastPrice'])

                        # Get perpetual futures price
                        perp_ticker = self.client.get_ticker(perp_symbol)
                        perp_price = float(perp_ticker['lastPrice'])

                        # Get funding rate history
                        funding_rates = self.client.get_funding_interval_rates(perp_symbol)
                        stats = self.calculate_backpack_basis_funding_stats(funding_rates)
                        
                        if stats:
                            # Calculate basis (price difference)
                            basis = ((perp_price - spot_price) / spot_price * 100)

                            # Format output
                            output = (
                                f"| {base:<7} | "
                                f"{spot_price:<9.2f} | "
                                f"{perp_price:<9.2f} | "
                                f"{stats['current_rate']:>8.4%} | "
                                f"{stats['last_day']:>8.4%} | "
                                f"{stats['last_week']:>8.4%} | "
                                f"{stats['annual_current']:>8.2f}% | "
                                f"{stats['annual_day']:>8.2f}% | "
                                f"{stats['annual_week']:>8.2f}% | "
                                f"{stats['min_rate']:>8.4%} | "
                                f"{stats['max_rate']:>8.4%} | "
                                f"{stats['positive_count']:>3}/{stats['total_count']:<3} | "
                                f"{basis:>6.2f}% |"
                            )

                            # Highlight good opportunities
                            # Green: Good weekly opportunity (7-day average)
                            # Yellow: Good daily opportunity (24h average)
                            if stats['annual_week'] >= min_annual_return and stats['positive_percentage'] >= 75:
                                print(f"\033[92m{output}\033[0m")
                            elif stats['annual_day'] >= min_annual_return:
                                print(f"\033[93m{output}\033[0m")
                            else:
                                print(output)
                    except Exception as e:
                        print(f"Error processing {base}: {str(e)}")

                time.sleep(10)  # Update every 10 seconds

            except Exception as e:
                print(f"Monitoring error: {str(e)}")
                print("Retrying in 5 seconds...")
                time.sleep(5)

if __name__ == "__main__":
    monitor = BackpackBasisTradingMonitor()
    
    print("\n🔍 Advanced Backpack Basis Trading Monitor")
    print("\nLegend:")
    print("🟢 Green: 7-day average APR > 10% AND positive funding rate > 75%")
    print("🟡 Yellow: 24h average APR > 10%")
    print("\nStrategy: Long Spot + Short Perpetual Futures")
    print("Note: Funding Rate is paid every 8 hours\n")
    monitor.monitor_backpack_basis_opportunities()