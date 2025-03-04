from qgis.core import QgsSymbol, QgsSymbolLayerAbstractMetadata, QgsProperty, QgsDataItem
from .symbol_layer import MilitarySymbolLayer
from .symbol_layer_widget import MilitarySymbolLayerWidget

class MilitarySymbolLayerMetadata(QgsSymbolLayerAbstractMetadata):

  def __init__(self):
    super().__init__("MilitarySymbolMarker", "Military Symbol", QgsSymbol.Marker)
    self.sidc = QgsProperty()

  def createSymbolLayer(self, props):
    radius = float(props["radius"]) if "radius" in props else 4.0
    return MilitarySymbolLayer(radius)

  def createSymbolLayerWidget(self, a0, QgsVectorLayer=None):
    return MilitarySymbolLayerWidget()
