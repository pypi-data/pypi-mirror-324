import typer
import os
from neutools import globalvars
from neutools import debug
from neutools import plugin


app = typer.Typer(no_args_is_help=True)

GLOB_VAR = "0.2.1"


@app.command()
def version():
    """显示版本并退出"""
    if (os.path.exists("/opt/neutron/neutron/version")):
        with open("/opt/neutron/neutron/version", "r") as f:
            ver = f.read().replace("\n", "").replace("\r", "")
    else:
        ver = "Unknown"
    print("neutron panel v"+ver)
    print("neutron tools v"+GLOB_VAR)


@app.command()
def start():
    """启动面板"""
    os.system("neu-start")


@app.command()
def stop():
    """停止面板"""
    os.system("neu-stop")


@app.command()
def restart():
    """重启面板"""
    os.system("neu-stop")
    os.system("neu-start")


@app.command()
def status():
    """查看面板状态"""
    os.system("neu-stat")


@app.command()
def fix():
    """安装/升级/卸载面板"""
    os.system("bash -c \"$(wget -O - n.cxykevin.top)\"")


app.add_typer(debug.app, name="debug", help="调试工具")
app.add_typer(plugin.app, name="plugin", help="插件管理")
app.add_typer(plugin.pip_typer, name="pip",
              help="对 neutron panel 的 venv 中模块操作")


@app.callback()
def set_neu_path(
    neu_path: str = typer.Option(
        "/opt/neutron/neutron",
        "--neu-path",
        help="设置 neutron panel 路径"
    )
):
    globalvars.NEU_PATH = os.path.abspath(neu_path)


if __name__ == "__main__":
    app()
