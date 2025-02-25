#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) Copyright 2019 Brion Mario.
# (c) This file is part of the CSSI REST API and is made available under MIT license.
# (c) For more information, see https://github.com/brionmario/cssi-api/blob/master/LICENSE.txt
# (c) Please forward any queries to the given email address. email: brion@apareciumlabs.com

"""Application routes module

This modules contains all the different routes to interact with applications.

Authors:
    Brion Mario

"""

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from app.models import Questionnaire, QuestionnaireSchema
from app import db

questionnaire = Blueprint('questionnaire', __name__)

questionnaire_schema = QuestionnaireSchema(strict=True)
questionnaires_schema = QuestionnaireSchema(many=True, strict=True)


@questionnaire.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_questionnaire_list():
    """Get a list of all the Questionnaire"""
    questionnaires = Questionnaire.query.all()
    result = questionnaires_schema.dump(questionnaires).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@questionnaire.route('/<int:id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_questionnaire(id):
    """Get questionnaire when an id is passed in"""
    questionnaire = Questionnaire.query.get(id)
    result = questionnaire_schema.dump(questionnaire).data
    return jsonify({'status': 'success', 'message': None, 'data': result}), 200


@questionnaire.route('/<int:id>/post', methods=['PATCH'])
@cross_origin(supports_credentials=True)
def update_questionnaire(id):
    """Get questionnaire when an id is passed in"""
    questionnaire = Questionnaire.query.get(id)
    questionnaire.post = request.json['post']
    db.session.commit()
    result = questionnaire_schema.dump(questionnaire).data
    return jsonify({'status': 'success', 'message': 'Successfully added the post questionnaire', 'data': result}), 200


@questionnaire.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_questionnaire():
    """Create a new Questionnaire"""
    pre = request.json['pre']
    post = request.json['post']

    new_questionnaire = Questionnaire(pre=pre, post=post)

    db.session.add(new_questionnaire)
    db.session.commit()

    result = questionnaire_schema.dump(new_questionnaire).data

    return jsonify({'status': 'success', 'message': 'Created new questionnaire', 'data': result}), 201
