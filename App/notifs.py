from gi.repository import Notify

def notif(title, message, icone):
    Notify.init('Suivit-candidature')
    notif = Notify.Notification.new(title,message,icone)
    notif.show()


def notif_relance():
    titre = 'Relance candidature'
    message = 'Il est temps de relancer ta candidature chez Decathlon (J+17) '
    icone = 'dialog-information'
    return notif(title=titre, message=message, icone=icone)


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