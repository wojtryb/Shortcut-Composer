from krita import *
from PyQt5.QtCore import QEvent
from time import time

from ..SETUP import INTERVAL

class keyFilter(QMdiArea):
	'object that handles one shortcut, installed on krita window and catches all keyboard inputs waiting for the correct one'

	def __init__(self, setLowFunction, setHighFunction, isHighStateFunction, relatedTool, addon, parent=None):
		super().__init__(parent)

		'reference to the whole addon holding time variable'
		self.addon = addon

		self.keyReleased = True									# is the pressed shortcut key already released?

		self.setLowFunction = setLowFunction
		self.setHighFunction = setHighFunction
		self.isHighStateFunction = isHighStateFunction
		self.relatedTool = relatedTool

		self.state = False										# is handled action already active? 
		

	def keyPress(self):
		'run when user presses a key assigned to this action'

		self.keyReleased = False								# key just pressed 
		self.addon.updateTime()									# remember the time of last key press of any modifier key

		'if the handled action wasnt already active, activate it - else, do nothing'
		self.state = self.isHighStateFunction(self.relatedTool[1]) 
		if not self.state:
			self.setHighFunction(self.relatedTool[1])


	def keyRelease(self):
		'run when user released a related key'

		self.keyReleased = True

		'if the key was pressed long time ago, and action is still active, deactivate it'
		if time() - self.addon.t > INTERVAL or self.state:
			self.setLowFunction()

	def eventFilter(self, obj, e):
		'activated each time user does anything - search for key releases'

		if e.type() == QEvent.KeyRelease:						# user released a key
			if (Krita.instance().action(self.relatedTool[0]).shortcut().matches(e.key()) > 0 # it was key for this action
			and not e.isAutoRepeat()							# this event is not sent because of long key press 
			and not self.keyReleased):							# user did not release key yet
				self.keyRelease()

		return False											# send this event further to krita

 
