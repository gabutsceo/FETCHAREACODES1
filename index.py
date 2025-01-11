import requests
import json
import time
import os

# Function to fetch area codes for a given city and state, using a proxy
def fetch_area_codes(city, state, api_key, proxies=None):
    api_url = f'https://api.api-ninjas.com/v1/zipcode?city={city}&state={state}'
    headers = {'X-Api-Key': api_key}
    
    retries = 3  # Retry count for failed connections
    for attempt in range(retries):
        try:
            response = requests.get(api_url, headers=headers, proxies=proxies)
            
            # If the request was successful
            if response.status_code == requests.codes.ok:
                data = response.json()
                if data and "area_codes" in data[0]:
                    print(f"Data found for {city}, {state}")
                    return data[0]["area_codes"]
                else:
                    print(f"No area codes found for {city}, {state}")
                    log_missing_city(city, state)
                    return []
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {city}, {state}, attempt {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                print(f"Retrying...")
                time.sleep(5)  # wait before retry
            else:
                log_error(f"Failed to fetch data for {city}, {state} after {retries} attempts.")
                log_missing_city(city, state)
                return []

    # If we exhausted retries and couldn't fetch the data
    return []

# Function to load existing data from a JSON file
def load_existing_data(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Existing file '{filepath}' contains invalid JSON. Starting fresh.")
    return {}

# Function to merge new data with existing data
def merge_area_codes(existing_data, new_data):
    for code, cities in new_data.items():
        if code not in existing_data:
            # If the area code does not exist in existing data, initialize a list with the cities
            existing_data[code] = cities
        else:
            # If the area code exists, merge the cities list
            # Ensure existing_data[code] is always a list
            if isinstance(existing_data[code], str):  # if it's a string, make it a list
                existing_data[code] = [existing_data[code]]
            
            for city in cities:
                if city not in existing_data[code]:
                    existing_data[code].append(city)
            
            # Sort and deduplicate
            existing_data[code] = sorted(set(existing_data[code]))
    return existing_data

# Function to save data incrementally
def save_incrementally(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# Function to configure the proxy
def configure_proxy():
    # Proxy credentials and URL setup
    username = "52xrymt17qdjxdn-odds-6+100"
    password = "00h90dhkmyeephq"
    proxy = "rp.scrapegw.com:6060"
    proxy_auth = "{}:{}@{}".format(username, password, proxy)
    
    # Create the proxy dictionary for requests
    proxies = {
        "http": "http://{}".format(proxy_auth),
        "https": "http://{}".format(proxy_auth)
    }
    return proxies

# Function to log errors to a file
def log_error(message):
    error_file = 'error_log.txt'
    with open(error_file, 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {message}\n")
    print(f"Error logged: {message}")

# Function to log cities that were not found
def log_missing_city(city, state):
    with open('not_found_cities.txt', 'a') as f:
        f.write(f"{city}, {state}\n")
    print(f"City not found: {city}, {state}. Logged to not_found_cities.txt")

# Main script
def main():
    # Configure proxy
    proxies = configure_proxy()
    
    # Prompt user for input file
    input_file = input("Enter the file name containing city names (e.g., CA.txt): ").strip()
    
    # Ensure the input file exists
    if not os.path.exists(input_file):
        log_error(f"File '{input_file}' not found.")
        print(f"Error: File '{input_file}' not found.")
        return
    
    # API key
    api_key = 'B7Q2JsSu15d6FT5bwGN3Jw==qE2l9hny25WV2buS'

    # Output folder
    output_folder = 'result_city'
    os.makedirs(output_folder, exist_ok=True)
    
    # Get state input from user
    state = input("Enter the state (e.g., CA, OR, TX): ").strip()
    
    # Output file path
    output_file = os.path.join(output_folder, f'result_{state}.json')
    
    # Load existing data if file exists
    existing_data = load_existing_data(output_file)
    
    # Load city names from the file
    with open(input_file, 'r') as f:
        cities = [line.strip() for line in f if line.strip()]
    
    # List to track cities that failed to fetch area codes
    missing_cities = []

    # Fetch area codes for each city
    for city in cities:
        print(f"Fetching area codes for {city}, {state}...")
        area_codes = fetch_area_codes(city, state, api_key, proxies)
        
        if area_codes:
            # Store new area codes and cities
            new_area_code_map = {}
            for code in area_codes:
                if code not in new_area_code_map:
                    new_area_code_map[code] = []
                new_area_code_map[code].append(city)
            
            # Merge new data with existing data
            updated_data = merge_area_codes(existing_data, new_area_code_map)
            
            # Save incrementally after each request
            save_incrementally(updated_data, output_file)
        else:
            # If no area codes found, log the city
            missing_cities.append(f"{city}, {state}")
        
        # Delay before the next request
        time.sleep(5)

    # Log missing cities if any
    if missing_cities:
        with open('not_found_cities.txt', 'a') as f:
            for city in missing_cities:
                f.write(f"{city}\n")
        print(f"Cities not found: {', '.join(missing_cities)}. Logged to not_found_cities.txt")

    print(f"Results synchronized and saved incrementally to {output_file}")



if __name__ == "__main__":
    main()
