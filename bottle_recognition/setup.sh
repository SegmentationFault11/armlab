#!/bin/bash

printf "\nApriltag setup started\n\n"

cd apriltags

# Removing .o and .a files
printf "Compiling Apriltag library.... "
if [[ -f *.o ]]; then
	rm *.o
fi

if [[ -f *.a ]]; then
	rm *.a
fi
printf "DONE\n"

# Creating new archived file
OPERATING_SYSTEM=$(uname -a | awk '{print $1}')

if [ $OPERATING_SYSTEM == "Darwin" ]; then
	# echo "This is a Macintosh system"

	INCLUDE_PATH="-I/usr/local/include -I/usr/local/include/eigen3 "

	printf "Compiling Apriltag library.... "
	g++ -c *.cc $INCLUDE_PATH
	printf "DONE\nArchiving .o files............ "
	ar rcs libapriltags.a *.o
	printf "DONE\n"

elif [ $OPERATING_SYSTEM == "Linux" ]; then
	echo "This is a Linux system"
fi

# Removing .o files
printf "Removing remaining .o files... "
if [[ -f *.o ]]; then
	rm *.o
fi
printf "DONE\n\nApriltag setup complete!\n\n"