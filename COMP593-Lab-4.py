import re
import sys
import pandas as pd

def get_log_file_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        print("Error: No log file path provided")
        sys.exit()

def filter_log_messages(log_file_path, regex, case_sensitive, print_records, print_summary):
    log_records = []
    matched_records = []
    matched_records_data = []
    
    with open(log_file_path, 'r') as file:
        log_records = file.readlines()
        
    if case_sensitive:
        pattern = re.compile(regex)
    else:
        pattern = re.compile(regex, re.IGNORECASE)
        
    for record in log_records:
        match = pattern.search(record)
        if match:
            matched_records.append(record)
            matched_records_data.append(match.groups())
            
    if print_records:
        for matched_record in matched_records:
            print(matched_record)
            
    if print_summary:
        print("{} records match the regex '{}' using {} case matching".format(
            len(matched_records), regex, "case-sensitive" if case_sensitive else "case-insensitive"))
        
    return matched_records, matched_records_data

def process_log_file(log_file_path):
    tallies = {}
    with open(log_file_path, 'r') as file:
        for line in file:
            if "DPT=" in line:
                dpt = line.split("DPT=")[1].split(" ")[0]
                if dpt in tallies:
                    tallies[dpt] += 1
                else:
                    tallies[dpt] = 1
    return tallies

def generate_destination_port_report(log_file_path, dpt):
    data = []
    with open(log_file_path, 'r') as file:
        for line in file:
            if "DPT={}".format(dpt) in line:
                line_data = line.split(" ")
                date = line_data[0]
                time = line_data[1]
                src = line_data[2]
                dst = line_data[4].split("DPT=")[0]
                src_port = line_data[3].split(":")[1]
                dst_port = line_data[4].split("DPT=")[1].split(" ")[0]
                data.append([date, time, src, dst, src_port, dst_port])
                
    df = pd.DataFrame(data, columns=["Date", "Time", "Source IP", "Destination IP", "Source Port", "Destination Port"])
    df.to_csv("{}_dpt_{}.csv".format(log_file_path, dpt), index=False)

if __name__ == "__main__":
    log_file_path = get_log_file_path()
    tallies = process_log_file(log_file_path)
    for dpt in tallies:
        generate_destination_port_report(log_file_path, dpt) 
