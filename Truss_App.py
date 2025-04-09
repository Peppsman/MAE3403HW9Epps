#MAE 3403 HW9 Epps, Patrick
#Copliot for the save
#Truss app from Dr Smay

# region imports
from Truss_GUI import Ui_TrussStructuralDesign
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from Truss_Classes import TrussController
import sys


# endregion

# region class definitions
#PBE Copilet gave me this as a fix
class MainWindow(Ui_TrussStructuralDesign, qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_Open.clicked.connect(self.OpenFile)
        self.spnd_Zoom.valueChanged.connect(self.setZoom)  # Double spinner widget for setting zoom level

        self.controller = TrussController()
        self.controller.setDisplayWidgets((self.te_DesignReport, self.le_LinkName, self.le_Node1Name,
                                           self.le_Node2Name, self.le_LinkLength, self.gv_Main))

        #PBE Copilet gave me this. Debug print statements to verify initialization
        print(f"Controller initialized: {self.controller}")
        print(f"View initialized: {self.controller.view}")
        print(f"Scene initialized: {self.controller.view.scene if self.controller.view else 'View is None'}")
        print("MainWindow initialized and now displaying...")

        #self.controller.installEventFilterOnScene(self)
        self.gv_Main.setMouseTracking(True)

        self.show()

    def setZoom(self):
        """ Adjusts the zoom level through the controller """
        self.controller.setZoom(self.spnd_Zoom.value())

    def eventFilter(self, obj, event):
        """
        Overrides default eventFilter for handling events via the controller.
        """
        #PBE updated with code from Copilot
        if obj == self.controller.getScene():
            et = event.type()
            if et == qtc.QEvent.GraphicsSceneMouseMove:
                scenePos = event.scenePos()
                strScene = "Mouse Position: x = {}, y = {}".format(round(scenePos.x(), 2), round(-scenePos.y(), 2))

                # FIX: Call controller method instead of directly referencing the view
                item_info = self.controller.getItemDetails(scenePos, self.gv_Main.transform())
                if item_info:
                    strScene += f" ({item_info})"

                self.lbl_MousePos.setText(strScene)

            elif et == qtc.QEvent.GraphicsSceneWheel:
                self.controller.adjustZoom(event.delta())

            elif et == qtc.QEvent.ToolTip:
                tooltip_data = self.controller.getTooltip(event.scenePos(), self.gv_Main.transform())
                if tooltip_data:
                    print(f"Tooltip: {tooltip_data}")
                return True  # Prevent unnecessary processing

        return super(MainWindow, self).eventFilter(obj, event)

    def OpenFile(self):
        """ Opens a file and passes data to the controller """
        filename = qtw.QFileDialog.getOpenFileName()[0]
        if len(filename) == 0:
            return

        self.te_Path.setText(filename)
        with open(filename, 'r') as file:
            data = file.readlines()

        self.controller.ImportFromFile(data)


# endregion

# region function definitions
def Main():
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
#PBE part C maybe
    self.controller.setSupports(left_node, right_node)
    left_load, right_load = self.controller.calculateVerticalLoads()
    self.controller.updateNodeTooltips(left_node, right_node, left_load, right_load)
#PBE Part C seams to work, but it doesn't change the image for the roller

# endregion

# region function calls
if __name__ == "__main__":
    Main()
# endregion
