import csv
import json
import os
import time

# Nacte JSON soubory z SRC_DIR, zpracuje je a ulozi v csv formatu
# do DST_DIR

# adresar, odkud cte json
SRC_DIR = "../RECONS"
# adresar, kam zapise cvs. Pokud neexistuje, vytvori ho
DST_DIR = "./RECONS_CSV"


def main():
    # vytvori cilovy adresar, pokud neexistuje
    if not os.path.exists(DST_DIR):
        os.makedirs(DST_DIR)

    # projde json soubory ve vstupnim adresari
    for entry in os.scandir(SRC_DIR):
        if not entry.name.startswith('.') and entry.is_file():
            try:
                print("Processing: " + entry.path)
                write_csv(entry)
            except Exception as e:
                print("Error occured while processing {} {} ".format(entry.path, e))


# Formatovani casu
def format_time(timestamp):
    t = time.localtime(timestamp)
    return time.asctime(t)


def write_csv(entry):
    # otevre json
    with open(entry.path) as json_file:
        # nacte json data
        json_data = json.load(json_file)

    # cesta a jmeno k csv
    csv_filename = entry.name + "-" + str(int(entry.stat().st_mtime))
    csv_path = os.path.join(DST_DIR, csv_filename)

    # vytvori a otevre cilovi csv soubor
    with open(csv_path, "w+") as csv_f:
        csv_file = csv.writer(csv_f)
        # zapise hlavicku do csv
        header = ["BSSID", "SSID", "CHANEL", "ENCRYPT", "POWER", "CLIENTS", "TIME"]
        csv_file.writerow(header)

        # projde AP a zapise
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
