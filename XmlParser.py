import xml.etree.ElementTree as ET

rev_version_array = []
rev_user_array = [] 
rev_txid_array = []
rev_objverid_array = []
rev_comment_array = []
rev_date_array = []

def init():
  
    tree = ET.parse('temp.xml')
    root = tree.getroot()

    for item in root[0].findall('item'):
        version = item.get('version')
        rev_version_array.append(version)

        user = item.get('user')
        rev_user_array.append(user)

        txid = item.get('txid')
        rev_txid_array.append(txid)
            
        objverid = item.get('objverid')
        rev_objverid_array.append(objverid)

        comment = item.get('comment')
        rev_comment_array.append(comment)
                 
        date = item.get('date')
        rev_date_array.append(date)
                

def VersionA():
    version_array = rev_version_array[::-1]
    return version_array

def UserA():
    user_array = rev_user_array[::-1] 
    return user_array

def TxidA():
    txid_array = rev_txid_array[::-1]
    return txid_array

def ObjveridA():
    objverid_array = rev_objverid_array[::-1]
    return objverid_array

def CommentA():
    comment_array = rev_comment_array[::-1]
    return comment_array

def DateA():
    date_array = rev_date_array[::-1]
    return date_array