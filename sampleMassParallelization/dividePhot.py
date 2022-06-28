# Python script to divid up the res file
# prior to running this script, it is advisable to trim the .res file as follows:
# cp ngc188.res ngc188.res.org
# cat ngc188.res.org | awk '{if (NR == 1 || $6 == 3) print $0}' > ngc188.res
# python dividePhot.py --res ngc188.res --phot NGC_188.phot --yaml base9.yaml --nthreads 4

import pandas as pd
import numpy as np
import argparse
import os
import shutil

def dividePhot(resFile, photFile, yamlFile, nThreads, cmdFile):

	# read in the phot file (as strings so that I keep the formatting)
	df = pd.read_csv(photFile, sep="\s+", converters={i: str for i in range(100)})

	# generate nthreads subsets of the res file
	split_df = np.array_split(df, nThreads)
	#print(split_df)

	# for each subset
	#   save the subset of the phot file 
	#   copy the res file so that it has the same root file name as the phot file
	#   create a file that contains all the commands to sampleMass, which will be executed in parallel

	# get the zfill amount
	nfill = int(np.ceil(np.log10(nThreads)))
	# get the root file name from the phot file
	fnameRoot = photFile.replace('.phot','')

	f = open(cmdFile, 'w')

	for i,usedf in enumerate(split_df):
		destRoot = fnameRoot + '_' + str(i+1).zfill(nfill)

		# save that phot file
		destPhot = destRoot + '.phot'
		usedf.to_csv(destPhot, index=None, sep=' ')

		# copy the res file
		shutil.copy(resFile, destRoot + '.res')

		# create the command

		cmd = f"sampleMass --config {yamlFile} --photFile {destPhot} --outputFileBase {destRoot}"
		f.write(cmd + '\n')
		print(cmd)

	f.close()


def define_args():
	parser = argparse.ArgumentParser()

	parser.add_argument("-r", "--res",
		type=str,
		help=".res file name [base9.res]", 
		default="base9.res"
	)
	parser.add_argument("-p", "--phot", 
		type=str, 
		help=".phot file name [base9.phot]", 
		default="base9.phot"
	)
	parser.add_argument("-y", "--yaml", 
		type=str, 
		help=".yaml file name [base9.yaml]", 
		default="base9.yaml"
	)
	parser.add_argument("-n", "--nthreads", 
		type=int, 
		help="number of threads [10]", 
		default=10
	)
	parser.add_argument("-o", "--output", 
		type=str, 
		help="output file name for command list [sampleMassCmds.sh]", 
		default='sampleMassCmds.sh'
	)

	#https://docs.python.org/2/howto/argparse.html
	args = parser.parse_args()
	#to print out the options that were selected (probably some way to use this to quickly assign args)
	opts = vars(args)
	options = { k : opts[k] for k in opts if opts[k] is not None }
	print(options)

	return args

if __name__ == "__main__":

	args = define_args()
	dividePhot(args.res, args.phot, args.yaml, args.nthreads, args.output)