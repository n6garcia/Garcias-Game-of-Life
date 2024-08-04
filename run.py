#!/usr/bin/python3

## LINUX ONLY

## Build Flags
#
# --windows [default:linux] - compile target for windows
# --gdb [default:disabled] - enables cmd debugger
#
##

import os, sys, subprocess
from random import random, uniform

CC = "g++"
C = "gcc"

libs = []  # ex -lGL


def genmain():
    o = []

    CONWH = genconwh()
    HEADER = genheader()
    BPLATE = genbplate()

    o.extend(
        [
            HEADER,
            CONWH,
            "int main() {",
            BPLATE,
        ]
    )

    o.append("}")
    o = "\n".join(o)
    return o


def genconwh():
    CODE = r"""
#define CELL(I,J) (field[size*(I)+(J)])
#define ALIVE(I,J) t[size*(I)+(J)] = 1
#define DEAD(I,J)  t[size*(I)+(J)] = 0

int count_alive(const char *field, int i, int j, int size){
    int x, y, a=0;
    for(x=i-1; x <= (i+1) ; x++)
    {
        for(y=j-1; y <= (j+1) ; y++)
        {
            if ( (x==i) && (y==j) ) continue;
            if ( (y<size) && (x<size) &&
                (x>=0)   && (y>=0) )
            {
                a += CELL(x,y);
            }
        }
    }
    return a;
}

void evolve(const char *field, char *t, int size) {
    int i, j, alive, cs;
    for(i=0; i < size; i++)
    {
        for(j=0; j < size; j++)
        {
            alive = count_alive(field, i, j, size);
            cs = CELL(i,j);
            if ( cs )
            {
                if ( (alive > 3) || ( alive < 2 ) )
                    DEAD(i,j);
                else
                    ALIVE(i,j);
            } else {
                if ( alive == 3 )
                    ALIVE(i,j);
                else
                    DEAD(i,j);
            }
        }
    }
}

void dump_field(const char *f, int size) {
    int i;
    int ln = 0;
    for (i=0; i < (size*size); i++) {
        if (f[i]) printf("X");
        else printf(".");
        ln ++;
        if (ln >= size){
            ln = 0;
            printf("\n");
        }
    }
    printf("\n=====================\n");
}
    """
    return CODE


def genheader():
    CODE = """
#include <stdio.h>

#define BLINKER_SIZE 3
#define BLINKER_GEN 3
char small_blinker[] = {
    0,0,0,
    1,1,1,
    0,0,0
};
char temp_blinker[BLINKER_SIZE*BLINKER_SIZE];

#define FIELD_SIZE 45
#define FIELD_GEN 175
char field[FIELD_SIZE * FIELD_SIZE];
char temp_field[FIELD_SIZE*FIELD_SIZE];

/* set the cell i,j as alive */
#define SCELL(I,J) field[FIELD_SIZE*(I)+(J)] = 1


    """
    return CODE


def genbplate(gliders=16):
    a = [
        """
    int i;
    char *fa, *fb, *tt;
    for(i=0; i < (FIELD_SIZE*FIELD_SIZE) ; i++) field[i]=0;
    """
    ]

    for g in range(gliders):
        x = int(random() * 40)
        y = int(random() * 40)
        a += [
            "SCELL(0+%s, 1+%s);" % (x, y),
            "SCELL(1+%s, 2+%s);" % (x, y),
            "SCELL(2+%s, 0+%s);" % (x, y),
            "SCELL(2+%s, 1+%s);" % (x, y),
            "SCELL(2+%s, 2+%s);" % (x, y),
        ]
    a.append(
        r"""
    /* evolve */
    fa = field;
    fb = temp_field;
    for (i=0; i < FIELD_GEN; i++) {
        dump_field(fa, FIELD_SIZE);
        evolve(fa, fb, FIELD_SIZE);
        tt = fb; fb = fa; fa = tt;
    }
    return 0;
    """
    )

    return "\n".join(a)


srcdir = os.path.abspath(".")


def build():
    cpps = []
    obfiles = []
    ffl = []

    open("/tmp/gen.ngol.main.cpp", "wb").write(genmain().encode("utf-8"))
    file = "/tmp/gen.ngol.main.cpp"
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

    ctr = 1
    for ff in ffl:
        fn = "gen.ngol." + ctr + ".cpp"
        open("/tmp/" + fn, "wb").write(ff().encode("utf-8"))
        file = "/tmp/" + fn
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
            "/tmp/ngol.so",
        ]
        + obfiles
        + libs
    )

    print(cmd)
    subprocess.check_call(cmd)

    exe = "/tmp/ngol"
    cmd = [
        C,
        "-o",
        exe,
    ]
    cmd += obfiles + libs

    print(cmd)

    subprocess.check_call(cmd)


print("building...")
build()

if "--gdb" in sys.argv:
    cmd = ["gdb", "/tmp/ngol"]
else:
    cmd = ["/tmp/ngol"]

print(cmd)

subprocess.check_call(cmd, cwd=srcdir)
# sys.exit()

## TODO: get working from python for testing
import ctypes

os.chdir(srcdir)

ngol_so = "/tmp/ngol.so"

dll = ctypes.CDLL(ngol_so)
print(dll)

print(dll.main)
dll.main()

print("hello!")
