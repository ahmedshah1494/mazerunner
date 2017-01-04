from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import subprocess, os
from threading import BoundedSemaphore
import threading
import datetime

from models import *

# Create your views here.
def index(r):
    starter = "goForward(1.0)\n\n\n\n\n\n\n\n\n"
    try:
        codes = Code.objects.all().order_by("-time")
        print codes, len(codes)
        now = datetime.datetime.now()
        delta = now - codes[0].time.replace(tzinfo=None)
        if delta.seconds < 600:
            starter = codes[0].code
    except Exception as e: print (str(e))
    starter = starter.replace("\n", "\\n").replace("\t", "\\t")
    return render(r, 'index.html', {"starter_code": starter})

def runcode(code):
    try:
        codes = Code.objects.all().order_by("-time")
        now = datetime.datetime.now()
        try:
            c = codes[0]
            delta = now - c.time.replace(tzinfo=None)
            if delta.seconds < 600:
                print ("GOOD")
                c.code = code
                c.time = now
                print (c.code)
                c.save()
        except Exception as e:
            print (str(e))
            newcode = Code(code=code)
            newcode.save()
    except Exception as e: print (str(e))
    with open("main.py", "w") as f:
        f.write(code+"\n")
    result = subprocess.check_output("~/run", shell=True)
    return result

@csrf_exempt
def run_code(r):
    settings.GLOBAL_LOCK.acquire()
    code = r.POST["code"]
    try:
        if (settings.PROGRAM_STATE != None):
            return HttpResponse("Code is running\n")
        settings.PROGRAM_STATE = 1
    finally:
        settings.GLOBAL_LOCK.release()
    try:
        result = runcode(code)
    except:
        result = "<span class='error'> Interrupted</span>"
    settings.GLOBAL_LOCK.acquire()
    settings.PROGRAM_STATE = None
    settings.GLOBAL_LOCK.release()
    print (result)
    return HttpResponse(result)

@csrf_exempt
def stop_robot(r):
    pid_code = subprocess.check_output("ps aux | grep 'runner.py'", shell=True)
    pid = [int(s) for s in pid_code.split() if s.isdigit()][0]
    subprocess.check_output("kill " + str(pid), shell=True)
    result = subprocess.check_output("echo 'stopMoving()' | python prompt/runner.py", shell=True)
    return HttpResponse(result)

def superuser(r):
    return render(r, "superuser.html", {})

def kill_robot(r):
    return HttpResponse("ok")


