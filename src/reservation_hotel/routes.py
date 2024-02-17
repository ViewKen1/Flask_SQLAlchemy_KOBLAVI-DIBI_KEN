from flask import Flask, request, jsonify, Blueprint, render_template
from .models import Client, Chambre, Reservation
from .database import db
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/api/chambres', methods=['POST'])
def add_chambre():
    data = request.get_json()
    numero = data['numero']
    type = data['type']
    prix = data['prix']

    existing_chambre = Chambre.query.filter_by(numero=numero).first()
    if existing_chambre:
        return jsonify({'error': 'Une chambre avec ce numéro existe déjà'}), 400
    else:
        nouvelle_chambre = Chambre(numero=numero, type=type, prix=prix)
        db.session.add(nouvelle_chambre)
        db.session.commit()
        return jsonify({'message': 'Chambre ajoutée avec succès'}), 200


@main.route('/api/chambres/<int:id>', methods=['PUT'])
def modifier_chambre(id):
    data = request.get_json()
    numero = data['numero']
    type = data['type']
    prix = data['prix']

    chambre = Chambre.query.get(id)
    if not chambre:
        return jsonify({'error': 'La chambre spécifiée n\'existe pas'}), 400

    chambre.numero = numero
    chambre.type = type
    chambre.prix = prix

    db.session.commit()

    return jsonify({'message': 'Chambre modifiée avec succès'}), 200


@main.route('/api/chambres/<int:id>', methods=['DELETE'])
def supprimer_chambre(id):
    chambre = Chambre.query.get(id)
    if not chambre:
        return jsonify({'error': 'La chambre spécifiée n\'existe pas'}), 400

    db.session.delete(chambre)
    db.session.commit()

    return jsonify({'message': 'Chambre supprimée avec succès'}), 200


@main.route('/api/clients', methods=['POST'])
def add_clients():
    data = request.get_json()
    nom = data['nom']
    email = data['email']

    existing_client = Client.query.filter_by(email=email).first()
    if existing_client:
        return jsonify({'error': 'Cette adresse email est déjà utilisé'}), 400
    else:
        new_client = Client(nom=nom, email=email)
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'message': 'Client ajouté avec succès'}), 200


@main.route('/api/reservations', methods=['POST'])
def add_reservation():
    data = request.get_json()
    id_client = data['id_client']
    id_chambre = data['id_chambre']
    date_arrivee = datetime.strptime(data['date_arrivee'], '%Y-%m-%d %H:%M:%S')
    date_depart = datetime.strptime(data['date_depart'], '%Y-%m-%d %H:%M:%S')

    reservations_existantes = Reservation.query.filter(
        (Reservation.id_chambre == id_chambre) &
        (
            (
                (Reservation.date_arrivee <= date_arrivee) &
                (Reservation.date_depart >= date_arrivee)
            ) |
            (
                (Reservation.date_arrivee <= date_depart) &
                (Reservation.date_depart >= date_depart)
            )
        )
    ).all()

    if reservations_existantes:
        return jsonify({'error': 'La chambre est déjà réservée pour cette période'}), 400
    else:
        nouvelle_reservation = Reservation(
            id_client=id_client, id_chambre=id_chambre, date_arrivee=date_arrivee, date_depart=date_depart)
        db.session.add(nouvelle_reservation)
        db.session.commit()
        return jsonify({'message': 'Réservation ajoutée avec succès'}), 200


@main.route('/api/reservations/<int:id>', methods=['DELETE'])
def supprimer_reservation(id):
    reservation = Reservation.query.get(id)
    if not reservation:
        return jsonify({'error': 'La reservation spécifiée n\'existe pas'}), 400
    else:
        db.session.delete(reservation)
        db.session.commit()

        return jsonify({'message': 'Réservation supprimée avec succès'}), 200


@main.route('/api/chambres/disponibles', methods=['GET'])
def recup_chambres_dispo():
    date_arrivee = request.args.get('date_arrivee')
    date_depart = request.args.get('date_depart')

    if not date_arrivee or not date_depart:
        return jsonify({'message': 'Les dates de début et de fin sont requises.'}), 400

    try:
        date_arrivee = datetime.strptime(date_arrivee, '%Y-%m-%d %H:%M:%S')
        date_depart = datetime.strptime(date_depart, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Format de date invalide. Utilisez le format YYYY-MM-DD HH:MM:SS.'}), 400

    if date_arrivee >= date_depart:
        return jsonify({'message': 'La date de départ doit être après la date d\'arrivée.'}), 400

    chambres_occupees = Reservation.query.filter(
        (Reservation.date_arrivee < date_depart) &
        (Reservation.date_depart > date_arrivee)
    ).with_entities(Reservation.id_chambre).all()

    chambres_occupees_ids = [occupee[0] for occupee in chambres_occupees]

    chambres_disponibles = Chambre.query.filter(
        ~Chambre.id.in_(chambres_occupees_ids)
    ).all()

    chambres_disponibles_json = [{
        'id': chambre.id,
        'numero': chambre.numero,
        'type': chambre.type,
        'prix': float(chambre.prix)
    } for chambre in chambres_disponibles]

    return jsonify(chambres_disponibles_json), 200
