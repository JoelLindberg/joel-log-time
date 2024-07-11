import argparse
import sys

parser = argparse.ArgumentParser(prog="Joel Log Time console app")

'''
parser.add_argument("date")
parser.add_argument("-i", "--time-in", metavar="time")
parser.add_argument("-o", "--time-out", metavar="time")
parser.add_argument("--sum", help="Calculate deltatime for a date and add it to the sum table as saldo for the day.", action="store_true")

args = parser.parse_args()

if args.sum and (args.time_in != None or args.time_out != None):
    print("Not allowed to calculate sum at the same time as adding time")
    sys.exit(1)


print(args.date)
print(args.sum)
print(args.time_in)
print(args.time_out)
print(args)
'''


parser.add_argument("-i", "--time-in", metavar="time")
args = parser.parse_args()

print(args.time_in)
