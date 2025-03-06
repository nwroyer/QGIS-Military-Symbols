import military_symbol
from qgis.core import QgsMarkerSymbolLayer, QgsSymbolLayer, QgsProperty, QgsFields, QgsSymbolRenderContext, QgsRenderContext
from qgis.PyQt.QtGui import QColor, QPainter
from qgis.PyQt.QtCore import QXmlStreamReader, QPointF, QRectF, Qt
from qgis.PyQt.QtSvg import QSvgRenderer

class MilitarySymbolLayer(QgsMarkerSymbolLayer):

    def __init__(self, sidc:str = '', size:float = 2.0):
        QgsMarkerSymbolLayer.__init__(self)
        self.setSize(size)
        self.sidc = ''

    def layerType(self):
        return "MilitarySymbolMarker"

    def properties(self):
        return {
            "size": str(self.size()),
            "sidc": str(self.sidc)
        }

    def startRender(self, context):
        pass

    def stopRender(self, context):
        pass

    def setSize(self, size):
        super().setSize(size)
        print(f'Updating size to {size} => {self.size()}')

    def renderPoint(self, point:QPointF, context:QgsSymbolRenderContext):
        """
        :param point: A QPointF of the point to render at, in painter units
        :param context: A QgsSymbolRenderContext for rendering
        :return:
        """
        # Rendering depends on whether the symbol is selected (QGIS >= 1.5)

        fields = context.fields()

        color = context.selectionColor() if context.selected() else QColor(255, 255, 0)
        render_context:QgsRenderContext = context.renderContext()
        painter:QPainter = context.renderContext().painter()

        painter.setPen(color)
        painter.drawEllipse(point, self.size() * 0.5, self.size() * 0.5)

        used_sidc = '10031000141504000008'
        svg_string = military_symbol.get_svg_string(used_sidc, is_sidc=True)
        svg_renderer = QSvgRenderer()

        xml_reader = QXmlStreamReader(svg_string)
        if not svg_renderer.load(xml_reader):
            print('Bad rendering of SVG')
            return

        size:float = render_context.convertToPainterUnits(self.size(), self.sizeUnit())
        svg_renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        print(f'Size: {self.size()} at unit {self.sizeUnit()} = {size}')
        svg_renderer.render(painter, QRectF(point.x() - (size * 0.5), point.y() - (size * 0.5), size, size))


    def clone(self):
        ret = MilitarySymbolLayer()
        ret.setSize(self.size())
        ret.sidc = self.sidc
        return ret