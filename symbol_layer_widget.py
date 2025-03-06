import qgis.utils
from qgis.gui import QgsSymbolLayerWidget, QgsFieldValuesLineEdit, QgsPropertyOverrideButton, QgsDoubleSpinBox, QgsLayerPropertiesWidget
from qgis.PyQt.QtWidgets import QLabel, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit
from qgis.core import QgsMarkerSymbolLayer, QgsProperty, QgsPropertyDefinition, QgsSymbolLayer, QgsApplication, QgsExpressionContext

from .symbol_layer import MilitarySymbolLayer
from qgis.utils import iface

class MilitarySymbolLayerWidget(QgsSymbolLayerWidget):
    def __init__(self, parent=None):
        QgsSymbolLayerWidget.__init__(self, parent)

        self.layer:MilitarySymbolLayer = None

        layout = QFormLayout()
        self.setLayout(layout)

        # Size item
        self.spinSize = QgsDoubleSpinBox(None)
        hbox = QHBoxLayout()
        layout.addRow('Size', hbox)
        hbox.addWidget(self.spinSize)
        self.spinSize.valueChanged.connect(self.sizeChanged)

        self.spinOverride = QgsPropertyOverrideButton(self.spinSize)
        hbox.addWidget(self.spinOverride)
        self.spinOverride.registerLinkedWidget(widget=self.spinSize)
        self.spinOverride.registerEnabledWidget(widget=self.spinSize, natural=False)

        # SIDC item
        self.spinOverride.changed.connect(self.sizeOverrideChanged)
        self.spinOverride.activated.connect(self.sizeOverrideChanged)

    def setSymbolLayer(self, layer:QgsSymbolLayer):
        if layer is None or layer.layerType() != "MilitarySymbolMarker":
            print('Bad marker')
            return

        print('Marker')
        self.layer = layer
        vector_layer = iface.activeLayer()

        self.spinSize.setValue(layer.get_size_value(None))

        self.spinOverride.init(MilitarySymbolLayer.Property.Size,
                               self.layer.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size),
                               self.layer.propertyDefinitions()[MilitarySymbolLayer.Property.Size],
                               vector_layer)

        self.spinOverride.setProperty('size_prop', self.layer.size_prop)
        self.spinOverride.setActive(self.layer.size_expression)

        if self.layer.size_expression:
            print(f'Layering expression {self.layer.size_prop}')
            self.spinOverride.setProperty(QgsProperty.fromExpression(self.layer.size_prop))

    def symbolLayer(self):
        return self.layer

    def sizeChanged(self, value):
        raw_value = self.spinSize.value()
        override_active:bool = self.spinOverride.isActive()

        print(f'Updating size: {raw_value} / override active: {override_active}')

        if override_active:
            self.layer.size_expression = True
            size_prop:QgsProperty = self.spinOverride.toProperty()
            self.layer.size_prop = size_prop.expressionString()
        else:
            self.layer.size_expression = False
            self.layer.size_prop = raw_value

        self.changed.emit()

    def sizeOverrideChanged(self):
        self.sizeChanged(0.0)


