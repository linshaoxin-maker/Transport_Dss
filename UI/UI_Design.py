from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QToolTip, \
    QPushButton, QMessageBox, QDesktopWidget, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, Qt

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  ##　加入路径

from MysqlDb.Mysqldb import add_data_producer, add_data_cosumer
from Others.logging_file import logger, init_logger
from Model.compute_demo import computer_express, computer_profit, compute_total_profit


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("运输决策支持系统")
        self.resize(800, 600)
        # self.move(400, 200)
        self.center()
        self.initUI()
        self.show()


    def initUI(self):
        # 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
        QToolTip.setFont(QFont('SansSerif', 10))

        le_a = QLineEdit(self)
        le_a.setFont(QFont("SanSerif", 14))
        print(le_a.size())
        le_a.resize(100, 60)
        # le_a.move(100, 100)
        le_a.setPlaceholderText("请输入生产商的产量分布")

        le_b = QLineEdit(self)
        le_b.setFont(QFont("SanSerif", 14))
        le_b.setPlaceholderText("请输入销售量分布")

        btn1 = QPushButton(self)
        btn1.setText("点击保存至数据库")
        btn1.setFont(QFont("SanSerif", 14))

        le_c = QLineEdit(self)
        le_c.setPlaceholderText("请输入运费分布列表")
        le_c.setFont(QFont("SanSerif", 14))

        le_d = QLineEdit(self)
        le_d.setPlaceholderText("请输入利润分布")
        le_d.setFont(QFont("SanSerif", 14))

        btn2 = QPushButton(self)
        btn2.setText("点击查看最优规划结果")
        btn2.setFont(QFont("SanSerif", 14))

        lable1 = QLabel(self)
        lable1.setText("运费最小")
        lable1.setFont(QFont("SanSerif", 14))

        lable2 = QLabel(self)
        lable2.setText("利润最大（不计运费）")
        lable2.setFont(QFont("SanSerif", 14))

        lable3 = QLabel(self)
        lable3.setText("总利润最大")
        lable3.setFont(QFont("SanSerif", 14))

        te = QTextEdit(self)
        te.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        te1 = QTextEdit(self)
        te1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        te2 = QTextEdit(self)
        te2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)






        grid = QGridLayout()
        grid.setSpacing(30)

        grid.addWidget(le_a, 1, 0)
        grid.addWidget(le_b, 1, 1)
        grid.addWidget(btn1, 1, 2, alignment=Qt.AlignCenter)

        grid.addWidget(le_c, 2, 0)
        grid.addWidget(lable1, 2, 1, alignment=Qt.AlignCenter)
        grid.addWidget(te, 2, 2)

        grid.addWidget(le_d, 3, 0)
        grid.addWidget(lable2, 3, 1, alignment=Qt.AlignCenter)
        grid.addWidget(te1, 3, 2)

        grid.addWidget(btn2, 4, 0)
        grid.addWidget(lable3, 4, 1, alignment=Qt.AlignCenter)
        grid.addWidget(te2, 4, 2)

        self.setLayout(grid)

        self.le_a = le_a
        self.le_b = le_b
        self.le_c = le_c
        self.le_d = le_d

        self.label1 = lable1
        self.label2 = lable2
        self.label3 = lable3

        self.te = te
        self.te1 = te1
        self.te2 = te2

        btn1.clicked.connect(self.btn1_action)
        btn2.clicked.connect(self.btn2_action)



        # # 创建一个PushButton并为他设置一个tooltip
        # btn = QPushButton('Button', self)
        # btn.setToolTip('按下储存至数据库')
        # # btn.sizeHint()显示默认尺寸
        # btn.resize(btn.sizeHint())
        # # 移动窗口的位置
        # btn.move(50, 50)

        # qbtn = QPushButton('Quit', self)
        # qbtn.resize(50, 50)
        # qbtn.move(100, 100)
        # qbtn.clicked.connect(QCoreApplication.instance().quit)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Warning', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, \
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        print(cp)
        qr.moveCenter(cp)
        print(qr)
        self.move(qr.topLeft())


    def btn1_action(self):
        # print(type(eval(self.le_a.text())[1]))
        data_a = eval(self.le_a.text())
        data_b = eval(self.le_b.text())

        total_a = sum(data_a)
        total_b = sum(data_b)

        if total_a > total_b:
            diff = total_a - total_b
            data_b.append(diff)
        # print(data_a)
        # print(data_b)
        add_data_producer(data_a)
        add_data_cosumer(data_b)


    def btn2_action(self):
        if self.le_c.text():
            data1 = eval(self.le_c.text())
        # data2 = eval(self.le_d.text())
            result, x, price = computer_express(data1)
            for (i, j) in price.keys():
                if x[i, j].primal > 0 and price[i, j] != 0:
                    self.te.insertPlainText("产地:%s -> 销地:%s 运输量:%-2d 运价:%2d" % (i, j, int(x[i, j].primal), int(price[i, j])))
                    self.te.insertPlainText("\n")
            self.te.insertPlainText("总费用:%d" % result)
            self.te.insertPlainText("\n")

        if self.le_d.text():
            data2 = eval(self.le_d.text())
            result, x, price = computer_profit(data2)
            for (i, j) in price.keys():
                if x[i, j].primal > 0 and price[i, j] != 0:
                    self.te1.insertPlainText("产地:%s -> 销地:%s 运输量:%-2d 运价:%2d" % (i, j, int(x[i, j].primal), int(price[i, j])))
                    self.te1.insertPlainText("\n")
            self.te1.insertPlainText("总费用:%d" % result)
            self.te1.insertPlainText("\n")


        if self.le_c.text() and self.le_d.text():
            data3 = self.computer_cost(eval(self.le_c.text()), eval(self.le_d.text()))
            result, x, price = compute_total_profit(data3)
            for (i, j) in price.keys():
                if x[i, j].primal > 0 and price[i, j] != 0:
                    self.te2.insertPlainText("产地:%s -> 销地:%s 运输量:%-2d 运价:%2d" % (i, j, int(x[i, j].primal), int(price[i, j])))
                    self.te2.insertPlainText("\n")
            self.te2.insertPlainText("总费用:%d" % result)
            self.te2.insertPlainText("\n")


    def computer_cost(self, data1, data2):
        assert len(data1) == len(data2)
        data3 = []
        for i, j in zip(data1, data2):
            list_a = []
            for p, q in zip(i, j):
                list_a.append(q - p)
            data3.append(list_a)
        return data3















if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_logger("logging.txt")
    window = Window()

    sys.exit(app.exec_())
