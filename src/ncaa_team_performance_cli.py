import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os
from datetime import datetime

class NCAABasketballAnalyzer:
    def __init__(self):
        self.games_data = None
        self.teams_data = None
        self.team_performances = None
        self.selected_team = None
        self.date_range = {'start': None, 'end': None}
    
    def load_data(self, games_file, teams_file):
        """Load and parse games and teams data from CSV files"""
        print(f"Loading data from {games_file} and {teams_file}...")
        
        try:
            # Parse games data
            games_raw = pd.read_csv(games_file, header=None)
            self.games_data = pd.DataFrame({
                'GameID': games_raw.iloc[:, 0],
                'Date': games_raw.iloc[:, 1],
                'TeamID1': games_raw.iloc[:, 2],
                'Location1': games_raw.iloc[:, 3],
                'Score1': games_raw.iloc[:, 4],
                'TeamID2': games_raw.iloc[:, 5],
                'Location2': games_raw.iloc[:, 6],
                'Score2': games_raw.iloc[:, 7]
            })
            
            # Add win/loss columns
            self.games_data['Win1'] = (self.games_data['Score1'] > self.games_data['Score2']).astype(int)
            self.games_data['Loss1'] = (self.games_data['Score1'] < self.games_data['Score2']).astype(int) 
            self.games_data['Win2'] = (self.games_data['Score1'] < self.games_data['Score2']).astype(int)
            self.games_data['Loss2'] = (self.games_data['Score1'] > self.games_data['Score2']).astype(int)
            
            # Parse teams data
            teams_raw = pd.read_csv(teams_file, header=0)
            self.teams_data = pd.DataFrame({
                'TeamID': teams_raw.iloc[:, 0].astype(int),
                'TeamName': teams_raw.iloc[:, 1]
            })
            
            print(f"Loaded {len(self.games_data)} games and {len(self.teams_data)} teams.")
            
            # Generate team performance stats
            self.generate_team_stats()
            
            return True
        
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def generate_team_stats(self):
        """Generate performance statistics for all teams"""
        print("Generating team statistics...")
        
        # Create teams dictionary for quick lookup
        teams_dict = self.teams_data.set_index('TeamID')['TeamName'].to_dict()
        
        # Initialize dictionary to store team performances
        team_performances = {}
        
        # Process each game
        for _, game in self.games_data.iterrows():
            # Process Team 1
            if game['TeamID1'] not in team_performances:
                team_performances[game['TeamID1']] = {
                    'TeamID': game['TeamID1'],
                    'TeamName': teams_dict.get(game['TeamID1'], f"Team {game['TeamID1']}"),
                    'TotalWins': 0,
                    'TotalLosses': 0,
                    'HomeWins': 0,
                    'HomeLosses': 0,
                    'AwayWins': 0,
                    'AwayLosses': 0,
                    'NeutralWins': 0,
                    'NeutralLosses': 0,
                    'GameHistory': []
                }
            
            team1 = team_performances[game['TeamID1']]
            
            # Update wins/losses
            if game['Win1'] == 1:
                team1['TotalWins'] += 1
                if game['Location1'] == 1:
                    team1['HomeWins'] += 1
                elif game['Location1'] == -1:
                    team1['AwayWins'] += 1
                else:
                    team1['NeutralWins'] += 1
            else:
                team1['TotalLosses'] += 1
                if game['Location1'] == 1:
                    team1['HomeLosses'] += 1
                elif game['Location1'] == -1:
                    team1['AwayLosses'] += 1
                else:
                    team1['NeutralLosses'] += 1
            
            # Add to game history
            team1['GameHistory'].append({
                'GameID': game['GameID'],
                'Date': game['Date'],
                'OpponentID': game['TeamID2'],
                'OpponentName': teams_dict.get(game['TeamID2'], f"Team {game['TeamID2']}"),
                'Location': game['Location1'],
                'Score': game['Score1'],
                'OpponentScore': game['Score2'],
                'Win': game['Win1'],
                'Loss': game['Loss1']
            })
            
            # Process Team 2 (similar logic)
            if game['TeamID2'] not in team_performances:
                team_performances[game['TeamID2']] = {
                    'TeamID': game['TeamID2'],
                    'TeamName': teams_dict.get(game['TeamID2'], f"Team {game['TeamID2']}"),
                    'TotalWins': 0,
                    'TotalLosses': 0,
                    'HomeWins': 0,
                    'HomeLosses': 0,
                    'AwayWins': 0,
                    'AwayLosses': 0,
                    'NeutralWins': 0,
                    'NeutralLosses': 0,
                    'GameHistory': []
                }
            
            team2 = team_performances[game['TeamID2']]
            
            # Update wins/losses
            if game['Win2'] == 1:
                team2['TotalWins'] += 1
                if game['Location2'] == 1:
                    team2['HomeWins'] += 1
                elif game['Location2'] == -1:
                    team2['AwayWins'] += 1
                else:
                    team2['NeutralWins'] += 1
            else:
                team2['TotalLosses'] += 1
                if game['Location2'] == 1:
                    team2['HomeLosses'] += 1
                elif game['Location2'] == -1:
                    team2['AwayLosses'] += 1
                else:
                    team2['NeutralLosses'] += 1
            
            # Add to game history
            team2['GameHistory'].append({
                'GameID': game['GameID'],
                'Date': game['Date'],
                'OpponentID': game['TeamID1'],
                'OpponentName': teams_dict.get(game['TeamID1'], f"Team {game['TeamID1']}"),
                'Location': game['Location2'],
                'Score': game['Score2'],
                'OpponentScore': game['Score1'],
                'Win': game['Win2'],
                'Loss': game['Loss2']
            })
        
        # Calculate percentages and sort game history for all teams
        for team_id, team in team_performances.items():
            # Sort game history by date
            team['GameHistory'] = sorted(team['GameHistory'], key=lambda x: x['Date'])
            
            # Calculate cumulative performance
            cum_wins = 0
            cum_losses = 0
            team['PerformanceOverTime'] = []
            
            for game in team['GameHistory']:
                if game['Win'] == 1:
                    cum_wins += 1
                else:
                    cum_losses += 1
                
                total_games = cum_wins + cum_losses
                win_pct = (cum_wins / total_games * 100) if total_games > 0 else 0
                
                team['PerformanceOverTime'].append({
                    'Date': game['Date'],
                    'CumulativeWins': cum_wins,
                    'CumulativeLosses': cum_losses,
                    'WinPercentage': round(win_pct, 2),
                    'OpponentName': game['OpponentName']
                })
            
            # Calculate win percentages
            total_games = team['TotalWins'] + team['TotalLosses']
            home_games = team['HomeWins'] + team['HomeLosses']
            away_games = team['AwayWins'] + team['AwayLosses']
            neutral_games = team['NeutralWins'] + team['NeutralLosses']
            
            team['TotalWinPct'] = round((team['TotalWins'] / total_games * 100), 2) if total_games > 0 else 0
            team['HomeWinPct'] = round((team['HomeWins'] / home_games * 100), 2) if home_games > 0 else 0
            team['AwayWinPct'] = round((team['AwayWins'] / away_games * 100), 2) if away_games > 0 else 0
            team['NeutralWinPct'] = round((team['NeutralWins'] / neutral_games * 100), 2) if neutral_games > 0 else 0
        
        # Convert to list
        self.team_performances = list(team_performances.values())
    
    def filter_by_date_range(self, start_date=None, end_date=None):
        """Filter games by date range and regenerate stats"""
        print(f"Filtering date range: {start_date} to {end_date}")
        
        self.date_range['start'] = start_date
        self.date_range['end'] = end_date
        
        if not start_date and not end_date:
            # Reset filter - use all games
            self.generate_team_stats()
            return
        
        # Convert dates to int format
        start = int(start_date.replace('-', '')) if start_date else 0
        end = int(end_date.replace('-', '')) if end_date else 99999999
        
        # Filter games
        filtered_games = self.games_data[
            (self.games_data['Date'] >= start) & 
            (self.games_data['Date'] <= end)
        ]
        
        # Create a backup of the original games
        original_games = self.games_data
        
        # Use filtered games for stats generation
        self.games_data = filtered_games
        self.generate_team_stats()
        
        # Restore original games
        self.games_data = original_games
    
    def select_team(self, team_id=None, team_name=None):
        """Select a team by ID or name"""
        if team_id:
            for team in self.team_performances:
                if team['TeamID'] == team_id:
                    self.selected_team = team
                    return team
        
        elif team_name:
            for team in self.team_performances:
                if team['TeamName'].lower() == team_name.lower():
                    self.selected_team = team
                    return team
        
        print(f"Team not found: ID={team_id}, Name={team_name}")
        return None
    
    def get_top_teams(self, n=10):
        """Get top N teams by win percentage"""
        return sorted(self.team_performances, key=lambda x: x['TotalWinPct'], reverse=True)[:n]
    
    def format_date(self, date_num):
        """Format a date number (YYYYMMDD) to a readable date string"""
        if not date_num:
            return ''
        
        date_str = str(date_num)
        if len(date_str) != 8:
            return date_str
        
        year = date_str[0:4]
        month = date_str[4:6]
        day = date_str[6:8]
        
        return f"{month}/{day}/{year}"
    
    def print_team_list(self):
        """Print a list of teams sorted by win percentage"""
        print("\nTeam List (sorted by win %):")
        print(f"{'Team Name':<30} {'W-L':<10} {'Win %':<6}")
        print("-" * 50)
        
        sorted_teams = sorted(self.team_performances, key=lambda x: x['TotalWinPct'], reverse=True)
        
        for team in sorted_teams:
            print(f"{team['TeamName']:<30} {team['TotalWins']}-{team['TotalLosses']:<6} {team['TotalWinPct']}%")
    
    def print_team_details(self, team=None):
        """Print detailed stats for a selected team"""
        if team is None:
            team = self.selected_team
        
        if team is None:
            print("No team selected.")
            return
        
        print(f"\n{team['TeamName']} Performance Details:")
        print("=" * 50)
        
        print(f"Overall:  {team['TotalWinPct']}% ({team['TotalWins']}-{team['TotalLosses']})")
        print(f"Home:     {team['HomeWinPct']}% ({team['HomeWins']}-{team['HomeLosses']})")
        print(f"Away:     {team['AwayWinPct']}% ({team['AwayWins']}-{team['AwayLosses']})")
        print(f"Neutral:  {team['NeutralWinPct']}% ({team['NeutralWins']}-{team['NeutralLosses']})")
        
        print("\nGame History:")
        print(f"{'Date':<12} {'Opponent':<25} {'Location':<10} {'Result':<6} {'Score':<10}")
        print("-" * 70)
        
        for game in team['GameHistory']:
            location = 'Home' if game['Location'] == 1 else 'Away' if game['Location'] == -1 else 'Neutral'
            result = 'W' if game['Win'] == 1 else 'L'
            print(f"{self.format_date(game['Date']):<12} {game['OpponentName']:<25} {location:<10} {result:<6} {game['Score']}-{game['OpponentScore']:<4}")
    
    def plot_win_percentage_over_time(self, team=None):
        """Plot win percentage over time for a team"""
        if team is None:
            team = self.selected_team
        
        if team is None:
            print("No team selected for plotting.")
            return
        
        # Extract data
        perf = team['PerformanceOverTime']
        dates = [self.format_date(p['Date']) for p in perf]
        win_pcts = [p['WinPercentage'] for p in perf]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(dates, win_pcts, 'b-', marker='o')
        
        # Improve readability by showing fewer x-axis labels
        if len(dates) > 10:
            plt.xticks(range(0, len(dates), len(dates) // 10))
        
        plt.title(f"{team['TeamName']} Win Percentage Over Time")
        plt.xlabel('Date')
        plt.ylabel('Win Percentage (%)')
        plt.ylim(0, 100)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save the plot
        filename = f"{team['TeamName'].replace(' ', '_')}_win_pct.png".lower()
        plt.savefig(filename)
        print(f"Plot saved as {filename}")
        
        # Display the plot
        plt.show()
    
    def plot_top_teams(self, n=10):
        """Plot bar chart of top N teams by win percentage"""
        top_teams = self.get_top_teams(n)
        
        team_names = [team['TeamName'] for team in top_teams]
        win_pcts = [team['TotalWinPct'] for team in top_teams]
        
        # Create horizontal bar chart
        plt.figure(figsize=(10, 8))
        bars = plt.barh(team_names, win_pcts, color='purple')
        
        # Add percentage labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2, f"{width}%", 
                     ha='left', va='center')
        
        plt.title(f"Top {n} Teams by Win Percentage")
        plt.xlabel('Win Percentage (%)')
        plt.xlim(0, max(win_pcts) * 1.1)  # Add some space for labels
        plt.grid(True, linestyle='--', alpha=0.7, axis='x')
        plt.tight_layout()
        
        # Save the plot
        plt.savefig('top_teams.png')
        print("Plot saved as top_teams.png")
        
        # Display the plot
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='NCAA Basketball Analysis Tool')
    parser.add_argument('--games', type=str, required=True, help='Path to games CSV file')
    parser.add_argument('--teams', type=str, required=True, help='Path to teams CSV file')
    parser.add_argument('--team', type=str, help='Team name to analyze')
    parser.add_argument('--start-date', type=str, help='Start date filter (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='End date filter (YYYY-MM-DD)')
    parser.add_argument('--list-teams', action='store_true', help='List all teams')
    parser.add_argument('--top-teams', action='store_true', help='Show top 10 teams chart')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = NCAABasketballAnalyzer()
    
    # Load data
    if not analyzer.load_data(args.games, args.teams):
        print("Failed to load data. Exiting.")
        return
    
    # Apply date filter if specified
    if args.start_date or args.end_date:
        analyzer.filter_by_date_range(args.start_date, args.end_date)
    
    # List teams if requested
    if args.list_teams:
        analyzer.print_team_list()
    
    # Select and analyze specific team if requested
    if args.team:
        team = analyzer.select_team(team_name=args.team)
        if team:
            analyzer.print_team_details(team)
            analyzer.plot_win_percentage_over_time(team)
    
    # Show top teams chart if requested
    if args.top_teams:
        analyzer.plot_top_teams()
    
    # If no specific actions were requested, show the team list
    if not (args.list_teams or args.team or args.top_teams):
        analyzer.print_team_list()
        print("\nUse --team [team name] to view details for a specific team")
        print("Use --top-teams to see a chart of the top 10 teams")

if __name__ == "__main__":
    main()
