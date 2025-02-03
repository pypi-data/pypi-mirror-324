import subprocess
from install_qt_creator.desktop import create_shortcut

arg0 = "msys2.cmd -defterm -here -no-start -ucrt64 -c".split()
arg1 = " ".join(
    [
        "pacman",
        "-S",
        "--needed",
        "--noconfirm",
        "mingw-w64-ucrt-x86_64-toolchain",
        "mingw-w64-ucrt-x86_64-cmake",
        "mingw-w64-ucrt-x86_64-clang-libs",
        "ucrt64/mingw-w64-ucrt-x86_64-qt-creator-devel",
        "ucrt64/mingw-w64-ucrt-x86_64-qt-creator-docs",
    ]
)


def main():
    args = arg0
    args.append(arg1)
    # print(args)
    subprocess.run(args)
    dst = subprocess.getoutput(
        'msys2 -defterm -here -no-start -ucrt64 -c "cygpath -m /ucrt64/bin/qtcreator.exe"'
    )
    create_shortcut(dst)


if __name__ == "__main__":
    main()
