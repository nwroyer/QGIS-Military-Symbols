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

        # SIDC item
        self.spinOverride.changed.connect(self.sizeOverrideChanged)
        self.spinOverride.activated.connect(self.sizeOverrideChanged)

        self.updating = False

    def setSymbolLayer(self, layer:QgsSymbolLayer):
        if layer is None or layer.layerType() != "MilitarySymbolMarker":
            print('Bad marker')
            return

        self.updating = True
        print('Marker')
        self.layer = layer
        vector_layer = iface.activeLayer()

        self.spinSize.setValue(layer.size())
        self.spinOverride.init(propertyKey=MilitarySymbolLayer.Property.Size,
                               property=self.layer.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size),
                               definition=self.layer.propertyDefinitions()[MilitarySymbolLayer.Property.Size],
                               layer=vector_layer,
                               auxiliaryStorageEnabled=True)

        # size_prop = self.layer.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size)
        # self.spinOverride.setToProperty(size_prop)
        #
        is_active = self.layer.is_size_data_defined()
        self.spinOverride.setActive(is_active)
        # self.spinSize.setEnabled(not is_active)

        self.updating = False

        # is_size_overridden = self.layer.is_size_data_defined()
        # self.spinSize.setProperty()
        # self.spinOverride.setActive(self.layer.is_size_data_defined())
        #
        # if is_size_overridden:
        #     print(f'Layering expression {self.layer.get_size_data_defined_expression()}')


    def symbolLayer(self):
        return self.layer

    def sizeChanged(self, value):
        if self.updating:
            return

        raw_value = self.spinSize.value()
        override_active:bool = self.spinOverride.isActive()

        print(f'Updating size: {raw_value} / override active: {override_active}')

        if override_active:
            size_prop: QgsProperty = self.spinOverride.toProperty()
            self.layer.set_size_data_defined(data_defined=True,
                                             expression=size_prop.expressionString())
        else:
            self.layer.set_size_data_defined(data_defined=False, value=raw_value)

        self.changed.emit()

    def sizeOverrideChanged(self):
        self.sizeChanged(0.0)


