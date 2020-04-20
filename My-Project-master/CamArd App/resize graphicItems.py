import sys
from PyQt5.QtCore import Qt, QRectF, QPointF,QRect
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap,QImage
from PyQt5.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem,QDialog,QWidget,QPushButton,QGraphicsPixmapItem,QFileDialog,QMessageBox

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

    # define shape of cursor(bien dang con tro)
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

    def __init__(self, *args):#*args: truyen tham so kieu list(1,2,3)
        """
        Initialize the shape.
        """
        super().__init__(*args)#ke thua lai lop cha va truyen tham so vao
        self.handles = {}           # define a dictionary
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)#cho phep nhan cac su kien di chuyen cua chout cho doi tuong 
        self.setFlag(QGraphicsItem.ItemIsMovable, True)#muc ho tro di chuyen hinh tuong tac theo con tro chuot
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)#muc hien cac hinh tuong chuot va cac bieu tuong khi nhap chuot vao doi tuong
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)# muc thong bao vi tri thay doi 
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)#muc tap trung cho phep ban phim
        self.updateHandlesPos()

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v in self.handles.items():   # handes.items Return all key and value from dictionary
            if v.contains(point):            # rectF.contains Return True if given point is inside or on the edge of the rectangle(tra ve true neu diem ben trong hoac canh)
                return k
        return None

    def hoverMoveEvent(self, moveEvent):          # function catch event hover-move mouse on an items(bat cac hinh dang chout trong doi tuong)
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():                     # isSelected() Return True if the Item is selected otherwise Return False
            handle = self.handleAt(moveEvent.pos()) # Handle is dictionary contain key relate to the key of dictionary Handlecursor 
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]  # cursor this property hold shape of cursor for this widget, Default cursor is Qt.ArrowCursor
            self.setCursor(cursor)                  # set shape of cursor for  this widget
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):       # function catch event when mouse move on the item and leave
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:                                 #handleSelected == 0 is False and =!0 is True . it give key of dictionary handle.
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()



    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o) # adjusted() Returns a new rectangle with dx1, dy1, dx2 and dy2 added respectively to the existing coordinates of this rectangle

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect() # define bounds of the item as rectangle
        self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)                                # boundingRect().left()or right() return x coordinate of the rectangle on the edge left or right
        self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)                # Center() Return the center point of the Rectangle
        self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace    # handleSize=8.0 and handleSapce=-4.0 is variable
        boundingRect = self.boundingRect()
        rect1 = self.rect()  #Returns a rect with the top-left corner at x, y and the specified width and height
        self.r = QRectF(rect1)
        rect = self.r
        #print(rect)
        diff = QPointF(0, 0)

        self.prepareGeometryChange() # If you want to change size of the rectangle you need it before

        if self.handleSelected == self.handleTopLeft:

            fromX = self.mousePressRect.left()          #mousePressRect= boudingRect()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)                    # Set the x coordinate of the point is to the give coordinate
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)       # Sets the left edge of the rectangle to the given x coordinate. May change the width, but will never change the right edge of the rectangle.
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left() + offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setTop(boundingRect.top() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            #print("MR")
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)             #Sets the coordinates of the rectangle's top-left corner to (x, y), and its size to the given width and height.

        elif self.handleSelected == self.handleBottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left() + offset)   # rect.setLeft(int x) set the left edge of rectangle to x coordirnate
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right() - offset)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():                       # isSelected() Return True if the Item is selected otherwise Return False
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        #painter.setBrush(QBrush(QColor(255, 0, 0, 100)))    # Qcolor Constructs a color with the RGB value r, g, b, and the alpha-channel (transparency) value of a.
        painter.setPen(QPen(QColor(255, 0, 0), 2.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(65, 205, 82, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.isSelected():
                painter.drawRect(rect)
            if self.handleSelected is not None or handle == self.handleSelected:
                #painter.drawEllipse(rect)
                painter.drawRect(rect)



class main(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(20,20,800,800)
        self.butt=QPushButton("nut xóa",self)
        self.butt.setGeometry(0,0,100,50)
        self.butt2=QPushButton("nut vẽ",self)
        self.butt2.setGeometry(150,0,100,50)

        self.btnLoadImage = QPushButton(self)
        self.btnLoadImage.setObjectName("btnLoadImage")
        self.btnLoadImage.clicked.connect(self.loadClicked)
        self.btnLoadImage.setGeometry(350, 0, 100, 50)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 680, 459)
        #self.scene.addPixmap(QPixmap('name.jpg'))
        #self.pix=QGraphicsPixmapItem(QPixmap('mat.jpg'))
        #self.pix.setPos(30,30)
        #self.pix.setZValue(1)
        #self.scene.addItem(self.pix)
        self.grview = QGraphicsView(self.scene,self)
        self.grview.setGeometry(QRect(0, 100, 700, 700))
        self.butt.clicked.connect(self.clearrect)
        self.butt2.clicked.connect(self.drawrect)
        self.name=False
        self.items=[]
        self.index=1
        self.item="Items{}"

    def drawrect(self):
            self.value=self.item.format(self.index)
        if self.value not in self.items:
            self.index+=1
            self.value = GraphicsRectItem(0, 0, 100, 50)
            self.value.setZValue(1)
            self.items.append(self.value)
            self.scene.addItem(self.value)
    def clearrect(self):
        for i in range(0,len(self.items)):
            if self.items[i].isSelected():
               self.scene.removeItem(self.items[i])

    def loadClicked(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            image = QImage(fileName)
            self.update()
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return
            if self.name:
                self.scene.removeItem(self.pix)
                self.name=True
            self.pix=QGraphicsPixmapItem(QPixmap.fromImage(image))
            self.name=True
            self.scene.addItem(self.pix)



if __name__=="__main__":
    app = QApplication(sys.argv)
    w = main()
    w.show()
    sys.exit(app.exec_())
