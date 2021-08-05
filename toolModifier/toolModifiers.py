from krita import *
from time import time
from PyQt5.QtCore import QObject, QEvent

from .currentTool import getCurrentTool


TOOLS = [
("Freehand selection (toggle)", "KisToolSelectOutline"),
("Gradient (toggle)", "KritaFill/KisToolGradient"),
("Line tool (toggle)", "KritaShape/KisToolLine"),
("Transform tool (toggle)", "KisToolTransform"),
("Move tool (toggle)", "KritaTransform/KisToolMove")
]

def setTool(toolName):
	Application.instance().action(toolName).trigger()

def setBrushTool():
	setTool("KritaShape/KisToolBrush")

def isToolSelected(toolName):
	if getCurrentTool() == toolName: return True
	else: return False



class Filter(QMdiArea):
	'object that handles one shortcut, installed on krita window and catches all keyboard inputs waiting for the correct one'

	def __init__(self, setLowFunction, setHighFunction, isHighStateFunction, relatedTool, addon, parent=None):
		super().__init__(parent)

		'reference to the whole addon holding time variable'
		self.addon = addon

		self.keyReleased = True						# is the pressed shortcut key already released?

		self.setLowFunction = setLowFunction
		self.setHighFunction = setHighFunction
		self.isHighStateFunction = isHighStateFunction
		self.relatedTool = relatedTool

		self.state = False							# is handled action already active? 
		

	def keyPress(self):
		'run when user presses a key assigned to this action'

		self.keyReleased = False					# key just pressed 
		self.addon.updateTime()						# remember the time of last key press of any modifier key

		'if the handled action wasnt already active, activate it - else, do nothing'
		self.state = self.isHighStateFunction(self.relatedTool[1]) 
		if not self.state:
			self.setHighFunction(self.relatedTool[1])


	def keyRelease(self):
		'run when user released a related key'

		self.keyReleased = True

		'if the key was pressed long time ago, and action is still active, deactivate it'
		if time() - self.addon.t > 0.3 or self.state:
			self.setLowFunction()

	def eventFilter(self, obj, e):
		'activated each time user does anything - search for key releases'

		if e.type() == QEvent.KeyRelease:			# user released a key
			if (Krita.instance().action(self.relatedTool[0]).shortcut().matches(e.key()) > 0 # it was key for this action
			and not e.isAutoRepeat()				# this event is not sent because of long key press 
			and not self.keyReleased):				# user did not release key yet
				self.keyRelease()

		return False								# send this event further to krita




class toolModifiers(Extension):
	'the extension'

	def __init__(self, parent):
		super(toolModifiers, self).__init__(parent)
		
		self.filters = []  							# hold the list of all installed filters - one for each shortcut
		self.updateTime()  							# create self.t variable that holds the time of last modifier press


	def setup(self):
		pass


	def updateTime(self):
		'trigger when one of modifiers pressed - remember the time of this event'
		self.t = time()


	def createActions(self, window):
		'create an action for each of the shortcuts'

		qwin = window.qwindow()
		for toolName, tool in TOOLS:

			action = window.createAction(toolName, toolName, "") # use human-readable name as action name and desctiption, dont show action in any of krita tabs
			action.setAutoRepeat(False) 						 # 'dont retrigger action when shortcut is pressed for a longer time'

			fil = Filter(										 # create a filter that catches keyboard events
				setLowFunction = setBrushTool,				     # when user switches to low state (releases the key) - set brush tool
				setHighFunction= setTool,						 # when user switches to high state (presses the key) - set a key passed in argument
				isHighStateFunction = isToolSelected,			 # function that returns True if krita is already in high state (like the tool is already active)
				relatedTool = (toolName, tool),					 # tool that should get activated - human-readable name and krita name
				addon = self) 									 # reference to the addon

			qwin.installEventFilter(fil)						 # install the filter on krita
			action.triggered.connect(fil.keyPress)				 # when action is triggered with keyboard shortcut, run keyPress function

			self.filters.append(fil)						     # store the filter object in the addon, so that it won't get removed 


'load the extension on krita start-up'
Krita.instance().addExtension(toolModifiers(Krita.instance()))