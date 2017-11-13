import os
import XmlParser
import argparse
from lazyme import color_print


## change these default variables as needed or use command line arguments  ##############################################################################################################################

git_repo_address = 'git@st-gitlab:APS/Express3-Heat.git' # The address to the git repo that you wish to move the files in SourceGear Vault to
gitDestination = "Express3-Heat" # The name of the git repo. should be the last part of the git address minus the .git

vaultRepo = "TableHeat" # change just the name of the vault repo you wish to migrate to git
vaultFolder = "EX3Heat" # change just the name of the vault folder you wish to migrate to git
vaultUser = ""
vaultPasswd = ""
vaultHost = ""

SourceGearLocation = "C:/Program Files (x86)/SourceGear/VaultPro Client "  # The location of the SourceGear Client on your machine
vault2Git_script_location = " C:\Python34\Temp4Git\VaultToGitActive\VaultToGit"  # The location of the VaultToGit.py and XmlParser.py on your machine

auto_pusher = 0
###################################################################################################################################################################

parser = argparse.ArgumentParser()

parser.add_argument("--user", "-u", help="Sourcegear Vault user\n")
parser.add_argument("--password", "-p", help="SourceGear Vault password\n")
parser.add_argument("--host", help="The host that your SourceGear Vault is located on (eq: localhost)")
parser.add_argument("--vaultrepo", "-vr", help="SourceGear Vault repo name (eq: RepoName)")
parser.add_argument("--vaultfolder", "-vf", help="SourceGear Vault folder name (eq: FolderName)")
parser.add_argument("--gitaddress", "-ga", help="The git repo address that you wish to migrate your SourceGear Vault repo to (eq: git@github.com:rapaportg/VaultToGit.git")
parser.add_argument("--gitdestination", "-gd", help="The name of the git repo. should be the last part of the git address minus the .git")
parser.add_argument("--sourcegear_location","-sgl", help="The location of the SourceGear Client on your machine")
parser.add_argument("--auto_push", "-ap", help="set to 0 or 1 if you would like the git repo to automatically push")

args = parser.parse_args()

if args.user:
    vaultUser = args.user

if args.password:
    vaultPasswd = args.password

if args.host:
    vaultHost = args.host

if args.vaultrepo:
    vaultRepo = args.vaultrepo

if args.vaultfolder:
    vaultFolder = args.vaultfolder

if args.gitaddress:
    git_repo_address = args.gitaddress

if args.gitdestination:
    gitDestination = args.gitdestination

if args.sourcegear_location:
    SourceGearLocation = args.sourcegear_location

if args.auto_push:
    auto_pusher = args.auto_push    


# initalizing local git repo
os.system('cd /D C:\Temp && git clone ' + git_repo_address)
os.system('git config user.name "Vault"')

# Grabing the Revision History to use as a guide for cloning each commit
credentials = " -host " + vaultHost + " -user " + vaultUser + " -password " + vaultPasswd
getRevHistory = "vault VERSIONHISTORY " + credentials
beginVersion = " -beginversion 0 "
RevHistoryLocation = ' "C:/Temp/temp.xml"'
vaultFolder_full = " $/" + vaultFolder
getRevHistoryCommand = getRevHistory + " -repository " + vaultRepo + beginVersion + vaultFolder_full + " > " + RevHistoryLocation

#print("\n",getRevHistoryCommand, '\n')

os.system("cd /D " + SourceGearLocation + "&& " + getRevHistoryCommand)
#os.system("cd /D"+ vault2git_script_location)

XmlParser.init()
comments = XmlParser.CommentA()
version = XmlParser.VersionA()
txid = XmlParser.TxidA()
objverid = XmlParser.ObjveridA()
date = XmlParser.DateA()
user = XmlParser.UserA()

gitDestination_full = " C:/Temp/" + gitDestination

# if the script fails part way through change startVersion to match the last know vault version to be committed to git.
# vault version are recorded at the beginning of the git commit messages 
startVersion = 0

loopLength = len(version)
print('\n\nThere are ', loopLength, ' commits to migrate\n\n')

for x in range(startVersion, loopLength, 1):
    commit_version = str(version[x])
    commit_user = str(user[x])
    commit_message = str(comments[x])
    commit_txid = str(txid[x]) 
    commit_objverid = str(objverid[x])
    commit_date = str(date[x])

    git_commit_msg = '"'+ commit_version + "  " + "VaultToGit: " + commit_date + " | " + commit_message +'"'

    getRepoCommand = "vault GETVERSION" + credentials +" -repository " + vaultRepo +" "+ commit_version + vaultFolder_full +" " + gitDestination_full
    #print('\n\n', getRepoCommand, '\n\n')
    print('\n\n', git_commit_msg, '\n\n')
    os.system("cd /D " + SourceGearLocation + " && " + getRepoCommand)    

    os.system("cd /D " + gitDestination_full + " && " + "git add --all .")
    git_commit = "cd /D " + gitDestination_full + " && "+ " git commit -a -m " + git_commit_msg
    git_user_email = commit_user+'@autobag.com'
    os.system(git_commit + ' --author '+'"'+ commit_user + '<'+ git_user_email +'>"')

    clearWorkingDir = "cd /D " + gitDestination_full + ' && git rm *'
    os.system(clearWorkingDir)

if auto_pusher == 1:
    os.system("git push origin master")
else:
    color_print("To push the git repository please go to the directory it is located in review the repo and push manually", color="green")