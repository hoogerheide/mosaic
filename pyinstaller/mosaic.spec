# -*- mode: python -*-
import sys
from mosaic.utilities.resource_path import resource_path, format_path

def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path

a = Analysis(['../runMOSAIC'],
			 pathex=['..'], 		# resource_path('.settings')
			 hiddenimports=['scipy.special._ufuncs_cxx', 'mosaicgui.mplwidget','Tkinter','FixTk','_tkinter','Tkconstants','FileDialog','Dialog'],
			 hookspath=None,
			 runtime_hooks=None)
# ('.settings', '../.settings',  'DATA'),

dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)

a.datas += [ 
				('icons/icon_100px.png', '../icons/icon_100px.png',  'DATA'),
				('commit-hash', '../commit-hash', 'DATA')
			]
pyz = PYZ(a.pure)
# On OS X, collect data files and  build an application bundle
if sys.platform=='darwin':
	exe = EXE(pyz,
		  a.scripts,
		  exclude_binaries=True,
		  name='MOSAIC',
		  debug=False,
		  strip=None,
		  upx=True,
		  console=False,
		  icon='icon.png' )
	coll = COLLECT(exe,
				   a.binaries,
				   Tree('../mosaicgui/ui', prefix='ui'),
				   a.zipfiles,
				   a.datas,
				   strip=None,
				   upx=True,
				   name=os.path.join('dist', 'MOSAIC'))
	app = BUNDLE(coll,
				   name=os.path.join('dist', 'MOSAIC.app'))
elif sys.platform=='win32' or sys.platform=='win64':
	for d in a.datas:
		if 'pyconfig' in d[0]: 
			a.datas.remove(d)
			break
	exe = EXE(pyz,
		a.scripts,
		a.binaries,
		Tree(format_path('../mosaicgui/ui'), prefix='ui'),
		a.zipfiles,
		a.datas,
		name='MOSAIC.exe',
		debug=False,
		strip=None,
		upx=True,
		console=False,
		icon='..\\icons\\icon_256px.ico' )
	# coll = COLLECT(exe,
	# 	a.binaries,
	# 	Tree(format_path('../mosaicgui/ui'), prefix='ui'),
	# 	a.zipfiles,
	# 	a.datas,
	# 	strip=None,
	# 	upx=True,
	# 	name=os.path.join('dist', 'MOSAIC'))