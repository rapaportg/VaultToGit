import os
import XmlParser

## change these variables as needed ##############################################################################################################################

git_repo_address = 'git@st-gitlab:APS/Express3-Heat.git' # The address to the git repo that you wish to move the files in SourceGear Vault to
gitDestination = "Express3-Heat" # The name of the git repo. should be the last part of the git address minus the .git

vaultRepo = "TableHeat" # change just the name of the vault repo you wish to migrate to git
vaultFolder = "EX3Heat" # change just the name of the vault folder you wish to migrate to git
vaultUser = "vpuser"
vaultPasswd = "archive"
vaultHost = "st-eng"

SourceGearLocation = "C:/Program Files (x86)/SourceGear/VaultPro Client "  # The location of the SourceGear Client on your machine
vault2Git_script_location = " C:\Python34\Temp4Git\VaultToGitActive\VaultToGit"  # The location of the VaultToGit.py and XmlParser.py on your machine

###################################################################################################################################################################

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

    os.system("cd /D " + gitDestination_full + " && " + "git add .")
    git_commit = "cd /D " + gitDestination_full + " && "+ " git commit -m " + git_commit_msg
    os.system(git_commit + ' --author '+'"'+ commit_user + '<>"')

    clearWorkingDir = "cd /D " + gitDestination_full + ' && git rm *'
    os.system(clearWorkingDir)



#os.system("git push")
