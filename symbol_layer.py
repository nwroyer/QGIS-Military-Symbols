import military_symbol
from qgis.core import QgsMarkerSymbolLayer, QgsSymbolLayer, QgsProperty, QgsFields, QgsSymbolRenderContext, QgsRenderContext
from qgis.PyQt.QtGui import QColor, QPainter
from qgis.PyQt.QtCore import QXmlStreamReader
from qgis.PyQt.QtSvg import QSvgRenderer

class MilitarySymbolLayer(QgsMarkerSymbolLayer):

    def __init__(self, radius=4.0):
        QgsMarkerSymbolLayer.__init__(self)
        self.radius = radius
        self.sidc = QgsProperty.fromValue(value='', isActive=True)

    def layerType(self):
        return "MilitarySymbolMarker"

    def properties(self):
        return {
            "radius" : str(self.radius),
            "sidc": str(self.sidc)
        }

    def startRender(self, context):
        pass

    def stopRender(self, context):
        pass

    def renderPoint(self, point, context:QgsSymbolRenderContext):
        # Rendering depends on whether the symbol is selected (QGIS >= 1.5)

        fields = context.fields()

        color = context.selectionColor() if context.selected() else QColor(255, 255, 0)
        render_context:QgsRenderContext = context.renderContext()
        painter:QPainter = context.renderContext().painter()

        painter.setPen(color)
        painter.drawEllipse(point, self.radius, self.radius)

        used_sidc = '10031000001211000000'
        svg_string = military_symbol.get_svg_string(used_sidc, is_sidc=True)
        svg_renderer = QSvgRenderer()

        xml_reader = QXmlStreamReader(svg_string)
        if not svg_renderer.load(xml_reader):
            print('Bad rendering of SVG')
            return

        print('Rendering')

        svg_renderer.render(painter)


    def clone(self):
        ret = MilitarySymbolLayer(self.radius)
        ret.sidc = self.sidc
        return ret