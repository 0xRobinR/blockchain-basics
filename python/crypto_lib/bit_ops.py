"""
This module provides various bitwise operations including AND, OR, XOR, NOT,
left shift, right shift, left rotate, and right rotate.
"""

def and_op(a, b):
    """Perform bitwise AND operation."""
    return a & b

def or_op(a, b):
    """Perform bitwise OR operation."""
    return a | b

def xor_op(a, b):
    """Perform bitwise XOR operation."""
    return a ^ b

def not_op(a):
    """Perform bitwise NOT operation."""
    return ~a

def shift_left_op(a, b):
    """Perform bitwise left shift operation."""
    return a << b

def shift_right_op(a, b):
    """Perform bitwise right shift operation."""
    return a >> b

def rotate_left_op(a, b):
    """Perform bitwise left rotate operation."""
    return shift_left_op(a, b) | shift_right_op(a, (32 - b))

def rotate_right_op(a, b):
    """Perform bitwise right rotate operation."""
    return shift_right_op(a, b) | shift_left_op(a, (32 - b))
