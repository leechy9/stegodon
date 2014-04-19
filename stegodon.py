'''
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''
 This program steg-hides a file into an xml file.

 Erases tail data in each node of the xml. Each node in the xml tree has 0 or
 more spaces in its tail data. Each space represents a 1 for a bit, while each
 new node represents a 0. The bits are written in lsb order, which appears 
 backwards when read sequentially, making most patterns less obvious.
 
 To further hide the information, the nodes are accessed in depth-first order.
 This means the bits may not appear in sequential order and are almost
 impossible to detect without first knowing that the data follows the
 depth-order scheme and parsing the xml.

 A tab character is used to denote the end of the stegged content. The ratio
 of storage between the hidden document and the carrier is inconsistent and
 very poor, so this should only be used to hide small files.
'''

import xml.etree.ElementTree as ET
import sys
import traceback

'''
 Takes the given file and steg hides it inside of another file.
 Required parameters:
  input_file - string, the location of the file to hide
  carrier_file - string, the location of the file to store in
  output_file - string, the location to output the stegged copy to
'''
def xml_steg_hide(input_file, carrier_file, output_file):
    # Open both input files for reading
    xml_tree = ET.parse(carrier_file)
    hide = open(input_file, 'rb')
    # Prevent tail data on root node
    xml_iter = xml_tree.getroot().iter()
    node = next(xml_iter)
    node.tail = ''
    node = next(xml_iter)
    node.tail = ''
    # Read in each byte of the input file
    byte_ = hide.read(1)
    while byte_ is not None and byte_ != b'':
        # Handle each bit
        for i in range(8):
            bit = (byte_[0] >> i) & 1
            # Append a space for each consecutive bit to the end of a node's tail
            if bit == 1:
                node.tail += ' '
            # Jump to the next node for each zero
            else:
                # Clear existing tail data on next node
                node = next(xml_iter)
                node.tail = ''
        byte_ = hide.read(1)
    # Write a tab to specify the end of the steg
    node.tail += '\t'
    # Write output and close files
    xml_tree.write(output_file)
    hide.close()


'''
 Reads the given input file and attempts to recover a stegged file from it.
 Required parameters:
  input_file - string, location of the file to recover from
  output_file - string, location of the file to output to
'''
def xml_steg_recover(input_file, output_file):
    xml_iter = ET.parse(input_file).getroot().iter()
    recover = open(output_file, 'wb')
    byte_ = 0
    # Prevent tail data on root node
    next(xml_iter)
    bit_count = -1
    for node in xml_iter:
        # Add a zero for each new node
        bit_count += 1
        # Make a new byte if 8 bits have been read
        if bit_count == 8:
            recover.write(byte_.to_bytes(1, byteorder='big'))
            bit_count = 0
            byte_ = 0
        # Count the spaces in each node
        if node.tail is not None:
            # Append a 1 to the byte for each space
            spaces = node.tail.count(' ')
            for i in range(spaces):
                byte_ = (byte_ | (1 << bit_count))
                bit_count += 1
                # Make a new byte if 8 bits have been read
                if bit_count == 8:
                    recover.write(byte_.to_bytes(1, byteorder='big'))
                    bit_count = 0
                    byte_ = 0
        # Stop when a tab is encountered
        if node.tail is not None and '\t' in node.tail:
            break
    recover.close()


# Main Method
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('  Hides a message in xml tail data (destroys tail data)')
        print('  To Hide: python stegodon.py <input> <carrier> <output>')
        print('  To Recover: python stegodon.py <input> <output>')
        exit(0)
    try:
        # Hide if four arguments
        if len(sys.argv) == 4:
            xml_steg_hide(sys.argv[1], sys.argv[2], sys.argv[3])
        # Recover if three arguments
        elif len(sys.argv) == 3:
            xml_steg_recover(sys.argv[1], sys.argv[2])
    except Exception as ex:
        print('An error occurred.')
        print(ex)
        traceback.print_exc()

