from decimal import Decimal, getcontext
import math
import os
import sys
import subprocess
import time
from tkinter import GROOVE, Tk, Button, Label, filedialog, messagebox
from tkinter.ttk import Progressbar
from pyfiglet import Figlet

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
    import getpass
    return getpass.getuser()

def default(txt,font = "larry3d"):
    """
    艺术字(pyfiglet)
    txt:字
    font:字体(默认3D字体)
    """
    f = Figlet(font=font, width=200)

    print(f.renderText(txt))

print('Hello! py-to-pyd')
default('py-to-pyd')
print(username(), system())
def convert_py_to_pyx(py_file):
        """将 .py 文件转换为 .pyx 文件。"""
        pyx_file = py_file[:-3] + '.pyx'
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(pyx_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return pyx_file

def create_setup_file(pyx_file):
    """创建 setup.py 文件以编译 .pyx 文件。"""
    setup_file = "setup.py"
    content = f"""
from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name='{os.path.splitext(os.path.basename(pyx_file))[0]}',
    ext_modules=cythonize(Extension(
        name='{os.path.splitext(os.path.basename(pyx_file))[0]}',
        sources=['{pyx_file}'],
    )),
    zip_safe=False,
)
"""
    with open(setup_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return setup_file

def compile_pyx_to_pyd(setup_file, pyx_file):
        """编译 .pyx 文件为 .pyd 文件，并实时输出进度。"""
        progress['value'] = 0  # 重设进度条

        # 启动子进程
        process = subprocess.Popen(
            [sys.executable, setup_file, "build_ext", "--inplace"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # 行缓冲
            universal_newlines=True
        )
        
        def update_progress():
            output = process.stdout.readline()
            
            if output:
                # 进度条假设每行输出增加一定比例，这里简单映射为增加10%（可根据实际情况修改）
                if progress['value'] < 90:  # 根据实际行数确定进度
                    progress['value'] += 10  
                progress.update_idletasks()  # 更新进度条
            
            # 检查进程是否仍在运行
            if process.poll() is None:  # 进程仍在运行
                root.after(100, update_progress)  # 每100毫秒调用一次
            else:  # 进程完成
                process.wait()
                if process.returncode == 0:
                    messagebox.showinfo("成功", "成功生成 .pyd 文件！")
                    clean_up(setup_file, pyx_file)  # 清理文件
                else:
                    error_output = process.stderr.read()
                    messagebox.showerror("编译错误", f"编译失败: {error_output}")

                progress['value'] = 100  # 设置进度条为 100%

        # 启动输出读取
        update_progress()

def clean_up(setup_file, pyx_file):
        """删除 .pyx、setup.py 以及生成的 .c 文件。"""
        try:
            if os.path.exists(setup_file):
                os.remove(setup_file)
            if os.path.exists(pyx_file):
                os.remove(pyx_file)

            # 确保对应的 .c 文件被删除
            c_file = pyx_file[:-4] + '.c'
            if os.path.exists(c_file):
                os.remove(c_file)  # 删除 .c 文件
        except Exception as e:
            messagebox.showwarning("清理错误", f"清理文件时出错: {str(e)}")

def process_file():
        """处理选择的 Python 文件。"""
        py_file = filedialog.askopenfilename(title="选择 Python (.py) 文件", filetypes=[("Python 文件", "*.py")])
        
        if not py_file:
            return

        try:
            # 转换 .py 为 .pyx
            pyx_file = convert_py_to_pyx(py_file)
            # 创建 setup.py 文件
            setup_file = create_setup_file(pyx_file)
            # 编译 .pyx 为 .pyd
            compile_pyx_to_pyd(setup_file, pyx_file)
            user = username()
            time.sleep(2.5)
            print("编译完成，.pyd 文件已保存到:",f'C:/Users/{user}>')
        except Exception as e:
            messagebox.showerror("错误", str(e))
            print('Error: '+str(e))

def main():
    global progress, root
    # 创建主 GUI 窗口
    print('Hello! py-to-pyd')
    default('py-to-pyd')
    print(username(), system())
    root = Tk()
    root.title("Py To Pyd")
    root.wm_iconbitmap('pytopyd.ico')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 500) // 2

    root.geometry(f"400x250+{x}+{y}")
    #root.wm_iconbitmap('PyToPyd.ico')

    # 创建和放置控件
    label = Label(root, text="选择要转换和编译的 Py 文件：",font=('黑体',15))
    label.pack(pady=20)

    process_button = Button(root, text="选择文件", command=process_file, bg='yellow', relief=GROOVE, width=15)
    process_button.pack(pady=10)

    label = Label(root, text="进度:",font=('黑体',12))
    label.place(x=45,y=140)

    # 创建进度条
    progress = Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress.pack(pady=60)

    # 启动 GUI 事件循环
    root.mainloop()

def Gcw(name = None):
    """
    Retrieve the current wallpaper and save it to desktop.获取当前壁纸并保存到桌面.
    name: 保存到桌面的名字,不填保存后名字为wallpaper.jpg #这个后缀名也得加上,后缀名jpg与png只要是照片的后缀名都行,动图的后缀名不行.
    """
    from tkinter import messagebox
    try:
        import shutil

        source_file_path = r"C:\Users\36376\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper"
        destination_directory = desktop()

        try:
            shutil.copy2(source_file_path, destination_directory)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            
        print('Successfully obtained file.')
        print('已成功获取文件.')

        """进行重命名"""
        from pathlib import Path

        desktop_path = str(Path.home() / "Desktop")
        print(f"Desktop path is {desktop_path}")

        old_file_name = 'TranscodedWallpaper'

        if name == None:
            new_file_name = 'wallpaper.jpg'#jpg与png图片都行.

        else:
            new_file_name = name

        try:
            old_full_path = os.path.join(desktop_path, old_file_name)
            new_full_path = os.path.join(desktop_path, new_file_name)

            # Check if the file exists before attempting to rename it.
            if not os.path.exists(old_full_path):
                raise FileNotFoundError(f"The specified file does not exist at location: '{old_full_path}'")

            os.rename(old_full_path, new_full_path)
            print("File renamed successfully.")
        except Exception as e:
            print(f"An error occurred while trying to rename the file: {e}")
    except Exception as e:
        messagebox.showerror('Error','Error:',e)

class Count:
    """进行计算"""
    global sin, cos, factorial, exp, cosh, sinh
    global log, d_tan, d_cos, d_sin, tan, tanh

    def factorial(n):
        """计算阶乘"""
        if not isinstance(n, int) or n < 0:
            raise ValueError("阶乘的输入必须是一个非负整数")
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result


    def sin(x, num_terms=10):
        """使用泰勒级数展开计算 sin(x)"""
        try:
            x = x % (2 * 3.141592653589793)
            result = 0
            for n in range(num_terms):
                term = ((-1) ** n) * (x ** (2 * n + 1)) / factorial(2 * n + 1)
                result += term
            return result
        except OverflowError:
            raise ValueError("计算 sin(x) 时发生溢出错误，请检查输入值或减少项数")


    def cos(x, num_terms=10):
        """使用泰勒级数展开计算 cos(x)"""
        try:
            x = x % (2 * 3.141592653589793)
            result = 0
            for n in range(num_terms):
                term = ((-1) ** n) * (x ** (2 * n)) / factorial(2 * n)
                result += term
            return result
        except OverflowError:
            raise ValueError("计算 cos(x) 时发生溢出错误，请检查输入值或减少项数")


    def exp(x, num_terms=10):
        """使用泰勒级数展开计算 e^x"""
        try:
            result = 0
            for n in range(num_terms):
                term = (x ** n) / factorial(n)
                result += term
            return result
        except OverflowError:
            raise ValueError("计算 exp(x) 时发生溢出错误，请检查输入值或减少项数")


    def log(x, tolerance=1e-6, max_iterations=100):
        """使用牛顿 - 拉夫逊方法计算自然对数 ln(x)"""
        if x <= 0:
            raise ValueError("对数的输入必须大于 0")
        y = 1  # 初始猜测值
        for _ in range(max_iterations):
            try:
                f = exp(y) - x
                f_prime = exp(y)
                y_new = y - f / f_prime
                if abs(y_new - y) < tolerance:
                    return y_new
                y = y_new
            except OverflowError:
                raise ValueError("计算 log(x) 时发生溢出错误，请检查输入值或调整迭代参数")
        raise ValueError("未能在最大迭代次数内收敛，请检查输入值或调整迭代参数")


    def d_sin(x):
        """计算 sin(x) 的导数"""
        try:
            return cos(x)
        except ValueError as e:
            raise ValueError(f"计算 d_sin(x) 时出错: {e}")


    def d_cos(x):
        """计算 cos(x) 的导数"""
        try:
            return -sin(x)
        except ValueError as e:
            raise ValueError(f"计算 d_cos(x) 时出错: {e}")


    def tan(x):
        """计算 tan(x)"""
        cos_val = cos(x)
        if cos_val == 0:
            raise ValueError("tan(x) 在 cos(x)=0 处无定义")
        return sin(x) / cos_val


    def d_tan(x):
        """计算 tan(x) 的导数"""
        try:
            cos_val = cos(x)
            if cos_val == 0:
                raise ValueError("d_tan(x) 在 cos(x)=0 处无定义")
            return 1 / (cos_val ** 2)
        except ValueError as e:
            raise ValueError(f"计算 d_tan(x) 时出错: {e}")


    def sinh(x, num_terms=10):
        """使用泰勒级数展开计算双曲正弦函数 sinh(x)"""
        try:
            result = 0
            for n in range(num_terms):
                term = (x ** (2 * n + 1)) / factorial(2 * n + 1)
                result += term
            return result
        except OverflowError:
            raise ValueError("计算 sinh(x) 时发生溢出错误，请检查输入值或减少项数")


    def cosh(x, num_terms=10):
        """使用泰勒级数展开计算双曲余弦函数 cosh(x)"""
        try:
            result = 0
            for n in range(num_terms):
                term = (x ** (2 * n)) / factorial(2 * n)
                result += term
            return result
        except OverflowError:
            raise ValueError("计算 cosh(x) 时发生溢出错误，请检查输入值或减少项数")


    def tanh(x):
        """计算双曲正切函数 tanh(x)"""
        try:
            sinh_val = sinh(x)
            cosh_val = cosh(x)
            return sinh_val / cosh_val
        except ValueError as e:
            raise ValueError(f"计算 tanh(x) 时出错: {e}")


    def pi(iterations):
        """
        计算圆周率
        iterations:到多少位(最高1076)
        """
        getcontext().prec = 1000
        sum_series = Decimal(0)
        for k in range(iterations):
            numerator = Decimal(math.factorial(4 * k)) * (Decimal(1103) + Decimal(26390 * k))
            denominator = (Decimal(math.factorial(k)) ** 4) * (Decimal(396) ** (4 * k))
            term = numerator / denominator
            sum_series += term
        constant = (Decimal(2) * Decimal(2).sqrt()) / Decimal(9801)
        pi = 1 / (constant * sum_series)
        return pi


    def evaluate_expression(expression):
        """计算表达式的值"""
        try:
            # 定义自定义函数和常量
            local_vars = {
                'sin': sin,
                'cos': cos,
                'factorial': factorial,
                'log': log,
                'd_sin': d_sin,
                'd_cos': d_cos,
                'tan': tan,
                'd_tan': d_tan,
                'sinh': sinh,
                'cosh': cosh,
                'tanh': tanh
            }
            return eval(expression, {"__builtins__": None}, local_vars)
        except SyntaxError:
            print(f"表达式 '{expression}' 语法错误，请检查表达式格式。")
        except ValueError as e:
            print(f"计算表达式 '{expression}' 时发生值错误: {e}")
        except Exception as e:
            print(f"计算表达式 '{expression}' 时发生未知错误: {e}")
        return None


    # 示例表达式
    expressions = [
        "sin(3.14 / 2)",
        "cos(0)",
        "factorial(5)",
        "log(2.71828)",
        "d_sin(0)",
        "d_cos(3.14 / 2)",
        "tan(0)",
        "d_tan(0)",
        "sinh(1)",
        "cosh(1)",
        "tanh(1)",
        # 可能引发错误的表达式
        "factorial(-1)",
        "log(-1)",
        "tan(3.14 / 2)"
    ]

    PI = 3.14159265358979323846
    2643383279
    5028841971
    6939937510
    5820974944
    59230781640628620899
    8628034825
    3421170679
    8214808651
    32823066470938446095
    5058223172
    5359408128
    4811174502
    8410270193
    8521105559
    6446229489
    5493038196
    4428810975
    6659334461
    2847564823
    3786783165
    2712019091
    4564856692
    3460348610
    4543266482
    13393607260249141273
    72458700660631558817
    4881520920
    9628292540
    9171536436
    78925903600113305305
    4882046652
    1384146951
    9415116094
    3305727036
    57595919530921861173
    8193261179
    31051185480744623799
    6274956735
    1885752724
    8912279381
    8301194912
    9833673362
    4406566430
    8602139494
    6395224737
    1907021798
    60943702770539217176
    2931767523
    8467481846
    76694051320005681271
    4526356082
    7785771342
    7577896091
    7363717872
    1468440901
    2249534301
    4654958537
    1050792279
    6892589235
    4201995611
    2129021960
    8640344181
    5981362977
    4771309960
    5187072113
    4999999837
    29780499510597317328
    1609631859
    5024459455
    3469083026
    4252230825
    3344685035
    2619311881
    7101000313
    7838752886
    5875332083
    8142061717
    7669147303
    5982534904
    2875546873
    1159562863
    8823537875
    9375195778
    1857780532
    1712268066
    1300192787
    6611195909
    2164201989
    3809525720
    1065485863
    2788659361
    5338182796
    82303019520353018529
    6899577362
    2599413891
    2497217752
    8347913151
    5574857242
    4541506959
    5082953311
    6861727855
    8890750983
    8175463746
    493931925506040092770167113900
    9848824012

if __name__ == '__main__':
    main()