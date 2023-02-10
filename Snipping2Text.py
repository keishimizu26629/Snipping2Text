import sys
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QApplication
from PIL import ImageGrab
import io
import tkinter
from tkinter import ttk

import environment_check
import cloud_vision

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        screen_width, screen_height, self.width_adjustment_value, self.second_offset = self.get_screen_size()
        self.setGeometry(0 - self.width_adjustment_value,0 + self.second_offset,screen_width, screen_height)
        self.setWindowTitle("")
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        print("Capture the screen...")
        self.show()

    def get_screen_size(self):
        main, second, position, offset = environment_check.get_monitors_size_and_position()
        point = 0
        if offset:
            if offset < 0:
                point = offset
        else:
            offset = 0
        if second:
            if position == 'right':
                return (main[0]+second[0], max(main[1], second[1]) + abs(offset), 0, point)
            else:
                return (main[0]+second[0], max(main[1], second[1])+ abs(offset), second[0], point)
        else:
            return (main[0], main[1], 0, 0)


    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor("black"), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.close()

        x1 = min(self.begin.x(), self.end.x()) - self.width_adjustment_value
        y1 = min(self.begin.y(), self.end.y()) + self.second_offset
        x2 = max(self.begin.x(), self.end.x()) - self.width_adjustment_value
        y2 = max(self.begin.y(), self.end.y()) + self.second_offset

        img = ImageGrab.grab(all_screens=True, bbox=(x1,y1,x2,y2))

        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        cloud_vision.image_to_text(img_bytes)

def conductMain():
    root.withdraw()
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # rootの作成
    root = tkinter.Tk()
    root.title("Snipping2Text")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=5,column=1,sticky=tkinter.W)

    # 実行ボタンの設置
    button1 = ttk.Button(root, text="切り取り", command=lambda: conductMain())
    button1.place(x=40, y=40, width=120, height=60)

    root.geometry("400x130+400+200")

    root.mainloop()
