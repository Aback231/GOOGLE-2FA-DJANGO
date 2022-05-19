import string

def encode(text: string, key: string) -> bytes:
    reps = (len(text)-1)//len(key) +1
    a1 = text.encode('utf-8')
    key = (key * reps)[:len(text)].encode('utf-8')
    cipher = bytes([i1^i2 for (i1,i2) in zip(a1,key)])
    return cipher

def decode(cipher: bytes, key: string):
    reps = (len(cipher)-1)//len(key) +1
    key = (key * reps)[:len(cipher)].encode('utf-8')
    clear = bytes([i1^i2 for (i1,i2) in zip(cipher,key)])
    return clear.decode('utf-8')