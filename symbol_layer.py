from qgis.core import QgsMarkerSymbolLayer
from qgis.PyQt.QtGui import QColor

class MilitarySymbolLayer(QgsMarkerSymbolLayer):

    def __init__(self, radius=4.0):
        QgsMarkerSymbolLayer.__init__(self)
        self.radius = radius

    def layerType(self):
        return "MilitarySymbolMarker"

    def properties(self):
        return { "radius" : str(self.radius) }

    def startRender(self, context):
        pass

    def stopRender(self, context):
        pass

    def renderPoint(self, point, context):
        # Rendering depends on whether the symbol is selected (QGIS >= 1.5)

        color = context.selectionColor() if context.selected() else QColor(255, 255, 0)
        p = context.renderContext().painter()
        p.setPen(color)
        p.drawEllipse(point, self.radius, self.radius)

    def clone(self):
        return MilitarySymbolLayer(self.radius)