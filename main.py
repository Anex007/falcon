import argparse
from xtractEXIF import *
from os import listdir
from os.path import isfile, isdir, join


RED = '\033[0;31m'
GREEN = '\033[0;32m'
RESET = '\033[0m'


def getImageFiles(dir):
	if not isdir(dir):
		return None
	onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
	return onlyfiles


def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-s', '--single', help='Specify a single image to extract the Data')
	group.add_argument('-d', '--dir', help='Specify a file with images to extract the Data')
	parser.add_argument('-v', '--verbose', help='need more verbose ouput', action='store_true')
	parser.add_argument('-j', '--just', help='Specify this argument if you don\'t just want the GPS info', action='store_true')

	args = parser.parse_args()
	if args.single:
		gps = getGPS(args.single)
		if gps:
			print(GREEN + 'GPS data found: ')
			to_print = '{} {} {} {}'.format(gps['latitude']['direction'], gps['latitude']['value'], gps['longitude']['direction'], gps['longitude']['value'])
			print(to_print)
			print(RESET, end='')
		else:
			print(RED + '[-] No GPS data found on the image' + RESET)
	elif args.dir:
		files = getImageFiles(args.dir)
		if not files:
			print(RED + 'No images found in the directory' + RESET)
		else:
			if args.just:
				for file in files:
					gps = getGPS(join(args.dir, file))
					if not gps:
						continue
					to_print = '{}: {} {} {} {}'.format(file, gps['latitude']['direction'], gps['latitude']['value'], gps['longitude']['direction'], gps['longitude']['value'])
					print(to_print)
			else:
				gpsDatas = {}
				for file in files:
					gps = getGPS(join(args.dir, file))
					if gps:
						gpsDatas[file] = gps
				print(gpsDatas)
				# More Code Goes here


if __name__ == '__main__':
	main()
