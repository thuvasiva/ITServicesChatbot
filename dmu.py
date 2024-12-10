class DMU:
  def __init__(self, tree):
    self.intent = None
    self.node = None
    self.tasks=[]
    self.lastPopped = None
    self.tree = tree
  
  #searches for node in tree with matching keyword in reverse-level order otherwise returns root of tree
  def reverseLevelSearch(self,root, phrase):
    queue = []
    queue.insert(0,root)
    stack = []
    while(len(queue) > 0):
      node = queue.pop()
      stack.append(node)
      if node == None:
        continue
      for i in range(len(node['subNodes'])-1,-1,-1):
        queue.insert(0,node['subNodes'][i])
    for i in range(len(stack)):
      unstacked = stack.pop()
      for keyword in unstacked['keywords']:
        fullkeyword = keyword.split(" ")
        if all(word.lower() in phrase.lower() for word in fullkeyword):
          return unstacked
    return root
    
  #sets the intent field of the dmu  
  def setIntent(self, intent):
    self.intent = intent

  #gets a response based on the set intent
  def getIntentResponse(self,query):
    if self.intent == "greetings":
      self.resetDMU()
      return "Hello there! How can I help?"
    elif self.intent == "goodbye":
      self.resetDMU()
      return "Goodbye! Thank you for using this chatbot."
    elif self.intent == "need_clarification":
      self.resetDMU()
      return "I'm sorry, I don't understand what you are trying to say."
    #if intent is not one of the main 3 standard intents
    else:
      root = self.tree[self.intent][0] #select tree associated with intent
      node = self.reverseLevelSearch(root, query) #find node
      if node == root and len(root['subNodes']) != 0: #if node find was unsuccessful
        return "What specifically do you need help with regarding " + str(root['nodeName']) + "?"
      else: #node was found succesfully
        #if node is a 1 level tree (ie has no subnodes)
        if len(node['subNodes']) == 0:
          self.resetDMU()
          return node['response'] + " " + "(Note: This is as specific as I can go with helping you. If this hasn't worked please contact IT Services directly.)"
        # node is part of a multi-level tree
        else:
          self.node = node #sets node field of dmu
          return self.getNodeResponse()

  #sets node field of dmu by searching for node
  def setNode(self, query):
    root = tree[self.intent][0]
    node = self.reverseLevelSearch(root, query)
    self.node = node
  
  #gets response according to the set node
  def getNodeResponse(self):
    self.appendTasks(self.node)
    return self.iterateThroughTask()

  #appends subtasks associated with particular node to the tasks array
  def appendTasks(self, node):
    for i in range(len(node['subNodes'])):
          self.tasks.append(node['subNodes'][i])

  #removes first element in tasks array and returns dialogue associated with task
  def iterateThroughTask(self):
    if len(self.tasks) > 0:
      self.lastPopped = self.tasks.pop(0)
      return self.lastPopped['response'] + ". " + "Have you followed this step?"
    return self.node['response']
  
  #appends subtasks associated with task to tasks array if user asks for more help
  def appendSubTasks(self):
    task = self.lastPopped
    if len(task['subNodes']) > 0:
      for i in range(len(task['subNodes'])):
        if i == len(task['subNodes'])-1:
          task['subNodes'][i]['response'] = task['subNodes'][i]['response'] + ' This is the last step for this subtask of ' + task['nodeName']
        self.tasks.insert(i, task['subNodes'][i])
      return "Ok lets dig deeper into your problem... "
    else:
      return "I'm sorry, I can't help you any further with this task. Please contact IT Services directly by calling 020 7882 8888 for more help." + " " + "I will now move on to the next step, say 'exit' if you want me to stop."
  
  #resets state of dmu to original state when first run
  def resetDMU(self):
    self.intent=None
    self.node=None
    self.tasks=[]
    self.lastPopped = None
      
  #parses 'no' or 'exit' or 'yes' phrases
  def parseAnswer(self, input):
    input = input.lower()
    no = ["no", "i need help", "help", "im stuck", "stuck", "more detail"]
    exitWords = ["exit", "that's all", "thats all", "thats", "i have done it already", "already"]
    for word in no:
      if input.find(word) != -1:
        return "no"
    for word in exitWords:
      if input.find(word) != -1:
        return "exit"
    return "yes"
  

import pickle
import json
#reads tree from data source
with open('dialoguetree.json') as user_file:
  tree = json.load(user_file)
#creates dmu object with loaded node tree from data source
dmu = DMU(tree)
#serializes dmu object to file
pickle.dump( dmu, open( "dmu.p", "wb"))