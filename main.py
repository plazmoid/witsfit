from PyQt5.QtWidgets import QApplication, QWidget
import sys

class WExample(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 300, 500)
        self.setWindowTitle('WITSFIT v 0.0.1')
        self.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WExample()
    sys.exit(app.exec_())