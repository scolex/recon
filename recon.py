import csv
import json
import os
import time

# adresar odkud cte json
SRC_DIR = "./RECONS"
# adresar kam je pise
DST_DIR = "./RECONS_CSV"


def main():
    # udela cilovej adresar kdyz neni
    if not os.path.exists(DST_DIR):
        os.makedirs(DST_DIR)

    for entry in os.scandir(SRC_DIR):
        if not entry.name.startswith('.') and entry.is_file():
            try:
                print("Processing: " + entry.path)
                write_csv(entry)
            except Exception as e:
                print("Error occured while processing {} {} ".format(entry.path, e))


def format_time(timestamp):
    t = time.localtime(timestamp)
    return time.asctime(t)


def write_csv(entry):
    with open(entry.path) as json_file:
        json_data = json.load(json_file)

        csv_filename = entry.name + "-" + str(int(entry.stat().st_mtime))
        csv_path = os.path.join(DST_DIR, csv_filename)

        with open(csv_path, "w+") as csv_f:
            csv_file = csv.writer(csv_f)
            header = ["BSSID", "SSID", "CHANEL", "ENCRYPT", "POWER", "CLIENTS", "TIME"]
            csv_file.writerow(header)
            for ap in json_data["ap_list"]:
                csv_file.writerow([
                    ap["bssid"],
                    ap["ssid"],
                    ap["channel"],
                    ap["encryption"],
                    ap["power"],
                    ap["clients"],
                    format_time(entry.stat().st_mtime)
                ])

if __name__ == "__main__":
    main()
