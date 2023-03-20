import fileinput

test = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
init_p = [1, 5, 2, 0, 3, 7, 4, 6]
inv_p = [3, 0, 2, 4, 6, 1, 7, 5]
key_p = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
subkey_p  = [0, 1, 5, 2, 6, 3, 7, 4, 9, 8]

S0 = [['01','00','11','10'],
      ['11','10','01','00'],
      ['00','10','01','11'],
      ['11','01','11','10']]

S1 = [['00','01','10','11'],
      ['10','00','01','11'],
      ['11','00','01','00'],
      ['10','01','00','11']]

def perm(list, order):
    result = []
    for i in range(len(list)):
        result.append(0)
    for i in range(len(list)):
        result[i] = list[order[i]]
    return result

def shift_l(list, n):
    return list[n:] + list[:n]

def shift_r(list, n):
    return list[-n:] + list[:-n]

def subkeys(key):
    tempKey = perm(key, key_p)
    tempKey = shift_l(tempKey[:5], 1) + shift_l(tempKey[5:], 1)
    subkey1 = perm(tempKey, subkey_p)
    subkey1.pop(0)
    subkey1.pop(0)
    tempKey = shift_l(tempKey[:5], 2) + shift_l(tempKey[5:], 2)
    subkey2 = perm(tempKey, subkey_p)
    subkey2.pop(0)
    subkey2.pop(0)
    return subkey1, subkey2

def convert(string):
    list1 = []
    list1[:0] = string
    return list1

def listToString(s):
    str1 = ""
    for i in s:
        str1 += str(i)
    return str1

def sbox(list, sbox):
    row = int(list[0] + list[3], 2)
    col = int(list[1] + list[2], 2)
    val = sbox[row][col]
    return val

def feisel(block, subkey):
    xored = []
    OGLeft = block[:4]
    OGRight = block[4:]
    expBlock = perm(OGRight, [3, 0, 1, 2]) + perm(OGRight, [1, 2, 3, 0])
    for i in range(len(subkey)):
        num = int(expBlock[i]) ^ int(subkey[i])
        xored.append(str(num))
    left = xored[:4]
    right = xored[4:]
    result = sbox(left, S0) + sbox(right, S1)
    result = perm(result, [1, 3, 2, 0])
    for i in range(len(result)):
        num = int(result[i]) ^ int(OGLeft[i])
        result[i] = num
    result = result + OGRight
    return result

def encrypt(key, plaintext):
    subkey1, subkey2 = subkeys(key)
    result = perm(plaintext, init_p)
    result = feisel(result, subkey1)
    result = perm(result, [4, 5, 6, 7, 0, 1, 2, 3])
    result = feisel(result, subkey2)
    result = perm(result, inv_p)
    print(listToString(result))

def decrypt(key, ciphertext):
    subkey1, subkey2 = subkeys(key)
    result = perm(ciphertext, init_p)
    result = feisel(result, subkey2)
    result = perm(result, [4, 5, 6, 7, 0, 1, 2, 3])
    result = feisel(result, subkey1)
    result = perm(result, inv_p)
    print(listToString(result))

def main():
    lines = []
    for line in fileinput.input():
        lines.append(line)

    mode = lines[0].strip()
    key = lines[1].strip()
    plainText = lines[2].strip()
    if mode == 'E':
        encrypt(key, plainText)
    else:
        decrypt(key, plainText)

if __name__ == "__main__":
    main()