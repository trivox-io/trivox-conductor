# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLayout, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QScrollArea, QSizePolicy,
    QStackedWidget, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
        self.actionStart = QAction(MainWindow)
        self.actionStart.setObjectName(u"actionStart")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(9, 9, 971, 521))
        self.mainV = QVBoxLayout(self.widget)
        self.mainV.setObjectName(u"mainV")
        self.mainV.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.mainV.setContentsMargins(0, 0, 0, 0)
        self.mainRow = QWidget(self.widget)
        self.mainRow.setObjectName(u"mainRow")
        self.horizontalLayoutWidget = QWidget(self.mainRow)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(-1, -1, 991, 541))
        self.mainH = QHBoxLayout(self.horizontalLayoutWidget)
        self.mainH.setObjectName(u"mainH")
        self.mainH.setContentsMargins(0, 0, 0, 0)
        self.navList = QListWidget(self.horizontalLayoutWidget)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        QListWidgetItem(self.navList)
        self.navList.setObjectName(u"navList")

        self.mainH.addWidget(self.navList, 0, Qt.AlignmentFlag.AlignLeft)

        self.stack = QStackedWidget(self.horizontalLayoutWidget)
        self.stack.setObjectName(u"stack")
        self.pageDashboard = QWidget()
        self.pageDashboard.setObjectName(u"pageDashboard")
        self.dashScroll = QScrollArea(self.pageDashboard)
        self.dashScroll.setObjectName(u"dashScroll")
        self.dashScroll.setGeometry(QRect(-1, -1, 731, 541))
        self.dashScroll.setWidgetResizable(True)
        self.dashContents = QWidget()
        self.dashContents.setObjectName(u"dashContents")
        self.dashContents.setGeometry(QRect(0, 0, 729, 539))
        self.gridLayoutWidget = QWidget(self.dashContents)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(-1, -1, 711, 521))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.recorder_and_session = QFrame(self.gridLayoutWidget)
        self.recorder_and_session.setObjectName(u"recorder_and_session")
        self.recorder_and_session.setFrameShape(QFrame.Shape.StyledPanel)
        self.recorder_and_session.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.recorder_and_session, 0, 1, 1, 1)

        self.replay_watch = QFrame(self.gridLayoutWidget)
        self.replay_watch.setObjectName(u"replay_watch")
        self.replay_watch.setFrameShape(QFrame.Shape.StyledPanel)
        self.replay_watch.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.replay_watch, 1, 0, 1, 1)

        self.quick_actions = QFrame(self.gridLayoutWidget)
        self.quick_actions.setObjectName(u"quick_actions")
        self.quick_actions.setFrameShape(QFrame.Shape.StyledPanel)
        self.quick_actions.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.quick_actions, 0, 0, 1, 1)

        self.recent_outputs = QFrame(self.gridLayoutWidget)
        self.recent_outputs.setObjectName(u"recent_outputs")
        self.recent_outputs.setFrameShape(QFrame.Shape.StyledPanel)
        self.recent_outputs.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.recent_outputs, 2, 0, 1, 1)

        self.pipeline_queue = QFrame(self.gridLayoutWidget)
        self.pipeline_queue.setObjectName(u"pipeline_queue")
        self.pipeline_queue.setFrameShape(QFrame.Shape.StyledPanel)
        self.pipeline_queue.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.pipeline_queue, 1, 1, 1, 1)

        self.system_health = QFrame(self.gridLayoutWidget)
        self.system_health.setObjectName(u"system_health")
        self.system_health.setFrameShape(QFrame.Shape.StyledPanel)
        self.system_health.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.system_health, 2, 1, 1, 1)

        self.dashScroll.setWidget(self.dashContents)
        self.stack.addWidget(self.pageDashboard)
        self.pageReplay = QWidget()
        self.pageReplay.setObjectName(u"pageReplay")
        self.stack.addWidget(self.pageReplay)
        self.pageColorHandoff = QWidget()
        self.pageColorHandoff.setObjectName(u"pageColorHandoff")
        self.stack.addWidget(self.pageColorHandoff)
        self.pageAI = QWidget()
        self.pageAI.setObjectName(u"pageAI")
        self.stack.addWidget(self.pageAI)
        self.pagePlugins = QWidget()
        self.pagePlugins.setObjectName(u"pagePlugins")
        self.stack.addWidget(self.pagePlugins)
        self.pageLogs = QWidget()
        self.pageLogs.setObjectName(u"pageLogs")
        self.stack.addWidget(self.pageLogs)
        self.pageSettings = QWidget()
        self.pageSettings.setObjectName(u"pageSettings")
        self.stack.addWidget(self.pageSettings)
        self.pageCapture = QWidget()
        self.pageCapture.setObjectName(u"pageCapture")
        self.stack.addWidget(self.pageCapture)

        self.mainH.addWidget(self.stack)


        self.mainV.addWidget(self.mainRow)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))

        __sortingEnabled = self.navList.isSortingEnabled()
        self.navList.setSortingEnabled(False)
        ___qlistwidgetitem = self.navList.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None));
        ___qlistwidgetitem1 = self.navList.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Capture", None));
        ___qlistwidgetitem2 = self.navList.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Replay", None));
        ___qlistwidgetitem3 = self.navList.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Cloor & Handoff", None));
        ___qlistwidgetitem4 = self.navList.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"AI", None));
        ___qlistwidgetitem5 = self.navList.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Plugins", None));
        ___qlistwidgetitem6 = self.navList.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Logs", None));
        ___qlistwidgetitem7 = self.navList.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Settings", None));
        self.navList.setSortingEnabled(__sortingEnabled)

        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

