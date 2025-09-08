import requests as r,os,glob,time
USER = os.path.expanduser("~")

RobloxLogsDirectory = USER+"\\AppData\\Local\\Roblox\\logs\\*"
RobloxVersionsDirectory = USER+"\\AppData\\Local\\Roblox\\Versions"
#RobloxVersions = [x[0] for x in os.walk(BloxstrapInstallment)]
#RobloxVersion = RobloxVersionDirectories[1] # Sometime studio gets in the way so it's disabled for manual insertion
SoundsFolder = RobloxVersionsDirectory+"\\"+"version-c1ac69007bdc4e48"+"\\content\\sounds\\"

Logs=glob.glob(RobloxLogsDirectory)
LogFile = max(Logs,key=os.path.getctime)

def Follow(File):
    File.seek(0,2)
    while True:
        Line = File.readline()
        if not Line:
            time.sleep(0.1)
            continue
        yield Line

f = open(LogFile,"r")
Lines = Follow(f)
Str = "[FLog::Error] Error: Failed to load sound "
for Line in Lines:
    Dat = Line.find(Str)
    if Dat > -1 and Line.find("rbxasset://") > -1:
        Text=Line[Dat+len(Str):]
        Name = Text[Text.find("sounds/")+7:Text.find(": ")]
        # The website used for this is only temp for now until I can get something better
        Dat = r.get("https://darkbluestealth.pythonanywhere.com/static/"+Name,headers={"Accept-Encoding":"gzip"})
        if Dat.status_code!="404":
            print("Got data.")
            File = open(SoundsFolder+Name,"wb")
            File.write(Dat.content)
            File.close()
