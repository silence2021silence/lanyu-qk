# -*- coding=utf-8 -*-
"""
Time:        2024/01/02 22:00
Version:     V 0.0.1
File:        lanyu-qk.py
Describe:
Author:      Lanyu
E-Mail:      silence2021silence@163.com
Blog link:   https://www.geeklanyu.com/
Github link: https://github.com/silence2021silence/
Gitee link:  https://gitee.com/silence2021silence/
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from PyQt5.Qt import *
import sys


def radioButtonsEven1():
    global mode
    if radioButton1.isChecked():
        textEdit1.setEnabled(True)
        radioButton3.setDisabled(True)
        radioButton4.setDisabled(True)
        radioButton5.setDisabled(True)
        radioButton6.setDisabled(True)
        checkBox1.setDisabled(True)
        checkBox2.setDisabled(True)
        checkBox3.setDisabled(True)
        checkBox4.setDisabled(True)
        checkBox5.setDisabled(True)
        mode = 0
    elif radioButton2.isChecked():
        textEdit1.setDisabled(True)
        radioButton3.setEnabled(True)
        radioButton4.setEnabled(True)
        radioButton5.setEnabled(True)
        radioButton6.setEnabled(True)
        checkBox1.setEnabled(True)
        checkBox2.setEnabled(True)
        checkBox3.setEnabled(True)
        checkBox4.setEnabled(True)
        checkBox5.setEnabled(True)
        mode = 1


def radioButtonsEven2():
    global course_type
    if radioButton3.isChecked():
        course_type = "全部"
    elif radioButton4.isChecked():
        course_type = "公共必修课"
    elif radioButton5.isChecked():
        course_type = "专业选修课"
    elif radioButton6.isChecked():
        course_type = "公共选修课"


def pushButtonEven():
    global course_id
    global ticked
    global sleep_time
    course_id = textEdit1.toPlainText()
    ticked = [int(checkBox1.checkState()), checkBox2.checkState(), checkBox3.checkState(), checkBox4.checkState(), checkBox5.checkState()]
    try:
        sleep_time = float(textEdit2.toPlainText())
    except ValueError:
        QMessageBox.warning(window, "Lanyu-QK", "网页刷新速度不能为空", QMessageBox.Ok)
    else:
        i = 5
        while i > 0:
            if ticked[0] == 2:
                ticked[0] = "隐藏时间冲突"
            elif ticked[1] == 2:
                ticked[1] = "隐藏已选满"
            elif ticked[2] == 2:
                ticked[2] = "隐藏已选"
            elif ticked[3] == 2:
                ticked[3] = "隐藏已修读"
            elif ticked[4] == 2:
                ticked[4] = "隐藏不在修读范围"
            i -= 1
        try:
            mode
        except NameError:
            QMessageBox.warning(window, "Lanyu-QK", "选择抢课模式", QMessageBox.Ok)
        else:
            if mode == 0:
                if course_id != "":
                    try:
                        course_id = [int(i) for i in course_id.split(";")]
                    except ValueError:
                        QMessageBox.warning(window, "Lanyu-QK", "课程id格式错误", QMessageBox.Ok)
                    else:
                        main()
                else:
                    QMessageBox.warning(window, "Lanyu-QK", "课程id不能为空", QMessageBox.Ok)
            elif mode == 1:
                try:
                    course_type
                except NameError:
                    QMessageBox.warning(window, "Lanyu-QK", "选择课程类型", QMessageBox.Ok)
                else:
                    main()


def click(xpath):
    n = 0
    while True:
        try:
            driver.find_element(By.XPATH, value=xpath).click()
        except:
            time.sleep(0.1)
            if n == 10:
                break
            n += 1
        else:
            break


def main():
    QMessageBox.warning(window, "Lanyu-QK",
                        "稍后会自动弹出Edge浏览器，并且留意接下来的另一个弹窗提示。",
                        QMessageBox.Ok)
    driver = webdriver.Edge()
    driver.get("https://sc.zhjpec.edu.cn")
    QMessageBox.warning(window, "Lanyu-QK",
                        "在弹出的浏览器里自行登录账号，进入选课界面，完成以上步骤后再点击确定(OK)",
                        QMessageBox.Ok)
    if mode == 0:
        while True:
            time.sleep(sleep_time)
            for i in course_id:
                driver.refresh()
                driver.find_element(By.XPATH, '//span[text()="更多条件"]').click()
                driver.find_element(By.XPATH, '//input[@placeholder="请输入教学班号"]').send_keys(i)
                driver.find_element(By.XPATH,
                                    '//div[@class="action-row el-row el-row--flex"]//span[text()="查询"]').click()
                time.sleep(sleep_time)
                click('//button[@class="el-button large-action el-button--primary"]')
    elif mode == 1:
        while True:
            driver.refresh()
            time.sleep(sleep_time)
            driver.find_element(By.XPATH, '//div[text()="%s"]' % course_type).click()
            for i in ticked:
                time.sleep(sleep_time)
                if i != 0:
                    driver.find_element(By.XPATH, '//span[text()="%s"]' % i).click()
            click('//button[@class="el-button large-action el-button--primary"]')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Lanyu-QK")
    window.resize(400, 550)
    window.move(760, 340)

    label1 = QLabel(window)
    label1.setText("-> 选择抢课模式:")
    label1.move(20, 20)

    radioButton1 = QRadioButton(window)
    radioButton1.setText("精准抢课")
    radioButton1.move(20, 40)
    radioButton1.toggled.connect(radioButtonsEven1)

    radioButton2 = QRadioButton(window)
    radioButton2.setText("随机抢课")
    radioButton2.move(180, 40)
    radioButton2.toggled.connect(radioButtonsEven1)

    buttonGroup1 = QButtonGroup(window)
    buttonGroup1.addButton(radioButton1)
    buttonGroup1.addButton(radioButton2)

    label2 = QLabel(window)
    label2.setText("-> 输入课程id(多个id用英文分行(;)分隔):")
    label2.move(20, 100)

    textEdit1 = QTextEdit(window)
    textEdit1.setGeometry(20, 120, 300, 50)

    label3 = QLabel(window)
    label3.setText("-> 筛选条件:")
    label3.move(20, 180)

    radioButton3 = QRadioButton(window)
    radioButton3.setText("全部")
    radioButton3.move(20, 200)
    radioButton3.toggled.connect(radioButtonsEven2)

    radioButton4 = QRadioButton(window)
    radioButton4.setText("公共必修课")
    radioButton4.move(180, 200)
    radioButton4.toggled.connect(radioButtonsEven2)

    radioButton5 = QRadioButton(window)
    radioButton5.setText("专业选修课")
    radioButton5.move(20, 220)
    radioButton5.toggled.connect(radioButtonsEven2)

    radioButton6 = QRadioButton(window)
    radioButton6.setText("公共选修课")
    radioButton6.move(180, 220)
    radioButton6.toggled.connect(radioButtonsEven2)

    buttonGroup2 = QButtonGroup(window)
    buttonGroup2.addButton(radioButton3)
    buttonGroup2.addButton(radioButton4)
    buttonGroup2.addButton(radioButton5)
    buttonGroup2.addButton(radioButton6)

    checkBox1 = QCheckBox(window)
    checkBox1.setText("隐藏时间冲突")
    checkBox1.move(20, 240)

    checkBox2 = QCheckBox(window)
    checkBox2.setText("隐藏已选满")
    checkBox2.move(180, 240)

    checkBox3 = QCheckBox(window)
    checkBox3.setText("隐藏已选")
    checkBox3.move(20, 260)

    checkBox4 = QCheckBox(window)
    checkBox4.setText("隐藏已修读")
    checkBox4.move(180, 260)

    checkBox5 = QCheckBox(window)
    checkBox5.setText("隐藏不在修读范围")
    checkBox5.move(20, 280)

    label4 = QLabel(window)
    label4.setText("-> 网页刷新速度(秒)\n(建议0.5或者1，出现卡顿闪退尝试1.5或者更大数值):")
    label4.move(20, 320)

    textEdit2 = QTextEdit(window)
    textEdit2.setGeometry(20, 360, 60, 30)

    pushButton1 = QPushButton(window)
    pushButton1.setText("启动！")
    pushButton1.move(150, 400)
    pushButton1.clicked.connect(pushButtonEven)

    label5 = QLabel(window)
    label5.setText("-> 蓝鱼抢课工具(幼专特供版)\n-> 本程序已由作者[极客蓝鱼]开源于GitHub\n-> 禁止用于商业用途\n-> 技术支持or问题反馈\n-> 前往微信公众号[极客蓝鱼]")
    label5.move(20, 450)

    window.show()
    QMessageBox.warning(window, "Lanyu-QK", "-> 蓝鱼抢课工具(幼专特供版)\n-> 本程序已由作者[极客蓝鱼]开源于GitHub\n-> 禁止用于商业用途\n-> 技术支持or问题反馈\n-> 前往微信公众号[极客蓝鱼]", QMessageBox.Ok)
    sys.exit(app.exec_())

