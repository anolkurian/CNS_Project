#Part of code has been 
#Derived from <ppdeep> (https://github.com/elceef/ppdeep)

import os
from io import BytesIO
import timeit


category = "Shopping"
folder = "apk"
directory_in_str = "D:/CNS/"+ folder+"/playstore/"+category+"/dex/"
directory = os.fsencode(directory_in_str)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print("D:/CNS/"+ folder+"/playstore/"+category+"/dex/"+filename)
    start = timeit.default_timer()
    hash1 = hash_from_file("D:/CNS/"+ folder+"/playstore/"+category+"/dex/"+filename)
    stop = timeit.default_timer()
    print('Time 1: ', stop - start)  
    print(hash1)
    print("D:/CNS/"+ folder+"/playstore/"+category+"/dex/"+filename)
    if os.path.isfile("D:/CNS/"+ folder+"/aurora/"+category+"/dex/"+filename):
        start = timeit.default_timer()
        hash2 = hash_from_file("D:/CNS/"+ folder+"/aurora/"+category+"/dex/"+filename)
        stop = timeit.default_timer()
        print('Time 2: ', stop - start)  
        print("hash2 is " )
        print(hash2)
        sum2 = 0
        if(hash2 == hash1):
            print("true")
        else :
            for x, y in zip(hash1, hash2):
                sum2 = sum2 +compare(x,y)
            tempstr ="Aurora repackaged app "+filename+" in category " +category+  " with similarity score : " + str(sum2/2)
            print("Aurora repackaged app with similarity score : " + sum2 )
            with open("D:/CNS/Output.txt", 'a') as f:
                f.write(str(tempstr) + "\n")
    else:
        print("file does not exist for hash 2")

#### ----BELOW CODE IS DUPLICATE OF ABOVE LOGIC WITH PATHS CHANGED FOR RESPECTIVE DIRECTORIES ----  ####
    if os.path.isfile("D:/CNS/"+ folder+"/Aptoide/"+category+"/dex/"+filename):
        start = timeit.default_timer()
        hash3 = hash_from_file("D:/CNS/"+ folder+"/Aptoide/"+category+"/dex/"+filename)
        stop = timeit.default_timer()
        print('Time 3: ', stop - start)
        print("hash3")
        print(hash3)
        sum3 = 0
        if(hash3 == hash1):
            print("true")
        else :
            for x, y in zip(hash1, hash3):
                sum3 = sum3 +compare(x,y)
            tempstr ="Aptoide repackaged app "+filename+" in category " +category+  " with similarity score : " + str(sum3/2)
            print(tempstr)
            with open("D:/CNS/Output.txt", 'a') as f:
                f.write(str(tempstr) + "\n")
    else:
        print("file does not exist for hash 3")

    if os.path.isfile("D:/CNS/"+ folder+"/apkmirror/"+category+"/dex/"+filename):
        start = timeit.default_timer()
        hash4 = hash_from_file("D:/CNS/"+ folder+"/apkmirror/"+category+"/dex/"+filename)
        stop = timeit.default_timer()
        print('Time 4: ', stop - start)
        print("hash4" )
        print(hash4)
        sum4 = 0
        if(hash4 == hash1):
            print("true")
        else :
            for x, y in zip(hash1, hash4):
                sum4 = sum4 +compare(x,y)
            tempstr = "Apkmirror repackaged app "+filename+" in category " +category+  " with similarity score : " + str(sum4/2)
            print(tempstr )
            with open("D:/CNS/Output.txt", 'a') as f:
                f.write(str(tempstr) + "\n")
    else:
        print("file does not exist for hash 4")
####----    ----####

BLOCKSIZE_MIN = 3
SPAMSUM_LENGTH = 64


def _spamsum(stream, slen,HASH_PRIME):
	STREAM_BUFF_SIZE = 8192
	# CODE USES A HUGE PRIME NUMBER HERE.INSTEAD WE CALL THE FUNCTION TWICE AND PASS OUR HUGE PRIME NUMBER AS ARGUMENT HERE.
	# HASH_PRIME = 0x01000193
	HASH_INIT = 0x28021967
	ROLL_WINDOW = 7
	B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

	roll_win = bytearray(ROLL_WINDOW)
	roll_h1 = int()
	roll_h2 = int()
	roll_h3 = int()
	roll_n = int()
	block_size = int()
	hash_string1 = str()
	hash_string2 = str()
	block_hash1 = int(HASH_INIT)
	block_hash2 = int(HASH_INIT)

	bs = BLOCKSIZE_MIN
	while (bs * SPAMSUM_LENGTH) < slen:
		bs = bs * 2
	block_size = bs

	while True:
		if block_size < BLOCKSIZE_MIN:
			raise RuntimeError('Calculated block size is too small')

		stream.seek(0)
		buf = stream.read(STREAM_BUFF_SIZE)
		while buf:
			for b in buf:
				block_hash1 = ((block_hash1 * HASH_PRIME) & 0xFFFFFFFF) ^ b
				block_hash2 = ((block_hash2 * HASH_PRIME) & 0xFFFFFFFF) ^ b

				roll_h2 = roll_h2 - roll_h1 + (ROLL_WINDOW * b)
				roll_h1 = roll_h1 + b - roll_win[roll_n % ROLL_WINDOW]
				roll_win[roll_n % ROLL_WINDOW] = b
				roll_n += 1
				roll_h3 = (roll_h3 << 5) & 0xFFFFFFFF
				roll_h3 ^= b

				rh = roll_h1 + roll_h2 + roll_h3

				if (rh % block_size) == (block_size - 1):
					if len(hash_string1) < (SPAMSUM_LENGTH - 1):
						hash_string1 += B64[block_hash1 % 64]
						block_hash1 = HASH_INIT
					if (rh % (block_size * 2)) == ((block_size * 2) - 1):
						if len(hash_string2) < ((SPAMSUM_LENGTH // 2) - 1):
							hash_string2 += B64[block_hash2 % 64]
							block_hash2 = HASH_INIT

			buf = stream.read(STREAM_BUFF_SIZE)

		if block_size > BLOCKSIZE_MIN and len(hash_string1) < (SPAMSUM_LENGTH // 2):
			block_size = (block_size // 2)

			roll_win = bytearray(ROLL_WINDOW)
			roll_h1 = roll_h2 = roll_h3 = int()
			roll_n = int()

			block_hash1 = block_hash2 = HASH_INIT
			hash_string1 = hash_string2 = str()
		else:
			rh = roll_h1 + roll_h2 + roll_h3
			if rh != 0:
				hash_string1 += B64[block_hash1 % 64]
				hash_string2 += B64[block_hash2 % 64]
			break

	return '{0}:{1}:{2}'.format(block_size, hash_string1, hash_string2)


def hash(buf):
	if isinstance(buf, bytes):
		pass
	elif isinstance(buf, str):
		buf = buf.encode()
	else:
		raise TypeError('Argument must be of bytes or string type, not %r' % type(buf))
	return _spamsum(BytesIO(buf), len(buf))


def hash_from_file(filename):
	if not isinstance(filename, str):
		raise TypeError('Argument must be of string type, not %r' % type(filename))
	if not os.path.isfile(filename):
		raise IOError('File not found')
	if not os.access(filename, os.R_OK):
		raise IOError('File is not readable')
	fsize = os.stat(filename).st_size
	# MODIFICATION STARTS
	# TWO HUGE PRIME NUMBERS PASSED TO THE FUNCTION TO GENERATE HASH AND STORE IN ARRAY AND RETURN ARRAY
	HASHPRIME1=0x01000193
	HASHPRIME2=0xFAEF275
	hashes=[]
	x=_spamsum(open(filename, 'rb'), fsize,HASHPRIME1)
	y=_spamsum(open(filename, 'rb'), fsize,HASHPRIME2)
	hashes=[x,y]
	return hashes
	# MODIFICATION ENDS


def _levenshtein(s, t):
	'''
	Implementation by Christopher P. Matthews
	'''
	if s == t: return 0
	elif len(s) == 0: return len(t)
	elif len(t) == 0: return len(s)
	v0 = [None] * (len(t) + 1)
	v1 = [None] * (len(t) + 1)
	for i in range(len(v0)):
		v0[i] = i
	for i in range(len(s)):
		v1[0] = i + 1
		for j in range(len(t)):
			cost = 0 if s[i] == t[j] else 1
			v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
		for j in range(len(v0)):
			v0[j] = v1[j]
	return v1[len(t)]


class _RollState(object):
	ROLL_WINDOW = 7

	def __init__(self):
		self.win = bytearray(self.ROLL_WINDOW)
		self.h1 = int()
		self.h2 = int()
		self.h3 = int()
		self.n = int()

	def roll_hash(self, b):
		self.h2 = self.h2 - self.h1 + (self.ROLL_WINDOW * b)
		self.h1 = self.h1 + b - self.win[self.n % self.ROLL_WINDOW]
		self.win[self.n % self.ROLL_WINDOW] = b
		self.n += 1
		self.h3 = (self.h3 << 5) & 0xFFFFFFFF
		self.h3 ^= b
		return self.h1 + self.h2 + self.h3


def _common_substring(s1, s2):
	ROLL_WINDOW = 7
	hashes = list()

	roll = _RollState()
	for i in range(len(s1)):
		b = ord(s1[i])
		hashes.append(roll.roll_hash(b))

	roll = _RollState()
	for i in range(len(s2)):
		b = ord(s2[i])
		rh = roll.roll_hash(b)
		if i < (ROLL_WINDOW - 1):
			continue
		for j in range(ROLL_WINDOW-1, len(hashes)):
			if hashes[j] != 0 and hashes[j] == rh:
				ir = i - (ROLL_WINDOW - 1)
				jr = j - (ROLL_WINDOW - 1)
				if (len(s2[ir:]) >= ROLL_WINDOW and
					s2[ir:ir+ROLL_WINDOW] == s1[jr:jr+ROLL_WINDOW]):
					return True
	return False


def _score_strings(s1, s2, block_size):
	if _common_substring(s1, s2) == False:
		return 0
	score = _levenshtein(s1, s2)
	score = (score * SPAMSUM_LENGTH) // (len(s1) + len(s2))
	score = (100 * score) // SPAMSUM_LENGTH
	score = 100 - score
	if score > (block_size // BLOCKSIZE_MIN * min([len(s1), len(s2)])):
		score = block_size // BLOCKSIZE_MIN * min([len(s1), len(s2)])
	return score


def _strip_sequences(s):
	r = s[:3]
	for i in range(3, len(s)):
		if (s[i] != s[i-1] or s[i] != s[i-2] or s[i] != s[i-3]):
			r += s[i]
	return r


def compare(hash1, hash2):
	if not (isinstance(hash1, str) and isinstance(hash2, str)):
		raise TypeError('Arguments must be of string type')
	try:
		hash1_bs, hash1_s1, hash1_s2 = hash1.split(':')
		hash2_bs, hash2_s1, hash2_s2 = hash2.split(':')
		hash1_bs = int(hash1_bs)
		hash2_bs = int(hash2_bs)
	except ValueError:
		raise ValueError('Invalid hash format') from None

	if hash1_bs != hash2_bs and hash1_bs != (hash2_bs * 2) and hash2_bs != (hash1_bs * 2):
		return 0

	hash1_s1 = _strip_sequences(hash1_s1)
	hash1_s2 = _strip_sequences(hash1_s2)
	hash2_s1 = _strip_sequences(hash2_s1)
	hash2_s2 = _strip_sequences(hash2_s2)

	if hash1_bs == hash2_bs and hash1_s1 == hash2_s1:
		return 100

	if hash1_bs == hash2_bs:
		score1 = _score_strings(hash1_s1, hash2_s1, hash1_bs)
		score2 = _score_strings(hash1_s2, hash2_s2, hash2_bs)
		score = int(max([score1, score2]))
		return score
	elif hash1_bs == (hash2_bs * 2):
		score = int(_score_strings(hash1_s1, hash2_s2, hash1_bs))
		return score
	else:
		score = int(_score_strings(hash1_s2, hash2_s1, hash2_bs))
		return score
	return 0
