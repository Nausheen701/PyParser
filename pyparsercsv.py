# License: LICENSE
# Usage: wget https://techcrunch.com
# python3 pyparser.py -f index.html

import re
import time
import csv
import os
import json, glob, argparse
import sys, traceback
# from utils import isFloat
from datetime import datetime


DEBUG = bool(os.getenv("DEBUG",None))

# Read a html file to parse
def parseHTML(filename):
    regex = r'<a\s+href="([^"]+)"\sclass="post-block__title__link">\s(.+)\s</a>'

    html = None

    with open('articles.csv', mode='w', newline='') as csv_file:
    # Create a CSV writer object
        writer = csv.writer(csv_file)
    
    # Write the header row
        writer.writerow(['Header','URL'])


    with open(filename,'r') as f:
        html = f.read()

    if html:
        print("INFO: Opened fie: ", filename)

        matches = re.finditer(regex, html, re.MULTILINE)
        
        for match in matches:
            print("URL:", match[1].strip())
            print("Header:", match[2].strip())

            writer.writerow([match[2].strip(), match[1].strip()])
        
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
