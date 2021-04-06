# -*- coding: utf-8 -*-


import pandas as pd
import tweepy
#authentification sur l'api de Twitter, il faut creer un token et entrer ces elements voir ici https://www.digitalocean.com/community/tutorials/how-to-authenticate-a-python-application-with-twitter-using-tweepy-on-ubuntu-14-04
consumer_key= ''
consumer_secret= ''
access_token=''
access_token_secret= ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

API = tweepy.API(auth, parser=tweepy.parsers.JSONParser()) #instanciation de la classe pour envoyer des requetes

listaiscontwi = [] #liste qui contiendra les id twitter des chercheurs 

df = pd.read_csv('/content/example.csv') #charger la liste des chercheurs sous format csv, remplacer '/content/example.csv' par le chemin de votre fichier

s=df[df.columns[0]]

#termes que nous chercherons dans la bio des comptes twitters quand il ya plusieurs comptes qui peuvent correspondre
#ne pas hesiter à changer, ajouter, supprimer pour que ca corresponde au domaine ex :'environnement', 'bio' etc..
matches = ["prof", "phd","ph.d", "research", "ai", "machine", "scien", "data"]  

for i in s :
  try : 
    profile = [] #stocke profile de l'utilisateur à chaque iteration
    search = API.search_users(i) #requete API twitter : ' chercher un utilisateur qui s'appelle 'i' 
    if len(search) > 1 : # si ca retourne plus d'un seul resultat alors cherche celui qui contient au moins un terme 'matches' dans sa bio
      for z in range(len(search)):
        a_string = search[0]['description']
        if any(x in a_string for x in matches):
          profile = search[z]
          break 
    elif len(search) == 1 : #si il n'y a qu'un resultat on dit que c'est lui (quelques faux positifs quand meme)
      profile = search[0]
    if profile['followers_count'] >= 80 and len(profile) != 0 : #on ne garde que ceux qui ont plus de 80 followers
      listaiscontwi.append(profile['id_str'])
  except : 
    continue 

#on va créer une nouvelle 'liste' sut twitter
nouvelleliste = API.create_list('mettrelenomdelaliste', mode = 'private')

#on va la remplir avec les ids des chercheurs qu'on a trouvé

for i in listaiscontwi :
  try : 
    API.add_list_member(list_id = nouvelleliste['id_str'], user_id =i)
  except : 
    print (i) #imprime les ids des comptes qui n'ont pas pu etre ajoutes
    continue 

print("C'est fini ! Allez sur votre compte pour voir le résultat!")