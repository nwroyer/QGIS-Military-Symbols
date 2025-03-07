import sys

import qgis.utils
from PyQt5.QtWidgets import QComboBox
from qgis.gui import QgsSymbolLayerWidget, QgsFieldValuesLineEdit, QgsPropertyOverrideButton, QgsDoubleSpinBox, QgsLayerPropertiesWidget
from qgis.PyQt.QtWidgets import QLabel, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox
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

        # SIDC is name
        self.sidcIsNameField = QCheckBox()
        hbox = QHBoxLayout()
        layout.addRow('Field is name', hbox)
        hbox.addWidget(self.sidcIsNameField)
        self.sidcIsNameField.stateChanged.connect(self.sidcIsNameChanged)

        self.sidcIsNameOverride = QgsPropertyOverrideButton(self.sidcIsNameField)
        hbox.addWidget(self.sidcIsNameOverride)
        self.sidcIsNameOverride.registerLinkedWidget(widget=self.sidcIsNameField)
        self.sidcIsNameOverride.registerEnabledWidget(widget=self.sidcIsNameField, natural=False)
        self.sidcIsNameOverride.changed.connect(self.sidcIsNameOverrideChanged)
        self.sidcIsNameOverride.activated.connect(self.sidcIsNameOverrideChanged)

        # Style
        self.styleField = QComboBox()
        self.styleField.addItems([d.capitalize() for d in MilitarySymbolLayer.STYLE_OPTIONS])
        layout.addRow('Style', self.styleField)
        self.styleField.currentIndexChanged.connect(self.styleChanged)

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

        # SIDC is name
        self.sidcIsNameField.setChecked(self.layer.sidc_is_name)
        self.sidcIsNameOverride.init(propertyKey=MilitarySymbolLayer.Property.JoinStyle,
                               property=self.layer.dataDefinedProperties().property(MilitarySymbolLayer.Property.JoinStyle),
                               definition=self.layer.propertyDefinitions()[MilitarySymbolLayer.Property.JoinStyle],
                               layer=vector_layer,
                               auxiliaryStorageEnabled=True)
        self.sidcIsNameOverride.setActive(self.layer.is_sidc_is_name_data_defined())
        self.sidcIsNameField.setEnabled(not self.layer.is_sidc_is_name_data_defined())

        # Style
        if self.layer.style in MilitarySymbolLayer.STYLE_OPTIONS:
            self.styleField.setCurrentIndex(MilitarySymbolLayer.STYLE_OPTIONS.index(self.layer.style))
        else:
            self.styleField.setCurrentIndex(0)

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

    def sidcIsNameChanged(self, on:bool):
        if self.layer is None or self.updating:
            return

        raw_value = self.sidcIsNameField.isChecked()
        override_active:bool = self.sidcIsNameOverride.isActive()

        if override_active:
            sidc_prop: QgsProperty = self.sidcIsNameOverride.toProperty()
            self.layer.set_sidc_is_name_data_defined(data_defined=True,
                                                     expression=sidc_prop.expressionString())
        else:
            self.layer.set_sidc_is_name_data_defined(data_defined=False,
                                                     value=raw_value)

        self.sidcIsNameField.setEnabled(not self.layer.is_sidc_is_name_data_defined())
        self.changed.emit()

    def sidcIsNameOverrideChanged(self):
        self.sidcIsNameChanged(False)

    def styleChanged(self, index):
        if self.layer is None or self.updating:
            return

        self.layer.style = MilitarySymbolLayer.STYLE_OPTIONS[index]
        self.changed.emit()

