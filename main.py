import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDateTime
import sqlite3
from PIL import Image

con = sqlite3.connect("MI.db")
cur = con.cursor()

#################### Grobal variable ################
#################### Overriding #####################

class QWFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")

class QWLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")

class QNumberEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignRight)
        self.setValidator(QDoubleValidator())
        self.setStyleSheet("background-color:white")

class QWComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")

class QWDateEdit(QDateEdit):
    def __init__(self, calendarPopup=True):
        super().__init__(calendarPopup=True)
        self.setStyleSheet("background-color:white; color:black")

class QWTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")

class QGPushButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("background-color:#F0F0F0")

class QTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setMovable(True)

class QPushButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)
        self.setStyleSheet(" border-color:black; background-color:orange")


################# Global Function #######################

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.closebutton = QWidget()
        self.setWindowTitle("MI Project")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(270, 150, 1500, 850)

        ######## 창 고정 ##############
        # self.setFixedSize(self.size())

        ######## 프로그램 작동 ########

        self.UI()
        self.show()

    def UI(self):
        self.widgets()



    def widgets(self):
        ########################## 메뉴바 ####################################
        ########################## 메인 메뉴 #################################
        self.menubar = self.menuBar()
        self.chitManagement = self.menubar.addMenu("전표관리")
        self.inventoryManagement = self.menubar.addMenu("재고관리")
        self.accountManagement = self.menubar.addMenu("거래처관리")
        ########################## 서브 메뉴 ##################################
        ########################## 매출전표 ###################################
        self.salesSlipMenu = QAction("매출전표", self)
        self.salesSlipMenu.triggered.connect(self.salesSlipFunc)
        self.chitManagement.addAction(self.salesSlipMenu)
        self.salesSlipTab = QWidget()
        ########################## 재고관리 ###################################
        ########################## 거래처관리 ##################################
        self.accountManagementM = QAction("거래처관리", self)
        self.accountManagementM.triggered.connect(self.accountManagementMFunc)
        self.accountManagement.addAction(self.accountManagementM)
        self.AMTab = QWidget()
        ########################## 툴바 #######################################
        self.toolBar = self.addToolBar("나의 툴바")
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.newFolder = QAction(QIcon("icons/folder.png"), "새로운 폴더", self)
        self.toolBar.addAction(self.newFolder)
        ########################## 메인 탭 설정 ################################
        self.mainTabs = QTabWidget()
        self.mainTabs.setTabsClosable(True)
        self.mainTabs.tabCloseRequested.connect(self.CloseTabEvent)
        self.setCentralWidget(self.mainTabs)
        ########################## 탭 설정 ####################################

    def salesSlipFunc(self):

        ########################## ss Tab Init ###############################
        if self.mainTabs.currentIndex() == -1:
            self.mainTabs.addTab(self.salesSlipTab, "매출전표")
        elif self.mainTabs.currentIndex() != -1:
            for i in range(len(self.mainTabs)):
                if "매출전표" == self.mainTabs.tabText(i):
                    index = i
                    self.mainTabs.setCurrentIndex(i)
                    break
                else:
                    self.mainTabs.addTab(self.salesSlipTab, "매출전표")
        ########################## ss Left Widgets ###################################
        ########################## ss tabs ###########################################
        self.ssOrderTab = QWFrame()
        self.ssTrading = QWidget()
        self.ssTax = QWidget()
        self.ssTotal = QWidget()
        self.sstabs = QTabWidget()
        self.sstabs.addTab(self.ssOrderTab, "수주")
        self.sstabs.addTab(self.ssTrading, "거래명세서")
        self.sstabs.addTab(self.ssTax, "세금계산서")
        self.sstabs.addTab(self.ssTotal, "전체")
        ########################## ss Combo items ######################################
        self.ssOrderAccountSelectCList = []
        query = "SELECT * FROM accounts"
        OrderAccounts = cur.execute(query)
        for account in OrderAccounts:
            self.ssOrderAccountSelectCList.append(account[1])


        self.ssOrderShapeList = [
            self.tr('STS 판'), self.tr('SUS 코일'), self.tr('SUS 평철'), self.tr('SUS 앵글'), self.tr('SUS 환봉'),
            self.tr('SUS 파이프'), self.tr('스크랩'), self.tr('프랜지'), self.tr('피팅'), self.tr('구조용부속'),
            self.tr('밸브'), self.tr('볼트/너트'), self.tr('가공비'), self.tr('사각파이프'), self.tr('파이프가공비'),
            self.tr('사각파이프가공비'), self.tr('환봉가공비'), self.tr('기타'), self.tr('원형절단품'), self.tr('사각봉'),
            self.tr('육각봉'), self.tr('사각절단품'), self.tr('임가공'), self.tr('사급(원형)'), self.tr('사급(사각)'),
            self.tr('사급(모형)'), self.tr('모형절단품'), self.tr('절단비'), self.tr('밴딩비'), self.tr('절단,절곡'),
            self.tr('니플'), self.tr('용접봉'), self.tr('잔넬')
        ]
        self.ssOrderStealTypeList = [
            self.tr('304'),
            self.tr('304L'),
            self.tr('316'),
            self.tr('316L'),
            self.tr('SUS 304'),
            self.tr('SUS 304L'),
            self.tr('202'),
            self.tr('201'),
            self.tr('301'),
            self.tr('310S'),
            self.tr('430'),
            self.tr('410S'),
            self.tr('304J1'),
            self.tr('304J1'),
            self.tr('420J1_판'),
            self.tr('321_판'),
            self.tr('420N1')
        ]

        self.ssOrderSurfaceList = [
            self.tr('2B'),
            self.tr('H/L'),
            self.tr('P/L'),
            self.tr('NO.1'),
            self.tr('CHECK'),
            self.tr('2B VIB'),
            self.tr('2B VIB NSP'),
            self.tr('HL BLACK'),
            self.tr('HL BLACK NSP'),
            self.tr('MR TI골드'),
            self.tr('MR TI골드'),
            self.tr('MR'),
            self.tr('단면 P/L'),
            self.tr('양면 P/L'),
            self.tr('MR INCO블랙'),
            self.tr('BEAD BLAST'),
            self.tr('BEAD BLAST BLACK'),
            self.tr('BA-BEAD TI골드'),
            self.tr('BEAD TIN BRONZE'),
            self.tr('BEAD BLAST BLACK NSP'),
            self.tr('NO.4'),
            self.tr('#4'),
            self.tr('PVC백'),
            self.tr('BA-VIB'),
            self.tr('TI-BLACK+NANO COATING'),
            self.tr('PVC부착')
        ]

        ########################## ss 수주 widgets ######################################
        self.ssOrderAccountSelectC = QWComboBox()
        self.ssOrderAccountSelectC.addItems(self.ssOrderAccountSelectCList)
        self.ssOrderShape = QWComboBox()
        self.ssOrderShape.addItems(self.ssOrderShapeList)
        self.ssStealType0 = QWComboBox()
        self.ssStealType0.addItems(self.ssOrderStealTypeList)
        self.ssStealType0.currentTextChanged.connect(self.ssStealTypeInsert)
        self.ssStealType1 = QNumberEdit()
        self.ssStealType1.setText("7.93")


        self.ssOrderStealTypes = QHBoxLayout()
        self.ssOrderStealTypes.addWidget(self.ssStealType0, 70)
        self.ssOrderStealTypes.addWidget(self.ssStealType1, 30)
        self.ssOrderSurface = QWComboBox()
        self.ssOrderSurface.addItems(self.ssOrderSurfaceList)
        self.ssOrderThick = QNumberEdit()
        self.ssOrderWidth = QNumberEdit()
        self.ssOrderLength = QNumberEdit()
        self.ssCalMethod = QWComboBox()
        self.ssOrderQuantities = QHBoxLayout()
        self.ssQuantity0 = QNumberEdit()
        self.ssQuantity1 = QWComboBox()
        self.ssQuantity2 = QRadioButton()
        self.ssOrderQuantities.addWidget(self.ssQuantity0)
        self.ssOrderQuantities.addWidget(self.ssQuantity1)
        self.ssOrderQuantities.addWidget(self.ssQuantity2)
        self.ssOrderLengths = QHBoxLayout()
        self.ssOrderLength0 = QNumberEdit()
        self.ssOrderLength1 = QWComboBox()
        self.ssOrderLength2 = QRadioButton()
        self.ssOrderLengths.addWidget(self.ssOrderLength0)
        self.ssOrderLengths.addWidget(self.ssOrderLength1)
        self.ssOrderLengths.addWidget(self.ssOrderLength2)
        self.ssOrderUnitPrice = QNumberEdit()
        self.ssOrderPrice = QNumberEdit()
        self.ssOrderDateEdit = QWDateEdit(calendarPopup=True)
        self.ssOrderDateEdit.setDateTime(QDateTime.currentDateTime())
        ############################ 수주 Form 좌측 상단 ####################################

        self.ssOrderForm = QFormLayout()
        self.ssOrderForm.addRow(QLabel("  업체선택"), self.ssOrderAccountSelectC)
        self.ssOrderForm.addRow(QLabel("        형상"), self.ssOrderShape)
        self.ssOrderForm.addRow(QLabel("        강종"), self.ssOrderStealTypes)
        self.ssOrderForm.addRow(QLabel("        표면"), self.ssOrderSurface)

        self.ssOrderForm.addRow(QLabel("외경(mm)"), self.ssOrderThick)
        self.ssOrderForm.addRow(QLabel("두께(mm)"), self.ssOrderWidth)
        self.ssOrderForm.addRow(QLabel("길이(mm)"), self.ssOrderLength)

        self.ssOrderForm.addRow(QLabel("  계산방법"), self.ssCalMethod)
        self.ssOrderForm.addRow(QLabel("        수량"), self.ssOrderQuantities)
        self.ssOrderForm.addRow(QLabel("        길이"), self.ssOrderLengths)
        self.ssOrderForm.addRow(QLabel("        단가"), self.ssOrderUnitPrice)
        self.ssOrderForm.addRow(QLabel("        금액"), self.ssOrderPrice)

        self.ssOrderForm.addRow(QLabel("  납기일자"), self.ssOrderDateEdit)

        ############################ 수주 Form 좌측 중단 ####################################

        self.ssOrderTextForm = QFormLayout()
        self.ssOrderTextEdit = QTextEdit()
        self.ssOrderTextEdit.setMaximumHeight(100)
        self.ssOrderTextEdit.setStyleSheet("background-color:white")
        self.ssOrderTextForm.addRow(QLabel("        메모"), self.ssOrderTextEdit)

        ############################ 수주 Form 좌측 하단 ####################################

        self.ssOrderSubmitBtn = QPushButton("등록")
        self.ssOrderSubmitBtn.setMaximumWidth(270)

        self.ssOrderButtonLayout = QHBoxLayout()
        self.ssOrderButtonLayout.addWidget(self.ssOrderSubmitBtn)

        ############################ 수주 List 우측 상단 ####################################

        self.ssOrderChitDate = QLabel("전표일자")
        self.ssOrderListSelect = QLabel("업체선택")
        self.ssOrderListSelectC = QWComboBox()
        self.ssOrderListSelectC.addItems(self.ssOrderAccountSelectCList)
        self.ssOrderListSearchB = QPushButton("조회")

        self.ssOrderListDateEdit = QWDateEdit(calendarPopup=True)
        self.ssOrderListDateEdit.setDateTime(QDateTime.currentDateTime())

        self.ssOrderTabRTLayout = QHBoxLayout()
        self.ssOrderTabRTLayout.addWidget(self.ssOrderChitDate)
        self.ssOrderTabRTLayout.addWidget(self.ssOrderListDateEdit)
        self.ssOrderTabRTLayout.addWidget(self.ssOrderListSelect)
        self.ssOrderTabRTLayout.addWidget(self.ssOrderListSelectC)
        self.ssOrderTabRTLayout.addWidget(self.ssOrderListSearchB)
        self.ssOrderTabRTLayout.addStretch(1)

        ############################ 수주 List 우측 중단 ####################################

        self.ssOrderTabTSbutton = QGPushButton("거래명세서")
        self.ssOrderTabIRbutton = QGPushButton("송장/인수증")
        self.ssOrderTabSIbutton = QGPushButton("출하지시서")

        self.ssOrderTabRMLayout = QHBoxLayout()
        self.ssOrderTabRMLayout.addWidget(self.ssOrderTabTSbutton)
        self.ssOrderTabRMLayout.addWidget(self.ssOrderTabIRbutton)
        self.ssOrderTabRMLayout.addWidget(self.ssOrderTabSIbutton)
        self.ssOrderTabRTLayout.addStretch(1)

        ############################ 수주 List 우측 Table ####################################

        self.ssOrderTable = QTableWidget()
        self.ssOrderTable.setColumnCount(9)
        self.ssOrderTable.setColumnHidden(0, True)
        self.ssOrderTable.setHorizontalHeaderItem(0, QTableWidgetItem("Order_Id"))
        self.ssOrderTable.setHorizontalHeaderItem(1, QTableWidgetItem("수주번호"))
        self.ssOrderTable.setHorizontalHeaderItem(2, QTableWidgetItem("제품명"))
        self.ssOrderTable.setHorizontalHeaderItem(3, QTableWidgetItem("수량"))
        self.ssOrderTable.setHorizontalHeaderItem(4, QTableWidgetItem("길이"))
        self.ssOrderTable.setHorizontalHeaderItem(5, QTableWidgetItem("단위"))
        self.ssOrderTable.setHorizontalHeaderItem(6, QTableWidgetItem("단가"))
        self.ssOrderTable.setHorizontalHeaderItem(7, QTableWidgetItem("금액"))
        self.ssOrderTable.setHorizontalHeaderItem(8, QTableWidgetItem("납기일자"))
        self.ssOrderTable.setHorizontalHeaderItem(9, QTableWidgetItem("메모"))

        ############################ ss Order Layouts ########################################

        self.ssOrderTabLeftLayout = QVBoxLayout()
        self.ssOrderTabLeftLayout.addLayout(self.ssOrderForm)
        self.ssOrderTabLeftLayout.addLayout(self.ssOrderTextForm)
        self.ssOrderTabLeftLayout.addStretch(1)
        self.ssOrderTabLeftLayout.addLayout(self.ssOrderButtonLayout)
        self.ssOrderTabLeftLayout.addStretch(5)
        self.ssOrderTabLeftFrame = QFrame()
        self.ssOrderTabLeftFrame.setLayout(self.ssOrderTabLeftLayout)
        self.ssOrderTabLeftFrame.setStyleSheet("background-color:#F0F0F0")

        self.ssOrderTabRightLayout = QVBoxLayout()
        self.ssOrderTabRightLayout.addLayout(self.ssOrderTabRTLayout)
        self.ssOrderTabRightLayout.addLayout(self.ssOrderTabRMLayout)
        self.ssOrderTabRightLayout.addWidget(self.ssOrderTable)
        self.ssOrderTabRightFrame = QFrame()
        self.ssOrderTabRightFrame.setLayout(self.ssOrderTabRightLayout)

        self.ssOrderTabMainLayout = QHBoxLayout()
        self.ssOrderTabMainLayout.addWidget(self.ssOrderTabLeftFrame, 20)
        self.ssOrderTabMainLayout.addWidget(self.ssOrderTabRightFrame, 80)

        self.ssOrderTab.setLayout(self.ssOrderTabMainLayout)


        ########################## ss Set Frame and Layouts ###############################

        self.ssMainLayout = QHBoxLayout()
        self.ssMainLayout.addWidget(self.sstabs)
        self.salesSlipTab.setLayout(self.ssMainLayout)

    def accountManagementMFunc(self):

        ########################## AM Tab Init ###############################
        if self.mainTabs.currentIndex() == -1:
            self.mainTabs.addTab(self.AMTab, "거래처관리")
        elif self.mainTabs.currentIndex() != -1:
            for i in range(len(self.mainTabs)):
                if "거래처관리" == self.mainTabs.tabText(i):
                    index = i
                    self.mainTabs.setCurrentIndex(i)
                    break
                else:
                    self.mainTabs.addTab(self.AMTab, "거래처관리")

        ######################### am Left Widgets ###################################
        ######################### am tabs ###########################################
        self.amInfoTab = QWFrame()
        self.amtabs = QTabWidget()
        self.amtabs.addTab(self.amInfoTab, "거래처정보")

        ########################## am Combo Items #####################################################
        self.companyDivComboList = ["법인사업자","개인사업자","개인"]

        ########################## am 거래처정보 ########################################################
        ########################## am 거래처정보 Form widgets ###########################################

        self.accountNameEntry = QWLineEdit()
        self.accountCodeEntry = QWLineEdit()

        self.companyRadioSales = QRadioButton("매출처")
        self.companyRadioPurchase = QRadioButton("매입처")
        self.companyRadioTransit = QRadioButton("운송사")
        self.companyRadioLayout = QHBoxLayout()
        self.companyRadioLayout.addWidget(self.companyRadioSales)
        self.companyRadioLayout.addWidget(self.companyRadioPurchase)
        self.companyRadioLayout.addWidget(self.companyRadioTransit)

        self.companyDivCombo = QWComboBox()
        self.companyDivCombo.addItems(self.companyDivComboList)
        self.companyDivLayout = QHBoxLayout()
        self.companyDivLayout.addWidget(self.companyDivCombo)

        self.corNumberEdit0 = QWLineEdit()
        self.corNumberEdit0.setMaxLength(6)
        self.corNumberEdit0.setValidator(QIntValidator())
        self.corNumberEdit1 = QWLineEdit()
        self.corNumberEdit1.setMaxLength(7)
        self.corNumberEdit1.setValidator(QIntValidator())
        self.corNumberLayout = QHBoxLayout()
        self.corNumberLayout.addWidget(self.corNumberEdit0)
        self.corNumberLayout.addWidget(QLabel("-"))
        self.corNumberLayout.addWidget(self.corNumberEdit1)

        self.comPanyResNumber0 = QWLineEdit()
        self.comPanyResNumber0.setMaxLength(3)
        self.comPanyResNumber0.setValidator(QIntValidator())
        self.comPanyResNumber1 = QWLineEdit()
        self.comPanyResNumber1.setMaxLength(2)
        self.comPanyResNumber1.setValidator(QIntValidator())
        self.comPanyResNumber2 = QWLineEdit()
        self.comPanyResNumber2.setMaxLength(5)
        self.comPanyResNumber2.setValidator(QIntValidator())
        self.comPanyResNumberLayout = QHBoxLayout()
        self.comPanyResNumberLayout.addWidget(self.comPanyResNumber0)
        self.comPanyResNumberLayout.addWidget(QLabel("-"))
        self.comPanyResNumberLayout.addWidget(self.comPanyResNumber1)
        self.comPanyResNumberLayout.addWidget(QLabel("-"))
        self.comPanyResNumberLayout.addWidget(self.comPanyResNumber2)

        self.comPanyTypeEdit = QWTextEdit()
        self.comPanyTypeEdit.setMaximumHeight(50)
        self.comPanyTypeLayout = QHBoxLayout()
        self.comPanyTypeLayout.addWidget(self.comPanyTypeEdit)

        self.comPanyItemEdit = QWTextEdit()
        self.comPanyItemEdit.setMaximumHeight(50)
        self.comPanyItemLayout = QHBoxLayout()
        self.comPanyItemLayout.addWidget(self.comPanyItemEdit)

        self.ceoName = QWLineEdit()
        self.companyPhone = QWLineEdit()
        self.ceoNameCompanyPhoneLayout = QHBoxLayout()
        self.ceoNameCompanyPhoneLayout.addWidget(QLabel("         대표자명"))
        self.ceoNameCompanyPhoneLayout.addWidget(self.ceoName)
        self.ceoNameCompanyPhoneLayout.addWidget(QLabel("대표번호"))
        self.ceoNameCompanyPhoneLayout.addWidget(self.companyPhone)

        self.companyAddress = QWLineEdit()
        self.companyAddressLayout = QHBoxLayout()
        self.companyAddressLayout.addWidget(self.companyAddress)

        self.bankAccountNumber = QWLineEdit()
        self.bankAccountNumberLayout = QHBoxLayout()
        self.bankAccountNumberLayout.addWidget(self.bankAccountNumber)

        self.AmInfoSaveBtn = QPushButton("저장")
        self.AmInfoSaveBtn.clicked.connect(self.addAccount)
        self.AmInfoSaveBtnLayout = QHBoxLayout()
        self.AmInfoSaveBtnLayout.addStretch(1)
        self.AmInfoSaveBtnLayout.addWidget(self.AmInfoSaveBtn)
        ########################### 거래처정보 Form Layouts ####################################

        self.AmInfoForm = QFormLayout()
        self.AmInfoForm.addRow(QLabel("         거래처명"), self.accountNameEntry)
        self.AmInfoForm.addRow(QLabel("      거래처코드"), self.accountCodeEntry)
        self.AmInfoForm.addRow(QLabel("         거래구분"), self.companyRadioLayout)
        self.AmInfoForm.addRow(QLabel("         회사구분"), self.companyDivCombo)
        self.AmInfoForm.addRow(QLabel("   법인등록번호"), self.corNumberLayout)
        self.AmInfoForm.addRow(QLabel("사업자등록번호"), self.comPanyResNumberLayout)
        self.AmInfoForm.addRow(QLabel("               업태"), self.comPanyTypeLayout)
        self.AmInfoForm.addRow(QLabel("               종목"), self.comPanyItemLayout)
        self.AmInfoForm.addRow(self.ceoNameCompanyPhoneLayout)
        self.AmInfoForm.addRow(QLabel("         회사주소"),self.companyAddressLayout)
        self.AmInfoForm.addRow(QLabel("         계좌번호"),self.bankAccountNumberLayout)
        self.AmInfoForm.addRow(self.AmInfoSaveBtnLayout)

        ########################### 거래처 목록 삭제 & 조회 #################################
        self.AccountListDeleteBtn = QPushButton("삭제")
        self.AccountListDeleteBtn.clicked.connect(self.accountDeleteBtnClickedEvent)
        self.AccountListSearchEdit = QWLineEdit()
        self.AccountListSearchEdit.setMinimumWidth(300)
        self.AccountListSearchBtn = QPushButton("조회")
        self.AccountListSearchBtn.clicked.connect(self.AccountListSearchBtnEvent)

        self.AccountListFunctionLayout = QHBoxLayout()
        self.AccountListFunctionLayout.addWidget(self.AccountListDeleteBtn)
        self.AccountListFunctionLayout.addStretch(30)
        self.AccountListFunctionLayout.addWidget(QLabel("거래처코드"))
        self.AccountListFunctionLayout.addWidget(self.AccountListSearchEdit)
        self.AccountListFunctionLayout.addStretch(1)
        self.AccountListFunctionLayout.addWidget(self.AccountListSearchBtn)





        ########################### 거래처 목록 Layouts ####################################

        self.AccountListTopLayout = QHBoxLayout()


        self.AccountListTable = QTableWidget()
        self.AccountListTable.setStyleSheet("background-color:white")
        self.AccountListTable.setColumnCount(13)
        self.AccountListTable.setColumnHidden(0, True)
        self.AccountListTable.setHorizontalHeaderItem(0, QTableWidgetItem("account_Id"))
        self.AccountListTable.setHorizontalHeaderItem(1, QTableWidgetItem("거래처명"))
        self.AccountListTable.setHorizontalHeaderItem(2, QTableWidgetItem("거래처코드"))
        self.AccountListTable.setHorizontalHeaderItem(3, QTableWidgetItem("거래구분"))
        self.AccountListTable.setHorizontalHeaderItem(4, QTableWidgetItem("회사구분"))
        self.AccountListTable.setHorizontalHeaderItem(5, QTableWidgetItem("법인등록번호"))
        self.AccountListTable.setHorizontalHeaderItem(6, QTableWidgetItem("사업자등록번호"))
        self.AccountListTable.setHorizontalHeaderItem(7, QTableWidgetItem("업태"))
        self.AccountListTable.setHorizontalHeaderItem(8, QTableWidgetItem("종목"))
        self.AccountListTable.setHorizontalHeaderItem(9, QTableWidgetItem("대표자명"))
        self.AccountListTable.setHorizontalHeaderItem(10, QTableWidgetItem("대표번호"))
        self.AccountListTable.setHorizontalHeaderItem(11, QTableWidgetItem("회사주소"))
        self.AccountListTable.setHorizontalHeaderItem(12, QTableWidgetItem("계좌번호"))
        self.AccountListTable.setColumnWidth(5,150)
        self.AccountListTable.setColumnWidth(6,130)
        self.AccountListTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.AccountListTable.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self.AccountListTable.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)
        self.AccountListTable.horizontalHeader().setSectionResizeMode(10, QHeaderView.ResizeToContents)
        self.AccountListTable.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeToContents)
        self.AccountListTable.horizontalHeader().setSectionResizeMode(12, QHeaderView.ResizeToContents)

        self.AccountListTableLayout = QVBoxLayout()
        self.AccountListTableLayout.addWidget(self.AccountListTable)

        self.disPlayAccounts()



        ############################ am AccountInfo Layouts ########################################

        self.amAccountInfoLeftLayout = QVBoxLayout()
        self.amAccountInfoLeftLayout.addLayout(self.AmInfoForm)
        self.amAccountInfoLeftLayout.addStretch(1)
        self.amAccountTabLeftFrame = QFrame()
        self.amAccountTabLeftFrame.setLayout(self.amAccountInfoLeftLayout)
        self.amAccountTabLeftFrame.setStyleSheet("background-color:#F0F0F0")

        self.amAcoountTabRightLayout = QVBoxLayout()
        self.amAcoountTabRightLayout.addLayout(self.AccountListFunctionLayout)
        self.amAcoountTabRightLayout.addLayout(self.AccountListTopLayout)
        self.amAcoountTabRightLayout.addLayout(self.AccountListTableLayout)
        self.amAccountTabRightFrame = QFrame()
        self.amAccountTabRightFrame.setStyleSheet("background-color:#F0F0F0")
        self.amAccountTabRightFrame.setLayout(self.amAcoountTabRightLayout)

        self.amAccountTabMainLayout = QHBoxLayout()
        self.amAccountTabMainLayout.addWidget(self.amAccountTabLeftFrame, 26)
        self.amAccountTabMainLayout.addWidget(self.amAccountTabRightFrame, 74)

        self.amInfoTab.setLayout(self.amAccountTabMainLayout)

        ########################## ss Set Frame and Layouts ###############################

        self.amMainLayout = QHBoxLayout()
        self.amMainLayout.addWidget(self.amtabs)
        self.AMTab.setLayout(self.amMainLayout)


    def addAccount(self):

        account_name = self.accountNameEntry.text()
        account_code = self.accountCodeEntry.text()

        if(self.companyRadioSales.isChecked()):
            trans_sort = "매출처"
        elif (self.companyRadioPurchase.isChecked()):
            trans_sort = "매입처"
        else:
            trans_sort = "운송사"

        company_sort = self.companyDivCombo.currentText()
        cor_number = self.corNumberEdit0.text() + "-" + self.corNumberEdit1.text()
        ent_number = self.comPanyResNumber0.text() + "-" + self.comPanyResNumber1.text() + "-" + self.comPanyResNumber2.text()
        company_type = self.comPanyTypeEdit.toPlainText()
        company_item = self.comPanyItemEdit.toPlainText()
        ceo_name = self.ceoName.text()
        company_number = self.companyPhone.text()
        company_loc = self.companyAddress.text()
        bank_account = self.bankAccountNumber.text()

        query = "SELECT * FROM 'accounts' WHERE account_name = ? OR account_code = ?"

        if(account_name !="" and account_code !=""):
            try:
                query = "SELECT * FROM 'accounts' WHERE account_name = ? OR account_code = ?"
                if (cur.execute(query, (account_name, account_code)).fetchall() == []):
                    try:
                        query = "INSERT INTO 'accounts' (account_name, account_code, trans_sort, company_sort, cor_number, ent_number, company_type, company_item, ceo_name, company_number, company_loc, bank_account) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) "
                        cur.execute(query, (
                        account_name, account_code, trans_sort, company_sort, cor_number, ent_number, company_type,
                        company_item, ceo_name, company_number, company_loc, bank_account))
                        con.commit()
                        QMessageBox.information(self, "정보", "거래처가 추가 되었습니다.")

                    except:
                        QMessageBox.information(self, "경고!", "거래처가 추가되지 않았습니다.")
                else :
                    QMessageBox.information(self, "경고!", "이미 같은 거래처명 혹은 거래처코드가 있습니다.")
            except:
                QMessageBox.information(self, "경고!", "알 수없는 문제가 생겼습니다.")
        else:
            QMessageBox.information(self, "경고!", "거래처명 혹은 거래처코드가 비어있습니다.")


        for i in reversed(range(self.AccountListTable.rowCount())):
            self.AccountListTable.removeRow(i)

        query = cur.execute("SELECT account_id, account_name, account_code, trans_sort, company_sort, cor_number, ent_number, company_type, company_item, ceo_name, company_number, company_loc, bank_account FROM accounts")
        for row_data in query:
            row_number = self.AccountListTable.rowCount()
            self.AccountListTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.AccountListTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))




    def disPlayAccounts(self):
        self.AccountListTable.setFont(QFont("돋움",12))
        for i in reversed(range(self.AccountListTable.rowCount())):
            self.AccountListTable.removeRow(i)

        query = cur.execute("SELECT account_id, account_name, account_code, trans_sort, company_sort, cor_number, ent_number, company_type, company_item, ceo_name, company_number, company_loc, bank_account FROM accounts")
        for row_data in query:
            row_number = self.AccountListTable.rowCount()
            self.AccountListTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.AccountListTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))

            # This is Spare Code
            # self.AccountListTable.setItem(row_number,5,QTableWidgetItem(str(row_data[5])))

        self.AccountListTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def CloseTabEvent(self, currentIndex):

        self.mainTabs.removeTab(currentIndex)

    def ssStealTypeInsert(self):

        search_text = self.ssStealType0.currentText()
        same_770 = ["430"]
        same_780 = ["420N1","420J1_판"]
        same_784 = ["410S"]
        same_785 = ["201","202"]
        same_793 = ["301","304","304L", "304J1", "SUS 304","SUS 304L","321_판" ]
        same_798 = ["310S","316","316L"]

        if search_text in same_770:
            self.ssStealType1.setText("7.70")
        elif search_text in same_780:
            self.ssStealType1.setText("7.80")
        elif search_text in same_784:
            self.ssStealType1.setText("7.84")
        elif search_text in same_785:
            self.ssStealType1.setText("7.85")
        elif search_text in same_793:
            self.ssStealType1.setText("7.93")
        elif search_text in same_798:
            self.ssStealType1.setText("7.98")

    def AccountListSearchBtnEvent(self):

        search_text = self.AccountListSearchEdit.text()

        try:
            query = "SELECT * FROM 'accounts' WHERE account_code LIKE ?"
            searched_data = cur.execute(query, ("%"+search_text+"%",)).fetchall()

            for i in reversed(range(self.AccountListTable.rowCount())):
                self.AccountListTable.removeRow(i)

            for row_data in searched_data:
                row_number = self.AccountListTable.rowCount()
                self.AccountListTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.AccountListTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except:
            pass


    def accountDeleteBtnClickedEvent(self):

        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('메세지')
        box.setText('정말 삭제하시겠습니까?')
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('네')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('아니요')
        reply = box.exec_()

        if reply == QMessageBox.Yes:
            try:
                row = self.AccountListTable.currentRow()
                col = self.AccountListTable.currentColumn()

                account = self.AccountListTable.item(row, 1).text()
                code = self.AccountListTable.item(row, 2).text()

                query = "DELETE FROM 'accounts' WHERE account_name = ? AND account_code = ?"
                cur.execute(query, (account, code)).fetchone()
                con.commit()
                QMessageBox.information(self, "정보", "거래처가 삭제되었습니다.")
                con.close()
            except:
                QMessageBox.information(self, "정보", "거래처가 삭제되지 않았습니다.")
        else:
            pass


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()