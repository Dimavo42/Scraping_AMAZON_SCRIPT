from one import Info
from database import Control
###POSTGRES SQL
###selenium have to dfine one the path of selenium
### the script is using BS4 to scrap the infromation


def main():
    question1=input("What kind information you would like from amazon?")
    infromation = Info(question1).make_running()
    db = Control('localhost', 'ma', 'postgres', '1234567', '5432') ###POSTGRES SQL (HOST,DB_NAME,USER,PASSWORD)
    for info in infromation:
        db.creat_and_insert(info,question1)
    question2=int(input("What you would like to do with the see? Order by lowest  ==1 OR order by highest==2 OR avg price ==3 ? "))
    while (question2 !=-1):
        if(question2==1 or question2==2):
            for item in db.find_lowest_price_or_highst(question1,question2):
                print(item)
        else:
            print(db.find_average_price(question1))
        question2 = int(input("What you would like to do with the see? Order by lowest  ==1 OR order by highest==2 OR avg price ==3 ? "))

if __name__ == '__main__':
    main()
