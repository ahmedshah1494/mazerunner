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
    starter = "robot.moveDistanceSmart(1.0)\n\n\n\n\n\n\n\n\n"
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
    if settings.IS_RUNNING == 1:
        result = "<span class='error'> iRobot Busy </span>"
        return HttpResponse(result)
    settings.IS_RUNNING = 1
    settings.GLOBAL_LOCK.acquire()
    dirPath = "/root/server/irobot/static/snapshots"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        os.remove(dirPath+"/"+fileName)
    code = r.POST["code"]
    try:
        pid_code = subprocess.check_output("ps aux | grep 'identify.py'", shell=True)
        pid = [int(s) for s in pid_code.split() if s.isdigit()][0]
        subprocess.check_output("kill " + str(pid), shell=True)
        result = subprocess.check_output("echo 'robot.robot.safe()\nrobot.close()' | python runner.py", shell=True)
        result = "<span class='error'> Good Luck :)</span>"
        return HttpResponse(result)
    except:
        pass

    try:
        pid_code = subprocess.check_output("ps aux | grep 'runner.py'", shell=True)
        pid = [int(s) for s in pid_code.split() if s.isdigit()][0]
        subprocess.check_output("kill " + str(pid), shell=True)
    except:
        pass
    
    try:
        result = runcode(code)
    except:
        result = "<span class='error'> Interrupted</span>"
    finally:
        settings.IS_RUNNING = 0
        settings.GLOBAL_LOCK.release()
    print (result)
    return HttpResponse(result)

@csrf_exempt
def stop_robot(r):
    pid_code = subprocess.check_output("ps aux | grep 'runner.py'", shell=True)
    pid = [int(s) for s in pid_code.split() if s.isdigit()][0]
    subprocess.check_output("kill " + str(pid), shell=True)
    result = subprocess.check_output("echo 'robot.close()' | python runner.py", shell=True)
    return HttpResponse(result)

def superuser(r):
    return render(r, "superuser.html", {})

def kill_robot(r):
    return HttpResponse("ok")


