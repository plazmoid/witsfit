from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import sys
import proxies

__author__ = 'p1azm0id'
__version__ = '0.0.2'

class WExample(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.btn_proxy = QPushButton("Get proxy", self)
        self.btn_proxy.move(30, 50)
        self.btn_proxy.clicked.connect(self.proxiesClicked)
        
        self.lbl_proxy = QLabel(self)
        self.lbl_proxy.move(2, 5)
        self.setGeometry(300, 300, 300, 500)
        self.setWindowTitle(f'WITSFIT v.{__version__}')
        self.show()
        
    def proxiesClicked(self):
        proxy = proxies.get_working_proxy('https')
        self.lbl_proxy.setText(proxy)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WExample()
    app.exec_()

