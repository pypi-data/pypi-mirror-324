import subprocess

def figlet(src):
    return subprocess.check_output("figlet -w 200 '%s'" % src, shell=True, universal_newlines=True).split("\n")

def figletsmall(src):
    return subprocess.check_output("figlet -f small -w 200 '%s'" % src, shell=True, universal_newlines=True).split("\n")
