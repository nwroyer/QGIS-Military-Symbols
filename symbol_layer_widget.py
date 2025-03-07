import sys

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
        self.spinSize.setMinimum(0)
        self.spinSize.setMaximum(10000)

        self.spinOverride = QgsPropertyOverrideButton(self.spinSize)
        hbox.addWidget(self.spinOverride)
        self.spinOverride.registerLinkedWidget(widget=self.spinSize)
        self.spinOverride.registerEnabledWidget(widget=self.spinSize, natural=False)
        self.spinOverride.changed.connect(self.sizeOverrideChanged)
        self.spinOverride.activated.connect(self.sizeOverrideChanged)

        # SIDC item
        self.sidcField = QLineEdit(None)
        hbox = QHBoxLayout()
        layout.addRow('SIDC', hbox)
        hbox.addWidget(self.sidcField)
        self.sidcField.textChanged.connect(self.sidcChanged)

        self.sidcOverride = QgsPropertyOverrideButton(self.sidcField)
        hbox.addWidget(self.sidcOverride)
        self.sidcOverride.registerLinkedWidget(widget=self.sidcField)
        self.sidcOverride.registerEnabledWidget(widget=self.sidcField, natural=False)
        self.sidcOverride.changed.connect(self.sidcOverrideChanged)
        self.sidcOverride.activated.connect(self.sidcOverrideChanged)

        self.updating = False

    def setSymbolLayer(self, layer:QgsSymbolLayer):
        if layer is None or layer.layerType() != "MilitarySymbolMarker":
            print('Bad marker', file=sys.stderr)
            return

        self.updating = True
        # Overall
        self.layer = layer
        vector_layer = iface.activeLayer()

        # Size
        self.spinSize.setValue(layer.size())
        self.spinOverride.init(propertyKey=MilitarySymbolLayer.Property.Size,
                               property=self.layer.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size),
                               definition=self.layer.propertyDefinitions()[MilitarySymbolLayer.Property.Size],
                               layer=vector_layer,
                               auxiliaryStorageEnabled=True)
        self.spinOverride.setActive(self.layer.is_size_data_defined())

        # SIDC
        self.sidcField.setText(layer.sidc)
        self.sidcOverride.init(propertyKey=MilitarySymbolLayer.Property.Name,
                               property=self.layer.dataDefinedProperties().property(MilitarySymbolLayer.Property.Name),
                               definition=self.layer.propertyDefinitions()[MilitarySymbolLayer.Property.Name],
                               layer=vector_layer,
                               auxiliaryStorageEnabled=True)
        self.sidcOverride.setActive(self.layer.is_sidc_data_defined())
        self.sidcField.setEnabled(not self.layer.is_sidc_data_defined())

        # Closeout
        self.updating = False

    def symbolLayer(self):
        return self.layer

    def sizeChanged(self, value):
        if self.updating:
            return

        raw_value = self.spinSize.value()
        override_active:bool = self.spinOverride.isActive()

        if override_active:
            size_prop: QgsProperty = self.spinOverride.toProperty()
            self.layer.set_size_data_defined(data_defined=True,
                                             expression=size_prop.expressionString())
        else:
            self.layer.set_size_data_defined(data_defined=False, value=raw_value)

        self.changed.emit()

    def sidcChanged(self, value):
        if self.updating:
            return

        raw_value = self.sidcField.text()
        override_active:bool = self.sidcOverride.isActive()

        if override_active:
            sidc_prop: QgsProperty = self.sidcOverride.toProperty()
            self.layer.set_sidc_data_defined(data_defined=True,
                                             expression=sidc_prop.expressionString())
        else:
            self.layer.set_sidc_data_defined(data_defined=False, value=raw_value)

        self.sidcField.setEnabled(not self.layer.is_sidc_data_defined())
        self.changed.emit()

    def sizeOverrideChanged(self):
        self.sizeChanged(0.0)

    def sidcOverrideChanged(self):
        self.sidcChanged('')


