import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Actor, Movie, setup_db
from app import create_app


casting_assistant = os.environ['casting_assistant']
casting_director = os.environ['casting_director']
executive_producer = os.environ['executive_producer']
database_path = os.environ['test_database']

class ACastingTestCase(unittest.TestCase):
    ''' This class represents the ACasting test case'''
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_get_actors(self):
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(casting_assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_actors_beyond_valid_page(self):
        res = self.client().get('/actors?page=1000', headers={
            'Authorization': "Bearer {}".format(casting_assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_actor(self):
        res = self.client().post('/actors', json={'name': 'test', 'age': '0', 'gender': 'M'}, headers={
            'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_actor(self):
        res = self.client().post('/actors', json={}, headers={
            'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_actor(self):
        actor = Actor(name="test", age="0", gender="F")
        actor.insert()
        res = self.client().patch(f'/actors/{actor.id}', json={'name': 'test1'},
                                  headers={'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_404_update_actor(self):
        res = self.client().patch(f'/actors/1000', json={'name': 'test1'},
                                  headers={'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        actor = Actor(name="test", age=0, gender='M')
        actor.insert()
        res = self.client().delete(f'/actors/{actor.id}', headers={
            'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_sent_deleting_non_existing_actor(self):
        res = self.client().delete(f'/actors/1000', headers={
            'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(casting_assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_sent_requesting_movies_beyond_valid_page(self):
        res = self.client().get('/movies?page=1000', headers={
            'Authorization': "Bearer {}".format(casting_assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_create_movie(self):
        res = self.client().post('/movies', json={'title': 'test', 'release_date': '12-12-1222'}, headers={
            'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_movie(self):
        res = self.client().post('/movies', json={}, headers={
            'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_movie(self):
        movie = Movie(title='test', release_date='12-12-1222')
        movie.insert()
        res = self.client().patch(f'/movies/{movie.id}', json={'title': 'test1'},
                                  headers={'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    def test_404_update_movie(self):
        res = self.client().patch(f'/movies/1000', json={'title': 'test1'},
                                  headers={'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        movie = Movie(title='test', release_date='12-12-1222')
        movie.insert()
        res = self.client().delete(f'/movies/{movie.id}', headers={
            'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_sent_deleting_non_existing_actor(self):
        res = self.client().delete(f'/movies/1000', headers={
            'Authorization': "Bearer {}".format(executive_producer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def create_movie_with_casting_assistant_token(self):
        res = self.client().post('/movies', json={'title': 'test', 'release_date': '12-12-1222'}, headers={
            'Authorization': "Bearer {}".format(casting_assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertIn('message', data)

    def delete_movie_with_casting_assistant_token(self):
        movie = Movie(title='test', release_date='12-12-1222')
        movie.insert()
        res = self.client().delete(f'/movies/{movie.id}', headers={
            'Authorization': "Bearer {}".format(casting_assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertIn('message', data)

    def delete_movie_with_casting_director_token(self):
        movie = Movie(title='test', release_date='12-12-1222')
        movie.insert()
        res = self.client().delete(f'/movies/{movie.id}', headers={
            'Authorization': "Bearer {}".format(casting_director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertIn('message', data)

    def create_movie_with_casting_director_token(self):
        res = self.client().post('/movies', json={'title': 'test', 'release_date': '12-12-1222'}, headers={
            'Authorization': "Bearer {}".format(casting_director)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
