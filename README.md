Ce projet fournit différentes API afin de gérer la gestion d'un hôtel, c'est-à-dire créer des chambres, ajouter des clients mais également effectuer des réservations et vérifier leur disponibilité.

Comment mettre en place le projet :

Tout d'abord effectuer un clone du projet sur git
Ensuite regarder sur docker-compose si le port proposé est disponible sinon changer

Maintenant le setup avec docker :

Tout d'abord lancer un docker ps afin de voir les conteneurs (Bien vérifier d'être sur la racine du projet)
docker-compose build pour mettre en place la configuration
docker-compose up afin de créer le conteneur db et web

Enfin ouvrir 2 terminaux supplémentaires afin de se connecter au conteneur pour la db et celui de l'application
grâce à la commande docker exec -it nom_début_container /bin/bash

Mettre à jour la db pour cela il faut être sur le conteneur web se mettre bien dans app/src/reservation_hotel
lancer flask db init, flask db migrate, et enfin flask db upgrade

Vérifier enfin que tout est bon au niveau de la structure de la db sur le conteneur DB
avec la commande mysql -u root -p

Si tout a bien fonctionné, vous pouvez maintenant commencer à tester l'API.
Pour ce faire, n'oubliez pas dans le conteneur app de faire dans app/src/reservation_hotel
flask run --host=0.0.0.0
utiliser l'IP récupérée pour l'URL de vos requêtes.

L'API :

Ajouter une Chambre (/api/chambres, méthode POST) : Cette route permet d'ajouter une nouvelle chambre à la base de données. Les informations de la chambre, telles que le numéro, le type et le prix, sont fournies dans le corps de la requête au format JSON.

Modifier une Chambre (/api/chambres/int:id, méthode PUT) : Permet de modifier les informations d'une chambre existante en spécifiant son ID dans l'URL. Les nouvelles informations de la chambre sont également fournies dans le corps de la requête au format JSON.

Supprimer une Chambre (/api/chambres/int:id, méthode DELETE) : Cette route permet de supprimer une chambre existante en spécifiant son ID dans l'URL.

Ajouter un Client (/api/clients, méthode POST) : Permet d'ajouter un nouveau client à la base de données. Les informations du client, telles que le nom et l'email, sont fournies dans le corps de la requête au format JSON.

Ajouter une Réservation (/api/reservations, méthode POST) : Cette route permet de créer une nouvelle réservation pour un client. Les informations de la réservation, telles que l'ID du client, l'ID de la chambre, la date d'arrivée et la date de départ, sont fournies dans le corps de la requête au format JSON.

Supprimer une Réservation (/api/reservations/int:id, méthode DELETE) : Permet de supprimer une réservation existante en spécifiant son ID dans l'URL.

Récupérer les Chambres Disponibles (/api/chambres/disponibles, méthode GET) : Cette route permet de récupérer les chambres disponibles pour une période spécifique. Les dates d'arrivée et de départ sont fournies en tant que paramètres de requête dans l'URL.

C'est tout pour le moment.
