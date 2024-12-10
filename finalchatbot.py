import pickle
import streamlit as st
import luc
import dmu

#creates text field and returns inputted value
def get_text():
    input_text = st.text_input("Enter text here:", value ="")
    return input_text

#writes the supplied text to the screen and appends the text to the session_state
def writeAndStoreChat(text):
  st.session_state.previousChat.append("Assistant> " + text)
  c.info("Assistant> " + text)

#same as above but for user rather than chatbot assistant
def writeAndStoreChatUser(text):
  st.session_state.previousChat.append("User> " + text)
  c.info("User> " + text)

#loads dmu and luc
def load_data():
  dmu = pickle.load( open( "dmu.p", "rb"))
  luc = pickle.load( open( "luc.p", "rb"))
  return dmu,luc

#stops program
def stopProgram():
  st.title("IT Services Chatbot")
  st.write("Your file should have downloaded, unfortunately if this is not the case, your chat cannot be recovered.")
  st.write("Chatbot Terminated, Refresh Page To Restart")
  st.stop()

dmu,luc = load_data()

st.title("IT Services Chatbot")
st.write("Welcome to the QM IT Services Chatbot")
st.write("Enter your queries within the textbox and I will try my best to answer them")
st.write("If I fail to answer your query please contact a member of the IT Staff by calling 020 7882 8888 between Monday-Friday 7am-7pm")
st.write("If I give an unintended response, type 'exit' and try to ask the question again.")
st.info("Assistant> Hi")

if 'previousChat' not in st.session_state:
    st.session_state.previousChat = []

c = st.container()

for text in st.session_state.previousChat:
  c.info(text)

query = get_text()
if query:
    writeAndStoreChatUser(query)
    if dmu.intent == None:
        intent = luc.processInput(query)
        dmu.setIntent(intent)
        writeAndStoreChat(dmu.getIntentResponse(query))
    elif dmu.node == None:
        dmu.setNode(query)
        writeAndStoreChat(dmu.getNodeResponse())
    elif len(dmu.tasks) > 0:
        answer = dmu.parseAnswer(query)
        if answer == "yes":
          writeAndStoreChat(dmu.iterateThroughTask())
        elif answer == "no":
          writeAndStoreChat(dmu.appendSubTasks())
          writeAndStoreChat(dmu.iterateThroughTask())
        elif answer == 'exit':
          writeAndStoreChat("Ok no problem. Feel free to ask any more questions.")
          dmu.resetDMU()
    elif len(dmu.tasks) == 0:
        answer = dmu.parseAnswer(query)
        if answer == "no":
          writeAndStoreChat(dmu.appendSubTasks())
          writeAndStoreChat(dmu.iterateThroughTask())
        writeAndStoreChat("Those are the steps for " + dmu.node['nodeName'])
        writeAndStoreChat("Feel free to ask any more questions on any other IT issues you may have.")
        dmu.resetDMU()
    pickle.dump( dmu, open( "dmu.p", "wb"))

st.download_button('Download Conversation and Exit', str(st.session_state.previousChat), on_click=stopProgram)

    