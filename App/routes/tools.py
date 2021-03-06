#from gi.repository import Notify
from ..lclass.candidacy import Candidacy
from flask_login import current_user
import datetime



def diff_date(date_to_compare ):
    
    date_now = str(datetime.date.today())
    annee_1 = date_now[0:4]
    mois_1 = date_now[5:7]
    jours_1 = date_now[8:]
    
    annee_2 = date_to_compare[0:4]
    mois_2 = date_to_compare[5:7]
    jours_2 = date_to_compare[8:]
    if (annee_1 >= annee_2 ) and (mois_1 > mois_2 ) :
        return True
    elif (annee_1 >= annee_2 ) and (mois_1 >= mois_2) and (jours_1 > jours_2):
        return True 
    else:
        return False
    
def count_alertes():
    
    alertes = 0 
    this_user = Candidacy.find_by_user_id(current_user.id)
    for i in this_user :
        if i['relance'] == False :
            if i['status'] == 'En cours': 
                if diff_date(math_relance(i['date'])):
                    alertes += 1
    return alertes


def notif_relance( alerte):
    # Notify.init('Suivit-candidature')
    # title = 'Simplon - Suivit candidature'
    # inside = "s" if alerte > 1 else ""
    # message = f" Tu as {alerte} candidature{inside} à relancer"
    # icone = 'dialog-information'
    # if alerte > 0 :
    #     notif = Notify.Notification.new(title,message,icone)
    #     notif.show()
    pass
            
            

def math_relance(date):
    annee = int(date.replace('-','')[0:4])
    mois = int(date.replace('-','')[4:6])
    jours = int(date.replace('-','')[6:])
    max_mois = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    max_current_mois = max_mois[mois]
    
    math_jour = jours + 7
    
    # Compare if 7 days more reached the end of mounth  
    if math_jour > max_current_mois :
        if mois == 12 :
            annee += 1 
            mois = 1 
            math_jour -= max_current_mois
        else:
            mois += 1 
            math_jour -= max_current_mois
        
    # For the correct format print
    if mois < 10 :
        mois = "0" + str(mois)
    if math_jour < 10 :
        math_jour = "0" + str(math_jour)
        
    result = str(annee) + "-" + str(mois) + "-" + str(math_jour)
    return result



    
