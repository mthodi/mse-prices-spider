#!/usr/bin/python3

import sys, os

class SQL_Encoder():

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = 0
        self.read_file()
    
    def read_file(self):
        handle =  open(os.path.join(sys.path[0], self.file_name), 'r+')
        self.data = handle.readlines()
    
    def get_number_of_fields(self):
        field_count = 0
        tmp_count = 0
        for line in self.data:
            tmp_count = len(line.split(" "))
            if field_count < tmp_count:
                field_count = tmp_count
        return field_count
    
    def compensate_fields(self):
        """Fill in missing fields"""
        field_count = self.get_number_of_fields()
        output_data = []
        for line in self.data:
            cols_in_line = line.split(" ")
            tmp_count = len(cols_in_line)
            if tmp_count < field_count:
                if field_count - len(cols_in_line) == 4 and cols_in_line[1] != 'NBS':
                    cols_to_be_copied = cols_in_line[2]
                    cols_in_line.insert(2,cols_to_be_copied)
                    cols_in_line.insert(2,cols_to_be_copied)
                # NBS needs special attention x_X
                elif field_count -len(cols_in_line) == 4 and cols_in_line[1] == 'NBS':
                    cols_to_be_copied = cols_in_line[5]
                elif field_count -len(cols_in_line) == 6 and cols_in_line[2] == 'NBS':
                    cols_to_be_copied = cols_in_line[2]
                    cols_in_line.insert(2,cols_to_be_copied)
                    cols_in_line.insert(2,cols_to_be_copied)
                elif cols_in_line[3] == 'NBS' and (field_count - len(cols_in_line) == 2):
                     output_line = "," # delimeter is now comma
                     output_line = output_line.join(cols_in_line) 
                     output_data.append(output_line)
                     continue
                else:
                    cols_to_be_copied = cols_in_line[5]
                # insert low
                cols_in_line.insert(1,cols_to_be_copied)
                # insert high
                cols_in_line.insert(1,cols_to_be_copied)
                output_line = "," # delimeter is now comma
                output_line = output_line.join(cols_in_line) 
                output_data.append(output_line)
            else:
                # change delimeter
                output_line = "," # delimeter is now comma
                output_line = output_line.join(cols_in_line) 
                output_data.append(output_line)
        return output_data

    def save_results(self):
        """Save the results in a SQL CSV file"""
        output_data = self.compensate_fields()
        output_file = self.file_name.split(".")[0] + ".tmp"
        out_handle = open(output_file, 'w+')
        for line in output_data:
            out_handle.write(line)
        out_handle.close()
        print("[+] Field compensation done.\n[+] Saved in : {}".format(output_file))




if len(sys.argv) < 2:
    print("Usage: {} file_name.csv".format(sys.argv[0]))
    sys.exit(-1)

my_reader = SQL_Encoder(sys.argv[1])
my_reader.save_results()
#sys.exit(0)

