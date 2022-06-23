class Quiz:
    questions=[]
    def __init__(self):
        self.questions=\
        [
            {"name":"question1","Q":"I’ve been feeling optimistic about the future"}
            , {"name":"question2","Q":"I’ve been feeling relaxed"}
            , {"name":"question3","Q":"I’ve been feeling confident"}
            , {"name":"question4","Q":"I’ve been interested in new things "}
            , {"name":"question5","Q":"I’ve been able to make up my own mind about things"}
            , {"name":"question6","Q":"I’ve been dealing with problems well "}
            , {"name":"question7","Q":"I’ve been feeling close to other people "}
            , {"name":"question8","Q":"I’ve been feeling good about myself"}
         ]

    def getQuestions(self):
        return self.questions

    def checkanswer(self,answers):
        ans={
            "None of the time":1,
            "Rarely":2,
            "Some of the time":3,
            "Often":4,
            "All of the time":5
        }
        sum=0
        for answer in answers:
            sum=sum+(ans[answer])
        return sum

