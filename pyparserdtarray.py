import re
    # regex
import time
    # lets you work with time in python
import os
    # lets you run a command in python script, needs to be imported in every single python doc
import json, glob, argparse
    # lets you convert json to python
import sys, traceback

# from utils import isFloat
from datetime import datetime

DEBUG = bool(os.getenv("DEBUG",None))


# Read a html file to parse
def parseHTML(filename):
    regex = r'<a\s+href="([^"]+)"\sclass="post-block__title__link">\s(.+)\s</a>'
    pattern = r'<time\s+class="river-byline__full-date-time"\s+datetime="([^"]+)"\s*>([^<]+)<span\s+class="full-date-time__separator">\s+at\s+</span>([^<]+)</time>'
    keywords_list = ['Raises', 'Raise', 'Seed', 'Series A', 'Series B', 'Series C', 'Stealth']
    html = None

    # Initialize results array
    results = []
   
   # Open the file to extract data from
    with open(filename,'r') as f:
        html = f.read()


    if html:
        print("INFO: Opened fie: ", filename)

        # matches = re.finditer(regex, html, re.MULTILINE)
        # url_match = re.search(regex, html, re.MULTILINE)
        # time_match = re.search(pattern, html, re.MULTILINE)
        
        # urls = re.findall(regex, html, re.MULTILINE)
        # date_time_values = re.findall(pattern, html, re.MULTILINE)
    
        urls_and_headers = re.findall(regex, html, re.MULTILINE)

        for url, header in urls_and_headers:
            # Extract dates and times from the header data
            date_and_time = re.search(pattern, header)
            if date_and_time:
                date, time, timezone = date_and_time.groups()
        else:
            date, time, timezone = None, None, None
    
        # Check if header matches any of the keywords
        if any(keyword in header for keyword in keywords_list):
        # Add the URL, header, date, and time to the results array
            results.append({'url': url, 'header': header, 'date': date, 'time': time})

        # Print the results array
        print(results)

    else:
        print("ERROR: Could not open %s" % filename)
        return None
#  ----------------------------------  
    # headers = []
    # for url, header in urls:
    #     for keyword in keywords_list:
    #         if keyword in header:
    #             headers.append({
    #                 'url': url,
    #                 'header': header,
    #                 'date': '',
    #                 'time': '',
    #             })
    #             break

    # # Add date and time values to matching headers
    # for date, _, time in date_time_values:
    #     for header in headers:
    #         if header['url'] in html and not header['date'] and not header['time']:
    #             header['date'] = date
    #             header['time'] = time

    # # Print out the headers
    # for header in headers:
    #     print(header)
#  --------------------------------------

    #     # for match in matches:
    #     #         print("URL:", match[1].strip())
    #     #         print("Header:", match[2].strip())
    #     #         print("Date:", match[3])
    #     #         print("Time:", match[4])
               
    #     if url_match and time_match:
    #         url = url_match.group(1)
    #         header = url_match.group(2)
    #         date = time_match.group(2)
    #         time = time_match.group(3)
    
    #      # Check if the header matches any of the keywords
    #         if any(keyword in header for keyword in keywords_list):
    #             print('URL:', url)
    #             print('Header:', header)
    #             print('Date:', date)
    #             print('Time:', time)      
        
  

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
