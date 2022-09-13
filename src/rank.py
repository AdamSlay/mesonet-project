from pathlib import Path
from datetime import datetime
import sys
import re
import argparse
import logging
import pandas as pd

# Log Messages
logging.basicConfig(
    filename="rank.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def read_csv_file(csv_file_path, parm, asc):
    # Read CSV file and sort parm column
    try:
        df = pd.read_csv(csv_file_path, usecols=["time", parm])
    except FileNotFoundError as e:
        msg = (
            f"{type(e)} '{csv_file_path}' not found. Expected path format: <path/to/csv>",
        )
        print(
            msg,
            file=sys.stderr,
        )
        logging.error(msg)
        raise SystemExit(1)
    except ValueError as e:
        msg = (
            f"{type(e)} '{parm}' was not found in '{csv_file_path}' Please enter a valid parameter",
        )
        print(
            msg,
            file=sys.stderr,
        )
        logging.error(msg)
        raise SystemExit(1)
    logging.info(f"{csv_file_path} imported successfully")
    sorted_df = df.sort_values([parm], ascending=asc)
    logging.info(f"{csv_file_path} sorted successfully")
    return sorted_df


def format_time(sorted_df, csv_file):
    # Format 'time' column to ISO 8601
    try:
        YY = int(csv_file[5:9])  # Year
        MM = int(csv_file[9:11])  # Month
        DD = int(csv_file[11:13])  # Day
        for row in sorted_df.index:
            HR = sorted_df.loc[row, "time"] // 60  # Hour
            MN = sorted_df.loc[row, "time"] % 60  # Minute
            dt = datetime(YY, MM, DD, HR, MN)
            sorted_df.loc[row, "time"] = dt.isoformat(timespec="minutes")
    except IndexError as e:
        msg = (
            f"{type(e)} CSV filename '{csv_file}' isn't the expected length: xxxx_YYYYMMDD.csv",
        )
        print(
            msg,
            file=sys.stderr,
        )
        logging.error(msg)
        raise SystemExit(1)
    except TypeError as e:
        msg = (
            f"{type(e)} CSV file '{csv_file}' does not match the expected format: xxxx_YYYYMMDD.csv",
        )
        print(msg, file=sys.stderr)
        logging.error(msg)
        raise SystemExit(1)
    logging.info("Time column formatted successfully")
    return sorted_df


def output_csv(final_df, csv_file, out, parm):
    # Output new CSV file
    if out:
        if not re.match(r"\\|/", out[-1]):
            if "/" in out:
                out = f"{out}/"
            elif "\\" in out:
                out = f"{out}\\"
            else:
                logging.warning(
                    f"Ouput Path '{out}' does not end in a trailing slash: '/'(Mac or Linux) or '\\'(Windows). Ex: /path/to/output/location/"
                )
    filename = f"{csv_file}_ranked_{parm}.csv"
    filepath = Path(f"{out}{filename}")
    try:
        final_df.to_csv(filepath, index=False)
    except OSError as e:
        msg = f"{type(e)} Output path '{out}' does not exist, please enter a valid output path"
        print(msg, file=sys.stderr)
        logging.error(msg)
        raise SystemExit(1)
    logging.info(f"'{filepath}' outputted successfully")


def main() -> int:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Sort a CSV file by column")
    parser.add_argument("-o", "--output", default="", help="Path to output location")
    parser.add_argument("csv", help="Path to csv file you would like to import")
    parser.add_argument("parm", help="Parameter you would like to sort by")
    parser.add_argument(
        "-a",
        "--ascending",
        default=False,
        action="store_true",
        help="Sort in ascending order",
    )
    args = parser.parse_args()
    # Get name of CSV_file
    csv_file = re.split(r"\\|/", args.csv)[-1][:13]
    if not re.match(r"[a-zA-Z]{4}_[0-9]{8}", csv_file):
        logging.warning(
            f"{csv_file} file does not match the expected format: xxxx_YYYYMMDD.csv"
        )
    sorted_df = read_csv_file(args.csv, args.parm, args.ascending)
    final_df = format_time(sorted_df, csv_file)
    output_csv(final_df, csv_file, args.output, args.parm)
    logging.info("---Task Completed Successfully---")
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except:
        logging.critical("Critical Error - Task Ended")
        raise SystemExit(1)
    else:
        raise SystemExit(status)
