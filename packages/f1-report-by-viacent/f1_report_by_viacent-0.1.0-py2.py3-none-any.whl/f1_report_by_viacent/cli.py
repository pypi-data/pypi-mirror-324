import argparse
from f1_report_by_viacent.functions import build_report, print_driver_report, print_report

"""Function parse arguments"""
def main():
    parser = argparse.ArgumentParser(description="Formula 1 Report Generator")
    parser.add_argument('--files', type=str, required=True, help="Path to the folder containing log files")
    parser.add_argument('--asc', action='store_true', help="Sort results in ascending order")
    parser.add_argument('--desc', action='store_true', help="Sort results in descending order")
    parser.add_argument('--driver', type=str, help="Display statistics for a specific driver")
    args = parser.parse_args()
    if args.asc and args.desc:                              #check if both --asc & --desc arguments  used
        parser.error("Dont use both --asc & --desc")        #raise an error if both arguments used
    order = 'desc' if args.desc else 'asc'                  #sort order to 'desc', otherwise set it to 'asc'
    if args.driver:                                         #if --driver argument is provided
        print_driver_report(args.files, args.driver)              #call the driver_report function
    else:
        report = build_report(args.files, order)            #build the report with the given files and order
        print_report(report)                               #format the report for output


if __name__ == '__main__':
    main()
