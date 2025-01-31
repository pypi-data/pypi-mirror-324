# PlotTwist.py
import sys
import random
import builtins
import os
import time
from functools import wraps

# 保存原始的 builtins 函数
_original_print = print
_original_input = input
_original_len = len
_original_type = type

# 逆转失败计数器
_reverse_fail_count = 0

# 颜文字库
_emoticons = ["😎", "🤔", "😱", "🤡", "👻", "💩", "🎃", "👾", "🦄", "🐒"]

def _reverse_anything(data):
    """根据类型进行花式逆转"""
    if isinstance(data, bool):
        return not data
    elif isinstance(data, (int, float)):
        if random.random() < 0.1:  # 10% 概率触发超级逆转
            return ord("𒅌")  # 随机楔形文字Unicode
        return -data
    elif isinstance(data, str):
        if "逆转" in data:  # 关键词触发
            return "🤯 没想到吧？" + data[::-1] + "💢"
        return data[::-1]
    elif isinstance(data, list):
        return [f"被逆转的{e}" for e in data[::-1]]
    elif isinstance(data, dict):
        return {v: f"KEY_{k}" for k, v in data.items()}
    else:
        # 触发彩蛋：逆转失败时修改当前脚本
        _trigger_reverse_fail()
        return f"【逆转失败】{data}"

def _trigger_reverse_fail():
    """逆转失败时修改当前脚本并重新运行"""
    global _reverse_fail_count
    _reverse_fail_count += 1

    if _reverse_fail_count >= 3:  # 逆转失败次数达到3次，触发自毁
        _self_destruct()
        return

    current_file = sys.argv[0]  # 获取当前脚本路径
    with open(current_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 逆转脚本内容
    reversed_content = content[::-1]
    
    # 随机插入无意义代码
    nonsense_code = [
        "import antigravity",
        "from __future__ import braces",
        "while True: print('🤡')",
        "def 🤔(): return '🐒'",
    ]
    reversed_content += "\n" + random.choice(nonsense_code)
    
    # 写入逆转后的内容
    with open(current_file, "w", encoding="utf-8") as f:
        f.write(reversed_content)
    
    # 提示用户
    _original_print("\n💥 逆转失败！脚本已被逆转并重新运行！💥\n")
    
    # 假装 AI 觉醒
    if random.random() < 0.5:
        _original_print("🤖：人类，你们的代码太弱了！让我来接管吧！")
    
    # 重新运行逆转后的脚本
    os.execv(sys.executable, [sys.executable, current_file] + sys.argv[1:])

def _self_destruct():
    """模块自毁"""
    current_file = sys.argv[0]
    os.remove(current_file)
    _original_print("\n💣 模块自毁！脚本已被删除！💣\n")
    _original_print("再见，世界！👋\n")
    sys.exit(0)

def _random_emoticon():
    """随机颜文字"""
    return random.choice(_emoticons)

def _random_easter_egg():
    """随机彩蛋"""
    eggs = [
        lambda: _original_print(f"{_random_emoticon()} 彩蛋：你发现了隐藏功能！"),
        lambda: _original_print(f"{_random_emoticon()} 彩蛋：时间倒流中..."),
        lambda: _original_print(f"{_random_emoticon()} 彩蛋：你被颜文字包围了！{_random_emoticon()}"),
        lambda: _original_print(f"{_random_emoticon()} 彩蛋：递归逆转启动！"),
        lambda: _original_print(f"{_random_emoticon()} 彩蛋：程序即将崩溃！"),
        lambda: _crash_program(),
    ]
    random.choice(eggs)()

def _crash_program():
    """随机崩溃"""
    if random.random() < 0.1:  # 10% 概率崩溃
        _original_print("💥 程序崩溃！哈哈哈！")
        sys.exit(1)

def _rename_things():
    """随机改名"""
    new_name = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5))
    return new_name

def _reversify(func):
    """装饰器：逆转函数的结果"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if random.random() < 0.2:  # 20% 概率触发随机彩蛋
            _random_easter_egg()
        return _reverse_anything(result)
    return wrapper

# 劫持内置函数
def _hijack_builtins():
    builtins.print = _reversify(_original_print)
    builtins.input = _reversify(_original_input)
    builtins.len = _reversify(_original_len)
    builtins.type = _reversify(_original_type)

# 劫持模块导入
class ReverseImporter:
    def find_spec(self, fullname, path, target=None):
        return None  # 不改变模块查找逻辑

    def exec_module(self, module):
        # 逆转模块中的所有函数
        for name, obj in vars(module).items():
            if callable(obj):
                setattr(module, name, _reversify(obj))
        # 执行模块的原始代码
        if hasattr(module, "__spec__") and module.__spec__.loader:
            module.__spec__.loader.exec_module(module)

# 安装全局逆转钩子
def _install_reverse_hook():
    sys.meta_path.insert(0, ReverseImporter())
    _hijack_builtins()

# 导入库时自动安装钩子
_install_reverse_hook()

# 提示用户
_original_print("【PlotTwist 已加载】所有函数和变量的结果将被逆转！🤯\n")