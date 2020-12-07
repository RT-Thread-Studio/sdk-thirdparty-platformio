import os
import shutil
import sys
from pathlib import Path
import platform


class PlatformioBuilder(object):
    """
    This is the platformio env builder
    """

    def __init__(self):
        dir_path = ""
        if getattr(sys, 'frozen', False):
            dir_path = os.path.dirname(sys.executable)
        elif __file__:
            dir_path = os.path.dirname(__file__)
        self.current_folder = Path(dir_path)
        self.home_path = Path.home()
        self.platformio_path = self.home_path.joinpath(".platformio")
        self.python_path = self.platformio_path.joinpath(".rt_studio/python377x64/python.exe")
        self.get_platformio_script_path = self.platformio_path.joinpath(".rt_studio/python377x64/get-platformio.py")
        self.is_pip_config_exists = False
        self.pip_config_dir_path = self.home_path.joinpath("pip")
        if self.home_path.joinpath("pip/pip.ini").exists():
            self.is_pip_config_exists = True

    def modify_pip_source(self):
        if self.is_pip_config_exists:
            shutil.move(str(self.home_path.joinpath("pip/pip.ini")), str(self.home_path.joinpath("pip/pip.ini.backup")))
        self.cp_fr_list(["pip.ini"], self.current_folder, self.pip_config_dir_path)

    def recover_pip_source(self):
        os.remove(self.pip_config_dir_path.joinpath("pip.ini"))
        if self.is_pip_config_exists:
            shutil.move(str(self.home_path.joinpath("pip/pip.ini.backup")), str(self.home_path.joinpath("pip/pip.ini")))

    def rm_fr_list(self, item_list, dst_path):
        for item_path in item_list:
            dst_item_path = str(dst_path.joinpath(item_path))
            dst_item_path = dst_item_path.replace('\\', '/')
            dst_item_path = Path(dst_item_path)
            if dst_item_path.exists():
                if Path.is_dir(dst_item_path):
                    shutil.rmtree(self.long_path_enable(dst_item_path))
                else:
                    os.remove(self.long_path_enable(dst_item_path))

    @staticmethod
    def long_path_enable(path_in):
        if os.name == "nt":
            return str('\\\\?\\' + str(path_in))
        else:
            return path_in

    def cp_fr_list(self, item_list, src_path, dst_path):
        item_list_temp = []
        for item_path in item_list:
            if str(item_path) == "*":
                item_list_temp.extend(os.listdir(src_path))
            else:
                item_list_temp.append(item_path)
        item_list_all = list(set(item_list_temp))
        for item_path in item_list_all:
            src_item_path = str(src_path.joinpath(item_path))
            dst_item_path = str(dst_path.joinpath(item_path))
            src_item_path = src_item_path.replace('\\', '/')
            dst_item_path = dst_item_path.replace('\\', '/')
            src_item_path = Path(src_item_path)
            dst_item_path = Path(dst_item_path)
            if dst_item_path.exists():
                if Path.is_dir(dst_item_path):
                    shutil.rmtree(self.long_path_enable(dst_item_path))
                else:
                    os.remove(self.long_path_enable(dst_item_path))
            if not dst_item_path.parent.exists():
                os.makedirs(self.long_path_enable(dst_item_path.parent))
            if src_item_path.is_dir():
                shutil.copytree(self.long_path_enable(src_item_path), self.long_path_enable(dst_item_path))
            else:
                shutil.copy(self.long_path_enable(src_item_path), self.long_path_enable(dst_item_path))

    def copy_platformio_packages(self):
        print("************* Copy and install platformio packages (Step 1/2) ***************")
        if not self.platformio_path.exists():
            os.makedirs(self.long_path_enable(self.platformio_path))
            self.cp_fr_list([".platformio"], self.current_folder, self.home_path)
        else:
            self.cp_fr_list(os.listdir(self.current_folder.joinpath(".platformio/packages")),
                            self.current_folder.joinpath(".platformio/packages"),
                            self.platformio_path.joinpath("packages"))
            self.cp_fr_list(os.listdir(self.current_folder.joinpath(".platformio/platforms")),
                            self.current_folder.joinpath(".platformio/platforms"),
                            self.platformio_path.joinpath("platforms"))
            print(self.current_folder.joinpath(".platformio"))
            other_file_and_folders = os.listdir(self.current_folder.joinpath(".platformio"))
            other_file_and_folders.remove("platforms")
            other_file_and_folders.remove("packages")
            self.cp_fr_list(other_file_and_folders, self.current_folder.joinpath(".platformio"), self.platformio_path)
        if self.platformio_path.joinpath("penv").exists():
            if Path.is_dir(self.platformio_path.joinpath("penv")):
                shutil.rmtree(self.long_path_enable(self.platformio_path.joinpath("penv")))
            else:
                os.remove(self.long_path_enable(self.platformio_path.joinpath("penv")))

    def copy_portble_python(self):
        self.cp_fr_list(['python377x64'], self.current_folder, self.platformio_path.joinpath(".rt_studio"))

    def install_platformio(self):
        print("************* Create platformio environment (Step 2/2) ***************")
        os.system(str(self.python_path.as_posix()) + " " + str(self.get_platformio_script_path.as_posix()))
        print("************* Done ***************")

    def make_platformio(self):
        self.copy_platformio_packages()
        self.copy_portble_python()
        self.install_platformio()


if len(sys.argv) > 2:
    builder = PlatformioBuilder()
    rt_studio_version = sys.argv[1]
    if "global" in str(sys.argv[2]).lower():
        is_studio_global_version = True
    else:
        is_studio_global_version = False
    print("rt_studio_version: " + str(rt_studio_version))
    if rt_studio_version >= "2.0.0":
        if platform.release()>="10":
            result = os.popen("""reg query HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\FileSystem /v LongPathsEnabled""")
            if "1" in result.read().strip().split(" ")[-1]:
                print("Long path support has enabled")
            else:        
                print("Long path support has not enabled")
                print("Enable windows long path support...")
                bat_path = builder.current_folder.joinpath("longpathenable.bat").as_posix()
                os.system(str(bat_path))
                result = os.popen("""reg query HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\FileSystem /v LongPathsEnabled""")
                if "1" in result.read().strip().split(" ")[-1]:
                    print("Long path support has enabled")
                else:
                    print("Enable long path support fail.")
                    sys.exit(1)
        else:
            print("Current windows os version is lower than 10, skip enable long path support")
        if is_studio_global_version:
            builder.make_platformio()
        else:
            builder.modify_pip_source()
            builder.make_platformio()
            builder.recover_pip_source()
    else:
        print("RT-Thread Studio version is not match")
else:
    print("Info:Please add RT-Thread Studio version number as parameter")
