import sys
import os
import json
import importlib

from PyQt5.QtCore import Qt
from qtpy.QtWidgets import *
from PyQt5.QtGui import *

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import ( FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib
matplotlib.rcParams.update({'font.size': 24})

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SignalProcessingGUI")
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        static_canvas = FigureCanvas(Figure())
        static_canvas.setSizePolicy(QSizePolicy.Policy.Minimum,QSizePolicy.Policy.Expanding)

        try:
            self.config=json.load(open('SignalGUI.json'))   
        except:
            self.config = {'fileIndex' : 0, 'val1' : 0,'val2' : 0, 'scriptIndex' : 0}

        reload_button = QPushButton('Reload')
        reload_button.clicked.connect(self.reload)
        reload_button.setFixedHeight(50)
        reload_button.setFixedWidth(200)

        self.comboScripts = QComboBox(self)
        for file in os.listdir("."):
            if file.endswith((".py")):
                f = open(file, "r").read()
                if(f.__contains__("def run(")):
                    module = importlib.import_module(file.rsplit('.', 1)[0])
                    if(hasattr(module, "run")):
                        self.comboScripts.addItem(file)
        if(self.config["scriptIndex"]<0 or self.config["scriptIndex"]>=self.comboScripts.count()): self.config["scriptIndex"]=0
        self.comboScripts.setCurrentIndex(self.config["scriptIndex"])
        self.comboScripts.currentTextChanged.connect(self.update)

        self.sld = QSlider(Qt.Orientation.Horizontal, self)
        self.sld.setRange(0, 100)
        self.sld.setPageStep(1)
        self.sld.setValue(self.config["val1"])
        self.sld.valueChanged.connect(self.changed)
        self.sld.sliderReleased.connect(self.update)

        self.label = QLabel(str(self.config["val1"]), self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label.setMinimumWidth(80)

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(self.sld)        
        layout2.addWidget(self.label)        

        self.sld2 = QSlider(Qt.Orientation.Horizontal, self)
        self.sld2.setRange(0, 100)
        self.sld2.setPageStep(1)
        self.sld2.setValue(self.config["val2"])
        self.sld2.valueChanged.connect(self.changed2)
        self.sld2.sliderReleased.connect(self.update)

        self.label2 = QLabel(str(self.config["val2"]), self)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label2.setMinimumWidth(80)

        layout3 = QtWidgets.QHBoxLayout()
        layout3.addWidget(self.sld2)        
        layout3.addWidget(self.label2)        

        self.combo = QComboBox(self)
        for file in os.listdir("."):
            if file.endswith((".ogg",".wav",".mp3")):
                self.combo.addItem(file)
        if(self.config["fileIndex"]<0 or self.config["fileIndex"]>=self.combo.count()): self.config["fileIndex"]=0
        self.combo.setCurrentIndex(self.config["fileIndex"])
        self.combo.currentTextChanged.connect(self.update)

        layout = QtWidgets.QVBoxLayout(self._main)
        layout4 = QtWidgets.QHBoxLayout()
        layout4.addWidget(self.comboScripts)
        layout4.addWidget(reload_button)
        
        layout.addLayout(layout4)
        layout.addWidget(self.combo)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addWidget(NavigationToolbar(static_canvas, self))
        layout.addWidget(static_canvas)
        
        self.process=None
        self.fig = static_canvas.figure
        self.changed(0)
        self.changed2(0)
        self.update()
        self.showMaximized()
    
    def reload(self):
        self.update()

    def changed(self,value):
        self.label.setText(str(value))

    def changed2(self,value):
        self.label2.setText(str(value))

    def update(self):
        script=str(self.comboScripts.currentText())
        value=self.sld.value()
        value2=self.sld2.value()
        fileName=self.combo.currentText()
        self.save()
        if(script!=""):
            module = __import__(script.rsplit('.', 1)[0])
            importlib.reload(module)
            moduleFct = getattr(module, "run")
            moduleFct(value,value2,fileName,self.fig,self.process)

    def save(self):
        self.config["val1"]=self.sld.value()
        self.config["val2"]=self.sld2.value()
        self.config["fileIndex"]=self.combo.currentIndex()
        self.config["scriptIndex"]=self.comboScripts.currentIndex()
        json.dump(self.config, open('SignalGUI.json', 'w'),default=lambda x: x.__dict__)
        #self.process=algo.run(value,value2,fileName,self.fig,self.process)

QSS = """
/* QSlider --------------------------------------  */
QSlider::groove:horizontal {
    border-radius: 10px;
    height: 20px;
    margin: 0px;
    background-color: rgb(52, 59, 72);
}
QSlider::groove:horizontal:hover {
    background-color: rgb(55, 62, 76);
}
QSlider::handle:horizontal {
    background-color: rgb(85, 170, 255);
    border: none;
    height: 60px;
    width: 60px;
    margin: -30px 0;
    border-radius: 30px;
    padding: -30px 0px;
}
QSlider::handle:horizontal:hover {
    background-color: rgb(155, 180, 255);
}
QSlider::handle:horizontal:pressed {
    background-color: rgb(65, 255, 195);
}
"""



if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.setStyle(QStyleFactory.create('Fusion'))
    app.setStyleSheet(QSS)
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()