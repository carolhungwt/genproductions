#!/bin/env/ python
import itertools
from itertools import izip
from itertools import izip_longest

pdfnumber = 31
nevents = 1

def gettag(productsstr):
	if productsstr == 'nu':			return 'NU'
	elif productsstr =='mu':		return 'MU'
	elif productsstr == 'tau' or productsstr == 't':		return 'TL'
	elif productsstr == 'e':		return 'EL'
	else:	
		raise IOError('Products tag cannot be found, Current tag: {0}'.format(productsstr))
#		return Exception

class mcfmInputCard():
	def __init__(self,process,products,width):
		self.processrawinput = [process,products]
		self.process = self.getprocessnumber(process)	
		self.products = self.getproducts(products)
		self.width = str(width)

	@property 
	def widthSM(self):
		if self.width == '1':		return ''
		elif self.width == '10':	return '10'
		elif self.width =='25':		return '25'

	@property
	def coupling(self):
		coupling = self.processrawinput[0]
		return coupling.upper()
			
	def getprocessnumber(self,process):
		if isinstance(process,int):
			return int(process)
		elif isinstance(process,str):
			processstr = process.lower()
			if processstr == 'bkg':		return 132
			elif processstr == 'sig':	return 128
			elif processstr == 'bsi':	return 131
			else:	raise IOError("Invalid input for process")
		else:		raise TypeError("Process can either be int(128/131/132) or string(sig/bsi/bkg). Current input: {0}. Try again.".format(process))

	def getproducts(self,products):
		singleflavor = True
		if isinstance(products,str):
			templist = [index for index,i in izip(range(0,len(products)),products) if i.isdigit()]
			if sum(int(products[index]) for index in templist) is not 4:	raise IOError("Total number of outgoing particles must be 4.")
			if len(templist)==2:	
				singleflavor = False
				separateindex = templist[1]
				products1 = products[1:separateindex]
				products2 = products[separateindex+1:]
			else:
				products1 = products[1:]
				products2 = products1
			print str(products1)+' '+str(products2)
			return ''.join([gettag(products1),gettag(products2)])
		else:	raise IOError("Invalid products input.")

	def writecard(self):
		with open('input_tmpl.DAT','r') as fin:
			with open('MCFM_JHUGen_13TeV_ggZZto{products}_{coupling}{width}_NNPDF31.DAT'.format(products=self.products,coupling=self.coupling,width=self.widthSM),'w') as fout:
				for line in fin:
					if '[nproc]' in line:			
						line = '{0}.{1}		[nproc] \n'.format(self.process,self.products)
					if '[LHAPDF group]' in line:	
						line = "'NNPDF{0}_lo_as_0130'			[LHAPDF group]\n".format(pdfnumber)
#					if '[nevtrequested]' in line:	
#						line = '{0}			[nevtrequested]\n'.format(nevents)
					if 'NU'in self.products and '[m56min]' in line:	
						line = '0d0			[m56min]\n'
					if '[Gamma_H/Gamma_H(SM)]' in line:	
						line = '{width}d0		[Gamma_H/Gamma_H(SM)]\n'.format(width=self.width)
					fout.write(line)
				fout.close()
			fin.close()


if __name__=='__main__':
	widths = []
	processtorun = ['sig','bsi']
	productslist = ['4mu','4e','4tau','2e2mu','2e2nu','2e2tau','2mu2nu','2mu2tau']
	for process,products in itertools.product(processtorun,productslist):
		if process == 'bsi':		widths = [1,10,25]
		elif process == 'sig':		widths = [1]	
		for width in widths:
			tempcard = mcfmInputCard(process, products, width)
			tempcard.writecard()



