#!/usr/bin/python3

## LINUX ONLY

## Build Flags
#
# --windows [default:linux] - compile target for windows
# --gdb [default:disabled] - enables cmd debugger
#
##

import os, sys, subprocess

CC = "g++"
C = "gcc"

libs = []  # ex -lGL


def genmain():
    o = []

    BPLATE = genbplate()

    o.extend(
        [
            "int main(int argc, char **argv) {",
            BPLATE,
        ]
    )

    o.append("}")
    o = "\n".join(o)
    return o


def genconways():
    CODE = """

    """
    return CODE


def genbplate():
    BPLATE = """
    
    """

    return BPLATE


srcdir = os.path.abspath(".")


def build():
    cpps = []
    obfiles = []

    open("/tmp/gen.main.cpp", "wb").write(genmain().encode("utf-8"))
    file = "/tmp/gen.main.cpp"
    print(file)
    ofile = "%s.o" % file
    obfiles.append(ofile)
    cpps.append(file)
    cmd = [
        #'gcc',
        C,
        "-c",  ## do not call the linker
        "-fPIC",  ## position indepenent code
        "-o",
        ofile,
        os.path.join(file),
    ]
    print(cmd)
    subprocess.check_call(cmd)

    os.system("ls -lh /tmp/*.o")

    ## finally call the linker,
    ## note: there's better linkers we could use here, like gold and mold

    cmd = (
        [
            #'ld',
            C,
            "-shared",
            "-o",
            "/tmp/eoncalc.so",
        ]
        + obfiles
        + libs
    )

    print(cmd)
    subprocess.check_call(cmd)

    exe = "/tmp/eoncalc"
    cmd = [
        C,
        "-o",
        exe,
    ]
    cmd += obfiles + libs

    print(cmd)

    subprocess.check_call(cmd)


build()

if "--gdb" in sys.argv:
    cmd = ["gdb", "/tmp/eoncalc"]
else:
    cmd = ["/tmp/eoncalc"]

print(cmd)

subprocess.check_call(cmd, cwd=srcdir)
# sys.exit()

## TODO: get working from python for testing
import ctypes

os.chdir(srcdir)

eoncalc_so = "/tmp/eoncalc.so"

dll = ctypes.CDLL(eoncalc_so)
print(dll)

print(dll.main)
dll.main()

print("hello!")
