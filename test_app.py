import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Actor, Movie, setup_db
from app import create_app


casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNUkR1ZjF2YzBXdTVKdnNFY2JhdSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzdGFjay5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBjZTYzM2RiZDk2NTQwMDcxMWFjOWQzIiwiYXVkIjoiYWdlbmN5RlNORCIsImlhdCI6MTYyNDIxNTgzNiwiZXhwIjoxNjI0MzAyMjM2LCJhenAiOiJUczBuUkZiY2ZSNnk1VnF1MjVmM0VCWlFJcnlENU1hQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.VLmjD-hok53GItPTxPebQEXa3Exz6C4cRBtCoaPvPa9xatd3Z_cg6UJo9-Ut7AkTvNENZO6KfsiZ8jAUa-Xr42SlqNXSGILujTzkZ6donyY1k4j0qwsdmACXvRy-KpeI0XmC7uSWFIjQJQZwzhjnf1yMQqyApOqQWdny88hcbHVyIUwRd_D1RRn0Y8J9PBUeUqgBqp1wfHAKFLSv_HJKmRKRevBH3uBROLu89qTnaNi5KWNrVhBUhMUrLeV9KhsMI0L7i1im4mKBs2rnZZbNP-3EXVWqRy2gyO0VWyMXsVl_mQ3LGvjD5BLFusjVlhanh6X69hF4KzM-JSt1foiu5Q'
casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNUkR1ZjF2YzBXdTVKdnNFY2JhdSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzdGFjay5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBjZTY0ODhlZjJhNWUwMDY4ZDVmOGFjIiwiYXVkIjoiYWdlbmN5RlNORCIsImlhdCI6MTYyNDIxNTc0OCwiZXhwIjoxNjI0MzAyMTQ4LCJhenAiOiJUczBuUkZiY2ZSNnk1VnF1MjVmM0VCWlFJcnlENU1hQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiXX0.OHMhSVIYeZ7Qeljzf_FJmbMaf5V5J5tqUhcZKQ6hF228hiEsax2ljvXJ0u0LdB_tOe4Px-QMzcKs6wK2gfpUxXZlgBtnbPX93rEyHKGY3gvwiw3YV3M8HOXJtSReFCcYM4H2S95539ZamFlPefyoT1-uoIJKwRfUtwJzu5gWx271B3_8811m1awGTZhCyByE2gguBqJ0up28k8FzHsj0ftKNti1UoPF6NY0wmm3TxKKnNvX5T-T1BLhF0JfYiwfu8oZNkO9IA0tSLEJ5vdJiCAIhONFspc-9es_pcX-gxT1r83i5LUw1Py89OZ6wwrrUBsLr2sKtia5fQvrvUSObDA'
executive_producer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNUkR1ZjF2YzBXdTVKdnNFY2JhdSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRzdGFjay5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBjZTY0ZGQ4MDhkMDQwMDY5ZmEyZjJmIiwiYXVkIjoiYWdlbmN5RlNORCIsImlhdCI6MTYyNDIxNTk0OCwiZXhwIjoxNjI0MzAyMzQ4LCJhenAiOiJUczBuUkZiY2ZSNnk1VnF1MjVmM0VCWlFJcnlENU1hQSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiYWRkOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUiXX0.hFM0KsGVWnaHbRLa_ObwvVA3IAKbybHvdPDKY4Nm5C00dQ99NZQqWWFvsAy-UqCL6tM-wuYHJN9DN2WvSNscT6ZsIQMtj3T-1NDxmIX0ONsMb0aFARE2SI9C6sIfEdZllewo_75ow7EWFc73ZodufTnyLfXwWkMbxDlvJYcss1DvM-2kZZJvtlMpHFOxf-C3xp4fu6C_JG7aMecE-4xbmFBL0tgCBUBd9Ar2dTKuvdC8l6lnIsvb5iWKmAvd-abqU92LFhMSU58FpxUIOP2_4qYKAnbF2Hc37nnFLKv6e17oVMunZaAPxVKUq2EZsjELGIGjNa9lHFJ7rCoKYCor0w'
database_path = 'postgresql://postgres:1234@localhost:5432/capstone_test'

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
