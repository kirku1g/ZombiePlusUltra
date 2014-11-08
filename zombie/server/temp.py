cdef char BASIC = 0
cdef char LIST_BYTE = 10
cdef char LIST_SHORT = 11
cdef char LIST_INT = 12


def unpack_data(data_format, data):
    
    cdef int data = 0
    
    for part_type, part_length in data_format:
        if part_type == BASIC:
            