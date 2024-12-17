# -*- mode: python ; coding: utf-8 -*-

# Analysis对象用于分析和收集程序的所有依赖
a = Analysis(
    ['tetris.py'],          # 主程序脚本
    pathex=[],              # 额外的导入路径
    binaries=[],            # 额外的二进制文件
    datas=[],               # 额外的数据文件
    hiddenimports=[],       # 隐式导入的模块
    hookspath=[],           # hook脚本的路径
    hooksconfig={},         # hook的配置选项
    runtime_hooks=[],       # 运行时hook脚本
    excludes=[],            # 要排除的模块
    noarchive=False,        # 是否不创建ZIP归档
    optimize=0,             # Python字节码优化级别
)

# PYZ对象用于创建包含所有Python模块的ZIP归档
pyz = PYZ(a.pure)

# EXE对象用于创建最终的可执行文件
exe = EXE(
    pyz,                            # PYZ归档
    a.scripts,                      # 脚本
    a.binaries,                     # 二进制文件
    a.datas,                        # 数据文件
    [],                            # 额外的选项
    name='Tetris',                 # 可执行文件名称
    debug=False,                   # 是否启用调试模式
    bootloader_ignore_signals=False,# 是否忽略引导加载器信号
    strip=False,                   # 是否剥离二进制文件
    upx=True,                      # 是否使用UPX压缩
    upx_exclude=[],                # 排除UPX压缩的文件
    runtime_tmpdir=None,           # 运行时临时目录
    console=False,                 # 是否显示控制台窗口
    disable_windowed_traceback=False,# 是否禁用窗口化回溯
    argv_emulation=False,          # 是否启用参数模拟
    target_arch=None,              # 目标架构
    codesign_identity=None,        # 代码签名身份
    entitlements_file=None,        # 授权文件
    icon=['tetris.ico'],           # 应用程序图标
)
