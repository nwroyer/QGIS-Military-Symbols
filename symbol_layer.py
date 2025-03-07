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
    DEFAULT_SIDC:str = '10011000000000000000'

    def __init__(self, sidc:str = '',
                 size:float = DEFAULT_SIZE,
                 size_expression:str = "",
                 is_size_expression:bool = False,
                 sidc_expression:str = "",
                 is_sidc_expression:bool = False):

        QgsMarkerSymbolLayer.__init__(self)

        self.sidc = sidc
        self.set_size_data_defined(data_defined=is_size_expression, expression=size_expression, value=size)
        self.set_sidc_data_defined(data_defined=is_sidc_expression, expression=sidc_expression, value=sidc)

    def is_size_data_defined(self) -> bool:
        prop:QgsProperty = self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size)
        return prop is not None and prop.isActive()

    def is_sidc_data_defined(self) -> bool:
        prop:QgsProperty = self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Name)
        return prop is not None and prop.isActive()

    def set_size_data_defined(self, data_defined:bool, value:float=DEFAULT_SIZE, expression:str="") -> None:
        if data_defined:
            self.setDataDefinedProperty(MilitarySymbolLayer.Property.Size, QgsProperty.fromExpression(expression))
            self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size).setActive(True)
        else:
            self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size).setActive(False)
            self.setSize(value)

    def set_sidc_data_defined(self, data_defined:bool, value:str='', expression:str="") -> None:
        if data_defined:
            self.setDataDefinedProperty(MilitarySymbolLayer.Property.Name, QgsProperty.fromExpression(expression))
            self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Name).setActive(True)
        else:
            self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Name).setActive(False)
            self.sidc = value

    def get_size_data_defined_expression(self):
        if not self.is_size_data_defined():
            return ''
        return self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size).expressionString()

    def get_sidc_data_defined_expression(self):
        if not self.is_sidc_data_defined():
            return ''
        return self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Name).expressionString()

    def layerType(self):
        return "MilitarySymbolMarker"

    def properties(self):
        ret = {
            "size": str(self.size()),
            "sidc": str(self.sidc),

            "size_expression": self.get_size_data_defined_expression(),
            "is_size_expression": self.is_size_data_defined(),

            "sidc_expression": self.get_sidc_data_defined_expression(),
            "is_sidc_expression": self.is_sidc_data_defined()
        }
        return ret

    def startRender(self, context):
        pass

    def stopRender(self, context):
        pass

    def get_size_value(self, context:QgsSymbolRenderContext):
        if self.is_size_data_defined():
            if context is not None:
                exp_context = QgsExpressionContext()
                if context is not None and context.renderContext() is not None:
                    exp_context = context.renderContext().expressionContext()

                size_prop:QgsProperty = self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Size)
                return size_prop.value(context=exp_context, defaultValue=MilitarySymbolLayer.DEFAULT_SIZE)[0]
            else:
                return MilitarySymbolLayer.DEFAULT_SIZE
        else:
            return self.size()

    def get_sidc_value(self, context:QgsSymbolRenderContext):
        if self.is_sidc_data_defined():
            if context is not None:
                exp_context = QgsExpressionContext()
                if context is not None and context.renderContext() is not None:
                    exp_context = context.renderContext().expressionContext()

                sidc_prop:QgsProperty = self.dataDefinedProperties().property(MilitarySymbolLayer.Property.Name)
                return sidc_prop.value(context=exp_context, defaultValue=MilitarySymbolLayer.DEFAULT_SIDC)[0]
            else:
                return MilitarySymbolLayer.DEFAULT_SIDC
        else:
            return self.sidc

    def renderPoint(self, point:QPointF, context:QgsSymbolRenderContext):
        """
        :param point: A QPointF of the point to render at, in painter units
        :param context: A QgsSymbolRenderContext for rendering
        :return:
        """
        # Rendering depends on whether the symbol is selected (QGIS >= 1.5)
        painter:QPainter = context.renderContext().painter()

        used_sidc:str = self.get_sidc_value(context)
        try:
            svg_string = military_symbol.get_svg_string(used_sidc, is_sidc=True)
        except Exception as ex:
            svg_string = military_symbol.get_svg_string(MilitarySymbolLayer.DEFAULT_SIDC, is_sidc=True)

        if svg_string is None or len(svg_string) < 1:
            svg_string=military_symbol.get_svg_string(MilitarySymbolLayer.DEFAULT_SIDC, is_sidc=True)

        svg_renderer = QSvgRenderer()

        xml_reader = QXmlStreamReader(svg_string)
        if not svg_renderer.load(xml_reader):
            return

        size:float = self.get_size_value(context) * 2.0
        # if self.is_size_data_defined():
        #     print(f'Size: Exp `{self.get_size_data_defined_expression()}` -> {size} with unit {self.sizeUnit()} = {size}')
        # else:
        #     print(f'Size: Val {size} with unit {self.sizeUnit()} = {size}')

        svg_renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        svg_renderer.render(painter, QRectF(point.x() - (size * 0.5), point.y() - (size * 0.5), size, size))

    def clone(self):
        ret = MilitarySymbolLayer(size=self.size(),
                                  sidc=self.sidc)

        self.copyDataDefinedProperties(ret)
        return ret