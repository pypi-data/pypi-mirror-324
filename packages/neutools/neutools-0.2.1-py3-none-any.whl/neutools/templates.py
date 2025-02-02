class applicationTemplate():
    get_args = {
        "description": "描述",
        "version": "版本",
        "author": "作者",
        "license": "开源许可证协议",
        "url": "项目主页",
        "app_name": "应用名称"
    }

    def __init__(self, args):
        self.args = args

    def create_dirs(self):
        return [
            "ui",
            "static",
            "server",
            "static/css",
            "static/js",
            ".vscode"
        ]

    def create_files(self):
        return {
            f"static/css/{self.args['name']}.css": """body {
    margin: 0;
    padding: 0;
}
""",
            f"static/js/{self.args['name']}.js": f"""neutron.setTitle("{self.args['app_name']}")
neutron.setMinSize(500, 300)
neutron.getInfo((data) => {{
    if (data[0]["h"] < 300) {{
        neutron.setWinSize(500, 300)
    }}
}});
""",
            "ui/index.html": f"""<html lang="zh-cn">
<head>
    <meta charset="UTF-8">
    <title>{self.args['name']}</title>
    <script src="{{{{winapi}}}}"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{{{static}}}}/css/{self.args['name']}.css">
    <script src="{{{{static}}}}/js/{self.args['name']}.js"></script>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>""",
            "icon.png": b'\x89PNG\r\n\x1a\n\x00\x00',
            "permission.toml": "",
            "server/main.py": """from neutron import Plugin,execute

app = Plugin(__file__)

@app.route.get("/")
async def hello():
    return "Hello, World!"
""",
            "manifest.toml": f"""
[common]
name = "{self.args['name']}"
version = "{self.args['version']}"
description = "{self.args['description']}"
author = "{self.args['author']}"
license = "{self.args['license']}"
url = "{self.args['url']}"

[icon]
name = "{self.args['app_name']}"
image = "icon.png"

[window]
path = "ui"
static = "static"

[api]
path = "server/main.py"
object = "app"
permission = "permission.toml"

""",
            ".vscode/settings.json": """{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.extraPaths": [
        "/opt/neutron/neutron/server/api"
    ],
}""",
            "jsconfig.json": """{
    "include": [
        "./static/js/**/*.js"
    ],
    "typeAcquisition": {
        "include": [
            "/opt/neutron/neutron/static/js/api.d.ts"
        ]
    },
    "exclude": [
        "./static"
    ]
}""",
        }


class additionTemplate():
    get_args = {
        "description": "描述",
        "version": "版本",
        "author": "作者",
        "license": "开源许可证协议",
        "url": "项目主页"
    }

    def __init__(self, args):
        self.args = args

    def create_dirs(self):
        return [
            ".vscode"]

    def create_files(self):
        return {

            f"{self.args['name']}.js": "",
            f"{self.args['name']}.py": "",
            f"{self.args['name']}.css": "",
            "jsconfig.json": """{
    "include": [
        "./static/js/**/*.js"
    ],
    "typeAcquisition": {
        "include": [
            "/opt/neutron/neutron/static/js/api.d.ts"
        ]
    },
    "exclude": [
        "./static"
    ]
}""",
            "manifest.toml": f"""
[common]
name = "{self.args['name']}"
version = "{self.args['version']}"
description = "{self.args['description']}"
author = "{self.args['author']}"
license = "{self.args['license']}"
url = "{self.args['url']}"

[addition]
js = "{self.args['name']}.js"
css = "{self.args['name']}.css"
py = "{self.args['name']}.py"

""",
            ".vscode/settings.json": """{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.extraPaths": [
        "/opt/neutron/neutron/server/api"
    ],
}"""
        }


class simpleTemplate():
    get_args = {
        "description": "描述",
        "version": "版本",
        "author": "作者",
        "license": "开源许可证协议",
        "url": "项目主页"
    }

    def __init__(self, args):
        self.args = args

    def create_dirs(self):
        return []

    def create_files(self):
        return {
            "manifest.toml": f"""
[common]
name = "{self.args['name']}"
version = "{self.args['version']}"
description = "{self.args['description']}"
author = "{self.args['author']}"
license = "{self.args['license']}"
url = "{self.args['url']}"
"""
        }
