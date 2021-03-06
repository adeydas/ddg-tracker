#!/usr/bin/env python3

import datetime
import sys
import os
import json
import argparse

def is_whitelisted(categories, whitelist):
	for white in whitelist:
		if white in categories:
			return True
	return False

def get_allowlisted_domains():
	with open('allowlisted_domains.txt', "r", encoding="utf-8") as f:
		ex = f.read().splitlines()
		return ex


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="path to the domain files", type=str)
	parser.add_argument("--fingerprinting_threshold", help="fingerprinting threshold", type=int, default=2)
	parser.add_argument("--output", help="absolute output file path", type=str, default="./duckduckgo_tracker.txt")
	args = parser.parse_args()

	# categories: https://github.com/duckduckgo/tracker-radar/blob/main/docs/CATEGORIES.md
	categories_to_block = ["action pixels",
							"ad fraud",
							"ad motivated tracking",
							"advertising",
							"analytics",
							"audience measurement",
							"malware",
							"obscure ownership",
							"session replay",
							"third-party analytics marketing",
							"unknown high risk behavior"]
	
	# categories that wont be blocked
	categories_whitelist = ["CDN"]

	fingerprinting_threshold = args.fingerprinting_threshold

	# common domains that are blocked by this script
	exclude_domains = get_allowlisted_domains()

	path = args.path
	domains = set()

	for subdir, dirs, files in os.walk(path):
		for domain in files:
			domain_file = os.path.join(subdir, domain)
			print("reading file {}".format(domain_file))
			with open(domain_file, "r", encoding="utf-8") as f:
				try:
					domain_json = json.load(f)

					categories = domain_json['categories']
					# get the primary domain
					domain = domain_json['domain']
					# get subdomains associated to block as well
					sub_domains = domain_json['subdomains']

					if domain_json['fingerprinting'] < fingerprinting_threshold:
						continue

					if is_whitelisted(categories, categories_whitelist):
						print("white listed domain: {}".format(domain))
						continue

					for cat in categories:
						cat = cat.lower()
						if cat in categories_to_block:
							domains.add(domain)
							print("adding domain: {}".format(domain))
							for d in sub_domains:
								domains.add(d + "." + domain)
								print("adding sub-domain: {}".format(d))
							break
				except ValueError:
					print ("Decoding JSON failed")

	for exclude in exclude_domains:
		if exclude not in domains:
			continue
		domains.remove(exclude)

	with open(args.output, "w", encoding="utf-8") as dest:
		dest.write("# generated at {}\n".format(datetime.datetime.now()))
		dest.write("# generated by deydas.com\n")
		dest.writelines(["0.0.0.0 " + d + "\n" for d in domains])

# vim: tabstop=4 shiftwidth=4 noexpandtab ft=python
