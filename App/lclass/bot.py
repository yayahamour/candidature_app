import datetime
from flask_mail import Message
from App import app, mail
class Bot:

    def __init__(self, date_tchecker=[1]):
        self.date_tchecker = date_tchecker


    def mail_relance(self, adresse):
        jour = str(datetime.date.today())[8:]
        if str(self.date_tchecker[-1]) != jour:
            msg = Message(subject="Relance suivit candidature Simplon", 
                        body="Bonjour Apprenant, \nJe suis le bot créer par tes confrères et je suis là pour te rappeler que tu as des alertes de candidatures à relancer. \nVa vite faire un tour sur http://suivicandidature.herokuapp.com/",
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=[adresse])
            try: 
                mail.send(msg)
                print('jour : ', jour)
                print('element liste all', self.date_tchecker )
                print('dernier element de la liste', self.date_tchecker[-1])
                print('-------------------   email envoyé! ------------------- \n')
            except:
                print('ERROR - Please tchek your email config')
            del self.date_tchecker[-1]
            self.date_tchecker.append(jour)
        else:
            print('Message Non envoyé')


