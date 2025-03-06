from qgis.core import QgsSymbol, QgsSymbolLayerAbstractMetadata, QgsProperty, QgsDataItem
from .symbol_layer import MilitarySymbolLayer
from .symbol_layer_widget import MilitarySymbolLayerWidget

class MilitarySymbolLayerMetadata(QgsSymbolLayerAbstractMetadata):

  def __init__(self):
    super().__init__("MilitarySymbolMarker", "Military Symbol", QgsSymbol.Marker)
    self.sidc = QgsProperty()

  def createSymbolLayer(self, props):
    size = float(props["size"]) if "size" in props else 4.0
    sidc = str(props["sidc"]) if "sidc" in props else ''
    return MilitarySymbolLayer(size=size, sidc=sidc)

  def createSymbolLayerWidget(self, a0, QgsVectorLayer=None):
    return MilitarySymbolLayerWidget()
