from PyQt5.QtWidgets import QVBoxLayout
from qgis.gui import QgsSymbolLayerWidget, QgsExpressionBuilderWidget
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
        label = QLabel("Radius:")
        hbox.addWidget(label)
        self.spinRadius = QDoubleSpinBox()
        hbox.addWidget(self.spinRadius)
        self.spinRadius.valueChanged.connect(self.radiusChanged)

        # SIDC item
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        self.sidc:QgsExpressionBuilderWidget = QgsExpressionBuilderWidget()
        hbox.addWidget(QLabel('SIDC:'))
        hbox.addWidget(self.sidc)

    def setSymbolLayer(self, layer):
        if layer is None or layer.layerType() != "MilitarySymbolMarker":
            print('Bad marker')
            return

        print('Marker')
        self.layer = layer
        self.spinRadius.setValue(layer.radius)



    def symbolLayer(self):
        return self.layer

    def radiusChanged(self, value):
        self.layer.radius = value
        self.changed.emit()