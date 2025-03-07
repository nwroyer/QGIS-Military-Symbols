from qgis.core import QgsSymbol, QgsSymbolLayerAbstractMetadata, QgsProperty, QgsDataItem
from .symbol_layer import MilitarySymbolLayer
from .symbol_layer_widget import MilitarySymbolLayerWidget

class MilitarySymbolLayerMetadata(QgsSymbolLayerAbstractMetadata):

  def __init__(self):
    super().__init__("MilitarySymbolMarker", "Military Symbol", QgsSymbol.Marker)
    self.sidc = QgsProperty()

  def createSymbolLayer(self, props):
    size = float(props.get("size", MilitarySymbolLayer.DEFAULT_SIZE))
    is_size_expression = bool(props.get("is_size_expression", False))
    size_expression = props.get("size_expression", "")
    sidc = props.get("sidc", "")

    print(f'Creating layer from size {size}')
    return MilitarySymbolLayer(size=size,
                               sidc=sidc,
                               is_size_expression=is_size_expression,
                               size_expression=size_expression)

  def createSymbolLayerWidget(self, a0, QgsVectorLayer=None):
    return MilitarySymbolLayerWidget()
