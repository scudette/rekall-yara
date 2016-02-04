#!/bin/bash

git submodule init
git submodule update

TOP_LEVEL=$(pwd)

cd rekall_yara/

echo Updating yara
cd yara/
git checkout master
git pull
git reset --hard
git clean -x -f -d
echo "Updating version to $TOP_LEVEL/version.txt"
git tag | tail -1 > $TOP_LEVEL/rekall_yara/version.txt

echo Running autotools.
./bootstrap.sh
cd ../

echo Updating yara-python
cd yara-python/
git checkout master
git pull
git reset --hard
rm config.h
cd ../
