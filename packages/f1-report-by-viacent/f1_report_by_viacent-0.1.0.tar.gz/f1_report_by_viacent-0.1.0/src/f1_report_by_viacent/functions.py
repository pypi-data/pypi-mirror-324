from datetime import datetime, timedelta
import os

"""Function to parse log files from the given folder path."""
def parse_logs(folder_path: str):
    abbreviations_file = os.path.join(folder_path, 'abbreviations.txt') #construct path to abbreviations.txt
    start_log = os.path.join(folder_path, 'start.log')                  #construct path to start.log
    end_log = os.path.join(folder_path, 'end.log')                      #construct path to nd.log

    abbreviations = {}                                                  #initialize an empty dictionary to store
    with open(abbreviations_file, 'r', encoding="utf-8") as f:          #open file for reading
        for line in f.read().splitlines():                              #read all lines and process each one
            parts = line.split('_')                                     #split the line by the underscore
            if len(parts) == 3:                                         #ensure the line has exactly three parts
                abbreviations[parts[0]] = [parts[1], parts[2]]          #store abbreviation and associated name and team

    start_times = {}                                                    #initialize an empty dictionary to store
    with open(start_log, 'r', encoding="utf-8") as f:                   #open file for reading
        for line in f.read().splitlines():                              #read all lines and process each one
            abbreviation = line[:3]                                     #extract the first 3 characters
            time_str = line[3:].strip()                                 #extract the timestamp and strip any whitespace
            start_times[abbreviation] = datetime.strptime(time_str,
                                        '%Y-%m-%d_%H:%M:%S.%f')  #convert timestamp to datetime

    end_times = {}                                                      #initialize an empty dictionary to store
    with open(end_log, 'r', encoding="utf-8") as f:                     #open file for reading
        for line in f.read().splitlines():                              #read all lines and process each one
            abbreviation = line[:3]                                     #Extract the first 3 characters
            time_str = line[3:].strip()                                 #extract the timestamp and strip any whitespace
            end_times[abbreviation] = datetime.strptime(time_str,
                                        '%Y-%m-%d_%H:%M:%S.%f')  #convert timestamp to datetime

    return {
        'abbreviations': abbreviations,                                 #driver abbreviations and team names
        'start_times': start_times,                                     #start times of drivers
        'end_times': end_times                                          #end times of drivers
    }

"""Function to calculate lap times based on start and end times."""
def calculate_lap_times(data: dict):
    lap_times = []                                                      #initialize an empty list to store
    for driver, start_time in data['start_times'].items():              #iterate over the start times dictionary
        if driver in data['end_times']:                                 #check if end time is available for the driver
            end_time = data['end_times'][driver]                        #get the end time for the driver
            lap_time = end_time - start_time                            #calculate lap time
            lap_times.append({
                'abbreviation': driver,                                 #driver's abbreviation
                'name': data['abbreviations'].get(driver,
                        ["Unknown", "Unknown"])[0].strip(),             #driver's name
                'team': data['abbreviations'].get(driver,
                        ["Unknown", "Unknown"])[1].strip(),             #driver's team
                'lap_time': lap_time                                    #lap time
            })
    return sorted(lap_times, key=lambda x: x['lap_time'])               #return lap times sorted by asc

"""Function to build a report of the race."""
def build_report(folder_path: str, order: str = 'asc') -> dict:
    data = parse_logs(folder_path)                                      #parse the log files and get the data
    lap_times = calculate_lap_times(data)                               #calculate lap times for all drivers
    if order == 'desc':                                                 #if order is 'desc', reverse the sorted
        lap_times.reverse()
    return {                                                            #return a dictionary containing:
        'top_15': lap_times[:15],                                       #top 15
        'rest': lap_times[15:]                                          #and the rest of the racers
    }

"""Function to format the lap time into a readable string."""
def format_time(lap_time: timedelta) -> str:
    total_seconds = lap_time.total_seconds()                            #get total sec from the timedelta object
    minutes = int(total_seconds // 60)                                  #calculate the number of minutes
    seconds = total_seconds % 60                                        #calculate the remaining seconds
    return f'{minutes}:{seconds:06.3f}'                                 #return the formatted time

"""Function to format and print the race report."""
def print_report(report: dict):
    print("Top 15 Racers:")                                             #print header for the top 15 racers
    for idx, racer in enumerate(report['top_15'], 1):                   #iterate over the top 15 racers
        print(f"{idx}. {racer['name']:20} | {racer['team']:40} | {format_time(racer['lap_time'])}") #racer's details
    print("-" * 80)                                                     #print a separator line
    print("Rest of the Racers:")                                        #print header for the rest of the racers
    for idx, racer in enumerate(report['rest'], 16):                    #iterate over index 16
        print(f"{idx}. {racer['name']:20} | {racer['team']:40} | {format_time(racer['lap_time'])}") #racer's details

"""Function to print the report for a specific driver."""
def print_driver_report(folder_path: str, driver: str):
    report = build_report(folder_path)                                  #build the full report
    for racer in report['top_15'] + report['rest']:                     #iterate over both top 15 and remaining racers
        if racer['name'].lower() == driver.lower():                     #check if the driver's name matches
            print(f"Driver: {racer['name']}\nTeam: {racer['team']}\nLap Time: {format_time(racer['lap_time'])}")
            return                                                      #exit the function after finding the driver
    print(f"No data found for driver: {driver}")                        #print a message if the driver was not found
