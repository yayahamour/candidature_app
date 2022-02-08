from gi.repository import Notify
from .models import Candidacy
from flask_login import current_user



def count_alertes():
    
    alertes = 0 
    this_user = Candidacy.find_by_user_id(current_user.id)
    for i in this_user :
        if i['relance'] == False :
            if i['status'] == 'En cours': 
                # If date > date.today()
                alertes += 1
    return alertes


def notif_relance( alerte):
    Notify.init('Suivit-candidature')
    title = 'Simplon - Suivit candidature'
    inside = "s" if alerte > 1 else ""
    message = f" Tu as {alerte} candidature{inside} à relancer"
    icone = 'dialog-information'
    if alerte > 0 :
        notif = Notify.Notification.new(title,message,icone)
        notif.show()


    


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

