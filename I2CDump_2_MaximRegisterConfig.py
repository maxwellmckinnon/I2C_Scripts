# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:51:58 2016
Changes the I2C dump format from Android/Linux systems to Maxim Config file format

I2C Dump Format Example:

     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
00: 00 e0 02 04 00 00 00 00 00 00 00 00 00 00 1b 00    .???..........?.
10: 14 00 03 33 60 40 40 44 44 00 00 10 00 00 00 00    ?.?3`@@DD..?....
20: 00 00 04 00 00 01 e0 0e 00 00 00 00 1a 1a 01 02    ..?..???....????
30: 05 2c 2c 00 00 00 00 00 00 15 00 00 15 80 10 c3    ?,,......?..????
40: 00 00 01 01 03 80 00 00 00 00 00 00 00 00 00 00    ..????..........

Maxim Config File Format Example:

0x00 	0x00
0x01 	0x00
0x02 	0x00
0x03 	0x00
0x04 	0x00
0x05 	0x00
0x06 	0x00

@author: Maxwell.McKinnon
"""
import sys

def main():
    c = -1
    for line in sys.stdin:
        if c == -1:
            c += 1
            continue #Skip the first line
        lineCollection = line.split()[1:17]
        i = 0
        for item in lineCollection:
            print('0x%02x' % (c*16 + i), "\t" + '0x' + item)
            i += 1
        c += 1
        

if __name__ == "__main__":
    main()
    