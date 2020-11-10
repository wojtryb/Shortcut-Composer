from krita import *
from time import time
from .currentTool import getCurrentTool

SHORTCUTS = [
(Qt.Key_W, "KisToolSelectOutline"),
(Qt.Key_S, "KritaFill/KisToolGradient"),
(Qt.Key_V, "KritaShape/KisToolLine")
]

TIMEINTERVAL = 0.3

class toolModifier(Extension):

	def __init__(self, parent):
			super(toolModifier, self).__init__(parent)

	class mdiAreaFilter(QMdiArea):
		def __init__(self, parent=None):
			super().__init__(parent)
			self.updateTime()
			self.updateDiscardTime(True)
			self.updateDiscardTime(False)
			self.state = False

		def updateTime(self):
			self.t = time()

		def updateDiscardTime(self, par):
			if par:
				self.discardTimer1 = time()
			else:
				self.discardTimer2 = time()

		def discardByTime(self, par):
			if par: t = self.discardTimer1
			else: t = self.discardTimer2
			if time() - t < 0.05: return True
			else: return False

		def eventFilter(self, obj, e):
			if e.type() == QEvent.KeyPress or e.type() == QEvent.KeyRelease:
				for shortcut in SHORTCUTS:
					if e.key() == shortcut[0] and not e.isAutoRepeat():
						if e.type() == QEvent.KeyPress:
							if not self.discardByTime(True):
								if getCurrentTool() != shortcut[1]:
									Application.instance().action(shortcut[1]).trigger()
								else:
									Application.instance().action("KritaShape/KisToolBrush").trigger()
								self.updateTime()
								self.updateDiscardTime(True)

						elif e.type() == QEvent.KeyRelease:
							if not self.discardByTime(False):

								if time() - self.t > TIMEINTERVAL:
									if getCurrentTool() == shortcut[1]:
										Application.instance().action("KritaShape/KisToolBrush").trigger()

								self.updateDiscardTime(False)

						break
			return False

	def setup(self):
		pass

	def createActions(self, window):
		self.qwin = window.qwindow()
		self.mdiArea = self.qwin.centralWidget().findChild(QMdiArea)

		self.mdiAreaFilter = self.mdiAreaFilter()
		self.mdiArea.installEventFilter(self.mdiAreaFilter)

Krita.instance().addExtension(toolModifier(Krita.instance()))