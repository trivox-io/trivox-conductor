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
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.mainV = QVBoxLayout()
        self.mainV.setObjectName(u"mainV")
        self.mainV.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.mainRow = QWidget(self.centralwidget)
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
        self.quick_actions = QFrame(self.dashContents)
        self.quick_actions.setObjectName(u"quick_actions")
        self.quick_actions.setGeometry(QRect(0, 0, 351, 131))
        self.quick_actions.setFrameShape(QFrame.Shape.StyledPanel)
        self.quick_actions.setFrameShadow(QFrame.Shadow.Raised)
        self.recorder_and_session = QFrame(self.dashContents)
        self.recorder_and_session.setObjectName(u"recorder_and_session")
        self.recorder_and_session.setGeometry(QRect(370, 0, 351, 131))
        self.recorder_and_session.setFrameShape(QFrame.Shape.StyledPanel)
        self.recorder_and_session.setFrameShadow(QFrame.Shadow.Raised)
        self.replay_watch = QFrame(self.dashContents)
        self.replay_watch.setObjectName(u"replay_watch")
        self.replay_watch.setGeometry(QRect(0, 140, 351, 131))
        self.replay_watch.setFrameShape(QFrame.Shape.StyledPanel)
        self.replay_watch.setFrameShadow(QFrame.Shadow.Raised)
        self.pipeline_queue = QFrame(self.dashContents)
        self.pipeline_queue.setObjectName(u"pipeline_queue")
        self.pipeline_queue.setGeometry(QRect(370, 140, 351, 131))
        self.pipeline_queue.setFrameShape(QFrame.Shape.StyledPanel)
        self.pipeline_queue.setFrameShadow(QFrame.Shadow.Raised)
        self.recent_outputs = QFrame(self.dashContents)
        self.recent_outputs.setObjectName(u"recent_outputs")
        self.recent_outputs.setGeometry(QRect(0, 280, 351, 131))
        self.recent_outputs.setFrameShape(QFrame.Shape.StyledPanel)
        self.recent_outputs.setFrameShadow(QFrame.Shadow.Raised)
        self.system_health = QFrame(self.dashContents)
        self.system_health.setObjectName(u"system_health")
        self.system_health.setGeometry(QRect(370, 280, 351, 131))
        self.system_health.setFrameShape(QFrame.Shape.StyledPanel)
        self.system_health.setFrameShadow(QFrame.Shadow.Raised)
        self.notifications = QFrame(self.dashContents)
        self.notifications.setObjectName(u"notifications")
        self.notifications.setGeometry(QRect(-1, 419, 351, 111))
        self.notifications.setFrameShape(QFrame.Shape.StyledPanel)
        self.notifications.setFrameShadow(QFrame.Shadow.Raised)
        self.log_glance = QFrame(self.dashContents)
        self.log_glance.setObjectName(u"log_glance")
        self.log_glance.setGeometry(QRect(370, 420, 351, 111))
        self.log_glance.setFrameShape(QFrame.Shape.StyledPanel)
        self.log_glance.setFrameShadow(QFrame.Shadow.Raised)
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


        self.gridLayout_3.addLayout(self.mainV, 0, 0, 1, 1)

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

