#!/usr/bin/env python
"""
Program for generating a rainbow table and cracking hashes using the given
rainbow table. Works with md5 and sha1 encryption algorithms.
"""

import argparse
import urllib2
import hashlib
import time

__author__ = "Jamin Chen"
__email__ = "jaminche@usc.edu"

if __name__ == "__main__":
    # Define arguments for argparse library
    parser = argparse.ArgumentParser()
    parser.add_argument("-ops", "--operations", help = "Specifies the type of \
                        operation. Must either be 'generate'  or 'crack'.",
                        metavar = '')
    parser.add_argument("-t", "--type", help = "Species the type of hash to \
                        use. Must either be 'md5' or 'sha1'.", metavar = '')
    parser.add_argument("-i", "--input", help = "Name of input file to be used",
                        metavar = '')
    parser.add_argument("-o", "--output", help = "Name of output file to write \
                        to", metavar = '')
    args = parser.parse_args();

    # Check that the user chose a correct option for -ops
    if args.operations not in ['generate', 'crack']:
        print "Operation type can only be 'generate' or 'crack'."
        print "Program will now exit."
        raise SystemExit

    # Check that input file is valid and can be opened from local or URL
    try:
        infile = open(args.input, "r")
        # Reads input file line-by-line
        inputfile = infile.read().splitlines()
    except:
        print "Unable to find input file on local machine. Trying web..."
        try:
            infile = urllib2.urlopen(args.input)
            # Reads input file line-by-line
            inputfile = infile.read().splitlines()
            print "File found on web!"
        except IOError:
            print "No file found with the name/address \'%s'"% args.input
            print "Program will now exit."
            raise SystemExit

    #
    # Generating Hashes
    #
    if args.operations == 'generate':
        # Prompt the user to let them know that the -t operator is redundant
        # when generating hashes.
        if args.type:
            print "NOTE: The system generates both md5 and sha1 hashes."
            print "      Type specification is used when cracking."
        # Quit if user specified an output option. Notify them of proper syntax.
        if args.output:
            print "Bad syntax. The output option is only used when cracking."
            print "Program will now exit."
            raise SystemExit

        # Past this point input is valid

        outfile = open("database.rbt", "w")
        # Initialize hash # counter and timer (time is in miliseconds)
        counter = 0;
        time_0 = time.clock()
        time_0 *= 1000
        # Hash each password with md5 and sha1 and store to database.rbt
        for password in inputfile:
            outfile.write(hashlib.md5(password).hexdigest())
            outfile.write(":")
            outfile.write(hashlib.sha1(password).hexdigest())
            outfile.write(":")
            outfile.write(password)
            outfile.write("\n")
            counter += 2;
        # Stop timer and close files
        time_1 = time.clock()
        time_1 *= 1000
        infile.close()
        outfile.close()
        # Display diagnostics to console
        print "\nNumber of hashes created:\t%s" % counter
        print "Time to create the table:\t%s" % (time_1 - time_0),
        print "ms"
        print "\nSuccessfully wrote to database.rbt."
        print "Now exiting."

    #
    # Cracking Hashes
    #
    elif args.operations == 'crack':
        # Check that user-specified hashing algorithm is supported (md5/sha1)
        if args.type not in ['md5', 'sha1']:
            print "Hash type can only be 'md5' or 'sha1'."
            print "Program will now exit."
            raise SystemExit
        # Check if database.rbt exists and can be opened
        try:
             with open("database.rbt", "r") as data:
                 database = data.read().splitlines()
        except IOError:
            print "Could not open database.rbt! Is it generated yet?"
            print "Program will now exit."
            raise SystemExit
        # Open output file and initialize counter variables and timer
        outfile = open(args.output, "w")
        hashes_found = 0;
        hashes_cracked = 0;
        time_0 = time.clock()
        time_0 *= 1000
        # Loop thru input file and compare with database.rbt
        for hash_value in inputfile:
            hashes_found += 1
            for data in database:
                # Split each line in database into md5, sha1, and original key
                md5, sha1, original_pass = data.split(":")
                if args.type == 'md5':
                    if hash_value == md5:
                        hashes_cracked += 1;
                        outfile.write(md5)
                        outfile.write(":")
                        outfile.write(original_pass)
                        outfile.write("\n")
                        continue
                elif args.type == 'sha1':
                    if hash_value == sha1:
                        hashes_cracked += 1;
                        outfile.write(sha1)
                        outfile.write(":")
                        outfile.write(original_pass)
                        outfile.write("\n")
                        continue
        # Stop timer and close files
        time_1 = time.clock()
        time_1 *= 1000
        infile.close()
        outfile.close()
        #Display diagnostics to console
        print "\nNumber of hashes found:\t\t%s" % hashes_found
        print "Number of hashes cracked:\t%s" % hashes_cracked
        print "Time to crack the hashes:\t%s" % (time_1 - time_0),
        print "ms"
        print "Type of hash used to crack:\t%s" % args.type
        print "\nSuccessfully wrote to %s" % args.output
        print "Program will now exit."
