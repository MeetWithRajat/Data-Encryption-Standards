# complete DES encryption
import random


def random_generator():
    """for generate randomly 64 bit key and plain text"""
    text = ""
    for i in range(64):
        text += str(random.randint(0, 1))
    return text


def permuted_choice_1(initial_key):
    """for permuted choice 1 64 bit"""
    pc1_table = [57, 49, 41, 33, 25, 17, 9,
                 1, 58, 50, 42, 34, 26, 18,
                 10, 2, 59, 51, 43, 35, 27,
                 19, 11, 3, 60, 52, 44, 36,
                 63, 55, 47, 39, 31, 23, 15,
                 7, 62, 54, 46, 38, 30, 22,
                 14, 6, 61, 53, 45, 37, 29,
                 21, 13, 5, 28, 20, 12, 4]
    pc1 = ""
    for i in range(56):
        pc1 += initial_key[pc1_table[i] - 1]
    return pc1


def left_shift(original, count):
    """for left shift (32 bit)"""
    if count == 1 or count == 2 or count == 9 or count == 16:
        return original[1:] + original[0]
    else:
        return original[2:] + original[:2]


def permuted_choice_2(cd):
    """for permuted choice 2 56 bit"""
    pc2_table = [14, 17, 11, 24, 1, 5,
                 3, 28, 15, 6, 21, 10,
                 23, 19, 12, 4, 26, 8,
                 16, 7, 27, 20, 13, 2,
                 41, 52, 31, 37, 47, 55,
                 30, 40, 51, 45, 33, 48,
                 44, 49, 39, 56, 34, 53,
                 46, 42, 50, 36, 29, 32]
    pc2 = ""
    for i in range(48):
        pc2 += cd[pc2_table[i] - 1]
    return pc2


def initial_permutation(plain_text):
    """for initial permutation (64 bit plain text)"""
    permuted_text = ""
    for i in range(8):
        if i <= 3:
            position = 57+i*2
        else:
            position = 56+(i-4)*2
        for j in range(8):
            permuted_text += plain_text[position]
            position -= 8
    return permuted_text


def expansion_permutation(right32):
    """for convert from right 32 bit to 48 bit"""
    right32 = right32[-1]+right32+right32[0]
    ep = ""
    for i in range(1, 32, 4):
        ep += right32[i-1:i+5]
    return ep


def xor_box(pt_bits1, ptk_bits2):
    """for 48 bit & 32 bit XOR"""
    length = len(pt_bits1)
    xor_bits = ""
    for i in range(length):
        if pt_bits1[i] == ptk_bits2[i]:
            xor_bits += "0"
        else:
            xor_bits += "1"
    return xor_bits


def substitution_box(xor_bits):
    """compressing 48 bits to 32 bits using substitution box"""
    sb_table = [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
                0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
                4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
                15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
                 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
                 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
                 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
                 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
                 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
                 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
                 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
                 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
                 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
                 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
                 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
                 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
                 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
                 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
                 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
                 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
                 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
                 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
                 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
                 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
                 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    sb = ""
    count = 0
    for i in range(0, 48, 6):
        row = int(xor_bits[i])*2 + int(xor_bits[i+5])*1
        col = int(xor_bits[i+1])*8 + int(xor_bits[i+2])*4 + int(xor_bits[i+3])*2 + int(xor_bits[i+4])*1
        val = sb_table[count][row*16+col]
        count += 1
        bin_str = ""
        for j in range(4):
            bin_str = str(val % 2) + bin_str
            val //= 2
        sb += bin_str
    return sb


def straight_permutation(s32):
    """for straight permutation (32 bit)"""
    sp_table = [16, 7, 20, 21, 29, 12, 28, 17,
                1, 15, 23, 26, 5, 18, 31, 10,
                2, 8, 24, 14, 32, 27, 3, 9,
                19, 13, 30, 6, 22, 11, 4, 25]
    sp = ""
    for i in range(32):
        sp += s32[sp_table[i]-1]
    return sp


def final_permutation(merge_string):
    """for final permutation (64 bit)"""
    fp_table = [40, 8, 48, 16, 56, 24, 64, 32,
                39, 7, 47, 15, 55, 23, 63, 31,
                38, 6, 46, 14, 54, 22, 62, 30,
                37, 5, 45, 13, 53, 21, 61, 29,
                36, 4, 44, 12, 52, 20, 60, 28,
                35, 3, 43, 11, 51, 19, 59, 27,
                34, 2, 42, 10, 50, 18, 58, 26,
                33, 1, 41, 9, 49, 17, 57, 25]
    fp = ""
    for i in range(64):
        fp += merge_string[fp_table[i] - 1]
    return fp


def encryption(plain_text, initial_key):
    """for controlling flow and call the all methods"""
    pc1 = permuted_choice_1(initial_key)
    rd = initial_permutation(plain_text)
    c = pc1[:28]
    d = pc1[28:]
    for i in range(1, 17):
        c = left_shift(c, i)
        d = left_shift(d, i)
        pc2 = permuted_choice_2(c+d)
        lpt = rd[:32]
        rpt = rd[32:]
        ep = expansion_permutation(rpt)
        xor1 = xor_box(ep, pc2)
        sb = substitution_box(xor1)
        sp = straight_permutation(sb)
        xor2 = xor_box(sp, lpt)
        rd = rpt+xor2
    ct = final_permutation(rd[32:]+rd[:32])
    return ct


if __name__ == '__main__':
    print("Press-> 1: Randomly generate 64 bit plain text and key\t\tOthers: User input 64 bit plain text and key")
    choice = input("Enter your choice: ")
    if choice == "1":
        pt = random_generator()
        k = random_generator()
        print(f"\nRandomly generated plain text is:\n{pt}\nRandomly generated key is:\n{k}")
    else:
        pt = input("\nEnter 64 bit plain text:\n")
        k = input("Enter 64 bit key:\n")
    cipher_text = encryption(pt, k)
    print(f"\nAfter encryption in DES algorithm the cipher text is:\n{cipher_text}")
