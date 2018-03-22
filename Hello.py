# Parsing command line argument in normal file.

import json
import parser
import argparse
parser = argparse.ArgumentParser()
#parser.add_argument("name") #If you are using this option then no need to put '--name' option while giving
                             #commandline arguments.

# while executing the program, you need to specify '--name anyname'(space)'--age integer'(space)'--id integer'
parser.add_argument("--name")
parser.add_argument("--age")
parser.add_argument("--id")

args = parser.parse_args()

print "Hello "+args.name
print "your age is :"+args.age
print "and your ID is :"+args.id