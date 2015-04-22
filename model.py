#then write methods to actually fill those columns
#naive bayes, onward

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

        new_status = Status(status_original=new_status, rank=new_rank)
        self.session.add(new_status)
        self.session.commit()

    def get_all(self):
        all = self.session.query(Status).all()
        statuses = {}
        for aStatus in all:
            statuses[aStatus.status_original] = aStatus.rank
        return statuses

    def update_stemmed(self,stemmed,idIn):
        #assume list comes in
        stemmed_string = ""
        for word in stemmed:
            stemmed_string += word + ","
        current = self.session.query(Status).filter(Status.id == idIn).all()[0]
        current.status_stemmed = stemmed_string[:-1]
        self.session.commit()

    def update_no_common(self,no_common,idIn):
        #assume list comes in
        no_common_string = ""
        for word in no_common:
            no_common_string += word + ","
        current = self.session.query(Status).filter(Status.id == idIn).all()[0]
        current.status_no_common = no_common_string[:-1]
        self.session.commit()

    def get_ind(self,idIn):
        current = self.session.query(Status).filter(Status.id == idIn).all()[0]
        return (current.status_original, current.rank, current.status_stemmed)

    def gather_excel(self,file_name):
        sheet = open(file_name,'r')
        statuses = sheet.readlines()
        for i in statuses:
            status = i[:-1].split(",")
            self.insert_status(status[1],int(status[0]))

    def empty_db(self):
        for i in self.session.query(Status).all():
            self.session.delete(i)



test = dbContainer()

#test.gather_excel("good.csv")

print(test.get_all())
