import os
import typer
from enum import Enum
from neutools import templates
from neutools import globalvars


class templateTypeEnum(str, Enum):
    application = "application"
    addition = "addition"
    simple = "simple"


template_list = {
    "application": templates.applicationTemplate,
    "addition": templates.additionTemplate,
    "simple": templates.simpleTemplate
}


app = typer.Typer(no_args_is_help=True)


@app.command()
def create(name: str, path: str = ".", template: templateTypeEnum = templateTypeEnum.application):
    """从模板创建"""
    template_use = template_list[template.value]
    args_res = {}
    args_res["name"] = name
    typer.echo(f"\033[34m使用模板\033[0m: {template.value}")
    for k, v in template_use.get_args.items():  # 获取模板参数
        args_res[k] = typer.prompt("\033[34m"+v+"\033[0m", prompt_suffix=": ")
    template_c = template_use(args_res)
    os.makedirs(path+os.sep+name, exist_ok=True)
    for i in template_c.create_dirs():
        os.makedirs(path+os.sep+name+os.sep+i, exist_ok=True)
    typer.echo("\033[32m创建中\033[0m...")
    for k, v in template_c.create_files().items():
        if (type(v) == str):  # 字符串
            with open(path+os.sep+name+os.sep+k, "w") as f:
                f.write(v)
        else:  # 字节流
            with open(path+os.sep+name+os.sep+k, "wb") as f:
                f.write(v)
    typer.echo("\033[32m创建完成！\033[0m")


@app.command()
def run(path: str = ".", port=1231):
    """运行"""
    if (not os.path.exists(globalvars.NEU_PATH)):
        raise ModuleNotFoundError(
            "Cannot Find neutron panel!\nYou can use \"--neu-path\" to set the path.")
    if (not os.path.exists(path+os.sep+"manifest.toml")):  # 检查描述文件
        raise FileNotFoundError(
            "manifest.toml is missing, maybe it is not a valid plugin.")
    abs_path = os.path.abspath(path)
    os.system(
        f"cd {globalvars.NEU_PATH} && source {globalvars.NEU_PATH}/venv/bin/activate && sudo python main.py --set-config:server.port={port} --set-config:debug.debug=True --add-config:plugin.load_single_plugins={abs_path}")  # 启动
