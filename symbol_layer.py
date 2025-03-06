from Tools.scripts.sortperf import DEFAULT_SIZE

import military_symbol
import qgis.core
from qgis.core import QgsMarkerSymbolLayer, QgsSymbolLayer, QgsProperty, QgsFields, QgsSymbolRenderContext, QgsRenderContext,\
    QgsExpressionContext, QgsExpression
from qgis.PyQt.QtGui import QColor, QPainter
from qgis.PyQt.QtCore import QXmlStreamReader, QPointF, QRectF, Qt
from qgis.PyQt.QtSvg import QSvgRenderer

class MilitarySymbolLayer(QgsMarkerSymbolLayer):

    DEFAULT_SIZE:float = 4.0

    def __init__(self, sidc:str = '', size = DEFAULT_SIZE, size_expression:bool = False):
        QgsMarkerSymbolLayer.__init__(self)
        self.size_prop = size
        self.sidc = sidc
        self.size_expression = size_expression
        #print(f'Initializing layer with {size} {"string" if isinstance(size, str) else "float"}')

    def layerType(self):
        return "MilitarySymbolMarker"

    def properties(self):
        ret = {
            "size": str(self.size_prop),
            "sidc": str(self.sidc),
            "size_expression": str(self.size_expression)
        }

        print(ret)
        return ret

    def startRender(self, context):
        pass

    def stopRender(self, context):
        pass

    def get_size_value(self, context:QgsRenderContext):
        if self.size_prop is None:
            return DEFAULT_SIZE

        if self.size_expression:
            exp_context: QgsExpressionContext = QgsExpressionContext([context.expressionContextScope()])
            return float(128)

        return float(self.size_prop)

    def renderPoint(self, point:QPointF, context:QgsSymbolRenderContext):
        """
        :param point: A QPointF of the point to render at, in painter units
        :param context: A QgsSymbolRenderContext for rendering
        :return:
        """
        # Rendering depends on whether the symbol is selected (QGIS >= 1.5)
        painter:QPainter = context.renderContext().painter()

        used_sidc = '10031000141504000008'
        svg_string = military_symbol.get_svg_string(used_sidc, is_sidc=True)
        svg_renderer = QSvgRenderer()

        xml_reader = QXmlStreamReader(svg_string)
        if not svg_renderer.load(xml_reader):
            return

        size:float = self.get_size_value(context)
        print(f'Size: {self.size_prop} -> {size} ({'expression' if self.size_expression else 'value'}) at unit {self.sizeUnit()} = {size}')

        svg_renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        svg_renderer.render(painter, QRectF(point.x() - (size * 0.5), point.y() - (size * 0.5), size, size))

    def clone(self):
        ret = MilitarySymbolLayer()
        ret.size_prop = self.size_prop
        ret.sidc = self.sidc
        ret.size_expression = self.size_expression
        return ret