# -*- coding: utf-8 -*-
"""
/***************************************************************************
 tuflowqgis_menu
                                 A QGIS plugin
 Initialises the TUFLOW menu system
                              -------------------
        begin                : 2013-08-27
        copyright            : (C) 2013 by Phillip Ryan
        email                : support@tuflow.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
build_vers = '2018-10-AB (QGIS 2.x)'
build_type = 'release' #release / developmental

# Import the PyQt and QGIS libraries

# Import the code for the dialog
from tuflowqgis_dialog import *

# Import the code for the 1D results viewer
from tuflowqgis_TuPlot import *
from TuPLOT_external import *
#from tuflow.tuflowqgis_bridge.tuflowqgis_bridge_gui import *

#par
from tuflowqgis_library import tuflowqgis_apply_check_tf

class tuflowqgis_menu:

	def __init__(self, iface):
		self.iface = iface
		self.dockOpened = False
		self.tpOpen = 'not open'
		self.intFile = ''
		self.cLayer = None
		self.tpExternal = None
		self.defaultPath = 'C:\\'
		self.resdock = None

	def initGui(self):
		# About Submenu
		self.about_menu = QMenu(QCoreApplication.translate("TUFLOW", "&About"))
		self.iface.addPluginToMenu("&TUFLOW", self.about_menu.menuAction())

		icon = QIcon(os.path.dirname(__file__) + "/icons/info.png")
		self.about_action = QAction(icon, "About", self.iface.mainWindow())
		QObject.connect(self.about_action, SIGNAL("triggered()"), self.about_tuflowqgis)
		self.about_menu.addAction(self.about_action)
		
		icon = QIcon(os.path.dirname(__file__) + "/icons/check_dependancy.png")
		self.check_dependancy_action = QAction(icon, "Check Python Dependencies Installed", self.iface.mainWindow())
		QObject.connect(self.check_dependancy_action, SIGNAL("triggered()"), self.check_dependencies)
		self.about_menu.addAction(self.check_dependancy_action)
		
		# Editing Submenu
		self.editing_menu = QMenu(QCoreApplication.translate("TUFLOW", "&Editing"))
		self.iface.addPluginToMenu("&TUFLOW", self.editing_menu.menuAction())
		
		#icon = QIcon(os.path.dirname(__file__) + "/icons/tuflow_increment_24px.png")
		icon = QIcon(os.path.dirname(__file__) + "/icons/tuflow.png")
		self.configure_tf_action = QAction(icon, "Configure / Create TUFLOW Project", self.iface.mainWindow())
		QObject.connect(self.configure_tf_action, SIGNAL("triggered()"), self.configure_tf)
		self.editing_menu.addAction(self.configure_tf_action)
		
		#icon = QIcon(os.path.dirname(__file__) + "/icons/tuflow.png")
		#self.create_tf_dir_action = QAction(icon, "Create TUFLOW Directory", self.iface.mainWindow())
		#QObject.connect(self.create_tf_dir_action, SIGNAL("triggered()"), self.create_tf_dir)
		#self.editing_menu.addAction(self.create_tf_dir_action)

		icon = QIcon(os.path.dirname(__file__) + "/icons/tuflow_import.png")
		self.import_empty_tf_action = QAction(icon, "Import Empty File", self.iface.mainWindow())
		QObject.connect(self.import_empty_tf_action, SIGNAL("triggered()"), self.import_empty_tf)
		self.editing_menu.addAction(self.import_empty_tf_action)
		
		# Add TUFLOW attribute fields to existing GIS layer Added ES 23/02/2018
		icon = QIcon(os.path.dirname(__file__) + "/icons/insert_tuflow_attributes.png")
		self.insert_TUFLOW_attributes_action = QAction(icon, "Insert TUFLOW Attributes to existing GIS layer", self.iface.mainWindow())
		QObject.connect(self.insert_TUFLOW_attributes_action, SIGNAL("triggered()"), self.insert_TUFLOW_attributes)
		self.editing_menu.addAction(self.insert_TUFLOW_attributes_action)
		
		icon = QIcon(os.path.dirname(__file__) + "/icons/tuflow_increment_24px.png")
		self.increment_action = QAction(icon, "Increment Selected Layer", self.iface.mainWindow())
		QObject.connect(self.increment_action, SIGNAL("triggered()"), self.increment_layer)
		self.editing_menu.addAction(self.increment_action)
		
		icon = QIcon(os.path.dirname(__file__) + "/icons/mif_2_shp.png")
		self.splitMI_action = QAction(icon, "Convert MapInfo file to Shapefile (beta)", self.iface.mainWindow())
		QObject.connect(self.splitMI_action, SIGNAL("triggered()"), self.split_MI)
		self.editing_menu.addAction(self.splitMI_action)

		icon = QIcon(os.path.dirname(__file__) + "/icons/mif_2_shp.png")
		self.splitMI_folder_action = QAction(icon, "Convert MapInfo files in folder Shapefile (beta)", self.iface.mainWindow())
		QObject.connect(self.splitMI_folder_action, SIGNAL("triggered()"), self.split_MI_folder)
		self.editing_menu.addAction(self.splitMI_folder_action)
		
		#Not tested enough to include
		#icon = QIcon(os.path.dirname(__file__) + "/icons/icon.png")
		#self.points_to_lines_action = QAction(icon, "Convert Points to Lines (survey to breaklines) ALPHA", self.iface.mainWindow())
		#QObject.connect(self.points_to_lines_action, SIGNAL("triggered()"), self.points_to_lines)
		#self.editing_menu.addAction(self.points_to_lines_action)
		
		

		# RUN Submenu
		self.run_menu = QMenu(QCoreApplication.translate("TUFLOW", "&Run"))
		self.iface.addPluginToMenu("&TUFLOW", self.run_menu.menuAction())
		
		icon = QIcon(os.path.dirname(__file__) + "/icons/Run_TUFLOW.png")
		self.run_tuflow_action = QAction(icon, "Run TUFLOW Simulation", self.iface.mainWindow())
		QObject.connect(self.run_tuflow_action, SIGNAL("triggered()"), self.run_tuflow)
		self.run_menu.addAction(self.run_tuflow_action)
		
		#top level in menu
		# Reload Data Added ES 16/07/18
		icon = QIcon(os.path.dirname(__file__) + "/icons/reload_data.png")
		self.reload_data_action = QAction(icon, "Reload Data", self.iface.mainWindow())
		self.reload_data_action.triggered.connect(self.reload_data)
		self.iface.addToolBarIcon(self.reload_data_action)
		self.iface.addPluginToMenu("&TUFLOW", self.reload_data_action)
		# TuPlot
		icon = QIcon(os.path.dirname(__file__) + "/icons/results.png")
		self.view_1d_results_action = QAction(icon, "TuPlot", self.iface.mainWindow())
		QObject.connect(self.view_1d_results_action, SIGNAL("triggered()"), self.results_1d)
		self.iface.addToolBarIcon(self.view_1d_results_action)
		self.iface.addPluginToMenu("&TUFLOW", self.view_1d_results_action)
		
		# TuPLOT External Added ES 2017/11
		icon = QIcon(os.path.dirname(__file__) + "/icons/TuPLOT_External.PNG")
		self.open_tuplot_external_action = QAction(icon, "TuPlot_Ext", self.iface.mainWindow())
		QObject.connect(self.open_tuplot_external_action, SIGNAL("triggered()"), self.open_tuplot_ext)
		self.iface.addToolBarIcon(self.open_tuplot_external_action)
		self.iface.addPluginToMenu("&TUFLOW", self.open_tuplot_external_action)
		
		# Added MJS 24/11
		icon = QIcon(os.path.dirname(__file__) + "/icons/tuflow_import.png")
		self.import_empty_tf_action = QAction(icon, "Import Empty File", self.iface.mainWindow())
		QObject.connect(self.import_empty_tf_action, SIGNAL("triggered()"), self.import_empty_tf)
		self.iface.addToolBarIcon(self.import_empty_tf_action)
		self.iface.addPluginToMenu("&TUFLOW", self.import_empty_tf_action)
		
		# insert TUFLOW attributes to existing GIS layer
		self.iface.addPluginToMenu("&TUFLOW", self.insert_TUFLOW_attributes_action)
		self.iface.addToolBarIcon(self.insert_TUFLOW_attributes_action)

		# Added MJS 24/11
		icon = QIcon(os.path.dirname(__file__) + "/icons/tuflow_increment_24px.png")
		self.increment_action = QAction(icon, "Increment Selected Layer", self.iface.mainWindow())
		QObject.connect(self.increment_action, SIGNAL("triggered()"), self.increment_layer)
		self.iface.addToolBarIcon(self.increment_action)
		self.iface.addPluginToMenu("&TUFLOW", self.increment_action)
  
		# Added MJS 11/02   
		icon = QIcon(os.path.dirname(__file__) + "/icons/check_files_folder.png")
		self.import_chk_action = QAction(icon, "Import Check Files from Folder", self.iface.mainWindow())
		QObject.connect(self.import_chk_action, SIGNAL("triggered()"), self.import_check)
		self.iface.addToolBarIcon(self.import_chk_action)
		self.iface.addPluginToMenu("&TUFLOW", self.import_chk_action)
	
		#PAR 2016/02/12
		icon = QIcon(os.path.dirname(__file__) + "/icons/check_files_open.png")
		self.apply_chk_action = QAction(icon, "Apply TUFLOW Styles to Open Layers", self.iface.mainWindow())
		QObject.connect(self.apply_chk_action, SIGNAL("triggered()"), self.apply_check)
		self.iface.addToolBarIcon(self.apply_chk_action)
		self.iface.addPluginToMenu("&TUFLOW", self.apply_chk_action)
		
		#PAR 2016/02/15
		icon = QIcon(os.path.dirname(__file__) + "/icons/check_files_currentlayer.png")
		self.apply_chk_cLayer_action = QAction(icon, "Apply TUFLOW Styles to Current Layer", self.iface.mainWindow())
		QObject.connect(self.apply_chk_cLayer_action, SIGNAL("triggered()"), self.apply_check_cLayer)
		self.iface.addToolBarIcon(self.apply_chk_cLayer_action)
		self.iface.addPluginToMenu("&TUFLOW", self.apply_chk_cLayer_action)
		
		#Auto label generator ES 8/03/2018
		icon = QIcon(os.path.dirname(__file__) + "/icons/Label_icon.PNG")
		self.apply_auto_label_action = QAction(icon, "Apply Label to Current Layer", self.iface.mainWindow())
		QObject.connect(self.apply_auto_label_action, SIGNAL("triggered()"), self.apply_label_cLayer)
		self.iface.addToolBarIcon(self.apply_auto_label_action)
		self.iface.addPluginToMenu("&TUFLOW", self.apply_auto_label_action)
		
		# ES 2018/01 ARR2016 Beta
		icon = QIcon(os.path.dirname(__file__) + "/icons/arr2016.PNG")
		self.extract_arr2016_action = QAction(icon, "Extract ARR2016 for TUFLOW (beta)", self.iface.mainWindow())
		QObject.connect(self.extract_arr2016_action, SIGNAL("triggered()"), self.extract_arr2016)
		self.iface.addPluginToMenu("&TUFLOW", self.extract_arr2016_action)
		self.iface.addToolBarIcon(self.extract_arr2016_action)
		
		# ES 2018/05 Load input files from TCF
		icon = QIcon(os.path.dirname(__file__) + "/icons/load_from_TCF.PNG")
		self.load_tuflowFiles_from_TCF_action = QAction(icon, "Load TUFLOW Layers from TCF", self.iface.mainWindow())
		QObject.connect(self.load_tuflowFiles_from_TCF_action, SIGNAL("triggered()"), self.loadTuflowLayers)
		self.iface.addPluginToMenu("&TUFLOW", self.load_tuflowFiles_from_TCF_action)
		self.iface.addToolBarIcon(self.load_tuflowFiles_from_TCF_action)
		
		# Check 1D network integrity
		self.check_1d_integrity_action = QAction("Check 1D Network Integrity (beta)", self.iface.mainWindow())
		self.check_1d_integrity_action.triggered.connect(self.check_1d_integrity)
		self.iface.addPluginToMenu("&TUFLOW", self.check_1d_integrity_action)

		# Bridge Editor
		#self.open_bridge_editor_action = QAction("Bridge Editor (beta)", self.iface.mainWindow())
		#self.open_bridge_editor_action.triggered.connect(self.open_bridge_editor)
		#self.iface.addPluginToMenu("&TUFLOW", self.open_bridge_editor_action)
		
		#Init classes variables
		self.dockOpened = False		#remember for not reopening dock if there's already one opened
		self.resdockOpened = False
		self.selectionmethod = 0						#The selection method defined in option
		self.saveTool = self.iface.mapCanvas().mapTool()			#Save the standard mapttool for restoring it at the end
		self.layerindex = None							#for selection mode
		self.previousLayer = None						#for selection mode
		self.plotlibrary = None							#The plotting library to use
		self.textquit0 = "Click for polyline and double click to end (right click to cancel then quit)"
		self.textquit1 = "Select the polyline in a vector layer (Right click to quit)"

	def unload(self):
		self.iface.removePluginMenu("&TUFLOW", self.about_menu.menuAction())
		self.iface.removePluginMenu("&TUFLOW", self.editing_menu.menuAction())
		self.iface.removePluginMenu("&TUFLOW", self.run_menu.menuAction())
		del self.import_chk_action

	def configure_tf(self):
		project = QgsProject.instance()
		dialog = tuflowqgis_configure_tf_dialog(self.iface,project)
		dialog.exec_()

	def create_tf_dir(self):
		project = QgsProject.instance()
		dialog = tuflowqgis_create_tf_dir_dialog(self.iface, project)
		dialog.exec_()
		
	def import_empty_tf(self):
		project = QgsProject.instance()
		dialog = tuflowqgis_import_empty_tf_dialog(self.iface, project)
		dialog.exec_()

	def increment_layer(self):
		dialog = tuflowqgis_increment_dialog(self.iface)
		dialog.exec_()
	
	def flow_trace(self):
		dialog = tuflowqgis_flowtrace_dialog(self.iface)
		dialog.exec_()
		
	def points_to_lines(self):
		#QMessageBox.information(self.iface.mainWindow(), "debug", "points to lines")
		dialog = tuflowqgis_line_from_points(self.iface)
		dialog.exec_()

	def split_MI(self):
		#QMessageBox.information(self.iface.mainWindow(), "debug", "points to lines")
		dialog = tuflowqgis_splitMI_dialog(self.iface)
		dialog.exec_()

	def split_MI_folder(self):
		#QMessageBox.information(self.iface.mainWindow(), "debug", "points to lines")
		QMessageBox.information( self.iface.mainWindow(),"debug", "starting" )
		dialog = tuflowqgis_splitMI_folder_dialog(self.iface)
		dialog.exec_()
		
#### external viewer interface
#	def results_1d_ext(self):
#		if self.dockOpened == False:
#			self.dock = TUFLOWifaceDock(self.iface)
#			self.iface.addDockWidget( Qt.RightDockWidgetArea, self.dock )
#			self.dockOpened = True
		
	def reload_data(self):
		try:
			if QGis.QGIS_VERSION_INT >= 211:
				layer = self.iface.mapCanvas().currentLayer()
				layer.dataProvider().forceReload()
				layer.triggerRepaint()
			else:
				QMessageBox.information(self.iface.mainWindow, 'Message', 'Reload tool is not compatible with QGIS version 2.10 or lower')
		except:
			pass
	
	def results_1d(self):
		#if self.resdockOpened == False:
		if self.dockOpened:
			#QMessageBox.information(self.iface.mainWindow(), "debug", "Show it")
			self.resdock.qgis_connect()
			self.resdock.show()
			self.resdock.layerChanged()
			
		else:
			self.dockOpened = True
			self.resdock = TuPlot(self.iface)
			self.iface.addDockWidget( Qt.RightDockWidgetArea, self.resdock)
		#else:
		#	if self.resdock.dockOpened:
		#		#QMessageBox.information(self.iface.mainWindow(), "debug", "Dock already open")
		#		#QMessageBox.information(self.iface.mainWindow(), "debug", "Show it")
		#		self.resdock.show()
		#	else:
		#		QMessageBox.information(self.iface.mainWindow(), "debug", "Dock not open??")
		
	def open_tuplot_ext(self):
		"""TuPLOT external function."""
		
		# initiate External TuPLOT library
		self.tpExternal = TuPLOT(self.iface)
		
		# below try statement just checks if TuPLOT is already open
		try:
			poll = self.tpOpen.poll()
			if poll == None: # TuPLOT is open
				self.tpOpen, self.intFile, self.defaultPath = self.tpExternal.open(self.tpOpen, self.intFile, self.defaultPath)
				self.cLayer = self.iface.mapCanvas().currentLayer()
			else: # TuPLOT is not already open
				self.tpOpen, self.intFile, self.defaultPath = self.tpExternal.open('not open', self.intFile, self.defaultPath)
				self.cLayer = self.iface.mapCanvas().currentLayer()
		except: # first time TuPLOT has been initiated so must not be open
			self.tpOpen, self.intFile, self.defaultPath = self.tpExternal.open('not open', self.intFile, self.defaultPath)
			self.cLayer = self.iface.mapCanvas().currentLayer()
		
		# connect external TuPLOT to signals
		try:
			poll = self.tpOpen.poll()
			if poll == None: # TuPLOT is running so connect
				if self.cLayer is not None: # there is a current layer selected so connect both selection change and layer change
					QObject.connect(self.cLayer,SIGNAL("selectionChanged()"),self.select_changed)
					QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.layer_changed)
				else: # there is no current layer selected so connect layer change only
					QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.layer_changed)
			else: # TuPLOT is not running so disconnect
				QObject.disconnect(self.cLayer,SIGNAL("selectionChanged()"),self.select_changed)
				QObject.disconnect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.layer_changed)
		except:
			None
		#QMessageBox.information(self.iface.mainWindow(), "Debug", "completed")
		
	def select_changed(self):
		"""Used with TuPLOT external function. Is called when current selection changes."""
		
		# check to see if TuPLOT is open
		poll = self.tpOpen.poll()
		if poll == None: # TuPLOT is open so update .int file
			self.tpOpen, self.intFile, self.defaultPath = self.tpExternal.open(self.tpOpen, self.intFile, self.defaultPath)
		else: # TuPLOT is not open so disconnect signals
			QObject.disconnect(self.cLayer,SIGNAL("selectionChanged()"),self.select_changed)
			QObject.disconnect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.layer_changed)
		
	def layer_changed(self):
		"""Used with TuPLOT external function. Is called when current layer changes."""
		
		self.cLayer = self.iface.mapCanvas().currentLayer()
		if self.cLayer is not None:
			QObject.connect(self.cLayer,SIGNAL("selectionChanged()"),self.select_changed)

	def cleaning_res(res):
		QMessageBox.information(self.iface.mainWindow(), "debug", "Dock Closed")
		self.dockOpened = False
		
	def run_tuflow(self):
		project = QgsProject.instance()
		dialog = tuflowqgis_run_tf_simple_dialog(self.iface, project)
		dialog.exec_()
	
	def check_dependencies(self):
		#QMessageBox.critical(self.iface.mainWindow(), "Info", "Not yet implemented!")
		from tuflowqgis_library import check_python_lib
		error = check_python_lib(self.iface)
		if error <> None:
			QMessageBox.critical(self.iface.mainWindow(), "Error", "Not all dependencies installed.")
		else:
			QMessageBox.information(self.iface.mainWindow(), "Information", "All dependencies installed :)")

	def about_tuflowqgis(self):
		#QMessageBox.information(self.iface.mainWindow(), "About TUFLOW QGIS", 'This is a developmental version of the TUFLOW QGIS utitlity, build: '+build_vers)
		QMessageBox.information(self.iface.mainWindow(), "About TUFLOW QGIS", "This is a {0} version of the TUFLOW QGIS utitlity\nBuild: {1}".format(build_type,build_vers))

	# Added MJS 11/02
	def import_check(self):
		project = QgsProject.instance()
		dialog = tuflowqgis_import_check_dialog(self.iface, project)
		dialog.exec_()
		
	def apply_check(self):
		error, message = tuflowqgis_apply_check_tf(self.iface)
		if error:
			QMessageBox.critical(self.iface.mainWindow(), "Error", message)
	
	def apply_check_cLayer(self):
		error, message = tuflowqgis_apply_check_tf_clayer(self.iface)
		if error:
			QMessageBox.critical(self.iface.mainWindow(), "Error", message)
	
	def extract_arr2016(self):
		dialog = tuflowqgis_extract_arr2016_dialog(self.iface)
		dialog.exec_()
		
	def insert_TUFLOW_attributes(self):
		project = QgsProject.instance()
		dialog = tuflowqgis_insert_tuflow_attributes_dialog(self.iface, project)
		dialog.exec_()
		
	def apply_label_cLayer(self):
		error, message = tuflowqgis_apply_autoLabel_clayer(self.iface)
		if error:
			QMessageBox.critical(self.iface.mainWindow(), "Error", message)
	
	def check_1d_integrity(self):
		self.dialog = tuflowqgis_check_1d_integrity_dialog(self.iface, self.dockOpened, self.resdock)
		self.dialog.exec_()
		self.dockOpened = self.dialog.dockOpened
		self.resdock = self.dialog.resdock
		
	def loadTuflowLayers(self):
		settings = QSettings()
		lastFolder = str(settings.value("TUFLOW/TCF_last_folder", os.sep))
		if (len(lastFolder) > 0):  # use last folder if stored
			fpath = lastFolder
		else:
			cLayer = self.iface.mapCanvas.currentLayer()
			if cLayer:  # if layer selected use the path to this
				dp = cLayer.dataProvider()
				ds = dp.dataSourceUri()
				fpath = os.path.dirname(unicode(ds))
			else:  # final resort to current working directory
				fpath = os.getcwd()
		
		inFileNames = QFileDialog.getOpenFileNames(self.iface.mainWindow(), 'Open TUFLOW TCF', fpath,
		                                           "TCF (*.tcf)")
		for inFileName in inFileNames:
			if not inFileName or len(inFileName) < 1:  # empty list
				return
			else:
				fpath, fname = os.path.split(inFileName)
				if fpath != os.sep and fpath.lower() != 'c:\\' and fpath != '':
					settings.setValue("TUFLOW/TCF_last_folder", fpath)
				if os.path.splitext(inFileName)[1].lower() != '.tcf':
					QMessageBox.information(self.iface.mainWindow(), "Message", 'Must select TCF')
					return
				else:
					error, message, scenarios = getScenariosFromTcf(inFileName, self.iface)
					if error:
						QMessageBox.information(self.iface.mainWindow(), "Message", message)
					if len(scenarios) > 0:
						self.dialog = tuflowqgis_scenarioSelection_dialog(self.iface, inFileName, scenarios)
						self.dialog.exec_()
					else:
						openGisFromTcf(inFileName, self.iface)


	def open_bridge_editor(self):
		self.bridgeGui = bridgeGui(self.iface)
		self.iface.addDockWidget(Qt.RightDockWidgetArea, self.bridgeGui)