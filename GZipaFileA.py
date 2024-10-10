# ------------------------------------------------------------------------------
# FileName: GZipaFileA.py
# Purpose:  Apply gzip compression to a target data file.
# Author: Donald Murray
# Date: 2018-06-20
# Notes:
#		Ingesting data to redshift via copy command is quicker if that source
#      data file is gzipped.
#   This code expects the source filename to be a single argument after 
#      name of the script on the command-line.
#      Example: python GZipaFileA.py MI_T1_ELA03_15-16.txt
# ------------------------------------------------------------------------------

import gzip
import sys

src = sys.argv[1]
trgt = src + '.gz'
print("Now compressing: " + src + " _to_ " + trgt + ".")
f_in = open(src, 'rb')
f_out = gzip.open(trgt, 'wb')
f_out.writelines(f_in)
f_out.close()
f_in.close()