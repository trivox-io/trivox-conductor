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
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QScrollArea, QSizePolicy, QStackedWidget,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
        self.actionStart = QAction(MainWindow)
        self.actionStart.setObjectName(u"actionStart")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mainRow = QWidget(self.centralwidget)
        self.mainRow.setObjectName(u"mainRow")
        self.mainRow.setEnabled(True)
        self.mainRowLayout = QHBoxLayout(self.mainRow)
        self.mainRowLayout.setObjectName(u"mainRowLayout")
        self.navList = QListWidget(self.mainRow)
        QListWidgetItem(self.navList)
        self.navList.setObjectName(u"navList")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navList.sizePolicy().hasHeightForWidth())
        self.navList.setSizePolicy(sizePolicy)
        self.navList.setMinimumSize(QSize(120, 0))
        self.navList.setMaximumSize(QSize(300, 16777215))

        self.mainRowLayout.addWidget(self.navList)

        self.stack = QStackedWidget(self.mainRow)
        self.stack.setObjectName(u"stack")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stack.sizePolicy().hasHeightForWidth())
        self.stack.setSizePolicy(sizePolicy1)
        self.pageDashboard = QWidget()
        self.pageDashboard.setObjectName(u"pageDashboard")
        self.pageDashboardLayout = QVBoxLayout(self.pageDashboard)
        self.pageDashboardLayout.setObjectName(u"pageDashboardLayout")
        self.dashScroll = QScrollArea(self.pageDashboard)
        self.dashScroll.setObjectName(u"dashScroll")
        self.dashScroll.setWidgetResizable(True)
        self.dashContents = QWidget()
        self.dashContents.setObjectName(u"dashContents")
        self.dashContents.setGeometry(QRect(0, 0, 682, 490))
        self.gridLayout = QGridLayout(self.dashContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.quick_actions = QFrame(self.dashContents)
        self.quick_actions.setObjectName(u"quick_actions")
        self.quick_actions.setFrameShape(QFrame.Shape.StyledPanel)
        self.quick_actions.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.quick_actions, 0, 0, 1, 1)

        self.recorder_and_session = QFrame(self.dashContents)
        self.recorder_and_session.setObjectName(u"recorder_and_session")
        self.recorder_and_session.setFrameShape(QFrame.Shape.StyledPanel)
        self.recorder_and_session.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.recorder_and_session, 0, 1, 1, 1)

        self.replay_watch = QFrame(self.dashContents)
        self.replay_watch.setObjectName(u"replay_watch")
        self.replay_watch.setFrameShape(QFrame.Shape.StyledPanel)
        self.replay_watch.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.replay_watch, 1, 0, 1, 1)

        self.pipeline_queue = QFrame(self.dashContents)
        self.pipeline_queue.setObjectName(u"pipeline_queue")
        self.pipeline_queue.setFrameShape(QFrame.Shape.StyledPanel)
        self.pipeline_queue.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.pipeline_queue, 1, 1, 1, 1)

        self.recent_outputs = QFrame(self.dashContents)
        self.recent_outputs.setObjectName(u"recent_outputs")
        self.recent_outputs.setFrameShape(QFrame.Shape.StyledPanel)
        self.recent_outputs.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.recent_outputs, 2, 0, 1, 1)

        self.system_health = QFrame(self.dashContents)
        self.system_health.setObjectName(u"system_health")
        self.system_health.setFrameShape(QFrame.Shape.StyledPanel)
        self.system_health.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.system_health, 2, 1, 1, 1)

        self.dashScroll.setWidget(self.dashContents)

        self.pageDashboardLayout.addWidget(self.dashScroll)

        self.stack.addWidget(self.pageDashboard)

        self.mainRowLayout.addWidget(self.stack)


        self.horizontalLayout.addWidget(self.mainRow)

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
        self.navList.setSortingEnabled(__sortingEnabled)

        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

