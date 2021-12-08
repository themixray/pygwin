import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('args')
# parser.add_argument()

args = parser.parse_args()
print(args.args)
