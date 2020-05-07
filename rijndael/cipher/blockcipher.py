from pip._vendor.msgpack.fallback import xrange

from rijndael.utils import padding


class BlockCipher():
    key_error_message = "Incorrect key size"

    def __init__(self, key, mode, IV, counter, cipher_module, args={}):
        self.key = key
        self.mode = mode
        self.cache = ''
        self.ed = None

        if 'keylen_valid' in dir(self):
            if not self.keylen_valid(key) and type(key) is not tuple:
                raise ValueError(self.key_error_message)

        if IV == None:
            self.IV = '\x00' * self.blocksize
        else:
            self.IV = IV

        self.cipher = cipher_module(self.key, **args)

        if (counter == None) or not callable(counter):
            raise Exception("Specify a valid counter object for CTR mode")
        self.chain = CTR(self.cipher, self.blocksize, counter)

    def encrypt(self, plaintext):
        self.ed = 'e'
        return self.chain.update(plaintext, 'e')

    def decrypt(self, ciphertext):
        self.ed = 'd'

        return self.chain.update(ciphertext, 'd')

    def final(self, padpad=padding.PKCS7):
        if self.ed == 'e':
            dummy = '0' * (self.chain.totalbytes % self.blocksize)
            pad = padpad(dummy, padding.PAD, self.blocksize)[len(dummy):]
            return self.chain.update(pad, 'e')
        else:
            pass


class CTR:
    def __init__(self, codebook, blocksize, counter):
        self.codebook = codebook
        self.counter = counter
        self.blocksize = blocksize
        self.keystream = []
        self.totalbytes = 0

    def update(self, data, ed):
        n = (data)
        blocksize = self.blocksize

        output = list(data)
        for i in xrange(n):
            if len(self.keystream) == 0:
                block = self.codebook.encrypt(self.counter())
                self.keystream = list(block)
            output[i] = chr(ord(output[i]) ^ ord(self.keystream.pop(0)))
        self.totalbytes += len(output)
        return ''.join(output)
