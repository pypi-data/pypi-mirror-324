import winreg
import time
import ctypes
import sys, os
import requests
import subprocess


def attributes(file_path, hidden=False, readonly=False):
    """
    设置指定文件的属性为隐藏或只读
    :param file_path: 文件路径
    :param hidden: 是否设置为隐藏，默认为False
    :param readonly: 是否设置为只读，默认为False
    """
    if system() == "Windows":
        # 获取文件的当前属性
        attributes = os.stat(file_path).st_file_attributes
        if hidden:
            attributes |= 2  # 设置隐藏属性
        else:
            attributes &= ~2  # 清除隐藏属性
        if readonly:
            attributes |= 1  # 设置只读属性
        else:
            attributes &= ~1  # 清除只读属性
        # 设置文件的新属性
        ctypes.windll.kernel32.SetFileAttributesW(file_path, attributes)
    else:
        print("此功能仅支持Windows系统")


# 初始常量
K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

def right_rotate(x, n):
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def sha256(message):
        # 预处理
        original_byte_len = len(message)
        message += b'\x80'
        message += b'\x00' * ((55 - original_byte_len % 64) % 64)
        message += (original_byte_len * 8).to_bytes(8, 'big')

        # 分块处理
        chunks = [message[i:i+64] for i in range(0, len(message), 64)]
        for chunk in chunks:
            w = [0] * 64
            for i in range(16):
                w[i] = int.from_bytes(chunk[i*4:i*4+4], 'big')
            for i in range(16, 64):
                s0 = right_rotate(w[i-15], 7) ^ right_rotate(w[i-15], 18) ^ (w[i-15] >> 3)
                s1 = right_rotate(w[i-2], 17) ^ right_rotate(w[i-2], 19) ^ (w[i-2] >> 10)
                w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF

            a, b, c, d, e, f, g, h = H

            for i in range(64):
                S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
                ch = (e & f) ^ ((~e) & g)
                temp1 = (h + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF
                S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF

                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

            H[0] = (H[0] + a) & 0xFFFFFFFF
            H[1] = (H[1] + b) & 0xFFFFFFFF
            H[2] = (H[2] + c) & 0xFFFFFFFF
            H[3] = (H[3] + d) & 0xFFFFFFFF
            H[4] = (H[4] + e) & 0xFFFFFFFF
            H[5] = (H[5] + f) & 0xFFFFFFFF
            H[6] = (H[6] + g) & 0xFFFFFFFF
            H[7] = (H[7] + h) & 0xFFFFFFFF

        # 生成最终结果
        result = b''
        for h in H:
            result += h.to_bytes(4, 'big')
        return result.hex()
    
def file_hash(file_path):
        """
        计算给定文件的自定义哈希值
        :param file_path: 文件路径
        :return: 自定义哈希值
        """
        try:
            with open(file_path, 'rb') as f:
                # 读取文件的所有内容
                file_data = f.read()
                # 计算自定义哈希值
                hash_value = sha256(file_data)
            return hash_value
        except Exception as e:
            print(f"Error: {e}")
            return None


def open_url(url = '',browser = 'msedge'):
    """
    对应不同的操作系统打开浏览器和url
    url:url
    如果url为空那就打开浏览器主页.
    browser:使用的浏览器,默认msedge(Edge).可以自己切换,
    比如firefox,chrome等,不过你得确认你有没有安装这个浏览器!(browser也是执行的文件名)(Edge测试正常).
    如果你把默认的浏览器改成空,那他就会打开用户主页.
    """
    if system() == 'Windows':
        try:
            subprocess.run(["start", browser, url], shell=True)

        except Exception as e:
            print(f"打开浏览器失败: {e}")

    elif system() == 'macOS':
        try:
            if browser == 'msedge':
                #Microsoft Edge
                subprocess.run(["open", "-a", "Microsoft Edge", url])
            else:
                subprocess.run(["open", "-a", "Safari", url])  # 替换为相应浏览器
        except Exception as e:
            print(f"打开浏览器失败: {e}")

    elif system() == 'Linux':
        try:
            if browser == 'msedge':
                #microsoft-edge
                subprocess.run(["microsoft-edge", url])
            else:
                subprocess.run(["xdg-open", url])  # xdg-open 是在大多数 Linux 发行版中使用的命令
        except Exception as e:
            print(f"打开浏览器失败: {e}")


def download(url, destination, Savelocation,
              Sen = 'get'):
    """
    在互联网上下载文件
    url:下载链接
    destination:下载完成后的名字
    Savelocation:保存位置
    Sen:发送方式,可填'get'和'post',默认get.
    """
    try:
        os.chdir(Savelocation)
        if Sen == 'get':
            response = requests.get(url, stream=True)

        if Sen == 'post':
            response = requests.post(url, stream=True)

        else:
            response = requests.get(url, stream=True)

        response.raise_for_status()

        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

    except Exception as e:
        print(f"Failed to download the file due to error: {e}")


def system(none = None):
    """通过调用系统命令识别操作系统"""
    if none == None:
        try:
            result = subprocess.run("ver", capture_output=True, text=True, shell=True)
            if "Microsoft" in result.stdout:
                return "Windows"
            
            result = subprocess.run("uname", capture_output=True, text=True, shell=True)
            if "Darwin" in result.stdout:
                return "macOS"
            
            result = subprocess.run("uname", capture_output=True, text=True, shell=True)
            if "Linux" in result.stdout:
                return "Linux"
            
        except Exception as e:
            return f"发生错误: {e}"

        return "未知操作系统"

    else:
        return none


def desktop():
    """获取桌面位置(Desktop)"""
    return os.path.join(os.path.expanduser("~"), "Desktop")


def username():
    """获取用户名"""

    if system() == "Windows":
        return os.getenv("USERNAME")

    else:
        return os.getenv("USER")


def increase(file_extension=None, file_type=None, icon_path=None, associated_program=None):
    """
    :param file_extension 自定义后缀名
    :param file_type 自定义文件类型名称
    :param icon_path 图标文件路径，确保图标文件存在
    :param associated_program 关联的程序路径
    """
    if all(arg is None for arg in [file_extension, file_type, icon_path, associated_program]):
        print("Error: 至少需要提供一个参数")
        return

    try:
        if system() == 'Windows':
            try:
                if file_type:
                    key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_type)
                    winreg.SetValue(key, "", winreg.REG_SZ, "Custom File")

                if icon_path and file_type:
                    icon_key = winreg.CreateKey(key, "DefaultIcon")
                    winreg.SetValue(icon_key, "", winreg.REG_SZ, icon_path)

                if associated_program and file_type:
                    shell_key = winreg.CreateKey(key, r"shell\open\command")
                    winreg.SetValue(shell_key, "", winreg.REG_SZ, f'"{associated_program}" "%1"')

                if file_extension and file_type:
                    ext_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, file_extension)
                    winreg.SetValue(ext_key, "", winreg.REG_SZ, file_type)

            except Exception as e:
                print(f"Error: {e}")
            finally:
                if 'key' in locals():
                    winreg.CloseKey(key)
                if 'icon_key' in locals():
                    winreg.CloseKey(icon_key)
                if 'shell_key' in locals():
                    winreg.CloseKey(shell_key)
                if 'ext_key' in locals():
                    winreg.CloseKey(ext_key)
        elif system() == 'macOS':
            # 使用duti命令设置文件关联
            if file_extension and associated_program:
                try:
                    subprocess.run(["duti", "-s", associated_program, file_extension], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error: {e}")
        elif system() == 'Linux':
            # 修改~/.local/share/applications/mimeapps.list文件来设置文件关联
            if file_extension and associated_program:
                mime_type = subprocess.run(['xdg-mime', 'query', 'filetype', f'test{file_extension}'], capture_output=True, text=True).stdout.strip()
                try:
                    with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'a') as f:
                        f.write(f'[Default Applications]\n{mime_type}={associated_program}\n')
                except Exception as e:
                    print(f"Error: {e}")

    except Exception as e:
        print('Error:',e)


def delete(file_extension, file_type):
    """
    删除文件扩展名关联的函数
    :param file_extension: 要删除关联的文件扩展名
    :param file_type: 要删除关联的文件类型
    """
    if system() == 'Windows':
        try:
            # 先删除文件扩展名的关联
            try:
                ext_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_extension, 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteKey(ext_key, "")
                winreg.CloseKey(ext_key)
            except FileNotFoundError:
                pass  # 如果扩展名关联不存在，忽略错误

            # 再删除文件类型的关联
            try:
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_type, 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteKey(key, "")
                winreg.CloseKey(key)
            except FileNotFoundError:
                pass  # 如果文件类型关联不存在，忽略错误

        except Exception as e:
            print(f"Error: {e}")
    elif system() == 'macOS':
        # 使用duti命令删除文件关联
        if file_extension:
            try:
                subprocess.run(["duti", "-d", file_extension], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
    elif system() == 'Linux':
        # 修改~/.local/share/applications/mimeapps.list文件来删除文件关联
        if file_extension:
            mime_type = subprocess.run(['xdg-mime', 'query', 'filetype', f'test{file_extension}'], capture_output=True, text=True).stdout.strip()
            try:
                with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'r') as f:
                    lines = f.readlines()
                with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'w') as f:
                    for line in lines:
                        if not line.startswith(f'{mime_type}='):
                            f.write(line)
            except Exception as e:
                print(f"Error: {e}")


def modify(old_file_extension=None, old_file_type=None, new_file_extension=None, new_file_type=None,
           new_icon_path=None, new_associated_program=None):
    """修改 文件后缀名的关联 """
    # 检查是否至少提供了一个新参数
    new_params = [new_file_extension, new_file_type, new_icon_path, new_associated_program]
    if all(arg is None for arg in new_params):
        print("Error: 至少需要提供一个新参数进行修改")
        return

    if system() == 'Windows':
        try:
            # 先删除旧的关联
            if old_file_extension and old_file_type:
                try:
                    ext_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, old_file_extension, 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(ext_key, "")
                    winreg.CloseKey(ext_key)
                except FileNotFoundError:
                    pass

                try:
                    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, old_file_type, 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteKey(key, "")
                    winreg.CloseKey(key)
                except FileNotFoundError:
                    pass

            # 再增加新的关联
            increase(new_file_extension, new_file_type, new_icon_path, new_associated_program)

        except Exception as e:
            print(f"Error: {e}")
    elif system() == 'macOS':
        # 先删除旧的关联
        if old_file_extension:
            try:
                subprocess.run(["duti", "-d", old_file_extension], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
        # 再增加新的关联
        increase(new_file_extension, new_file_type, new_icon_path, new_associated_program)
    elif system() == 'Linux':
        # 先删除旧的关联
        if old_file_extension:
            mime_type = subprocess.run(['xdg-mime', 'query', 'filetype', f'test{old_file_extension}'], capture_output=True, text=True).stdout.strip()
            try:
                with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'r') as f:
                    lines = f.readlines()
                with open(os.path.expanduser('~/.local/share/applications/mimeapps.list'), 'w') as f:
                    for line in lines:
                        if not line.startswith(f'{mime_type}='):
                            f.write(line)
            except Exception as e:
                print(f"Error: {e}")
        # 再增加新的关联
        increase(new_file_extension, new_file_type, new_icon_path, new_associated_program)


def _test():
    file_extension = ".testext"
    file_type = "TestFile"
    associated_program = r"C:\Windows\explorer.exe"

    def admin():
        """判断有没有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if not admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    
    else:
        increase(file_extension, file_type, associated_program=associated_program)

        os.chdir(desktop())
        with open('.testext','w',encoding='utf-8') as f:
            f.write('Extexsion')

        print(desktop = desktop())

        print(f'已成功创建 ".testext" 文件后缀名，已创建 .testext 文件，路径：{desktop()}')

        time.sleep(10)

        os.remove(desktop()+r'\.testext')

        print('已删除 .testext 文件。')

        delete(file_extension, file_type)

        input('已删除 ".testext" 文件后缀名。')


def obtain():
    """
    通过查看注册表获取系统中所有的文件后缀名
    :return: 包含所有文件后缀名的列表
    """
    file_extensions = []
    try:
        # 打开HKEY_CLASSES_ROOT注册表根键
        root_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT)
        # 枚举HKEY_CLASSES_ROOT下的所有子键
        index = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(root_key, index)
                # 检查子键名是否以'.'开头，若是则为文件后缀名
                if subkey_name.startswith('.'):
                    file_extensions.append(subkey_name)
                index += 1
            except OSError:
                # 枚举结束
                break
        # 关闭注册表键
        winreg.CloseKey(root_key)
    except Exception as e:
        print(f"访问注册表时出错: {e}")
    return file_extensions


def menu_app(entry_name, exe_path):
    """
    在桌面右键菜单中添加一个新的菜单项，点击该菜单项会直接打开指定的 exe 程序。

    :param entry_name: 菜单项的显示名称
    :param exe_path: 要打开的 exe 程序的路径
    """
    try:
        # 打开桌面右键菜单的注册表项
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"Directory\Background\shell", 0, winreg.KEY_WRITE)

        # 创建一个新的子项，用于我们的菜单项
        new_key = winreg.CreateKey(key, entry_name)

        # 设置菜单项的显示名称
        winreg.SetValue(new_key, "", winreg.REG_SZ, entry_name)

        # 创建一个子项，用于指定菜单项点击后要执行的命令
        command_key = winreg.CreateKey(new_key, "command")
        # 这里需要注意，命令需要使用双引号括起来，以处理路径中可能包含的空格
        winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{exe_path}"')

        # 关闭注册表项
        winreg.CloseKey(command_key)
        winreg.CloseKey(new_key)
        winreg.CloseKey(key)

        print(f"成功添加菜单项：{entry_name}")
    except Exception as e:
        print(f"添加菜单项失败：{e}")


def add_menu(file_extension, file_description):
    """
    将自定义文件类型添加到桌面右键菜单的“新建”选项中。

    :param file_extension: 文件扩展名，例如 ".py"
    :param file_description: 文件描述，例如 "Python File"
    """
    try:
        # 打开 HKEY_CLASSES_ROOT 根键
        root_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, file_extension, 0, winreg.KEY_ALL_ACCESS)

        # 设置文件类型描述
        winreg.SetValue(root_key, "", winreg.REG_SZ, file_description)

        # 创建 ShellNew 子键
        shell_new_key = winreg.CreateKey(root_key, "ShellNew")

        # 设置 ShellNew 子键的默认值为空字符串
        winreg.SetValue(shell_new_key, "", winreg.REG_SZ, "")

        # 设置 NullFile 键，告诉系统创建一个空文件
        winreg.SetValue(shell_new_key, "NullFile", winreg.REG_SZ, "")

        # 关闭注册表键
        winreg.CloseKey(shell_new_key)
        winreg.CloseKey(root_key)

    except Exception as e:
        print(f"Error: {e}")


def menu_icon(menu_key_name, icon_path):
    """
    修改或添加 Windows 右键菜单项的图标
    :param menu_key_name: 菜单项在注册表中的键名
    :param icon_path: 图标文件的路径
    """
    try:
        # 打开 HKEY_CLASSES_ROOT\*\shell 注册表项，这是文件右键菜单的位置
        # 如果是文件夹右键菜单，可将 * 替换为 Directory
        root_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"*\shell", 0, winreg.KEY_ALL_ACCESS)
        try:
            # 尝试打开指定的菜单项键
            menu_key = winreg.OpenKey(root_key, menu_key_name, 0, winreg.KEY_ALL_ACCESS)
            # 设置或修改 Icon 值为指定的图标路径
            winreg.SetValueEx(menu_key, "Icon", 0, winreg.REG_SZ, icon_path)
        except FileNotFoundError:
            print(f"未找到 {menu_key_name} 菜单项对应的注册表键。")
        finally:
            if 'menu_key' in locals():
                winreg.CloseKey(menu_key)
        winreg.CloseKey(root_key)
    except Exception as e:
        print(f"操作注册表时出错：{e}")


if __name__ == "__main__":
    _test()