# If interested in viewing summarized version of the scraped data in python

from bs4 import BeautifulSoup
import pandas as pd
import requests 
import time

# URL for the Premier League standings
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# Fetch and parse the standings data
data = requests.get(standings_url)
time.sleep(5)  # Delay to avoid overwhelming the server
soup = BeautifulSoup(data.text, 'html.parser')

# Extract the standings table
standings_table = soup.select('table.stats_table')[0]

# Check if the standings table exists
if not standings_table:
    print("No standings table found.")

# Extract team links from the standings table
links = [l.get('href') for l in standings_table.find_all('a') if '/squads/' in l.get('href')]
team_urls = [f"https://fbref.com{l}" for l in links]  # Format links to full URLs

# Scrape data for each team
for team_url in team_urls: 
    team_name = team_url.split("/")[-1].replace("-Stats", "")  # Extract team name
    data = requests.get(team_url).text
    soup = BeautifulSoup(data, 'lxml')
    stats = soup.find_all('table', class_="stats_table")[0]  # Get the first stats table

    # Format the stats DataFrame
    if stats and stats.columns: 
        stats.columns = stats.columns.droplevel() 

    team_data = pd.read_html(str(stats))[0]  # Convert to DataFrame
    team_data["Team"] = team_name  # Add team name to DataFrame
    all_teams.append(team_data)  # Append data to the list
    time.sleep(5)  # Delay before the next request

# Combine all team DataFrames and save to CSV
stat_df = pd.concat(all_teams) 
stat_df.to_csv("matches.csv") 
