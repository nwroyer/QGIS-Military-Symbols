from qgis.core import QgsSymbol, QgsSymbolLayerAbstractMetadata, QgsProperty, QgsDataItem
from .symbol_layer import MilitarySymbolLayer
from .symbol_layer_widget import MilitarySymbolLayerWidget

class MilitarySymbolLayerMetadata(QgsSymbolLayerAbstractMetadata):

  def __init__(self):
    super().__init__("MilitarySymbolMarker", "Military Symbol", QgsSymbol.Marker)
    self.sidc = QgsProperty()

  def createSymbolLayer(self, props):
    size = str(props.get("size", MilitarySymbolLayer.DEFAULT_SIZE))
    size_expression = bool(props.get("size_expression", False).lower() == "true")
    print(f'Creating layer from size {size}')
    return MilitarySymbolLayer(size=size, size_expression=size_expression)

  def createSymbolLayerWidget(self, a0, QgsVectorLayer=None):
    return MilitarySymbolLayerWidget()
