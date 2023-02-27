# License: LICENSE
# Usage: wget https://techcrunch.com
# python3 pyparser.py -f index.html

import re
import csv
import time
import os
import json, glob, argparse
import sys, traceback
# from utils import isFloat
from datetime import datetime

DEBUG = bool(os.getenv("DEBUG",None))

# Read a html file to parse
def parseHTML(filename):
    
    url_pattern = r'<a\s+href="([^"]+)"\sclass="post-block__title__link">\s(.+)\s</a>'
    date_pattern = r'<time\s+class="river-byline__full-date-time"\s+datetime="([^"]+)"\s*>([^<]+)<span\s+class="full-date-time__separator">\s+at\s+</span>([^<]+)</time>'

    html = None

    # List of keywords to search for in headers
    keywords_list = ['Raises', 'Raise', 'Seed', 'Series A', 'Series B', 'Series C', 'Stealth']

    # Create an empty array to store matching headers
    matching_headers = []

    with open('results.csv', mode='w', newline='') as csv_file:
    # Create a CSV writer object
        writer = csv.writer(csv_file)
    
    # Write the header row
        writer.writerow(['URL', 'Header', 'Date', 'Time'])

    with open(filename, mode='r') as f:
        html = f.read()

    if html:

        print("INFO: Opened fie: ", filename)

        # Find all matches for the URL pattern
        url_matches = re.findall(url_pattern, html)
        
        # Find all matches for the date/time pattern
        date_matches = re.findall(date_pattern, html)

         # Iterate over the URL matches
        for url_match in url_matches:
            # Get the URL and header from the match
            url, header = url_match
            
            # Iterate over the date/time matches
            for date_match in date_matches:
                # Get the date and time from the match
                date, time, _ = date_match
                
                # Check if the header contains any of the keywords
                if any(keyword in header for keyword in keywords_list):
                    # Add the header to the matching headers array
                    matching_headers.append(header)
                    
                    # Write the URL, header, date, and time to the CSV file
                    writer.writerow([url, header, date, time])
        
        # Print the matching headers array
        print(matching_headers)
        
    else:
        print("ERROR: Could not open %s" % filename)
        return None

# wget https://techcrunch.com
if __name__ == "__main__":
    
    # Build CLI arguments
    parser = argparse.ArgumentParser(description='Process portfolio from downloaded html file.')
    parser.add_argument("-l", "--loop", help="Loops every 5 minutes", action="store_true")
    parser.add_argument("-f", "--filename", type=str, help='Path to the input file', required=True)
    args = parser.parse_args()


    print("INFO: Parsing Portfolio from: ", args.filename)
    parseHTML(args.filename)
    
    # Check for loop
    if args.loop:
        while True:
            print("INFO: Going to sleep for 300 seconds, Control-C to exit")
            time.sleep(300)
            parseHTML(args.filename)
