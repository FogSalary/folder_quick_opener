import os
import sys
from ConfigHandler import ConfigHandler
from PyQt5.QtWidgets import QApplication, QWidget, QStatusBar, QLabel, QVBoxLayout, QFileDialog
from Ui_opener import Ui_Form


class Opener(QWidget, Ui_Form):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setup_ui()
        self.setup_widget_connect()

    def setup_ui(self):
        self.ini_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.inicfg = ConfigHandler(self.ini_path)
        self.user_cfg_path = self.inicfg.get_value('settings', 'name')
        self.cfg = ConfigHandler(self.user_cfg_path)

        self.setWindowTitle('Opener')
        self.status_bar = QStatusBar()  # 创建状态栏
        self.layout = QVBoxLayout()     # 创建竖直布局
        self.layout.addWidget(self.frame)  # 添加控件到布局
        self.layout.addWidget(self.status_bar)  # 添加状态栏到布局底部
        self.setLayout(self.layout)     # 设置布局
        self.layout.setStretch(0, 5)    # 设置 frame 占 5 份
        self.layout.setStretch(0, 1)    # 设置 frame 占 1 份
        self.status_bar.showMessage('Current Config ini: %s' % os.path.basename(self.user_cfg_path))  # 更新状态栏上的消息

        if self.radiobtn_localhost.isChecked():
            self.lineEdit_remote_ip.setDisabled(True)
        else:
            self.lineEdit_remote_ip.setDisabled(False)

        ip_str = self.cfg.get_value('info', 'ip_address')
        if ip_str == 'localhost':
            self.radiobtn_localhost.setChecked(True)
        else:
            self.radiobtn_remote.setChecked(True)
            self.lineEdit_remote_ip.setText(ip_str)
        self.cbBox_folder_name.addItems(self.cfg.get_options('folder_path'))
        curr_folder_name = self.cbBox_folder_name.currentText()
        self.lineEdit_folder_name.setText(curr_folder_name)
        self.lineEdit_folder_path.setText(self.cfg.get_value('folder_path', "%s" % curr_folder_name))
        self.cbBox_folder_name.setEditable(True)

    def reset_ui(self):
        pass

    def setup_widget_connect(self):
        self.btn_add.clicked.connect(self.on_btn_add_clicked_slot)
        self.btn_del.clicked.connect(self.on_btn_del_clicked_slot)
        self.btn_open.clicked.connect(self.on_btn_open_clicked_slot)
        self.btn_modify.clicked.connect(self.on_btn_modify_clicked_slot)
        self.btn_load_cfg.clicked.connect(self.on_btn_load_cfg_clicked_slot)
        self.radiobtn_localhost.clicked.connect(self.on_radiobtn_clicked_slot)
        self.radiobtn_remote.clicked.connect(self.on_radiobtn_clicked_slot)
        self.cbBox_folder_name.currentTextChanged.connect(self.on_cbBox_folder_name_currentTextChanged_slot)

    def on_btn_add_clicked_slot(self):
        folder_name = self.lineEdit_folder_name.text()
        folder_path = self.lineEdit_folder_path.text()
        self.cfg.add_items('folder_path', folder_name, folder_path)
        self.update_cbBox_folder_name_items()

    def on_btn_del_clicked_slot(self):
        folder_name = self.lineEdit_folder_name.text()
        self.cfg.remove_option('folder_path', folder_name)
        self.update_cbBox_folder_name_items()

    def on_btn_open_clicked_slot(self):
        folder_path = self.lineEdit_folder_path.text()
        os.startfile(folder_path)

    def on_btn_modify_clicked_slot(self):
        curr_folder_name = self.cbBox_folder_name.currentText()
        new_folder_name = self.lineEdit_folder_name.text()
        self.cfg.update_option('folder_path', curr_folder_name, new_folder_name)
    
    def on_btn_load_cfg_clicked_slot(self):
        self.user_cfg_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Config FIle (*.ini);;All Files (*)")
        self.status_bar.showMessage('Current Config ini: %s' % os.path.basename(self.user_cfg_path))
        self.cfg.read(self.user_cfg_path)
        self.update_cbBox_folder_name_items()
        print(self.cfg.get_options('folder_path'))

    def on_radiobtn_clicked_slot(self):
        radio_btn = self.sender()
        if radio_btn.isChecked():
            # print(radio_btn.objectName())
            # print(radio_btn.text())
            # print(radio_btn.isChecked())
            # print(radio_btn.property())
            # print(radio_btn.pos())
            # print(self.radiobtn_remote == self.sender())
            if radio_btn.objectName() == 'radiobtn_remote':
                self.lineEdit_remote_ip.setDisabled(False)
            elif radio_btn.objectName() == 'radiobtn_localhost':
                self.lineEdit_remote_ip.setDisabled(True)

    def on_cbBox_folder_name_currentTextChanged_slot(self):
        folder_name = self.cbBox_folder_name.currentText()
        if folder_name == '':
            return
        self.lineEdit_folder_name.setText(folder_name)
        self.lineEdit_folder_path.setText(self.cfg.get_value('folder_path', folder_name))

    def update_cbBox_folder_name_items(self):
        self.cbBox_folder_name.clear()
        self.lineEdit_folder_name.clear()
        self.lineEdit_folder_path.clear()
        self.cbBox_folder_name.addItems(self.cfg.get_options('folder_path'))






if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Opener()
    w.show()
    sys.exit(app.exec_())