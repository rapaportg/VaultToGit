# VaultToGit


This script is used to migrate repositories in SourceGear Vault to a Git repository.

### JADAK Example

#### Example for FW-Hx6146-02 from Vault; adjust as needed for what you are migrating
`python VaultToGit.py -ga git@github.com:jdkvision/FW-Hx6146-02.git -vr '\"JADAK LLC\"' -vf '\"Engineering/Projects - JADAK/Abstraction/Trunk/Code/FW-Hx6146-02\"' -u jcairns -p <password> --host syr-srv-vault1 -sgl "C:\Program Files (x86)\SourceGear\Vault Client"`

The local git repo will be placed in `C:\Temp\`.  So for the above example, it will be in `C:\Temp\FW-Hx6146-02\`.

#### To Remove Vault's _sgbak Folders BEFORE Git Commit (run in Windows command prompt in root of project folder)

`FOR /d /r . %d IN (_sgbak) DO @IF EXIST %d rd /s /q "%d"`

#### To Remove Vault's _sgbak Folders AFTER Git Commit (run in Windows command prompt in root of project folder)

`FOR /d /r . %d IN (_sgbak) DO @IF EXIST %d git rm -rf "%d"`

##### Note: In order to run the script you must either use all the available arguments or change the defaults at the top of the VaultToGit.py script.


#### The only variables that you would need to change are as follows:

- The `git_repo_address`, which can be modified using the command line argument `--gitaddress` or `-ga`.
	-  Example: `python  VaultToGit.py --gitaddress git@gitlab:ABC/Example.git`

- The `vaultRepo`, which is the repository in SourceGear vault you want to access. Its argument variables are `--vaultrepo` or `-vr`. 
	- Example: `python VaultToGit.py --vaultrepo RepoName`
- The `vaultFolder`, which is the folder in the vault repo you want to migrate. Its argument are `--vaultfolder` or `-vf`. 
	- Example: `python VaultToGit.py --vaultfolder RepoFolder`.

- The `vaultUser`, which is the username used to log into SourceGear Vault. Its arguements are `--user` or `-u`.
	- Example: `python VaultToGit.py -u Useranme`

- The `vaultPasswd`, which is the password for the specified vaultUser. Its arguments are `--password` or `-p`. 
	- Example: `pythonVaultToGit.py -p abc123`

- The `vaultHost`, which the host server your SourceGear Vault repository. Its argument is just `--host`. 
	- Example: `python VaultToGit.py --host localhost:3001`

- The `SourceGearLocation`, which is the location of Sourcegear Vault on your machine. Its arguments are `--sourcegear_location` or `-sgl`.
	- Example: `python VaultToGit.py -sgl C:\Program Files (x86)\SourceGear\VaultPro Client`

###### Optional argument:

- The `auto_pusher`, which is used to toggle auto pushing to git. It accepts a value of 1 or 0. Its arguments are `--auto_puser` or `-ap`. 
	- Example: `python VaultToGit.py -ap 1`