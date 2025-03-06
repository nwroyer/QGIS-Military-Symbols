from PyQt5.QtWidgets import QVBoxLayout
from qgis.gui import QgsSymbolLayerWidget, QgsFieldValuesLineEdit
from qgis.PyQt.QtWidgets import QLabel, QDoubleSpinBox, QHBoxLayout
from .symbol_layer import MilitarySymbolLayer

class MilitarySymbolLayerWidget(QgsSymbolLayerWidget):
    def __init__(self, parent=None):
        QgsSymbolLayerWidget.__init__(self, parent)

        self.layer:MilitarySymbolLayer = None

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Radius item
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        label = QLabel("Size:")
        hbox.addWidget(label)
        self.spinSize = QDoubleSpinBox()
        hbox.addWidget(self.spinSize)
        self.spinSize.valueChanged.connect(self.sizeChanged)

        # SIDC item
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        hbox.addWidget(QLabel('SIDC:'))
        hbox.addWidget(self.sidc)

    def setSymbolLayer(self, layer):
        if layer is None or layer.layerType() != "MilitarySymbolMarker":
            print('Bad marker')
            return

        print('Marker')
        self.layer = layer
        self.spinSize.setValue(layer.size())



    def symbolLayer(self):
        return self.layer

    def sizeChanged(self, value):
        print(f'Changing size to {value}')
        self.layer.setSize(value)
        self.changed.emit()