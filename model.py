#then write methods to actually fill those columns
#naive bayes, onward

__author__ = 'Mariah and David'


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Status, Base
from cleaner import cleaner

class dbContainer:
    def __init__(self):
        self.clean = cleaner()
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
        big = []
        for aStat in all:
            big.append([aStat.status_original,aStat.rank,aStat.status_stemmed,aStat.status_no_common])
        return big

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
        return (current.status_original, current.rank, current.status_stemmed, current.status_no_common)

    def gather_excel(self,file_name):
        sheet = open(file_name,'r')
        statuses = sheet.readlines()
        for i in statuses:
            status = i[:-1].split(",")
            self.insert_status(status[1],int(status[0]))

    def fill_table(self):
        for status in self.session.query(Status).all():
            tokens = self.clean.tokenizeText(status.status_original)
            self.update_stemmed(tokens,status.id)
            self.update_no_common(self.clean.tokenizeText(self.clean.removeCommon(status.status_original)),status.id)
    def empty_db(self):
        for i in self.session.query(Status).all():
            self.session.delete(i)

