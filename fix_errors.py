import os
import time

try:
    import vkquick
    import wikipedia
    import ping3
    import py_expression_eval
    import vk_api
    from loguru import logger
    import sys
except ModuleNotFoundError:
    installer = input(f"""
У вас не установлен модуль.

Введите Вашу операционную систему:
1. Termux
2. PC
3. Ubuntu (VDS)
""")
    pip = 'pip'
    if int(installer) == 1:
        pip = 'pip'
    elif int(installer) == 2:
        pip = 'pip'
    elif int(installer) == 3:
        pip = input("Введите ваш установщик пакетов (python3.8 -m pip)")

    print("[vqlp] Package manager. Downloading packages", )
    os.system(f"{pip} install --upgrade pip")
    print("[vqlp] Download package 'vkquick' ")
    time.sleep(1)
    os.system(f"{pip} install --upgrade https://github.com/deknowny/vkquick/archive/1.0.zip --no-cache-dir")
    os.system(f"export CRYPTOGRAPHY_DONT_BUILD_RUST=1")
    os.system(f"{pip} install --upgrade https://github.com/deknowny/vkquick/archive/1.0.zip --no-cache-dir")
    os.system("clear" if int(installer) == 1 or int(installer) == 3 else "cls")
    os.system(f"export CRYPTOGRAPHY_DONT_BUILD_RUST=0")
    print("[vqlp] Downloading module wikipedia..")
    os.system(f"{pip} install wikipedia")
    os.system("clear" if int(installer) == 1 or int(installer) == 3 else "cls")
    os.system(f"{pip} install py_expression_eval")
    os.system("clear" if int(installer) == 1 or int(installer) == 3 else "cls")
    os.system(f"{pip} install ping3")
    os.system("clear" if int(installer) == 1 or int(installer) == 3 else "cls")
    os.system(f"{pip} install vk_api")
    os.system("clear" if int(installer) == 1 or int(installer) == 3 else "cls")
    print("[vqlp] Complete download packages. "
          "\nStarting vqlp...")
    time.sleep(3)
    os.system("python -m src")

print("У вас всё установленно.")
