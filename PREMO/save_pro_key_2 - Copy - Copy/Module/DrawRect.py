import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt, QRectF, QPointF, QRect, QObject
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QDialog, \
    QWidget, QPushButton, QGraphicsPixmapItem, QGraphicsObject, QFileDialog
import math


class GraphicsRectItem(QGraphicsRectItem):  # class QGraphicsRectItem for draw rectangle ingraphicsence

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0

    # define shape of cursor
    handleCursors = {
        handleTopLeft: Qt.SizeFDiagCursor,
        handleTopMiddle: Qt.SizeVerCursor,
        handleTopRight: Qt.SizeBDiagCursor,
        handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomLeft: Qt.SizeBDiagCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}  # define a dictionary
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()
        self.identifycursor = 0

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():  # handes.items Return all key and value from dictionary
            if v.contains(point):  # rectF.contains Return True if given point is inside or on the edge of the rectangle
                return k
        return None

    def hoverMoveEvent(self, moveEvent):  # function catch event hover-move mouse on an items
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        self.scene().update()
        if self.isSelected():  # isSelected() Return True if the Item is selected otherwise Return False
            handle = self.handleAt(
                moveEvent.pos())  # Handle is dictionary contain key relate to the key of dictionary Handlecursor
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[
                handle]  # cursor this property hold shape of cursor for this widget, Default cursor is Qt.ArrowCursor
            self.setCursor(cursor)  # set shape of cursor for  this widget
            if cursor != Qt.ArrowCursor:
                self.identifycursor = 1
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):  # function catch event when mouse move on the item and leave
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)

        self.identifycursor = 0
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """

        self.PressPos = mouseEvent.pos()
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:  # handleSelected == 0 is False and =!0 is True . it give key of dictionary handle.
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """

        fromX = mouseEvent.pos().x() - self.PressPos.x()
        fromY = mouseEvent.pos().y() - self.PressPos.y()
        scenebouding = self.sceneBoundingRect()
        if self.handleSelected is not None:
            self.scene().update()
            self.updateHandlesPos()
            self.interactiveResize(mouseEvent.pos())
        else:
            if scenebouding.left() + 4 > 1 and scenebouding.right() - 4 < 639 and scenebouding.top() + 4 > 1 and scenebouding.bottom() - 4 < 479:
                super().mouseMoveEvent(mouseEvent)
            elif fromX > 0 and scenebouding.left() <= 1:
                super().mouseMoveEvent(mouseEvent)
            elif fromY > 0 and scenebouding.top() <= 1:
                super().mouseMoveEvent(mouseEvent)
            elif fromX < 0 and scenebouding.right() >= 639:
                super().mouseMoveEvent(mouseEvent)
            elif fromY < 0 and scenebouding.bottom() >= 479:
                super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)

        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.changeCoordinate()
        self.update()

    def changeCoordinate(self):
        topleft = self.boundingRect().topLeft() + QPoint(4, 4)
        bottomRight = self.boundingRect().bottomRight() - QPoint(4, 4)
        self.setRect(QRectF(topleft, bottomRight))

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        self.rect().adjusted(-o, -o, o,
                             o)  # adjusted() Returns a new rectangle with dx1, dy1, dx2 and dy2 added respectively to the existing coordinates of this rectangle
        self.rect()
        return self.rect().normalized().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()  # define bounds of the item as rectangle
        self.handles[self.handleTopLeft] = QRectF(b.left() + 4, b.top() + 4, 4,
                                                  4)  # boundingRect().left()or right() return x coordinate of the rectangle on the edge left or right
        # self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)                # Center() Return the center point of the Rectangle
        self.handles[self.handleTopRight] = QRectF(b.right() - 2 - 4, b.top() + 4, 4, 4)
        # self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        # self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left() + 4, b.bottom() - 2 - 4, 4, 4)
        # self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - 2 / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - 2 - 4, b.bottom() - 2 - 4, 4, 4)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace  # handleSize=8.0 and handleSapce=-4.0 is variable
        boundingRect = self.boundingRect()
        scenebouding = self.sceneBoundingRect()
        rect = self.rect()  # Returns a rect with the top-left corner at x, y and the specified width and height
        # self.r = QRectF(rect1).normalized()
        # rect = self.r
        diff = QPointF(0, 0)
        self.prepareGeometryChange()  # If you want to change size of the rectangle you need it before
        self.updateHandlesPos()

        if self.handleSelected != None:
            self.scene().entered.emit()

        if self.handleSelected == self.handleTopLeft:
            fromZ = mousePos.x() - self.mousePressPos.x()
            fromE = mousePos.y() - self.mousePressPos.y()
            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + fromZ
            toY = fromY + fromE
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            if fromZ < 0 and scenebouding.top() > 0 and scenebouding.left() > 0:
                self.setRect(rect)
            if fromZ > 0:
                self.setRect(rect)
            self.scene().update()

        elif self.handleSelected == self.handleTopMiddle:
            fromE = mousePos.y() - self.mousePressPos.y()
            fromY = self.mousePressRect.top()
            toY = fromY + fromE
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            # rect.normalized()
            rect.setTop(boundingRect.top() + offset)
            if fromE < 0 and scenebouding.top() > 0:
                self.setRect(rect)
            elif fromE > 0:
                self.setRect(rect)
            # self.scene().update()

        elif self.handleSelected == self.handleTopRight:

            fromZ = mousePos.x() - self.mousePressPos.x()
            fromE = mousePos.y() - self.mousePressPos.y()
            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + fromZ
            toY = fromY + fromE
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            if fromZ > 0 and (scenebouding.top() > 0 or scenebouding.right() < 637):
                self.setRect(rect)
                self.update()
            elif fromZ < 0:
                self.setRect(rect)
                self.update()
            self.scene().update()

        elif self.handleSelected == self.handleMiddleLeft:

            fromZ = mousePos.x() - self.mousePressPos.x()
            fromX = self.mousePressRect.left()
            toX = fromX + fromZ
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            if fromZ < 0 and scenebouding.left() > 0:
                self.setRect(rect)
                self.update()
            elif fromZ > 0:
                self.setRect(rect)
                self.update()
            self.scene().update()

        elif self.handleSelected == self.handleMiddleRight:

            fromZ = mousePos.x() - self.mousePressPos.x()
            fromX = self.mousePressRect.right()
            toX = fromX + fromZ
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            rect.normalized()
            if fromZ > 0 and scenebouding.right() < 637:
                self.setRect(
                    rect)  # Sets the coordinates of the rectangle's top-left corner to (x, y), and its size to the given width and height.
            elif fromZ < 0:
                self.setRect(rect)
            self.update()
            self.scene().update()

        elif self.handleSelected == self.handleBottomLeft:

            fromZ = mousePos.x() - self.mousePressPos.x()
            fromE = mousePos.y() - self.mousePressPos.y()
            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + fromZ
            toY = fromY + fromE
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(
                boundingRect.left() + offset)  # rect.setLeft(int x) set the left edge of rectangle to x coordirnate
            rect.setBottom(boundingRect.bottom() - offset)
            if fromZ > 0 and (scenebouding.left() > 0 or scenebouding.bottom() < 479):
                self.setRect(rect)
            elif fromZ < 0:
                self.setRect(rect)
            self.update()
            self.scene().update()

        elif self.handleSelected == self.handleBottomMiddle:
            print("BTM")
            fromE = mousePos.y() - self.mousePressPos.y()
            fromY = self.mousePressRect.bottom()
            toY = fromY + fromE
            # diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            if fromY > 0 and scenebouding.bottom() < 479:
                self.setRect(rect)
            elif fromE < 0:
                self.setRect(rect)
            self.update()
            self.scene().update()

        elif self.handleSelected == self.handleBottomRight:

            fromZ = mousePos.x() - self.mousePressPos.x()
            fromE = mousePos.y() - self.mousePressPos.y()
            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + fromZ
            toY = fromY + fromE
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            if fromZ > 0 and (scenebouding.bottom() < 479 or scenebouding.right() < 637):
                self.setRect(rect)
            elif fromZ < 0:
                self.setRect(rect)
            self.update()
            self.scene().update()
        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():  # isSelected() Return True if the Item is selected otherwise Return False
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        # painter.setBrush(QBrush(QColor(255, 0, 0, 100)))    # Qcolor Constructs a color with the RGB value r, g, b, and the alpha-channel (transparency) value of a.
        painter.setPen(QPen(QColor(12, 183, 84), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(241, 71, 66, 255)))
        painter.setPen(QPen(QColor(241, 71, 66, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.isSelected():
                painter.drawEllipse(rect)


