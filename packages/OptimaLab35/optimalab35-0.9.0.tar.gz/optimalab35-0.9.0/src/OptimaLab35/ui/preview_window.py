# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preview_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Preview_Window(object):
    def setupUi(self, Preview_Window):
        if not Preview_Window.objectName():
            Preview_Window.setObjectName(u"Preview_Window")
        Preview_Window.resize(803, 775)
        Preview_Window.setMinimumSize(QSize(800, 700))
        self.centralwidget = QWidget(Preview_Window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.QLabel = QLabel(self.centralwidget)
        self.QLabel.setObjectName(u"QLabel")
        self.QLabel.setMinimumSize(QSize(628, 628))
        self.QLabel.setFrameShape(QFrame.Box)
        self.QLabel.setScaledContents(False)

        self.horizontalLayout.addWidget(self.QLabel)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(150, 628))
        self.widget.setMaximumSize(QSize(150, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.image_path_lineEdit = QLineEdit(self.widget)
        self.image_path_lineEdit.setObjectName(u"image_path_lineEdit")

        self.verticalLayout_4.addWidget(self.image_path_lineEdit)

        self.load_Button = QPushButton(self.widget)
        self.load_Button.setObjectName(u"load_Button")

        self.verticalLayout_4.addWidget(self.load_Button)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 250))
        self.widget_2.setMaximumSize(QSize(16777215, 250))
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.brightness_spinBox = QSpinBox(self.widget_2)
        self.brightness_spinBox.setObjectName(u"brightness_spinBox")
        self.brightness_spinBox.setMinimum(-100)
        self.brightness_spinBox.setMaximum(100)

        self.verticalLayout.addWidget(self.brightness_spinBox)

        self.brightness_Slider = QSlider(self.widget_2)
        self.brightness_Slider.setObjectName(u"brightness_Slider")
        self.brightness_Slider.setMinimum(-100)
        self.brightness_Slider.setMaximum(100)
        self.brightness_Slider.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.brightness_Slider)

        self.reset_brightness_Button = QPushButton(self.widget_2)
        self.reset_brightness_Button.setObjectName(u"reset_brightness_Button")

        self.verticalLayout.addWidget(self.reset_brightness_Button)

        self.contrast_Slider = QSlider(self.widget_2)
        self.contrast_Slider.setObjectName(u"contrast_Slider")
        self.contrast_Slider.setMinimum(-100)
        self.contrast_Slider.setMaximum(100)
        self.contrast_Slider.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.contrast_Slider)

        self.contrast_spinBox = QSpinBox(self.widget_2)
        self.contrast_spinBox.setObjectName(u"contrast_spinBox")
        self.contrast_spinBox.setMinimum(-100)
        self.contrast_spinBox.setMaximum(100)

        self.verticalLayout.addWidget(self.contrast_spinBox)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.reset_contrast_Button = QPushButton(self.widget_2)
        self.reset_contrast_Button.setObjectName(u"reset_contrast_Button")

        self.verticalLayout.addWidget(self.reset_contrast_Button)

        self.grayscale_checkBox = QCheckBox(self.widget_2)
        self.grayscale_checkBox.setObjectName(u"grayscale_checkBox")

        self.verticalLayout.addWidget(self.grayscale_checkBox)


        self.verticalLayout_4.addWidget(self.widget_2)

        self.widget_5 = QWidget(self.widget)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_2 = QVBoxLayout(self.widget_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout_4.addWidget(self.widget_5)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.live_update = QCheckBox(self.widget_4)
        self.live_update.setObjectName(u"live_update")

        self.verticalLayout_3.addWidget(self.live_update)

        self.update_Button = QPushButton(self.widget_4)
        self.update_Button.setObjectName(u"update_Button")
        self.update_Button.setAutoFillBackground(False)

        self.verticalLayout_3.addWidget(self.update_Button)

        self.checkBox = QCheckBox(self.widget_4)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setLayoutDirection(Qt.LeftToRight)
        self.checkBox.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox)

        self.close_Button = QPushButton(self.widget_4)
        self.close_Button.setObjectName(u"close_Button")

        self.verticalLayout_3.addWidget(self.close_Button)


        self.verticalLayout_4.addWidget(self.widget_4)


        self.horizontalLayout.addWidget(self.widget)

        Preview_Window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Preview_Window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 803, 27))
        Preview_Window.setMenuBar(self.menubar)

        self.retranslateUi(Preview_Window)
        self.brightness_Slider.valueChanged.connect(self.brightness_spinBox.setValue)
        self.brightness_spinBox.valueChanged.connect(self.brightness_Slider.setValue)
        self.contrast_Slider.valueChanged.connect(self.contrast_spinBox.setValue)
        self.contrast_spinBox.valueChanged.connect(self.contrast_Slider.setValue)

        QMetaObject.connectSlotsByName(Preview_Window)
    # setupUi

    def retranslateUi(self, Preview_Window):
        Preview_Window.setWindowTitle(QCoreApplication.translate("Preview_Window", u"OptimaLab35 - Preview", None))
        self.QLabel.setText("")
#if QT_CONFIG(tooltip)
        self.image_path_lineEdit.setToolTip(QCoreApplication.translate("Preview_Window", u"Enter the path to the image file or use the 'Select Image' button to browse.", None))
#endif // QT_CONFIG(tooltip)
        self.image_path_lineEdit.setPlaceholderText(QCoreApplication.translate("Preview_Window", u"Image Path", None))
        self.load_Button.setText(QCoreApplication.translate("Preview_Window", u"Select image", None))
        self.label.setText(QCoreApplication.translate("Preview_Window", u"Brightness", None))
#if QT_CONFIG(tooltip)
        self.reset_brightness_Button.setToolTip(QCoreApplication.translate("Preview_Window", u"Click to reset the brightness to its default value (0).", None))
#endif // QT_CONFIG(tooltip)
        self.reset_brightness_Button.setText(QCoreApplication.translate("Preview_Window", u"Reset", None))
        self.label_2.setText(QCoreApplication.translate("Preview_Window", u"Contrast", None))
#if QT_CONFIG(tooltip)
        self.reset_contrast_Button.setToolTip(QCoreApplication.translate("Preview_Window", u"Click to reset the contrast to its default value (0).", None))
#endif // QT_CONFIG(tooltip)
        self.reset_contrast_Button.setText(QCoreApplication.translate("Preview_Window", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.grayscale_checkBox.setToolTip(QCoreApplication.translate("Preview_Window", u"Convert the image to grayscale (black and white).", None))
#endif // QT_CONFIG(tooltip)
        self.grayscale_checkBox.setText(QCoreApplication.translate("Preview_Window", u"Black n White", None))
#if QT_CONFIG(tooltip)
        self.live_update.setToolTip(QCoreApplication.translate("Preview_Window", u"Enable live updates to immediately preview changes as you adjust brightness, contrast, or grayscale. Be aware that this might impact performance, especially with large images.", None))
#endif // QT_CONFIG(tooltip)
        self.live_update.setText(QCoreApplication.translate("Preview_Window", u"Live update", None))
#if QT_CONFIG(tooltip)
        self.update_Button.setToolTip(QCoreApplication.translate("Preview_Window", u"Apply Changes to Preview", None))
#endif // QT_CONFIG(tooltip)
        self.update_Button.setText(QCoreApplication.translate("Preview_Window", u"Update Preview", None))
#if QT_CONFIG(tooltip)
        self.checkBox.setToolTip(QCoreApplication.translate("Preview_Window", u"Enable to copy adjustments to the main window upon closing", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox.setText(QCoreApplication.translate("Preview_Window", u"Copy Values", None))
#if QT_CONFIG(tooltip)
        self.close_Button.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.close_Button.setText(QCoreApplication.translate("Preview_Window", u"Close", None))
    # retranslateUi

