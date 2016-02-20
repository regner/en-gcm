

import os
import logging

from gcloud import datastore
from eveauth.contrib.flask import authenticate

from flask import Flask, abort, request
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

# App Settings
app.config['BUNDLE_ERRORS'] = True

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)

# Datastore Settings
DS_CLIENT = datastore.Client()
GCM_KIND = 'EN-GCM'


class DatastoreClient(object):
    @staticmethod
    def get_client():
        if not hasattr(DatastoreClient, "_client"):
            DatastoreClient._client = datastore.Client()
        return DatastoreClient._client


def get_client():
    return DatastoreClient.get_client()


class Internal(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('character_ids', type=str, required=True)
        args = parser.parse_args(strict=True)
        
        client = get_client()
        character_ids = args['character_ids'].split(',')
        character_keys = [client.key(GCM_KIND, int(x)) for x in character_ids]
        data = []
        
        for entity in client.get_multi(character_keys):
            data = data + entity['tokens']
        
        return data


class External(Resource):
    def get(self):
        return {'project_id': os.environ.get('ProjectID', '1045503414087')}


class ExternalCharacterSettings(Resource):
    @authenticate(match_data=['character_id'])
    def put(self, character_id):
        parser = reqparse.RequestParser()
        parser.add_argument('gcm_token', type=str, required=True)

        args = parser.parse_args(strict=True)
        
        client = get_client()
        character_gcm_tokens = client.get(client.key(GCM_KIND, character_id))
        
        if character_gcm_tokens is None:
            app.logger.info('First time access for character {}.'.format(character_id))
            character_gcm_tokens = datastore.Entity(client.key(GCM_KIND, character_id))
            character_gcm_tokens['tokens'] = []
        
        if args['gcm_token'] not in character_gcm_tokens['tokens']:
            app.logger.info('Adding new GCM token to character {}.'.format(character_id))
            character_gcm_tokens['tokens'].append(args['gcm_token'])
            client.put(character_gcm_tokens)
            return {}, 201
        
        else:
            app.logger.info('GCM token already exists for character {}.'.format(character_id))
            return {}, 304
    

api.add_resource(Internal, '/internal/')
api.add_resource(External, '/external/')
api.add_resource(ExternalCharacterSettings, '/external/characters/<int:character_id>/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
