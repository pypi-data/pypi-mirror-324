# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'updater_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_Updater_Window(object):
    def setupUi(self, Updater_Window):
        if not Updater_Window.objectName():
            Updater_Window.setObjectName(u"Updater_Window")
        Updater_Window.setEnabled(True)
        Updater_Window.resize(372, 196)
        self.centralwidget = QWidget(Updater_Window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_last_check = QLabel(self.centralwidget)
        self.label_last_check.setObjectName(u"label_last_check")

        self.gridLayout_2.addWidget(self.label_last_check, 0, 0, 1, 1)

        self.label_last_check_2 = QLabel(self.centralwidget)
        self.label_last_check_2.setObjectName(u"label_last_check_2")
        self.label_last_check_2.setEnabled(True)

        self.gridLayout_2.addWidget(self.label_last_check_2, 0, 1, 1, 1)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_optima35_localversion = QLabel(self.widget_2)
        self.label_optima35_localversion.setObjectName(u"label_optima35_localversion")
        self.label_optima35_localversion.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_optima35_localversion, 2, 1, 1, 1)

        self.label_9 = QLabel(self.widget_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_optima35_latestversion = QLabel(self.widget_2)
        self.label_optima35_latestversion.setObjectName(u"label_optima35_latestversion")
        self.label_optima35_latestversion.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_optima35_latestversion, 2, 2, 1, 1)

        self.label_optimalab35_localversion = QLabel(self.widget_2)
        self.label_optimalab35_localversion.setObjectName(u"label_optimalab35_localversion")
        self.label_optimalab35_localversion.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_optimalab35_localversion, 1, 1, 1, 1)

        self.label_6 = QLabel(self.widget_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)

        self.label_optimalab35_latestversion = QLabel(self.widget_2)
        self.label_optimalab35_latestversion.setObjectName(u"label_optimalab35_latestversion")
        self.label_optimalab35_latestversion.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_optimalab35_latestversion, 1, 2, 1, 1)

        self.label_latest_version = QLabel(self.widget_2)
        self.label_latest_version.setObjectName(u"label_latest_version")
        self.label_latest_version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_latest_version, 0, 2, 1, 1)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.check_for_update_Button = QPushButton(self.widget)
        self.check_for_update_Button.setObjectName(u"check_for_update_Button")

        self.horizontalLayout.addWidget(self.check_for_update_Button)

        self.update_and_restart_Button = QPushButton(self.widget)
        self.update_and_restart_Button.setObjectName(u"update_and_restart_Button")

        self.horizontalLayout.addWidget(self.update_and_restart_Button)


        self.gridLayout_2.addWidget(self.widget, 2, 0, 1, 2)

        Updater_Window.setCentralWidget(self.centralwidget)

        self.retranslateUi(Updater_Window)

        QMetaObject.connectSlotsByName(Updater_Window)
    # setupUi

    def retranslateUi(self, Updater_Window):
        Updater_Window.setWindowTitle(QCoreApplication.translate("Updater_Window", u"Updater", None))
        self.label_last_check.setText(QCoreApplication.translate("Updater_Window", u"Last update check:", None))
        self.label_last_check_2.setText(QCoreApplication.translate("Updater_Window", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("Updater_Window", u"OptimaLab35", None))
        self.label_optima35_localversion.setText(QCoreApplication.translate("Updater_Window", u"0.0.0", None))
        self.label_9.setText(QCoreApplication.translate("Updater_Window", u"Package", None))
        self.label_optima35_latestversion.setText(QCoreApplication.translate("Updater_Window", u"unknown", None))
        self.label_optimalab35_localversion.setText(QCoreApplication.translate("Updater_Window", u"0.0.0", None))
        self.label_6.setText(QCoreApplication.translate("Updater_Window", u"Local Version", None))
        self.label_optimalab35_latestversion.setText(QCoreApplication.translate("Updater_Window", u"unknown", None))
        self.label_latest_version.setText(QCoreApplication.translate("Updater_Window", u"Latest version", None))
        self.label_2.setText(QCoreApplication.translate("Updater_Window", u"optima35", None))
        self.check_for_update_Button.setText(QCoreApplication.translate("Updater_Window", u"Check for update", None))
        self.update_and_restart_Button.setText(QCoreApplication.translate("Updater_Window", u"Update and restart", None))
    # retranslateUi

