#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import argparse

#region args
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
#endregion

#region main
def main() -> None:
	args: argparse.Namespace = parser.parse_args()
	print(args)
#endregion

if __name__ == '__main__':
	main()