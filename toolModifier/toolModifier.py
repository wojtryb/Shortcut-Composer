from krita import *

SHORTCUTS = [
(Qt.Key_U, "KisToolSelectOutline"),
(Qt.Key_T, "KritaFill/KisToolGradient")
]

class toolModifier(Extension):

	def __init__(self, parent):
			super(toolModifier, self).__init__(parent)

	class mdiAreaFilter(QMdiArea):
		def __init__(self, parent=None):
			super().__init__(parent)
			
		def eventFilter(self, obj, e):
			if e.type() == QEvent.KeyPress or e.type() == QEvent.KeyRelease:
				for shortcut in SHORTCUTS:
					if e.key() == shortcut[0] and not e.isAutoRepeat():
						if e.type() == QEvent.KeyPress:
							Application.instance().action(shortcut[1]).trigger()
						elif e.type() == QEvent.KeyRelease:
							Application.instance().action("KritaShape/KisToolBrush").trigger()
			return False

	def setup(self):
		pass

	def createActions(self, window):
		self.qwin = window.qwindow()
		self.mdiArea = self.qwin.centralWidget().findChild(QMdiArea)

		self.mdiAreaFilter = self.mdiAreaFilter()
		self.mdiArea.installEventFilter(self.mdiAreaFilter)
		print("created")

Krita.instance().addExtension(toolModifier(Krita.instance()))