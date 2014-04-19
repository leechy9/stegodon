# Stegodon

## Overview
This program steg-hides a file into an xml file.

Erases tail data in each node of the xml. Each node in the xml tree has 0 or more spaces in its tail data. Each space represents a 1 for a bit, while each new node represents a 0. The bits are written in lsb order, which appears backwards when read sequentially, making most patterns less obvious.

To further hide the information, the nodes are accessed in depth-first order. This means the bits may not appear in sequential order and are almost impossible to detect without first knowing that the data follows the depth-order scheme and parsing the xml.

A tab character is used to denote the end of the stegged content. The ratio of storage between the hidden document and the carrier is inconsistent and very poor, so this should only be used to hide small files.

## Usage
This program requires Python3, but could probably work in Python2 with minimal modifications.

Carrier is the xml file that will be used to store the input file. Output will be the xml file containing the stegged content.

To Hide: `python stegodon.py <input> <carrier> <output>`

To Recover: `python stegodon.py <input> <output>`

## License
Stegodon is released under the GPL version 3 license. View the provided file `LICENSE` for more information.
