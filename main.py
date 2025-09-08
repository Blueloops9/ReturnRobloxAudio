import requests as r,os,glob,time

Webserver = "https://darkbluestealth.pythonanywhere.com/static/"
USER = os.path.expanduser("~")

RobloxLogsDirectory = USER+"\\AppData\\Local\\Roblox\\logs\\*"
RobloxVersionsDirectory = USER+"\\AppData\\Local\\Roblox\\Versions"
RobloxClientVersions = [RobloxVersionsDirectory+"\\"+x for x in os.listdir(RobloxVersionsDirectory) if os.path.isdir(RobloxVersionsDirectory+"\\"+x) and os.path.exists(RobloxVersionsDirectory+"\\"+x+"\\RobloxPlayerBeta.exe")]
RobloxVersion = max(RobloxClientVersions,key=os.path.getctime)

SoundsFolder = RobloxVersionsDirectory+"\\"+RobloxVersion+"\\content\\sounds\\"

Logs=[x for x in glob.glob(RobloxLogsDirectory) if x.find("Player") > -1]
LogFile = max(Logs,key=os.path.getctime)

def Follow(File):
    File.seek(0,2)
    while True:
        Line = File.readline()
        if not Line:
            time.sleep(0.1)
            continue
        yield Line

Str = "[FLog::Error] Error: Failed to load sound "

f = open(LogFile,"r")
Lines = Follow(f)
for Line in Lines:
    Dat = Line.find(Str)
    if Dat > -1 and Line.find("rbxasset://") > -1:
        Text=Line[Dat+len(Str):]
        Name = Text[Text.find("sounds/")+7:Text.find(": ")]
        Dat = r.get(Webserver+Name,headers={"Accept-Encoding":"gzip"})
        if Dat.status_code!=404:
            File = open(SoundsFolder+Name,"wb")
            File.write(Dat.content)
            File.close()
