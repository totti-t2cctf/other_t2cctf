import sys

def main():
	strmap = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	deci = len(strmap)

	argvs = sys.argv
	argc = len(argvs)

	if argc != 2:
		print "error arg_length"
		exit(1)

	strout62 = ""

	strin10 = int(argvs[1], 16)
	q = int(argvs[1], 16)

	flag = 0
	while(deci < q):
		r = q % deci
		q = q / deci

		strout62 += strmap[r]
		if q < deci:
			strout62 += strmap[q]
			flag = 1

	if flag:
		print strout62[::-1]

	else:
		print strmap[q]


if __name__ == '__main__':

	main()