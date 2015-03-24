import os
import sys
import os.path
import subprocess
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

from scripts import utils


def call_script(name, *args, python=sys.executable):
    path = os.path.join(os.path.dirname(__file__), name)
    subprocess.check_call([python, path] + list(args))


def build_common(args):
    """Common buildsteps used for all OS'."""
    utils.print_title("Running asciidoc2html.py")
    if args.asciidoc is not None:
        a2h_args = ['--asciidoc'] + args.asciidoc
    else:
        a2h_args = []
    call_script('asciidoc2html.py', *a2h_args)


def build_windows():
    """Build windows executables/setups."""
    ver = ''.join([str(sys.version_info.major), str(sys.version_info.minor)])
    python_x86 = r'C:\Python{}_x32\python.exe'.format(ver)
    python_x64 = r'C:\Python{}\python.exe'.format(ver)

    utils.print_title("Running 32bit freeze.py build_exe")
    call_script('freeze.py', 'build_exe', python=python_x86)
    utils.print_title("Running 64bit freeze.py build_exe")
    call_script('freeze.py', 'build_exe', python=python_x64)
    utils.print_title("Running 32bit freeze.py bdist_msi")
    call_script('freeze.py', 'bdist_msi', python=python_x86)
    utils.print_title("Running 64bit freeze.py bdist_msi")
    call_script('freeze.py', 'bdist_msi', python=python_x64)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--asciidoc', help="Full path to python and "
                        "asciidoc.py. If not given, it's searched in PATH.",
                        nargs=2, required=False,
                        metavar=('PYTHON', 'ASCIIDOC'))
    args = parser.parse_args()
    utils.change_cwd()
    if os.name == 'nt':
        build_common(args)
        build_windows()
    else:
        print("This script does nothing except on Windows currently.")


if __name__ == '__main__':
    main()
