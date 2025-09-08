import requests as r,os,glob,time

Webserver = "https://darkbluestealth.pythonanywhere.com/static/"
RobloxLogsDirectory = "\\AppData\\Local\\Roblox\\logs\\"
RobloxVersionsDirectory = "\\AppData\\Local\\Roblox\\Versions"

if os.path.exists("settings"):
    File = open("settings","r")
    Dat = File.read().split("\n")
    for I in Dat:
        A = I.find("=")
        Name,Value = I[:A],I[A+1:]
        if Name=="Webserver":Webserver=Value
        if Name=="Logs":RobloxLogsDirectory=Value
        if Name=="Versions":RobloxVersionsDirectory=Value
    File.close()
else:
    File = open("settings","w")
    File.write("""Webserver={}
Logs={}
Versions={}""".format(Webserver,RobloxLogsDirectory,RobloxVersionsDirectory))
    File.close()

USER = os.path.expanduser("~")

RobloxLogsDirectory=USER+RobloxLogsDirectory+"*"
RobloxVersionsDirectory=USER+RobloxVersionsDirectory
RobloxClientVersions = [RobloxVersionsDirectory+"\\"+x for x in os.listdir(RobloxVersionsDirectory) if os.path.isdir(RobloxVersionsDirectory+"\\"+x) and os.path.exists(RobloxVersionsDirectory+"\\"+x+"\\RobloxPlayerBeta.exe")]
RobloxVersion = max(RobloxClientVersions,key=os.path.getctime)

SoundsFolder = RobloxVersion+"\\content\\sounds\\ReturnRobloxAudio\\"

if not os.path.exists(SoundsFolder):
    os.makedirs(SoundsFolder)

Logs=[x for x in glob.glob(RobloxLogsDirectory) if x.find("Player") > -1]
LogFile = max(Logs,key=os.path.getctime)

def Follow(File):
    try:
        File.seek(0,2)
        while True:
            Line = File.readline()
            if not Line:
                time.sleep(0.1)
                continue
            yield Line
    except KeyboardInterrupt:
        Dat = input("Would you like to clear the cache? (Y/N): ")
        if Dat[0].lower()=="y":
            for i in os.listdir(SoundsFolder):
                if os.path.isfile(SoundsFolder+i):os.unlink(SoundsFolder+i)
        print("Goodbye!")
        time.sleep(3)
        quit()

Str = "[FLog::Error] Error: Failed to load sound "

f = open(LogFile,"r")
Lines = Follow(f)
for Line in Lines:
    Dat = Line.find(Str)
    if Dat > -1 and Line.find("rbxasset://") > -1:
        Text=Line[Dat+len(Str):]
        Name = Text[Text.find("ReturnRobloxAudio/")+18:Text.find(": ")]
        print("Found "+Name)
        Dat = r.get(Webserver+Name,headers={"Accept-Encoding":"gzip"})
        if Dat.status_code!=404:
            print("Saved "+Name)
            File = open(SoundsFolder+Name,"wb")
            File.write(Dat.content)
            File.close()
