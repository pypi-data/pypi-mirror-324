import typer
import tarfile
import os
import shutil
import sys
import subprocess
from neutools import globalvars

app = typer.Typer(no_args_is_help=True)


@app.command("pack")
def plug_pack(plugin_name_or_path: str, o: str | None = typer.Option(None, "-o", "--output", help="输出文件")):
    """打包插件

输入路径会按路径打包，否则在config/plugins与plugins下查找插件并打包"""
    if (not os.path.exists(plugin_name_or_path)):  # 当前目录
        real_path = os.path.join(
            globalvars.NEU_PATH+"/config/plugins", plugin_name_or_path)
        if (not os.path.exists(real_path)):  # 用户插件目录
            real_path = os.path.join(
                globalvars.NEU_PATH+"/plugins", plugin_name_or_path)
            if (not os.path.exists(real_path)):  # 系统插件目录
                raise typer.BadParameter("Plugin not found")
    else:
        real_path = plugin_name_or_path
    typer.echo("打包中")
    if (o == None):  # 自动生成文件名
        o = plugin_name_or_path.split("/")[-1]+".neuplugin"
    with tarfile.open(o, "w:xz") as tar:  # 打包
        for i in os.listdir(real_path):
            real_path_i = os.path.join(real_path, i)
            tar.add(real_path_i, arcname=os.path.basename(real_path+"/"+i))
    typer.echo("打包完毕")


@app.command("install")
def plug_install(plugin_path: str):
    """安装插件"""
    if (not os.path.exists(plugin_path)):
        raise typer.BadParameter("Plugin not found")
    typer.echo("安装中")
    ext_name = plugin_path.split(".")[-1].split(".neuplugin")[0]
    if (os.path.exists(globalvars.NEU_PATH+"/config/plugins/" +
                       ext_name)):  # 更新前删除
        shutil.rmtree(globalvars.NEU_PATH+"/config/plugins/" + ext_name)
    os.makedirs(globalvars.NEU_PATH+"/config/plugins", exist_ok=True)
    if (os.path.isfile(plugin_path)):  # 压缩的插件
        os.makedirs(globalvars.NEU_PATH+"/config/plugins/" +
                    ext_name, exist_ok=True)
        with tarfile.open(plugin_path, "r:xz") as tar:  # 解压
            tar.extractall(globalvars.NEU_PATH+"/config/plugins/" +
                           plugin_path.split("/")[-1].split(".neuplugin")[0])
    else:
        shutil.copytree(plugin_path, globalvars.NEU_PATH +
                        "/config/plugins/" + ext_name)  # 直接复制

    if (os.path.exists(globalvars.NEU_PATH+"/config/plugins/"+ext_name+"/requirements.txt")):
        pip_install(req=globalvars.NEU_PATH+"/config/plugins/" +
                    ext_name+"/requirements.txt")  # 自动安装依赖
        # TODO: 更新环境时修复安装依赖
    typer.echo("安装完毕")


@app.command("remove")
def plug_remove(plugin_name: str):
    """卸载插件"""
    if (not os.path.exists(globalvars.NEU_PATH+"/config/plugins/" +
                           plugin_name)):
        raise typer.BadParameter("Plugin not found")
    typer.echo("卸载中")
    shutil.rmtree(globalvars.NEU_PATH+"/config/plugins/" + plugin_name)
    typer.echo("卸载完毕")


@app.command("list")
def plug_list():
    """列出插件"""
    typer.echo('\n'.join(
        os.listdir(globalvars.NEU_PATH+"/config/plugins")))


pip_typer = typer.Typer(no_args_is_help=True)


@pip_typer.command("install")
def pip_install(module_name: list[str] | None = typer.Argument(None, help="包名"), req: str | None = typer.Option(None, "-r", help="安装 requirements.txt")):
    """安装模块"""
    if (req != None):  # 指定 requirements.txt 文件
        os.system(
            f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/bin/activate && sudo pip install -r "+req)
    else:
        if (module_name == None):  # 从当前目录安装
            if (os.path.exists(globalvars.NEU_PATH+"/requirements.txt")):
                os.system(
                    f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/" +
                    "bin/activate && sudo pip install -r "+req  # type: ignore
                )
            else:
                raise typer.BadParameter("No module name")
        else:
            os.system(
                f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/bin/activate && pip install "+(
                    " ".join(module_name)
                ))


@pip_typer.command("uninstall")
def pip_uninstall(module_name: list[str] | None = typer.Argument(None, help="包名"), req: str | None = typer.Option(None, "-r", help="安装 requirements.txt")):
    """卸载模块"""
    if (req != None):
        os.system(
            f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/bin/activate && sudo pip uninstall -r "+req)
    else:
        if (module_name == None):
            if (os.path.exists(globalvars.NEU_PATH+"/requirements.txt")):
                os.system(
                    f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/" +
                    "bin/activate && sudo pip uninstall -r "+req  # type:ignore
                )
            else:
                raise typer.BadParameter("No module name")
        os.system(
            f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/bin/activate && pip uninstall " +
            (" ".join(module_name)  # type:ignore
             ))


@pip_typer.command("freeze")
def pip_freeze():
    """生成 requirements.txt"""
    os.system(
        f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/bin/activate && pip freeze")


@pip_typer.command("list")
def pip_list():
    """列出包"""
    os.system(
        f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/bin/activate && pip list")
