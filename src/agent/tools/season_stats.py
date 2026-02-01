def get_season_stats(yahoo_client):
    """
    Retrieves season statistics from the Yahoo Fantasy Football API.

    Args:
        yahoo_client: An instance of YahooClient to make API requests.

    Returns:
        A dictionary containing season statistics.
    """
    # Define the endpoint for season statistics
    endpoint = "/fantasy/v2/season/stats"
    
    # Make the API request
    response = yahoo_client.get(endpoint)
    
    # Check if the response is successful
    if response.status_code == 200:
        return response.json()  # Return the JSON data if successful
    else:
        raise Exception(f"Error retrieving season stats: {response.status_code} - {response.text}")

def format_season_stats(stats):
    """
    Formats the season statistics for display.

    Args:
        stats: A dictionary containing season statistics.

    Returns:
        A formatted string representation of the statistics.
    """
    formatted_stats = "Season Statistics:\n"
    
    for key, value in stats.items():
        formatted_stats += f"{key}: {value}\n"
    
    return formatted_stats.strip()  # Remove trailing newline characters