#!/bin/sh

if test "$TRAVIS" = true; then 
    pip install --user PyYAML
    sudo apt-get -o Acquire::CompressionTypes::Order::=bz2 update
    sudo apt-get -y install software-properties-common
#    sudo add-apt-repository ppa:smspillaz/cmake-2.8.12 -y
    sudo apt-get update -qq
#    sudo apt-get purge cmake -qq
    sudo apt-get -y install make
    sudo free -m
    echo "test cmake version"
    cmake --version
    wget http://www.cmake.org/files/v3.0/cmake-3.0.2.tar.gz
    tar xf cmake-3.0.2.tar.gz
    cd cmake-3.0.2
    ./configure
    make install

fi
