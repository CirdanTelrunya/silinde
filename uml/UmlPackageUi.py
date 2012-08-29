# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/Package.ui'
#
# Created: Wed Aug 29 17:31:07 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DlgPackage(object):
    def setupUi(self, DlgPackage):
        DlgPackage.setObjectName(_fromUtf8("DlgPackage"))
        DlgPackage.resize(754, 459)
        self.verticalLayout = QtGui.QVBoxLayout(DlgPackage)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(DlgPackage)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabUML = QtGui.QWidget()
        self.tabUML.setObjectName(_fromUtf8("tabUML"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabUML)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.lblName = QtGui.QLabel(self.tabUML)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblName)
        self.ldtNom = QtGui.QLineEdit(self.tabUML)
        self.ldtNom.setObjectName(_fromUtf8("ldtNom"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.ldtNom)
        self.lblStereotype = QtGui.QLabel(self.tabUML)
        self.lblStereotype.setObjectName(_fromUtf8("lblStereotype"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblStereotype)
        self.cbxStereotype = QtGui.QComboBox(self.tabUML)
        self.cbxStereotype.setEditable(True)
        self.cbxStereotype.setObjectName(_fromUtf8("cbxStereotype"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.cbxStereotype)
        self.lblDescription = QtGui.QLabel(self.tabUML)
        self.lblDescription.setObjectName(_fromUtf8("lblDescription"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.lblDescription)
        self.tdtDescription = QtGui.QPlainTextEdit(self.tabUML)
        self.tdtDescription.setObjectName(_fromUtf8("tdtDescription"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.SpanningRole, self.tdtDescription)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.tabWidget.addTab(self.tabUML, _fromUtf8(""))
        self.tabCpp = QtGui.QWidget()
        self.tabCpp.setObjectName(_fromUtf8("tabCpp"))
        self.formLayout = QtGui.QFormLayout(self.tabCpp)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lblSourcesDir = QtGui.QLabel(self.tabCpp)
        self.lblSourcesDir.setObjectName(_fromUtf8("lblSourcesDir"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblSourcesDir)
        self.ldtSourcesDir = QtGui.QLineEdit(self.tabCpp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ldtSourcesDir.sizePolicy().hasHeightForWidth())
        self.ldtSourcesDir.setSizePolicy(sizePolicy)
        self.ldtSourcesDir.setObjectName(_fromUtf8("ldtSourcesDir"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.ldtSourcesDir)
        self.lblHeadersDir = QtGui.QLabel(self.tabCpp)
        self.lblHeadersDir.setObjectName(_fromUtf8("lblHeadersDir"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblHeadersDir)
        self.ldtHeadersDir = QtGui.QLineEdit(self.tabCpp)
        self.ldtHeadersDir.setObjectName(_fromUtf8("ldtHeadersDir"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ldtHeadersDir)
        self.lblNamespace = QtGui.QLabel(self.tabCpp)
        self.lblNamespace.setObjectName(_fromUtf8("lblNamespace"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lblNamespace)
        self.ldtNamespace = QtGui.QLineEdit(self.tabCpp)
        self.ldtNamespace.setObjectName(_fromUtf8("ldtNamespace"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.ldtNamespace)
        self.tabWidget.addTab(self.tabCpp, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(DlgPackage)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DlgPackage)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DlgPackage.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DlgPackage.reject)
        QtCore.QMetaObject.connectSlotsByName(DlgPackage)

    def retranslateUi(self, DlgPackage):
        DlgPackage.setWindowTitle(QtGui.QApplication.translate("DlgPackage", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("DlgPackage", "name:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStereotype.setText(QtGui.QApplication.translate("DlgPackage", "stereotype:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDescription.setText(QtGui.QApplication.translate("DlgPackage", "description:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabUML), QtGui.QApplication.translate("DlgPackage", "UML", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSourcesDir.setText(QtGui.QApplication.translate("DlgPackage", "sources directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblHeadersDir.setText(QtGui.QApplication.translate("DlgPackage", "headers directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblNamespace.setText(QtGui.QApplication.translate("DlgPackage", "namespace:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCpp), QtGui.QApplication.translate("DlgPackage", "C++", None, QtGui.QApplication.UnicodeUTF8))

