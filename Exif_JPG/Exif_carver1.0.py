import sys
import struct
from tkinter import filedialog as fd
"""
Author: Axel Dominguez-Cruz

Description: Exif tool carver for images. With this tool we can carve all
important information necessary to access exif data in a JPEG.
"""
FILENAME = fd.askopenfilename()
JPEG = False
METADATA = dict()
print(FILENAME)

def file_identifier(data:bytes):
    i = 0
    if b'\xff\xd8' in data:
        JPEG = True
        print("jpeg detected!")
    else:
        print("other!") 

def ID_tag(tag_num:int): # should give us the the name of the tag
    tag = 0
    with open('Tag_information.txt','r') as file:
        while True:
            buffer = file.readline()
            if str(tag_num) in buffer:
                tag = buffer
                break
            if buffer == '':
                tag = tag_num    
    return tag

def ID_data_format(field_type:int,data:bytes,components:int,byte_order:str): # Needs to give us the format and bytes/components
    """
    Paramaters:
        field_type -> value in the entry
        data -> our buffer of data
        byte_order -> little or big endian

    Values
    1: Unsigned byte (1 byte)           7: undefined (1 byte)
    2: ascii Strings (1 byte)           8: signed short (2 bytes)
    3: unsigned short (2 bytes)         9: signed long (4 bytes)
    4: unsigned long (4 bytes)         10: signed rational (8 bytes)
    5: unsigned rational(8 bytes)      11: signed float (4 bytes)
    6: signed byte (1 byte)            12: double float (8 bytes)
    """

    if field_type == 1:
        x = 1
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 2:
        x = 1
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 3:
        x = 2
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 4:
        x = 4
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 5:
        x = 8
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 6:
        x = 1
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 7:
        x = 1
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 8:
        x = 2
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 9:
        x = 4
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 10:
        x = 8
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 11:
        x = 4
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    elif field_type == 12:
        x = 8
        data_length = x * components
        if data_length < 4:
            return True,None
        return False,data_length
    



def IFD_parser(data:bytes,offset:int,byte_order:str):
    """
    IFD consists of 18 bytes:
    
    # of directories -> 2 bytes
    Field entries -> 12 bytes
    Next IFD -> 4 bytes

    1) to parse we first check the num of directory entries in our current IFD
    2) Each entry has 12 bytes allocated to it in this format:
        0:2 -> Tag that IDs field
        2:4 -> Field Type
        4:8 -> # of values, count of the indicated type
        8:12 -> Value offset, Can point anywhere!
    3) Once all entries have been parsed and accounted for we go to the next IFD

    """

    num_directories = int.from_bytes(data[offset:offset+2],byte_order)
    new_dict = dict()
    i = 0
    updated_offset = offset+2
    if num_directories == 0:
        print("No EXIF data available!")
        return "No EXIF data available!"
    while i < num_directories:
        tag = int.from_bytes(data[updated_offset:updated_offset+2],byte_order)
        type1 = int.from_bytes(data[updated_offset+2:updated_offset+4],byte_order)
        num_values = int.from_bytes(data[updated_offset+4:updated_offset+8],byte_order)
        dict_key = "Tag ID:" + str(i)
        desc_key = "Desc: " + str(i)

        tag_buffer = ID_tag(tag)
        new_tag = tag_buffer.split('    ',3)
        new_dict[dict_key] = new_tag[1]
        new_dict[desc_key] = new_tag[2]
        updated_offset = updated_offset + 12
        i+=1
    return new_dict

    

        
                

        


        
    

def jpeg_carver(data:bytes):
    """
    marker -> 2:4   Length -> 4:6   Identifier -> 6:11
    Version -> 11:12/12:13  Units -> 13:14  Density -> 14:16/16:18
    Thumbnail -> 18:19/19:20
    """
    if data[2:4] == b'\xFF\xE0':
        print("APP0")
        METADATA["Marker"] = "APP0"
        METADATA["Length"] = int.from_bytes(data[4:6],'big')
        METADATA["Identifier"] = data[6:11].decode()
        METADATA["Version"] = str(int.from_bytes(data[11:12],'big')) + "." + str(int.from_bytes(data[12:13],'big'))
        if int.from_bytes(data[13:14],'big') == 0:
            METADATA["Units"] = "No units"
        elif int.from_bytes(data[13:14],'big') == 1:
            METADATA["Units"] = "Pixels per inch"
        elif int.from_bytes(data[13:14],'big') == 2:
            METADATA["Units"] = "Pixels per centimeter"

        METADATA["Density"] =  str(int.from_bytes(data[14:16],'big')) + "x" + str(int.from_bytes(data[16:18],'big'))
        METADATA["Thumbnail"] = str(int.from_bytes(data[18:19],'big')) + "x" + str(int.from_bytes(data[19:20],'big'))
    if data[2:4] == b'\xFF\xE1':
        """
        start -> 0:2
        marker-> 2:4 (str)
        Length-> 4:6 (int)
        EXIF DATA -> 6:12 in ascii (str)
        TIFF HEADER (8 bytes):
            ByteOrder -> 12:14
            offset of first IFD -> 16:20
        """
        print("APP1")
        byte_order = data[12:14]
        print(byte_order)
        if byte_order == b'\x49\x49': # little endian
            first_IFD = int.from_bytes(data[16:20],'little')
            new_dict = IFD_parser(data,first_IFD+12,'little') # Should return a dict
        else: # big endian
            first_IFD = int.from_bytes(data[16:20],'big')
            new_dict = IFD_parser(data,first_IFD+12,'big')



        METADATA["Marker"] = "APP1(EXIF)"
        METADATA["Length"] = int.from_bytes(data[4:6],'big')
        METADATA["Byte Order"] = data[12:14].decode()
        METADATA["Information"] = new_dict # Dict if there is info, string if not!

BUFFER = bytes()
def main():
    # read in all bytes and then identify if file is a JPEG
    with open(FILENAME,'rb') as file:
       BUFFER = file.read()
    file_identifier(BUFFER)
    # Read in the necessary bytes to get our metadata
    jpeg_carver(BUFFER)
    print(METADATA)

       



if __name__ == "__main__":
    main()