#git repo address parser for the git repo name

def gitParser(gitaddress ="git@st-gitlab:APS/Express3-Heat.git"):
    count = 0
    newString = ""
    for char in gitaddress:
        if (char == '.'):
            break

        if count == 1:
            newString = newString + char

        if (char == '/'):
            count = 1

    print(newString)
    return newString

