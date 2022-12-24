#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide2.QtWidgets import (
    QTableView,
    QApplication,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit,
    QFrame,
    QLabel,
    QHeaderView,
    QDateEdit,
    QTabWidget
)
from PySide2.QtCore import (
    Signal
)
from PySide2.QtCore import QSortFilterProxyModel, Qt, QRect
from sqlalchemy import create_engine
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Text,
    ForeignKey,
    insert,
    delete,
)
import sys


class DateBase:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database2.db")
        self.engine.connect()
        metadata = MetaData()
        self.Seller = Table(
            "Seller",
            metadata,
            Column("Код_продавца", Text(), nullable=False),
            Column("ФИО", Text(), nullable=False),
            Column("Дата_рождения", Text(), nullable=False),
            Column("Работает_с", Text(), nullable=False),
        )

        self.Client = Table(
            "Client",
            metadata,
            Column("Уникальный_номер", Text(), primary_key=True),
            Column("ФИО", Text(), nullable=False),
            Column("Дата_покупки", Text(), nullable=False),
            Column("Номер_телефона", Text(), nullable=False),
        )

        self.Board = Table(
            "Board",
            metadata,
            Column("Уникальный_номер", ForeignKey(self.Client.c.Уникальный_номер)),
            Column("Код_продавца", ForeignKey(self.Seller.c.Код_продавца)),
            Column("Способ_оплаты", Text(), nullable=False),
            Column("Статус_сделки", Text(), nullable=False),
        )
        metadata.create_all(self.engine)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database2.db")
        if not db.open():
            return False
        self.conn = self.engine.connect()

        if not self.table_is_empty():
            ins = insert(self.Seller)
            r = self.conn.execute(
                ins,
                Код_продавца="RC6",
                ФИО="Бобров Н.В.",
                Дата_рождения="19.12.2002",
                Работает_с="01.10.2021",
            )
            r = self.conn.execute(
                ins,
                Код_продавца="CR7",
                ФИО="Иванов И.И.",
                Дата_рождения="20.12.2001",
                Работает_с="01.09.2020",
            )
            r = self.conn.execute(
                ins,
                Код_продавца="MS1",
                ФИО="Смирнов С.С.",
                Дата_рождения="14.05.2000",
                Работает_с="24.03.2019",
            )
            ins = insert(self.Client)
            r = self.conn.execute(
                ins,
                Уникальный_номер="202",
                ФИО="Плотников Д.В.",
                Дата_покупки="15.08.2021",
                Номер_телефона="+7 918 765 67 92",
            )
            r = self.conn.execute(
                ins,
                Уникальный_номер="303",
                ФИО="Злыгостев И.С.",
                Дата_покупки="21.12.2021",
                Номер_телефона="+7 918 765 67 92",
            )
            r = self.conn.execute(
                ins,
                Уникальный_номер="404",
                ФИО="Галяс Д.И.",
                Дата_покупки="14.06.2020",
                Номер_телефона="+7 909 445 64 70",
            )
            ins = insert(self.Board)
            r = self.conn.execute(
                ins,
                Уникальный_номер="202",
                Код_продавца="RC6",
                Способ_оплаты="Наличный расчёт",
                Статус_сделки="Закрыта",
            )
            r = self.conn.execute(
                ins,
                Уникальный_номер="303",
                Код_продавца="CR7",
                Способ_оплаты="Безналичный",
                Статус_сделки="Отложена",
            )
            r = self.conn.execute(
                ins,
                Уникальный_номер="404",
                Код_продавца="MS1",
                Способ_оплаты="Безналичный",
                Статус_сделки="Активна",
            )

    def table_is_empty(self):
        data = self.Seller.select()
        table_data = self.conn.execute(data)
        return table_data.fetchall()


class TableView:
    tabBarClicked = Signal(int)

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.SetupUI()
        self.current_tab = "Seller"
        self.tab_id = "Код_продавца"

    def SetupUI(self):
        self.parent.setGeometry(400, 500, 1000, 650)
        self.parent.setWindowTitle("База данных торгового дома")
        self.main_conteiner = QGridLayout()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        self.frame2.setVisible(False)
        self.main_conteiner.addWidget(self.frame1, 0, 0)
        self.main_conteiner.addWidget(self.frame2, 0, 0)
        self.frame1.setStyleSheet(
            """
            font: bold;
            font-size: 12px;
            """
        )
        self.frame2.setStyleSheet(
            """
            font: bold;
            font-size: 12px;
            """
        )
        self.table_view = QTableView()
        self.table_view.setModel(self.tableCar())
        self.table_view2 = QTableView()
        self.table_view2.setModel(self.tableOwner())
        self.table_view3 = QTableView()
        self.table_view3.setModel(self.tableDocs())
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.layout_main = QGridLayout(self.frame1)
        self.layh = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_del = QPushButton("Удалить")
        self.layh.addWidget(self.btn_add)
        self.layh.addWidget(self.btn_del)
        self.tab_conteiner = QTabWidget()
        self.tab_conteiner.setTabShape(QTabWidget.Triangular)
        self.tab_conteiner.addTab(self.table_view, "Продавцы")
        self.tab_conteiner.addTab(self.table_view2, "Клиенты")
        self.tab_conteiner.addTab(self.table_view3, "Данные о завершенных покупках")
        self.layout_main.addWidget(self.tab_conteiner, 0, 0)
        self.layout_main.addLayout(self.layh, 1, 0)
        self.parent.setLayout(self.main_conteiner)
        self.btn_del.clicked.connect(self.delete)
        self.btn_add.clicked.connect(self.add)
        self.layout_grid = QGridLayout(self.frame2)
        self.btn_add2 = QPushButton("Добавить данные")
        self.btn_add2.setFixedWidth(300)
        self.btn_otmena = QPushButton("Отмена")
        self.line_name = QLineEdit()
        self.name = QLabel("ФИО клиента: ")
        self.uid_client_line = QLineEdit()
        self.uid_client = QLabel("Уникальный номер клиента: ")
        self.work_with_line = QDateEdit()
        self.work_with_line.setCalendarPopup(True)
        self.work_with_line.setTimeSpec(Qt.LocalTime)
        self.work_with_line.setGeometry(QRect(220, 31, 133, 20))
        self.work_with = QLabel("Работает с: ")
        self.dateb_line = QDateEdit()
        self.dateb_line.setCalendarPopup(True)
        self.dateb_line.setTimeSpec(Qt.LocalTime)
        self.dateb_line.setGeometry(QRect(220, 31, 133, 20))
        self.dateb = QLabel("Дата продажи: ")
        self.phone_number_line = QLineEdit()
        self.phone_number = QLabel("Номер телефона: ")
        self.name_seller_line = QLineEdit()
        self.name_seller = QLabel("ФИО продавца: ")
        self.date_birthday_seller_line = QDateEdit()
        self.date_birthday_seller_line.setCalendarPopup(True)
        self.date_birthday_seller_line.setTimeSpec(Qt.LocalTime)
        self.date_birthday_seller_line.setGeometry(QRect(220, 31, 133, 20))
        self.date_birthday_seller = QLabel("Дата рождения продавца: ")
        self.code_seller_line = QLineEdit()
        self.code_seller = QLabel("Уникальный код продавца: ")
        self.pay = QLabel("Способ оплаты: ")
        self.pay_line = QLineEdit()
        self.status_line = QLineEdit()
        self.status = QLabel("Статус сделки: ")
        self.layout_grid.addWidget(self.line_name, 0, 1)
        self.layout_grid.addWidget(self.name, 0, 0)
        self.layout_grid.addWidget(self.uid_client, 1, 0)
        self.layout_grid.addWidget(self.uid_client_line, 1, 1)
        self.layout_grid.addWidget(self.dateb, 2, 0)
        self.layout_grid.addWidget(self.dateb_line, 2, 1)
        self.layout_grid.addWidget(self.date_birthday_seller_line, 3, 1)
        self.layout_grid.addWidget(self.date_birthday_seller, 3, 0)
        self.layout_grid.addWidget(self.code_seller_line, 4, 1)
        self.layout_grid.addWidget(self.code_seller, 4, 0)
        self.layout_grid.addWidget(self.phone_number_line, 5, 1)
        self.layout_grid.addWidget(self.phone_number, 5, 0)
        self.layout_grid.addWidget(self.name_seller_line, 6, 1)
        self.layout_grid.addWidget(self.name_seller, 6, 0)
        self.layout_grid.addWidget(self.work_with_line, 7, 1)
        self.layout_grid.addWidget(self.work_with, 7, 0)
        self.layout_grid.addWidget(self.pay_line, 8, 1)
        self.layout_grid.addWidget(self.pay, 8, 0)
        self.layout_grid.addWidget(self.status, 9, 0)
        self.layout_grid.addWidget(self.status_line, 9, 1)
        self.layout_grid.addWidget(self.btn_add2, 10, 1)
        self.layout_grid.addWidget(self.btn_otmena, 10, 0)
        self.btn_otmena.clicked.connect(self.back)
        self.btn_add2.clicked.connect(self.add_data)
        self.tab_conteiner.tabBarClicked.connect(self.handle_tabbar_clicked)

    def tableCar(self):
        self.raw_model = QSqlTableModel()
        self.query = self.db.Seller.select()
        self.sqlquery = QSqlQuery()
        self.sqlquery.exec_(str(self.query))
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Seller"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableOwner(self):
        self.raw_model = QSqlTableModel()
        self.query = self.db.Client.select()
        self.sqlquery = QSqlQuery()
        self.sqlquery.exec_(str(self.query))
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Client"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableDocs(self):
        self.raw_model = QSqlTableModel()
        self.query = self.db.Board.select()
        self.sqlquery = QSqlQuery()
        self.sqlquery.exec_(str(self.query))
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Board"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def add(self):
        self.frame1.setVisible(False)
        self.frame2.setVisible(True)

    def back(self):
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def update(self):
        self.table_view.setModel(self.tableCar())
        self.table_view2.setModel(self.tableOwner())
        self.table_view3.setModel(self.tableDocs())

    def add_data(self):
        ins = insert(self.db.Seller)
        r = self.db.conn.execute(
            ins,
            Код_продавца=self.code_seller_line.text(),
            ФИО=self.name_seller_line.text(),
            Дата_рождения=self.date_birthday_seller_line.text(),
            Работает_с=self.work_with_line.text(),
        )
        ins = insert(self.db.Client)
        r = self.db.conn.execute(
            ins,
            Уникальный_номер=self.uid_client_line.text(),
            ФИО=self.line_name.text(),
            Дата_покупки=self.dateb_line.text(),
            Номер_телефона=self.phone_number_line.text(),
        )
        ins = insert(self.db.Board)
        r = self.db.conn.execute(
            ins,
            Уникальный_номер=self.uid_client_line.text(),
            Код_продавца=self.code_seller_line.text(),
            Способ_оплаты=self.pay_line.text(),
            Статус_сделки=self.status_line.text(),
        )
        self.update()
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def cell_click(self):
        if self.current_tab == "Seller":
            return self.table_view.model().data(self.table_view.currentIndex())
        if self.current_tab == "Client":
            return self.table_view3.model().data(self.table_view3.currentIndex())
        if self.current_tab == "Board":
            return self.table_view2.model().data(self.table_view2.currentIndex())

    def delete(self):
        if self.current_tab == "Seller":
            del_item = delete(self.db.Seller).where(
                self.db.Seller.c.Код_продавца.like(self.cell_click())
            )
            r = self.db.conn.execute(del_item)
        if self.current_tab == "Board":
            del_item = delete(self.db.Board).where(
                self.db.Board.c.Уникальный_номер.like(self.cell_click())
            )
            r = self.db.conn.execute(del_item)
        if self.current_tab == "Client":
            del_item = delete(self.db.Client).where(
                self.db.Client.c.Уникальный_номер.like(self.cell_click())
            )
            r = self.db.conn.execute(del_item)
        self.update()

    def handle_tabbar_clicked(self, index):
        if index == 0:
            self.current_tab = "Seller"
            self.tab_id = "Код_продавца"
        elif index == 1:
            self.current_tab = "Client"
            self.tab_id = "Уникальный_номер"
        else:
            self.tab_id = "Уникальный_номер"
            self.current_tab = "Board"


class MainWindow(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        my_datebase = DateBase()
        self.main_view = TableView(self, my_datebase)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
