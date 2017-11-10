import os
import XmlParser

## change these variables as needed ##############################################################################################################################

git_repo_address = 'git@st-gitlab:APS/Express3-Heat.git' # The address to the git repo that you wish to move the files in SourceGear Vault to
gitDestination = "Express3-Heat" # The name of the git repo. should be the last part of the git address minus the .git

vaultRepo = "TableHeat"
vaultFolder = "EX3Heat" # just the name of the vault folder you wish to migrate to git

SourceGearLocation = "C:/Program Files (x86)/SourceGear/VaultPro Client "
vault2Git_script_location = " C:/Python34/Lunch Break/VaultToGit"

###################################################################################################################################################################

# initalizing local git repo
os.system('cd /D C:\Temp && git clone ' + git_repo_address)
os.system('git config user.name "Vault"')

# optional: git branch 
#branch = "Master"
#os.system('git checkout -b ' + branch)

# Grabing the Revision History to use as a guide for cloning each commit
getRevHistory = "vault VERSIONHISTORY -user vpuser -host st-eng -password archive -repository "
beginVersion = " -beginversion 0 "
RevHistoryLocation = ' "C:/Temp/temp.xml"'
vaultFolder_full = " $/" + vaultFolder

getRevHistoryCommand = getRevHistory + vaultRepo + beginVersion + vaultFolder_full + " > " + RevHistoryLocation

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

credentials = " -host st-eng -user vpuser -password archive -repository "
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

    git_commit_msg = '"'+ commit_version + "  " + "VaultToGit: " + commit_user +' | ' + commit_date + " | " + commit_message +'"'

    getRepoCommand = "vault GETVERSION" + credentials + vaultRepo +" "+ commit_version + vaultFolder_full +" " + gitDestination_full
    #print('\n\n', getRepoCommand, '\n\n')
    print('\n\n', git_commit_msg, '\n\n')
    os.system("cd /D " + SourceGearLocation + " && " + getRepoCommand)    

    os.system("cd /D " + gitDestination_full + " && " + "git add .")
    git_commit = "cd /D " + gitDestination_full + " && "+ " git commit -m " + git_commit_msg
    os.system(git_commit + 'git --author '+'"'+ commit_user + '<>"')

    #print('\n\n', git_commit, '\n')
    os.system("cd /D " + gitDestination_full + 'git rm *')



#os.system("git push")
