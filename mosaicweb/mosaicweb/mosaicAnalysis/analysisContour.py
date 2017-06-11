"""
	A module that queries analysis Histograms.

	:Created:	4/15/2017
	:Author: 	Arvind Balijepalli <arvind.balijepalli@nist.gov>
	:License:	See LICENSE.TXT
	:ChangeLog:
	.. line-block::
		4/15/17		AB 	Initial version
"""
from mosaic.utilities.sqlQuery import query, rawQuery
import mosaic.mdio.sqlite3MDIO as sqlite
from mosaicweb.plotlyUtils import plotlyWrapper
import numpy as np
import base64

class QuerySyntaxError(Exception):
	pass

class analysisContour:
	"""
		A class that compiles MOSAIC analysis contour plots.
	"""
	def __init__(self, dbFile, qstr, bins, showContours):
		self.AnalysisDBFile = dbFile
		self.numBins=bins

		dbHnd=sqlite.sqlite3MDIO()
		dbHnd.openDB(self.AnalysisDBFile)
		analysisInfo=dbHnd.readAnalysisInfo()

		self.processingAlgorithm=analysisInfo['processingAlgorithm']

		self.queryString=self._queryString(qstr)

		if showContours:
			self.plotType="contour"
		else:
			self.plotType="heatmap"

		self.responseDict={}

	def analysisContour(self):
		# xlabel={
		# 	"BlockDepth"	: "i/i<sub>0</sub>",
		# 	"ResTime"		: "t (ms)"
		# }[self.queryString.split('from')[0].split('select')[1].split()[0]]

		layout={}
		layout['xaxis']= { 
						'title': "i/i<sub>0</sub>", 
						'type': 'linear',
						"titlefont": {
										"family": 'Roboto, Helvetica',
										"size": 16,
										"color": '#7f7f7f'
									},
									"tickfont": {
										"family": 'Roboto, Helvetica',
										"size": 16,
										"color": '#7f7f7f'
									}
						}
		layout['yaxis']= {
						'title': 't (ms)', 
						'type': 'linear',
						"titlefont": {
										"family": 'Roboto, Helvetica',
										"size": 16,
										"color": '#7f7f7f'
									},
									"tickfont": {
										"family": 'Roboto, Helvetica',
										"size": 16,
										"color": '#7f7f7f'
									}
						}
		layout['zaxis']= { 'type': 'linear' }
		layout['paper_bgcolor']='rgba(0,0,0,0)'
		layout['plot_bgcolor']='rgba(0,0,0,0)'
		layout['margin']={'l':'50', 'r':'50', 't':'0', 'b':'50'}
		layout['showlegend']=False
		layout['autosize']=True

		Z,xe,ye = self._hist2d()

		contour={}
		contour["z"]=Z.tolist()
		contour["x"]=list(ye)
		contour["y"]=list(xe)
		contour["type"]=self.plotType
		contour['colorscale']="YIGnBu"
		contour['line']={'shape':'spline', 'smoothing': 1.}

		self.responseDict['data']=[contour]
		self.responseDict['layout']=layout
		self.responseDict['options']={'displayLogo': False}

		self.responseDict['queryString']=base64.b64encode(str(self.queryString))

		return self.responseDict

	def _queryString(self, qstr):
		if qstr:
			return qstr
		else:
			if self.processingAlgorithm=="adept2State":
				return """select BlockDepth, ResTime from metadata where ProcessingStatus='normal' and ResTime > 0.02"""
			else:
				return """select BlockDepth, StateResTime from metadata where ProcessingStatus='normal' and ResTime > 0.02"""


	def _hist2d(self):
		try:
			q=query(
				self.AnalysisDBFile,
				self.queryString
			)

			y,x=np.transpose(np.array(q))
			
			Y=np.hstack(y)
			X=np.hstack(x)

			xmin=np.max(0, min(X))
			xmax=max(X)

			ymin=np.max(0, min(Y))
			ymax=max(Y)
		
			return np.histogram2d(X, Y, bins=(self.numBins, self.numBins), range=[[xmin, xmax], [ymin, ymax]])
		except ValueError:
			raise QuerySyntaxError("")

if __name__ == '__main__':
	import mosaic

	a=analysisContour(
			mosaic.WebServerDataLocation+"/m40_0916_RbClPEG/eventMD-20161208-130302.sqlite",
			"select BlockDepth, ResTime from metadata where ProcessingStatus='normal' and ResTime > 0.02",
			50
		)

	print a.analysisContour()