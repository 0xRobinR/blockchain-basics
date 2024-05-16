def and_op(a, b):
    return a & b

def or_op(a, b):
    return a | b

def xor_op(a, b):
    return a ^ b

def not_op(a):
    return ~a

def shift_left_op(a, b):
    return a << b

def shift_right_op(a, b):
    return a >> b

def rotate_left_op(a, b):
    return shift_left_op(a, b) | shift_right_op(a, (32 - b))

def rotate_right_op(a, b):
    return shift_right_op(a, b) | shift_left_op(a, (32 - b))
