from IPython.display import display, HTML, clear_output
from pathlib import Path
import subprocess
import requests
import sys


def progress(value, max):
    p = int(100 * value / max)
    html = f"<div style='font-size: 18px; display: flex; justify-content: space-between; width:25%;'><span>Manim Installation</span><span>{p}%</span></div><progress value='{value}' max='{max}' style='width: 25%; accent-color: #41FDFE;'></progress>"
    return HTML(html)


def find_package(pkg):
    cmd = ("dpkg", "-s", pkg)
    process = subprocess.run(cmd)
    found = process.returncode == 0
    return found


def install_manim(lite=False):
    cmd = [("apt-get", "-qq", "update")]

    if not lite and not find_package("texlive"):
        latex_pkg = (
            "texlive",
            "texlive-latex-extra",
            "texlive-science",
            "texlive-fonts-extra",
        )
        for pkg in latex_pkg:
            cmd.append(("apt-get", "-qq", "install", "-y", pkg))

    if not "manim" in sys.modules:
        cmd.append(("apt-get", "-qq", "install", "-y", "libpango1.0-dev"))
        cmd.append(("uv", "pip", "install", "-q", "--system", "manim"))
        # cmd.append(("uv", "pip", "install", "-q", "--system", "IPython==8.21.0"))

    n = len(cmd)

    if n > 1:
        # [optional font] STIX Two Text (stixfonts.org)
        font_url = "https://raw.githubusercontent.com/stipub/stixfonts/master/fonts/static_ttf/STIXTwoText-Regular.ttf"
        font_path = "/usr/share/fonts/truetype/stixfonts"
        font_cmd = ("wget", "-nv", "-nc", "-P", font_path, font_url)
        subprocess.run(font_cmd)

        output = display(progress(0, n), display_id=True)

        for i, c in enumerate(cmd, 1):
            subprocess.run(c)
            output.update(progress(i, n))


def config_manim(about=True):
    config.disable_caching = True
    config.verbosity = "WARNING"
    config.media_width = "50%"
    config.media_embed = True

    Text.set_default(font="STIX Two Text")

    clear_output()

    if about:
        info = f"Manim – Mathematical Animation Framework (Version {version('manim')})\nhttps://www.manim.community"
        print(info)


def add_plugins():
    mscene_path = Path(__file__).parent

    plugin_url = "https://raw.githubusercontent.com/curiouswalk/mscene/refs/heads/main/plugins/source"

    plugins_py = f"{plugin_url}/plugins.py"

    text = requests.get(plugins_py).text.strip().split()

    plugins = ["plugins"]

    for t in text:
        if "." in t:
            plugins.append(t.lstrip("."))

    # plugins_str = ", ".join(plugins[1:])

    for p in plugins:
        filename = f"{p}.py"
        path = f"{mscene_path}/{filename}"
        url = f"{plugin_url}/{filename}"
        cmd = ("wget", "-nv", "-O", path, url)
        subprocess.run(cmd)

    msg = f"Mscene Plugins: Enhance the Features of Manim\nhttps://mscene.curiouswalk.com/plugins"
    print(msg)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "manim" in args and len(args) == 1:
        install_manim()

        from manim import *

        config_manim()

    elif all(i in args for i in ("-l", "manim")) and len(args) == 2:
        install_manim(lite=True)

        from manim import *

        config_manim()

    elif "plugins" in args and len(args) == 1:
        add_plugins()

    elif "-h" in args and len(args) == 1:
        cmd_info = (
            "— Run '%mscene -l manim' to install Manim without LaTeX.",
            "— Run '%mscene manim' to install Manim with LaTeX.",
            "— Run '%mscene mscene' to render an example scene.",
            "— Run '%mscene plugins' to add Manim plugins.",
        )

        print("Commands", "-" * 8, *cmd_info, sep="\n")

    elif "mscene" in args and len(args) == 1:
        if not "manim" in sys.modules:
            install_manim(lite=True)

        from manim import *

        config_manim(about=False)

        from IPython import get_ipython

        ipy = get_ipython()

        class ExampleScene(Scene):
            def construct(self):
                banner = ManimBanner()
                self.play(banner.create())
                self.play(banner.expand())
                self.wait(1.5)

        ipy.run_line_magic("manim", "-qm ExampleScene")

    else:
        print("Error: Invalid Command\nRun '%mscene -h' to view commands.")
