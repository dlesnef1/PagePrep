__author__ = 'Mariah and David'


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Status, Base
from nltk.tokenize import RegexpTokenizer

class dbContainer:
    def __init__(self):
        engine = create_engine('sqlite:///statuses.db')
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def insert_status(self,new_status,new_rank):
        if (new_status == "" or new_rank>2 or new_rank<-2):
            return

        new_status = Status(status=new_status, rank=new_rank)
        self.session.add(new_status)
        self.session.commit()

    def get_all(self):
        all = self.session.query(Status).all()
        statuses = {}
        for aStatus in all:
            statuses[aStatus.status] = aStatus.rank

        return statuses

    def gather_excel(self,file_name):
        sheet = open(file_name,'r')
        statuses = sheet.readlines()
        for i in statuses:
            status = i[:-1].split(",")
            self.insert_status(status[1],int(status[0]))

    def empty_db(self):
        for i in self.session.query(Status).all():
            self.session.delete(i)

    def clean(self,status):
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(status)  # return the tokens
        print(tokens)



test = dbContainer()

#test.gather_excel("good.csv")

#print(test.get_all())
test.clean("@kwefgf going to cinda's sooonnnnnnn123")
