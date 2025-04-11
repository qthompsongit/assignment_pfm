#Standard Libraries
import argparse
import os
import sys

#Third-Party

#Local

def main():
    parse_test = argparse.ArgumentParser(description="This is a test parser to make sure this program works.")
    parse_test.add_argument("headline_text_file", type=str, help="The name of the headline text file.")
    parse_test.add_argument("headline_source", type=str, help="The source of the provided headline text file.")
    args_get = parse_test.parse_args()
    
    print("Headline Text File:", args_get.headline_text_file)
    print("Headline Source:", args_get.headline_source)
    print("Test")

if __name__ == "__main__":
    main()