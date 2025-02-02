import typer
import tarfile
import os
import shutil
import random
import tomllib
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
    USER_PLUGIN_PATH = globalvars.NEU_PATH+"/config/plugins"
    if (not os.path.exists(plugin_path)):
        raise typer.BadParameter("Plugin not found")

    rand_id = ".cache"+str(random.randint(100000, 999999))  # 生成随机目录
    typer.echo("开始安装")
    os.makedirs(USER_PLUGIN_PATH+"/" +
                rand_id, exist_ok=True)
    if (os.path.isfile(plugin_path)):
        typer.echo("解压插件")

        def unzip_cmd():
            try:
                with tarfile.open(plugin_path, "r:xz") as tar:  # 解压
                    tar.extractall(USER_PLUGIN_PATH+os.sep +
                                   rand_id)
                return False
            except:
                return True
        if (unzip_cmd()):
            typer.echo("解压失败\n正在清理")
            shutil.rmtree(USER_PLUGIN_PATH+os.sep+rand_id)
            raise typer.BadParameter("Unzip failed")
    else:
        typer.echo("复制插件")
        shutil.copytree(plugin_path, USER_PLUGIN_PATH+os.sep +
                        rand_id)  # 直接复制
    typer.echo("读取元信息")
    try:
        with open(USER_PLUGIN_PATH+os.sep+rand_id+os.sep+"manifest.toml",
                  "r") as f:
            manifest = tomllib.loads(f.read())
        real_plug_name = manifest["common"]["name"]
        typer.echo(
            "  插件 id: "+real_plug_name)
        typer.echo(
            "  插件版本: "+manifest["common"]["version"])
        typer.echo(
            "  插件作者: "+manifest["common"]["author"])
        typer.echo(
            "  插件描述: "+manifest["common"]["description"])
    except:  # 利用KeyError同时检查元数据
        typer.echo("读取元信息失败"+"\n正在清理")
        shutil.rmtree(USER_PLUGIN_PATH+os.sep+rand_id)
        raise typer.BadParameter("Read manifest failed")
    plug_path = USER_PLUGIN_PATH+os.sep+real_plug_name
    if (os.path.exists(plug_path)):
        typer.echo("删除旧版本")
        shutil.rmtree(plug_path)
    if (os.path.exists(plug_path+".disable")):  # 处理禁用的情况
        typer.echo("删除旧版本")
        shutil.rmtree(plug_path+".disable")
    shutil.move(USER_PLUGIN_PATH+os.sep+rand_id, plug_path)
    # if (os.path.exists(globalvars.NEU_PATH+"/config/plugins/"+ext_name+"/requirements.txt")):
    #     pip_install(req=globalvars.NEU_PATH+"/config/plugins/" +
    #                 ext_name+"/requirements.txt")  # 自动安装依赖
    #     # TODO: 更新环境时修复安装依赖
    typer.echo("安装完毕")


@app.command("disable")
def plug_disable(plugin_name: str):
    """禁用插件"""
    if (not os.path.exists(globalvars.NEU_PATH+"/config/plugins/" +
                           plugin_name)):
        raise typer.BadParameter("Plugin not found")
    shutil.move(globalvars.NEU_PATH+"/config/plugins/" +
                plugin_name, globalvars.NEU_PATH+"/config/plugins/" +
                plugin_name+".disable")


@app.command("enable")
def plug_enable(plugin_name: str):
    """启用插件"""
    if (not os.path.exists(globalvars.NEU_PATH+"/config/plugins/" +
                           plugin_name+".disable")):
        raise typer.BadParameter("Plugin not found")
    shutil.move(globalvars.NEU_PATH+"/config/plugins/" +
                plugin_name+".disable", globalvars.NEU_PATH+"/config/plugins/" +
                plugin_name)


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
        [i for i in os.listdir(globalvars.NEU_PATH+"/config/plugins") if
         (i != "neuplugin"
          and i != ".NEUTRON_PLUGIN"
          and not i.startswith(".cache")
          and os.path.exists(globalvars.NEU_PATH+"/config/plugins"+os.sep+i+os.sep+"manifest.toml"))]))


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
