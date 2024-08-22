import ast
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from utils import assetsUtil


from chanblockweb.settings.base import env
client = MongoClient(env('MONGOATLAS_USER'))


def note_user(myDict):
    myDict.pop('csrfmiddlewaretoken')
  
    comment={}
    for value in myDict:
       
        comment["user_id"]=myDict['id'][0]
        comment['title']=myDict['title'][0]
        if len(myDict['dataGraph1'][0])!=0:
         comment["dataGraph1"]=myDict['dataGraph1'][0]
        if len(myDict['comment_graph1'][0])!=0:
            comment["commentGraph1"]= myDict['comment_graph1'][0]
        if len(myDict['dataGraph2'][0])!=0:
             comment["dataGraph2"]=myDict['dataGraph2'][0]
        if len(myDict['comment_graph2'][0])!=0:
            comment["commentGraph2"]= myDict['comment_graph2'][0]
        if len(myDict['dataGraph3'][0])!=0: 
            comment["dataGraph3"]=myDict['dataGraph3'][0]
        if len(myDict['comment_graph3'][0])!=0:
            comment["commentGraph3"]= myDict['comment_graph3'][0]
    
    today = datetime.now()
    comment["date"]=today
    for val in comment:
        print((comment[val]))
    db = client.chancblock.user_graph
    
    try:
        db.insert_one(comment)
        return True
    except:
        return False


def listNotes(id):
     db = client.chancblock.user_graph
     queryNotes= db.find({"user_id": id}).sort("date", -1)
     listNotes=list(queryNotes)    
     arrayNotes=[]
     for value in listNotes:
        listNotess={}        
        for metric in value:
            if metric == '_id':            
               listNotess['id']=value[metric]              
            if metric == 'dataGraph1' or metric == 'dataGraph2' or metric == 'dataGraph3':                
                value[metric]=ast.literal_eval(value[metric])
                listNotess[metric]=value[metric]
            #     context=assetsUtil.graph(prueba)                    
            if type(value[metric]) is datetime:
                value[metric]=value[metric].ctime()
                listNotess[metric]=value[metric]

            listNotess[metric]=value[metric]
        arrayNotes.append(listNotess)    
     return arrayNotes

def detailNote(id):
    db = client.chancblock.user_graph
    queryNotes= dict(db.find_one({"_id": ObjectId(id)},{"_id":0}))  
    arraylist=[]   
    list1={}
    graph={}
    for value in queryNotes:
        
        if value == 'dataGraph1' or value == 'dataGraph2' or value == 'dataGraph3':
            list={}
            
            queryNotes[value]=ast.literal_eval(queryNotes[value])
            context=assetsUtil.graph(queryNotes[value])
            list['div']=context['div']
            list['script']=context['script']
            graph[value]=list
            arraylist.append(graph)

        if type(queryNotes[value]) is datetime:
                queryNotes[value]=queryNotes[value].ctime()
                list1[value]=queryNotes[value]
        
        list1[value]=queryNotes[value]
               
    sendDate={
        'graph': graph,
        'query':queryNotes

     }   
    
            
    return sendDate
def deleteNote(id):
    db = client.chancblock.user_graph

    try:
        db.delete_one({"_id": ObjectId(id)})
        return True
    except:
        return False