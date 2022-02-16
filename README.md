# candi-app
Interface pour candidature

# Slide  
https://docs.google.com/presentation/d/1O9zXKJWueaOo5ks6hLcOdiCrG406ic1YNmFEwpuxc1k/edit#slide=id.p

# Lien de l'application déployé :
http://candidature-app1.herokuapp.com/

# Jira :
https://ayoubh.atlassian.net/jira/software/projects/CS/boards/1

# Deployment:

La version en prodcution utilise Postgre sql. Attention la dernière version de SQLAlchemy n'est pas compatible avec heroku, il faut utiliser la version dans les requirements.
Après avoir push sur heroku, il faut accèder à la console du serveur et initialiser la db: python create.py
