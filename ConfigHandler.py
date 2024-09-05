import configparser


class ConfigHandler:
    def __init__(self, ini_path: str) -> None:
        self.ini_path = ini_path
        self.config = configparser.ConfigParser()
        self.config.read(ini_path, encoding='utf-8-sig')

    def read(self, ini_path):
        self.config.clear()
        self.config.read(ini_path, encoding='utf-8-sig')

    def add_section(self, sec):
        self.config.add_section(sec)

    def add_items(self, sec, opt, value):
        if not self.config.has_option(sec, opt):
            self.config.set(sec, opt, value)
        self._write()

    def get_sections(self):
        return self.config.sections()
    
    def get_options(self, sec):
        return self.config.options(sec)
    
    def get_value(self, sec, opt):
        return self.config.get(sec, opt)

    def update_value(self, sec, opt, value):
        if self.config.has_option(sec, opt):
            self.config.set(sec, opt, value)
        self._write()

    def remove_section(self, sec):
        self.config.remove_section(sec)
        self._write()

    def remove_option(self, sec, opt):
        if self.config.has_option(sec, opt):
            self.config.remove_option(sec, opt)
        self._write()

    def update_option(self, sec, opt_old, opt_new):
        # 检查 section 和 option 是否存在
        if self.config.has_section(sec) and self.config.has_option(sec, opt_old):
            # 获取旧 option 的值
            value = self.get_value(sec, opt_old)
            # 删除旧 option
            self.remove_option(sec, opt_old)
            # 添加新 option 并赋值
            self.add_items(sec, opt_new, value)

    def _write(self):
        with open(self.ini_path, 'w', encoding='UTF-8') as f:
            self.config.write(f)



if __name__ == '__main__':
    ini_path = 'test.ini'
    cfg_handler = ConfigHandler(ini_path)
    print(cfg_handler.get_sections())
    print(cfg_handler.get_options('foldername'))
    print(cfg_handler.get_value('foldername', 'folder1'))
    cfg_handler.add_section('victor')
    cfg_handler.add_items('victor', 'name', 'wu')
        