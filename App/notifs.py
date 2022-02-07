from gi.repository import Notify
from .models import Candidacy
from App import app
from flask_login import current_user

def notif(title, message, icone):
    Notify.init('Suivit-candidature')
    notif = Notify.Notification.new(title,message,icone)
    notif.show()



def notif_relance(alerte):
    titre = 'Suivit candidature Simplon'
    icone = 'dialog-information'
    message = f" Tu as {alerte} candidature(s) à relancer"
    if alerte == 0 :
        return notif(titre, "Aucune candidature à relancer", icone)
    else:
        return notif(titre, message, icone)
    


def math_relance(date):
    annee = int(date.replace('-','')[0:4])
    mois = int(date.replace('-','')[4:6])
    jours = int(date.replace('-','')[6:])
    max_mois = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    max_current_mois = max_mois[mois]
    
    math_date = jours + 7
    
    # Compare if its the end of current mounth and year is crossed or not
    if math_date > max_current_mois :
        if mois == 12 :
            annee += 1 
            mois = 1 
            math_date -= max_current_mois
        else:
            mois += 1 
            math_date -= max_current_mois
        
    # For the print format
    if mois < 10 :
        mois = "0" + str(mois)
    if math_date < 10 :
        math_date = "0" + str(math_date)
        
    result = str(annee) + "-" + str(mois) + "-" + str(math_date)
    
    return result

def count_alertes():
    
    test = Candidacy.find_by_user_id(current_user.id)
    alertes = 0 
    for i in test :
        if i['relance'] == False :
            if i['status'] == 'En cours': 
                alertes += 1
    return alertes