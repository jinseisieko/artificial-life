import typing
from time import sleep
import sqlite3 as sql
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import life
import ast

SCREEN_SIZE = [1800, 900]
MAIN_SIZE = [380, 410]
NEW_MAP_SIZE = [250, 660]
SIZE_IMAGE = 900
RUN_OPEN_BOT_SIZE = [210, 110]
ADD_LEAD_SIZE = [380, 370]
DELETE_SIZE = [750, 370]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(*MAIN_SIZE)
        self.setWindowTitle("Main")

        self.name = QLineEdit(self)
        self.name.resize(360, 30)
        self.name.move(10, 10)
        self.name.textChanged.connect(self.input_text)

        self.table = QListWidget(self)
        self.table.resize(360, 300)
        self.table.move(10, 55)
        self.table.itemClicked.connect(self.play)

        self.button_new = QPushButton(self, text="new")
        self.button_new.resize(80, 30)
        self.button_new.move(10, 370)
        self.button_new.clicked.connect(self.new_map)

        self.button_del = QPushButton(self, text="delete")
        self.button_del.resize(80, 30)
        self.button_del.move(100, 370)
        self.button_del.clicked.connect(self.delete_)

        self.con = sql.connect("db.db")
        self.cur = self.con.cursor()
        self.maps = list(self.cur.execute("SELECT name FROM maps"))
        self.table.clear()
        for e in self.maps:
            self.table.addItem(*e)

    def play(self, item):
        self.con = sql.connect("db.db")
        self.cur = self.con.cursor()

        r = list(*self.cur.execute(f"SELECT * FROM maps WHERE name = '{item.text()}'"))
        life.EDIBILITY = r[1]
        life.VALUE_FOOD = r[2]
        life.SUPERFOOD_MULTIPLIER = r[3]
        life.MAP_SIZE = r[4]
        life.FOOD_SPAWN = r[5]
        life.FOOD_SPAWN_AREAS = None
        life.FOOD_COUNT_SPAWN = r[7]
        life.BOT_SPAWN = r[8]
        life.BOT_SPAWN_AREAS = None
        life.BOT_COUNT_SPAWN = r[10]
        life.POWER_POISON = r[11]
        life.WASTE_LIFE = r[12]
        life.ATTACK_BOT = r[14]
        life.OLD_BOT = r[15]
        life.CHANCE_MUTATE = r[16]

        WinPlayer().exec()

    def new_map(self):
        NewMap(self).exec()
        self.maps = list(self.cur.execute("SELECT name FROM maps"))
        self.table.clear()
        for e in self.maps:
            self.table.addItem(*e)

    def delete_(self):
        Delete().exec()
        self.maps = list(self.cur.execute("SELECT name FROM maps"))
        self.table.clear()
        for e in self.maps:
            self.table.addItem(*e)

    def input_text(self):
        result = list(self.cur.execute(f"SELECT name FROM maps WHERE name LIKE '{self.name.text()}%'"))
        self.table.clear()
        for e in result:
            self.table.addItem(*e)


class Delete(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(*DELETE_SIZE)
        self.setWindowTitle("Delete")

        self.name1 = QLineEdit(self)
        self.name1.resize(360, 30)
        self.name1.move(10, 10)
        self.name1.textChanged.connect(self.input_text1)

        self.table1 = QListWidget(self)
        self.table1.resize(360, 300)
        self.table1.move(10, 55)
        self.table1.itemClicked.connect(self.click1)

        self.name2 = QLineEdit(self)
        self.name2.resize(360, 30)
        self.name2.move(380, 10)
        self.name2.textChanged.connect(self.input_text2)

        self.table2 = QListWidget(self)
        self.table2.resize(360, 300)
        self.table2.move(380, 55)
        self.table2.itemClicked.connect(self.click2)

        self.con = sql.connect("db.db")
        self.cur = self.con.cursor()

        self.maps = list(self.cur.execute("SELECT name FROM maps"))
        self.table1.clear()
        for e in self.maps:
            self.table1.addItem(*e)

        self.bots = list(self.cur.execute("SELECT name, score, color FROM bots"))
        self.table2.clear()
        for e in self.bots:
            item = QListWidgetItem(f"{e[0]} {e[1]}")
            item.setBackground(QColor(*ast.literal_eval(e[2])))
            self.table2.addItem(item)

    def input_text1(self, s):
        self.maps = list(self.cur.execute(f"SELECT name FROM maps WHERE name LIKE '{s}%'"))
        self.table1.clear()
        for e in self.maps:
            self.table1.addItem(*e)

    def click1(self, item):
        self.cur.execute(f"DELETE FROM maps WHERE name = '{item.text()}'")
        self.input_text1("")

        self.con.commit()

    def input_text2(self, s):
        self.bots = list(self.cur.execute(f"SELECT name, score, color FROM bots WHERE name LIKE '{s}%'"))
        self.table2.clear()
        for e in self.bots:
            item = QListWidgetItem(f"{e[0]} {e[1]}")
            item.setBackground(QColor(*ast.literal_eval(e[2])))
            self.table2.addItem(item)

    def click2(self, item):
        r = item.text().split()
        name = r[0]
        self.cur.execute(f"DELETE FROM bots WHERE name = '{name}'")
        self.input_text2("")

        self.con.commit()


class NewMap(QDialog):
    def __init__(self, main: MainWindow):
        self.main = main
        super().__init__()
        self.resize(*NEW_MAP_SIZE)
        self.setWindowTitle("New Map")
        self.con = sql.connect("db.db")
        self.cur = self.con.cursor()

        self.EDIBILITYtext_ = QLabel(self, text="EDIBILITY")
        self.EDIBILITYtext_.resize(160, 30)
        self.EDIBILITYtext_.move(10, 10)
        self.EDIBILITY_ = QLineEdit(self)
        self.EDIBILITY_.resize(60, 30)
        self.EDIBILITY_.move(180, 10)

        self.VALUE_FOODtext_ = QLabel(self, text="VALUE_FOOD")
        self.VALUE_FOODtext_.resize(160, 30)
        self.VALUE_FOODtext_.move(10, 50)
        self.VALUE_FOOD_ = QLineEdit(self)
        self.VALUE_FOOD_.resize(60, 30)
        self.VALUE_FOOD_.move(180, 50)

        self.SUPERFOOD_MULTIPLIERtext_ = QLabel(self, text="SUPERFOOD_MULTIPLIER")
        self.SUPERFOOD_MULTIPLIERtext_.resize(160, 30)
        self.SUPERFOOD_MULTIPLIERtext_.move(10, 90)
        self.SUPERFOOD_MULTIPLIER_ = QLineEdit(self)
        self.SUPERFOOD_MULTIPLIER_.resize(60, 30)
        self.SUPERFOOD_MULTIPLIER_.move(180, 90)

        self.MAP_SIZEtext_ = QLabel(self, text="MAP_SIZE")
        self.MAP_SIZEtext_.resize(160, 30)
        self.MAP_SIZEtext_.move(10, 130)
        self.MAP_SIZE_ = QLineEdit(self)
        self.MAP_SIZE_.resize(60, 30)
        self.MAP_SIZE_.move(180, 130)

        self.FOOD_SPAWNtext_ = QLabel(self, text="FOOD_SPAWN")
        self.FOOD_SPAWNtext_.resize(160, 30)
        self.FOOD_SPAWNtext_.move(10, 170)
        self.FOOD_SPAWN_ = QLineEdit(self)
        self.FOOD_SPAWN_.resize(60, 30)
        self.FOOD_SPAWN_.move(180, 170)

        self.FOOD_SPAWN_AREAStext_ = QLabel(self, text="FOOD_SPAWN_AREAS")
        self.FOOD_SPAWN_AREAStext_.resize(160, 30)
        self.FOOD_SPAWN_AREAStext_.move(10, 210)
        self.FOOD_SPAWN_AREAS_ = QLineEdit(self)
        self.FOOD_SPAWN_AREAS_.resize(60, 30)
        self.FOOD_SPAWN_AREAS_.move(180, 210)

        self.FOOD_SPAWN_AREAS_.setEnabled(False)

        self.FOOD_COUNT_SPAWNtext_ = QLabel(self, text="FOOD_COUNT_SPAWN")
        self.FOOD_COUNT_SPAWNtext_.resize(160, 30)
        self.FOOD_COUNT_SPAWNtext_.move(10, 250)
        self.FOOD_COUNT_SPAWN_ = QLineEdit(self)
        self.FOOD_COUNT_SPAWN_.resize(60, 30)
        self.FOOD_COUNT_SPAWN_.move(180, 250)

        self.BOT_SPAWNtext_ = QLabel(self, text="BOT_SPAWN")
        self.BOT_SPAWNtext_.resize(160, 30)
        self.BOT_SPAWNtext_.move(10, 290)
        self.BOT_SPAWN_ = QLineEdit(self)
        self.BOT_SPAWN_.resize(60, 30)
        self.BOT_SPAWN_.move(180, 290)

        self.BOT_SPAWN_AREAStext_ = QLabel(self, text="BOT_SPAWN_AREAS")
        self.BOT_SPAWN_AREAStext_.resize(160, 30)
        self.BOT_SPAWN_AREAStext_.move(10, 330)
        self.BOT_SPAWN_AREAS_ = QLineEdit(self)
        self.BOT_SPAWN_AREAS_.resize(60, 30)
        self.BOT_SPAWN_AREAS_.move(180, 330)

        self.BOT_SPAWN_AREAS_.setEnabled(False)

        self.BOT_COUNT_SPAWNStext_ = QLabel(self, text="BOT_COUNT_SPAWN")
        self.BOT_COUNT_SPAWNStext_.resize(160, 30)
        self.BOT_COUNT_SPAWNStext_.move(10, 370)
        self.BOT_COUNT_SPAWNS_ = QLineEdit(self)
        self.BOT_COUNT_SPAWNS_.resize(60, 30)
        self.BOT_COUNT_SPAWNS_.move(180, 370)

        self.ATTACK_BOTStext_ = QLabel(self, text="ATTACK_BOT")
        self.ATTACK_BOTStext_.resize(160, 30)
        self.ATTACK_BOTStext_.move(10, 410)
        self.ATTACK_BOT_ = QLineEdit(self)
        self.ATTACK_BOT_.resize(60, 30)
        self.ATTACK_BOT_.move(180, 410)

        self.OLD_BOTtext_ = QLabel(self, text="OLD_BOT")
        self.OLD_BOTtext_.resize(160, 30)
        self.OLD_BOTtext_.move(10, 450)
        self.OLD_BOT_ = QLineEdit(self)
        self.OLD_BOT_.resize(60, 30)
        self.OLD_BOT_.move(180, 450)

        self.CHANCE_MUTATEtext_ = QLabel(self, text="CHANCE_MUTATE")
        self.CHANCE_MUTATEtext_.resize(160, 30)
        self.CHANCE_MUTATEtext_.move(10, 490)
        self.CHANCE_MUTATE_ = QLineEdit(self)
        self.CHANCE_MUTATE_.resize(60, 30)
        self.CHANCE_MUTATE_.move(180, 490)

        self.POWER_POISONtext_ = QLabel(self, text="POWER_POISON")
        self.POWER_POISONtext_.resize(160, 30)
        self.POWER_POISONtext_.move(10, 530)
        self.POWER_POISON_ = QLineEdit(self)
        self.POWER_POISON_.resize(60, 30)
        self.POWER_POISON_.move(180, 530)

        self.WASTE_LIFEtext_ = QLabel(self, text="WASTE_LIFE")
        self.WASTE_LIFEtext_.resize(160, 30)
        self.WASTE_LIFEtext_.move(10, 570)
        self.WASTE_LIFE_ = QLineEdit(self)
        self.WASTE_LIFE_.resize(60, 30)
        self.WASTE_LIFE_.move(180, 570)

        self.name_ = QLineEdit(self)
        self.name_.resize(100, 30)
        self.name_.move(10, 620)

        self.button_save = QPushButton(self, text="save")
        self.button_save.resize(70, 30)
        self.button_save.move(120, 620)
        self.button_save.clicked.connect(self.save_)

    def save_(self):
        params = (int(self.EDIBILITY_.text()), int(self.VALUE_FOOD_.text()), int(self.SUPERFOOD_MULTIPLIER_.text()),
                  int(self.MAP_SIZE_.text()), int(self.FOOD_SPAWN_.text()),
                  str(str(self.FOOD_SPAWN_AREAS_.text()) if self.FOOD_SPAWN_AREAS_.text() != "" else 'None'),
                  int(self.FOOD_COUNT_SPAWN_.text()), int(self.BOT_SPAWN_.text()),
                  str(self.BOT_SPAWN_AREAS_.text()) if self.BOT_SPAWN_AREAS_.text() != "" else 'None',
                  int(self.BOT_COUNT_SPAWNS_.text()), int(self.POWER_POISON_.text()), int(self.WASTE_LIFE_.text()),
                  self.name_.text(), int(self.ATTACK_BOT_.text()), int(self.OLD_BOT_.text()),
                  int(self.CHANCE_MUTATE_.text()))
        self.cur.execute(
            f"""INSERT INTO maps(EDIBILITY, VALUE_FOOD, SUPERFOOD_MULTIPLIER, MAP_SIZE, FOOD_SPAWN, FOOD_SPAWN_AREAS, FOOD_COUNT_SPAWN, BOT_SPAWN, BOT_SPAWN_AREAS, BOT_COUNT_SPAWN, POWER_POISON, WASTE_LIFE, name, ATTACK_BOT, OLD_BOT, CHANCE_MUTATE) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            params)
        self.con.commit()

        self.close()


class WinPlayer(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(*SCREEN_SIZE)
        self.setWindowTitle("Run")
        self.map_ = life.Map()

        self.button_stop = QPushButton(self, text="stop")
        self.button_stop.resize(60, 25)
        self.button_stop.move(SIZE_IMAGE + 5, 5)
        self.button_stop.clicked.connect(self.stop_timer)
        self.button_stop.show()

        self.button_start = QPushButton(self, text="start")
        self.button_start.resize(60, 25)
        self.button_start.move(SIZE_IMAGE + 5, 35)
        self.button_start.clicked.connect(self.start_timer)
        self.button_start.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(self.step_)
        self.timer.timeout.connect(self.set_time)
        self.timer.timeout.connect(self.update_bot_list)
        self.timer_s = 15

        self.time_ = QLabel(self, text="0")
        self.time_.resize(120, 30)
        self.time_.move(SIZE_IMAGE + 5, SCREEN_SIZE[1] - 25)

        self.bot_list = QListWidget(self)
        self.bot_list.resize(360, SCREEN_SIZE[1] - 20)
        self.bot_list.move(SCREEN_SIZE[0] - 380, 10)
        self.bot_list.itemClicked.connect(self.open_bot)

        self.infor_text = QLabel(self, text="information")
        self.infor_text.resize(140, 20)
        self.infor_text.move(SIZE_IMAGE + 10, 70)

        self.EDIBILITY_ = QLabel(self, text=f"EDIBILITY: {life.EDIBILITY}")
        self.EDIBILITY_.resize(140, 20)
        self.EDIBILITY_.move(SIZE_IMAGE + 10, 90)

        self.VALUE_FOOD_ = QLabel(self, text=f"VALUE_FOOD: {life.VALUE_FOOD}")
        self.VALUE_FOOD_.resize(140, 20)
        self.VALUE_FOOD_.move(SIZE_IMAGE + 10, 110)

        self.SUPERFOOD_MULTIPLIER_ = QLabel(self, text=f"SUPERFOOD_MULTIPLIER: {life.SUPERFOOD_MULTIPLIER}")
        self.SUPERFOOD_MULTIPLIER_.resize(140, 20)
        self.SUPERFOOD_MULTIPLIER_.move(SIZE_IMAGE + 10, 130)

        self.MAP_SIZE_ = QLabel(self, text=f"MAP_SIZE: {life.MAP_SIZE}")
        self.MAP_SIZE_.resize(140, 20)
        self.MAP_SIZE_.move(SIZE_IMAGE + 10, 150)

        self.FOOD_SPAWN_ = QLabel(self, text=f"FOOD_SPAWN: {life.FOOD_SPAWN}")
        self.FOOD_SPAWN_.resize(140, 20)
        self.FOOD_SPAWN_.move(SIZE_IMAGE + 10, 170)

        self.FOOD_SPAWN_AREAS_ = QLabel(self, text=f"FOOD_SPAWN_AREAS: {life.FOOD_SPAWN_AREAS}")
        self.FOOD_SPAWN_AREAS_.resize(140, 20)
        self.FOOD_SPAWN_AREAS_.move(SIZE_IMAGE + 10, 190)

        self.FOOD_COUNT_SPAWN_ = QLabel(self, text=f"FOOD_COUNT_SPAWN: {life.FOOD_COUNT_SPAWN}")
        self.FOOD_COUNT_SPAWN_.resize(140, 20)
        self.FOOD_COUNT_SPAWN_.move(SIZE_IMAGE + 10, 210)

        self.BOT_SPAWN_ = QLabel(self, text=f"BOT_SPAWN: {life.BOT_SPAWN}")
        self.BOT_SPAWN_.resize(140, 20)
        self.BOT_SPAWN_.move(SIZE_IMAGE + 10, 230)

        self.BOT_SPAWN_AREAS_ = QLabel(self, text=f"BOT_SPAWN_AREAS: {life.BOT_SPAWN_AREAS}")
        self.BOT_SPAWN_AREAS_.resize(140, 20)
        self.BOT_SPAWN_AREAS_.move(SIZE_IMAGE + 10, 250)

        self.BOT_COUNT_SPAWN_ = QLabel(self, text=f"BOT_COUNT_SPAWN: {life.BOT_COUNT_SPAWN}")
        self.BOT_COUNT_SPAWN_.resize(140, 20)
        self.BOT_COUNT_SPAWN_.move(SIZE_IMAGE + 10, 270)

        self.POWER_POISON_ = QLabel(self, text=f"POWER_POISON: {life.POWER_POISON}")
        self.POWER_POISON_.resize(140, 20)
        self.POWER_POISON_.move(SIZE_IMAGE + 10, 290)

        self.WASTE_LIFE_ = QLabel(self, text=f"POWER_POISON: {life.WASTE_LIFE}")
        self.WASTE_LIFE_.resize(140, 20)
        self.WASTE_LIFE_.move(SIZE_IMAGE + 10, 310)

        self.CHANCE_MUTATE_ = QLabel(self, text=f"CHANCE_MUTATE: {life.CHANCE_MUTATE}")
        self.CHANCE_MUTATE_.resize(140, 20)
        self.CHANCE_MUTATE_.move(SIZE_IMAGE + 10, 330)

        self.HP_BOT_ = QLabel(self, text=f"HP_BOT: {life.HP_BOT}")
        self.HP_BOT_.resize(140, 20)
        self.HP_BOT_.move(SIZE_IMAGE + 10, 350)

        self.ATTACK_BOT_ = QLabel(self, text=f"ATTACK_BOT: {life.ATTACK_BOT}")
        self.ATTACK_BOT_.resize(140, 20)
        self.ATTACK_BOT_.move(SIZE_IMAGE + 10, 370)

        self.OLD_BOT_ = QLabel(self, text=f"OLD_BOT: {life.OLD_BOT}")
        self.OLD_BOT_.resize(140, 20)
        self.OLD_BOT_.move(SIZE_IMAGE + 10, 390)

        self.UNMOUNTING_BOT_ = QLabel(self, text=f"UNMOUNTING_BOT: {life.UNMOUNTING_BOT}")
        self.UNMOUNTING_BOT_.resize(140, 20)
        self.UNMOUNTING_BOT_.move(SIZE_IMAGE + 10, 410)

        self.slider = QSlider(Qt.Horizontal, parent=self)
        self.slider.resize(120, 40)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setMaximum(500)
        self.slider.setMinimum(0)
        self.slider.setTickInterval(50)
        self.slider.setSingleStep(100)
        self.slider.setValue(500)
        self.slider.move(SIZE_IMAGE + 80, 5)
        self.slider.actionTriggered.connect(self.slider_)

        self.leads_ = QListWidget(self)
        self.leads_.resize(180, 200)
        self.leads_.move(SCREEN_SIZE[0] - 570, 10)
        self.leads_.setEnabled(False)
        self.leads_.itemClicked.connect(self.click_item_leads_)

        self.button_add_leads = QPushButton(self, text="add leader")
        self.button_add_leads.resize(80, 30)
        self.button_add_leads.move(SCREEN_SIZE[0] - 570, 220)
        self.button_add_leads.clicked.connect(self.add_lead)
        self.button_add_leads.setEnabled(False)

        self.check_is_leads = QCheckBox(self)
        self.check_is_leads.resize(40, 30)
        self.check_is_leads.move(SCREEN_SIZE[0] - 400, 220)
        self.check_is_leads.setChecked(False)
        self.check_is_leads.clicked.connect(self.click_check_is_leads)

        self.stop_timer()

    def click_item_leads_(self, item):
        r = item.text().split()
        self.map_.del_leads(r[0], int(r[1]))
        self.update_leads_()

    def step_(self):
        self.map_.step(is_leads=self.check_is_leads.isChecked())

    def click_check_is_leads(self):
        if self.check_is_leads.isChecked():
            self.button_add_leads.setEnabled(True)
            self.leads_.setEnabled(True)
        else:
            self.button_add_leads.setEnabled(False)
            self.leads_.setEnabled(False)

    def update_leads_(self):
        self.leads_.clear()
        for el in self.map_.leads:
            item = QListWidgetItem(f"{el.name}\t{el.score}")
            item.setBackground(QColor(*el.color))
            self.leads_.addItem(item)

    def add_lead(self):
        AddLead(self.map_).exec()
        self.update_leads_()

    def open_bot(self, item):
        if self.timer.isActive():
            return
        r = item.text().split(": ")
        hp = int(r[-3][:-2])
        score = int(r[-4][:-3])
        y = int(r[-1])
        x = int(r[-2][:-2])
        if self.map_.field[x][y].__class__.__name__ != "Bot":
            for bot_ in self.map_.bots:
                if bot_.x == x and bot_.y == y and bot_.score == score and bot_.hp == hp:
                    RunOpenBot(bot_).exec()
                    break
        else:
            if self.map_.field[x][y].score == score and self.map_.field[x][y].hp == hp:
                bot = self.map_.field[x][y]
                RunOpenBot(bot).exec()
            else:
                for bot_ in self.map_.bots:
                    if bot_.x == x and bot_.y == y and bot_.score == score and bot_.hp == hp:
                        RunOpenBot(bot_).exec()
                        break

    def update_bot_list(self):
        self.bot_list.clear()
        for bot in self.map_.bots[::-1]:
            elem = QListWidgetItem(f"score: {bot.score}\thp: {bot.hp}\tx: {bot.x} y: {bot.y}")
            elem.setBackground(QColor(*bot.color))
            self.bot_list.addItem(elem)

    def slider_(self):
        self.timer_s = 500 - self.slider.value()
        if self.timer.isActive():
            self.timer.start(self.timer_s)

    def stop_timer(self):
        self.button_stop.setStyleSheet("background-color:rgb(100,100,100)")
        self.button_start.setStyleSheet("background-color:rgb(0,150,0)")
        self.button_start.setEnabled(True)
        self.button_stop.setEnabled(False)

        if self.check_is_leads.isChecked():
            self.leads_.setEnabled(True)
            self.button_add_leads.setEnabled(True)
        self.check_is_leads.setEnabled(True)

        self.timer.stop()

    def set_time(self):
        self.time_.setText("Time: " + str(self.map_.time))

    def start_timer(self):
        self.button_stop.setStyleSheet("background-color:rgb(0,150,0)")
        self.button_start.setStyleSheet("background-color:rgb(100,100,100)")
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)

        self.button_add_leads.setEnabled(False)
        self.leads_.setEnabled(False)
        self.check_is_leads.setEnabled(False)

        self.timer.start(self.timer_s)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_map(qp)
        qp.end()

    def draw_map(self, qp):

        rect = [SIZE_IMAGE // len(self.map_.field), SIZE_IMAGE // len(self.map_.field[0])]
        a = 0
        for line in self.map_.field:
            b = 0
            for el in line:
                if str(el.__class__.__name__) == "Point":
                    qp.setBrush(QColor(255, 255, 255))
                elif str(el.__class__.__name__) == "Bot":
                    qp.setBrush(QColor(*el.color))
                elif str(el.__class__.__name__) == "Food":
                    qp.setBrush(QColor(0, 180, 0))
                elif str(el.__class__.__name__) == "SuperFood":
                    qp.setBrush(QColor(0, 140, 50))
                elif str(el.__class__.__name__) == "Wall":
                    qp.setBrush(QColor(0, 0, 0))
                elif str(el.__class__.__name__) == "Waste":
                    qp.setBrush(QColor(255, 180, 0))
                qp.drawRect(b, a, rect[0], rect[1])
                b += rect[1]
            a += rect[0]


class AddLead(QDialog):
    def __init__(self, map_: life.Map):
        super().__init__()
        self.resize(*ADD_LEAD_SIZE)
        self.setWindowTitle("Add Lead")
        self.map_ = map_

        self.con = sql.connect("db.db")
        self.cur = self.con.cursor()

        self.name = QLineEdit(self)
        self.name.resize(360, 30)
        self.name.move(10, 10)
        self.name.textChanged.connect(self.input_text)

        self.table = QListWidget(self)
        self.table.resize(360, 300)
        self.table.move(10, 55)
        self.table.itemClicked.connect(self.add_lead)

        self.bots = list(self.cur.execute("SELECT * FROM bots"))
        for bot_ in self.bots:
            item = QListWidgetItem(f"{bot_[1]}\t{bot_[2]}")
            item.setBackground(QColor(*ast.literal_eval(bot_[-1])))
            self.table.addItem(item)

    def input_text(self):
        self.table.clear()
        bots = list(self.cur.execute(f"SELECT * FROM bots WHERE name LIKE '{self.name.text()}%'"))
        for bot_ in bots:
            item = QListWidgetItem(f"{bot_[1]}\t{bot_[2]}")
            item.setBackground(QColor(*ast.literal_eval(bot_[-1])))
            self.table.addItem(item)

    def add_lead(self, item):
        name = item.text().split()[0]
        bot = list(self.cur.execute(f"SELECT * FROM bots WHERE name = '{name}'"))[0]
        self.map_.add_leads(bot[1], ast.literal_eval(bot[-2]), ast.literal_eval(bot[-1]), int(bot[2]))
        self.close()


class RunOpenBot(QDialog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.resize(*RUN_OPEN_BOT_SIZE)
        self.setWindowTitle("Bot")
        self.con = sql.connect("db.db")
        self.cur = self.con.cursor()

        self.color_bot = QPushButton(self, text="")
        self.color_bot.setEnabled(False)
        self.color_bot.resize(60, 60)
        self.color_bot.move(5, 5)
        self.color_bot.setStyleSheet(f"background-color:rgb({bot.color[0]},{bot.color[1]},{bot.color[2]})")

        self.score_ = QLabel(self, text=f"score: {bot.score}")
        self.score_.setFont(QFont("Times", 20))
        self.score_.resize(180, 30)
        self.score_.move(70, 17)

        self.name = QLineEdit(self)
        self.name.resize(130, 30)
        self.name.move(5, 70)

        self.button_save = QPushButton(self, text="save")
        self.button_save.resize(60, 30)
        self.button_save.move(140, 70)
        self.button_save.clicked.connect(self.save_)

    def save_(self):
        params = (str(self.name.text()), int(self.bot.score), str(self.bot.chromosome), str(self.bot.color))
        self.cur.execute("""INSERT INTO bots(name, score, chromosome, color) VALUES (?,?,?,?)""", params)
        self.con.commit()
        self.close()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
