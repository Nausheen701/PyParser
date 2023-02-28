#!/bin/bash
while :
do
    wget -O index.html https://techcrunch.com
    python3 pyparserdtarraycsv.py -f index.html
    cp results.csv "/Users/nausheenakhter/Library/CloudStorage/GoogleDrive-nausheen701@gmail.com/My Drive/FORMSORT/ARTICLES"
    echo "Going to sleep for 300 seconds"
    sleep 300 
done