from qgis.PyQt.QtGui import QAction
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from .symbol_layer_metadata import MilitarySymbolLayerMetadata

# initialize Qt resources from file resources.py
# from . import resources

class MilitarySymbolPlugin:
    def __init__(self, iface:QgisInterface):
        self.iface = iface

        # Add the symbol layer
        print('Adding symbol layer')
        symbol_layer_metadata = MilitarySymbolLayerMetadata()
        QgsApplication.symbolLayerRegistry().addSymbolLayerType(symbol_layer_metadata)

    def initGui(self):
        self.action = QAction('Go!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        QMessageBox.information(None, 'Minimal plugin', 'Do something useful to here')
