class f1(object):
	def cal(self, a):
		print self.cal2(a)
		
	def cal2(self, a):
		assert 2 == 1
		return a
		
class f2(f1):
	def cal2(self, a):
		return a + 1

if __name__ == '__main__':
	f = f1()
	f.cal(2)
	print 'ok'