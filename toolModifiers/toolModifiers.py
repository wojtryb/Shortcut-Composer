from krita import *
from time import time

from .importCode.keyFilter import keyFilter
from .importCode.passFunctions import setTool, setBrushTool, isToolSelected, isEraserActive, toggleEraser, isAlphaLocked, toggleAlphaLock
from .importCode.definedActions import definedActions

from .SETUP import TOOLS





class toolModifiers(Extension):
	'the extension'

	def __init__(self, parent):
		super(toolModifiers, self).__init__(parent)
		
		self.filters = []  										# hold the list of all installed filters - one for each shortcut
		self.updateTime()  										# create self.t variable that holds the time of last modifier press


	def setup(self):
		pass


	def updateTime(self):
		'trigger when one of modifiers pressed - remember the time of this event'
		self.t = time()


	'-----=========------'

	def createShortcut(self, humanName, kritaName, setLowFunction, setHighFunction, isHighStateFunction):
		'creates a single shortcut action, installs its filter and saves in a addon'

		action = self.window.createAction(humanName, humanName, "") # use human-readable name as action name and desctiption, dont show action in any of krita tabs
		action.setAutoRepeat(False) 					 # dont retrigger action when shortcut is pressed for a longer time'

		fil = keyFilter(								 # create a filter that catches keyboard events
			setLowFunction = setLowFunction,			 # what to do on raising slope
			setHighFunction= setHighFunction,		     # what to do on falling slope
			isHighStateFunction = isHighStateFunction,	 # how to know that the shortcut is activated
			relatedTool = (humanName, kritaName),	     # tool that should get activated - human-readable name and krita name
			addon = self) 								 # reference to the addon

		self.window.qwindow().installEventFilter(fil)	 # install the filter on krita
		action.triggered.connect(fil.keyPress)			 # when action is triggered with keyboard shortcut, run keyPress function

		self.filters.append(fil)						 # store the filter object in the addon, so that it won't get removed 


	'-----=========------'


	def createActions(self, window):
		'run on startup - creates all keyboard shortcuts in the plugin - tool modifiers needed by the user, and toggles for eraser and preserve alpha'

		self.window = window							 # hold the reference to krita window
		i = 1										     # counter for tools using default name - not defined in .action file

		'create an action for each of the tool toggle shortcuts'
		for kritaName in TOOLS:
			humanName = definedActions.get(kritaName, f'Tool {i} (toggle)') # get human-readable name, or default name, if its name isn't defined in actions
			if humanName.split(" ")[0] == "Tool": i += 1	 			    # raise counter for default tool name

			self.createShortcut(
				humanName=humanName,
				kritaName=kritaName,
				setLowFunction=setBrushTool,		     # when user switches to low state (releases the key) - set brush tool
				setHighFunction=setTool,				 # when user switches to high state (presses the key) - set a key passed in argument
				isHighStateFunction=isToolSelected)		 # function that returns True if krita is already in high state (like the tool is already active)


		'create action for eraser'
		self.createShortcut('Eraser (toggle)', '', toggleEraser, toggleEraser, isEraserActive)

		'create action for alpha lock'
		self.createShortcut('Preserve alpha (toggle)', '', toggleAlphaLock, toggleAlphaLock, isAlphaLocked)




'load the extension on krita start-up'
Krita.instance().addExtension(toolModifiers(Krita.instance()))