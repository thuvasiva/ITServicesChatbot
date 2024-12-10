class LUC:
    def __init__(self,model, vectorizer):
        self.model = model
        self.vectorizer = vectorizer

    #converts encoded tag to english tag
    def intentMapper(self,number):
        if number == 1:
            return "email_issue"
        elif number == 2:
            return "goodbye"
        elif number == 3:
            return "greetings"
        elif number == 4:
            return "matlab"
        elif number == 5:
            return "password_requirement"
        elif number == 6:
            return "password_reset"
        elif number == 7:
            return "wifi"
        elif number == 0:
            return "need_clarification"

    #processes input by returning the predicted intent associated with the input
    def processInput(self, query):
        outputNumber = self.model.predict(self.vectorizer.transform([query]))
        intent = self.intentMapper(outputNumber)
        return intent
    
import pickle
model = pickle.load( open( "model.p", "rb" ) )
vectorizer = pickle.load( open( "vectorizer.p", "rb"))
luc = LUC(model, vectorizer)
pickle.dump( luc, open( "luc.p", "wb"))
