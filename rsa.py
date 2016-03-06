from random import randrange
from math import gcd
from binascii import hexlify, unhexlify

class RSA():
	""""
	self.prKey
	self.puKey
	self.mod
	"""
	def __init__(self, pr=None, pu=None, mod=None):
		if not mod and not pr and not pu:
			self._genKeys()
		else: 
			self.prKey = pr
			self.puKey = pu
			self.mod = mod
	
	def getPrKey(self):
		return (self.prKey, self.mod)
		
	def getPuKey(self):
		return (self.puKey, self.mod)
	
	def encrypt(self, msg):
		return str(pow(self._strToInt(msg), self.prKey, self.mod))
		
	def decrypt(self, cif):
		return unhexlify(hex(pow(int(cif), self.puKey, self.mod)).lstrip('0x')).decode('utf-8')
		
	def _strToInt(self, s):
		return int(hexlify(bytes(s, 'utf-8')), 16)
	
	def _genKeys(self):
		p = self._getRndPrime()
		q = self._getRndPrime()
		
		modulus = p * q
		totient = (p-1) * (q-1)
		e = self._genE(totient)
		d = self._modMulInv(e, totient)
		
		self.prKey = d
		self.puKey = e
		self.mod = modulus
		
	def _isPrime(self, n):
		if 1 < n < 4:
			return True 
		if n < 2 or n % 2 == 0 or n % 3 == 0:
			return False
		i = 5
		while i ** 2 <= n:
			if n % i == 0 or n % (i+2) == 0:
				return False
			i = i + 6
		return True
		
	def _getRndPrime(self, N=10**15):	# 10**15: 99bit, 5sec; 10**18: 119bit, 2min;
		p = 1
		while not self._isPrime(p):
			p = randrange(int(N/2), N)
		return p
	
	def _genE(self, t):
		e = randrange(2, t)
		while not gcd(e, t) == 1:
			e = randrange(2, t)
		return e
	
	def _modMulInv(self, a, b):
		c,d = a,b
		uc,vc,ud,vd = 1,0,0,1
		while c:
			q = d // c
			c,d = d - q * c, c
			uc,vc,ud,vd = ud - q * uc, vd - q * vc, uc, vc
		return ud % b
	