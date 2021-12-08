import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('args')

args = parser.parse_args()
print(args.accumulate(args.args))
