import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, movie, actor, init_db

asnt = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNfQUhINGx4UkF5ZGN6VUFUdnZvMyJ9.eyJpc3MiOiJodHRwczovL2FsYmxvd2kxMi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyYjAwNWI2MzUwNGMwMDcxZGYwNTI2IiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYxMzc1NzE1MCwiZXhwIjoxNjEzODQzNTUwLCJhenAiOiJzSlRWS09pSXQ1MDZIa3JKaGFRTTYwZHp6R25Ib2xrWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.MZOvOVPThjEfVrXXUCn0_701tI8rnA9OBI902uW-EbYL_27ra8TJcCbdjyNO9TaU8Z4sBB6Z_fLdmv4x-TQ8NeuDW59W4To4aRWAjsTWbboVVdyoUUKycCdKOLxqTZVctQLcmExiengX28gSYJ6QBhDb_6BUaf6ALdr0VGApt6n_r22JcsEN3K_9mkgmGcKeHEdXai8jO7e14J-nVGjBOinf5FWidLDmMjPXEoych43IoRmF5uS6N1mwMM2_aCLFQF_KkdTSyUSmUtdo9CvNAxnSNH2v0Pk4TpftzBXIhGvhOEnNcGLzk76UJT3z4UPAQx9S2rbq_t7Fjvk-oOFrGw')
dirc = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNfQUhINGx4UkF5ZGN6VUFUdnZvMyJ9.eyJpc3MiOiJodHRwczovL2FsYmxvd2kxMi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyYjAwY2E2MzUwNGMwMDcxZGYwNTNiIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYxMzc2MTA2MywiZXhwIjoxNjEzODQ3NDYzLCJhenAiOiJzSlRWS09pSXQ1MDZIa3JKaGFRTTYwZHp6R25Ib2xrWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.QjGEyBGlHhzUycsM_B-dm4q4pbdwjgUHEmfjW49ihPUcb17Q3Cg6O6-GqPR_zzNhHH9d3JKcHZ1oD54aNv4U2321ugh1HSKvZ5GZP0LE7GBcswViQkDXk0G7eUotOwBeMpRnGPLQt-1gdYWver5zpHoaiAcPMXBMR4XKCTYI4UwBLAIw2csy_xA5LfwPdWdUEDO8vASrAJgvPKFPIkkl14r4TjemGZ-aVPP-SZN9gSahi-INbewcSEFa4VvqJUyLPOxM97CRPZxaH-ZmvGjZVnrQZN51jed2EVE6Pud_BdUrovbxOjJmijefthUhlmpo4U7DFepSSqo_s-P5A4UGGA')
prod = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNfQUhINGx4UkF5ZGN6VUFUdnZvMyJ9.eyJpc3MiOiJodHRwczovL2FsYmxvd2kxMi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyYjAwZWQyMTQxMGQwMDcxMjdhODgxIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTYxMzc1Nzk0OSwiZXhwIjoxNjEzODQ0MzQ5LCJhenAiOiJzSlRWS09pSXQ1MDZIa3JKaGFRTTYwZHp6R25Ib2xrWCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.ydXW6oXBpyfJU9QgGmdz4exsIIoKH_YVq65Z55A9JO6a8ZQZjfbHk8Hs8s_ypyHpbgM4i587HrUAoh2O0xHBWcXhEZZ4EJUUT_m59DP9pj4npkJ55QHxwmVJ3nTmkn8_i65y3aaCxt0G4gp7AMeOPe2FQ2k7oSXS7fqIiMxK5XHPli0HRwT6euUGRHfuoIjWskwy7UOZc2fOMFlFl-xKoj1Jp57rquW3JYkR7CDzlMtG5ynAbyuVddZ5JRRbrOH6Uxrt8uZ6uUIsocxISat1MGrs1U_lTzxHKvrdUBCJxNX-Ivi020HHleYOvcZHtmEgVJGSHI2R7Dlg-VYDWanZ4g')


class AppTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = 'postgresql://ypgbozimookkky:ffafc5535389b50429c888ca99959c802e5f5ca2ffe10255ca6ce5eef199438f@ec2-3-87-180-131.compute-1.amazonaws.com:5432/df300nbstbk47k'
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

#  Movie Tests

    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + asnt})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movie_byID(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        response = self.client().get(
            f'/movies/{movie_id}',
            headers={"Authorization": "Bearer " + asnt}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'], mov.format())

    def test_404_get_movie_byID(self):
        response = self.client().get(
            '/movies/1000',
            headers={"Authorization": "Bearer " + asnt}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_movie(self):
        new_movie = {
            'title': 'capstone',
            'genres': 'Drama',
            'year': '2021'
        }

        mov = movie(title='capstone', genres='Drama', year='2021')
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + prod}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'added Successfully')

    def test_422_post_movie(self):
        new_movie = {
            'title': 'capstone'
        }
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + prod}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_Unauth_post_movie(self):

        new_movie = {
            'title': 'capstone',
            'genres': 'Drama',
            'year': '2021'
        }
        response = self.client().post(
            '/movies',
            headers={"Authorization": " Bearer " + dirc}, json=new_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], {
                'code': 'unauthorized', 'description': 'Permission not authorized.'})

    def test_patch_movie(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        edit_movie = {
            'title': 'capstone2',
            'genres': 'comedy',
            'year': '2022'
        }
        response = self.client().patch(
            f'/movies/{movie_id }',
            headers={"Authorization": " Bearer " + prod}, json=edit_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Updated Successfully')
        self.assertEqual(data['movie'], mov.format())

    def test_404_patch_movie(self):

        edit_movie = {
            'title': 'capstone2',
            'genres': 'comedy',
            'year': '2022'
        }
        response = self.client().patch(
            '/movies/1800',
            headers={"Authorization": " Bearer " + prod}, json=edit_movie
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_movie(self):

        mov = movie(title='capstone', genres='Drama',
                    year='2021')
        mov.insert()
        movie_id = mov.id

        response = self.client().delete(
            f'/movies/{movie_id }',
            headers={"Authorization": " Bearer " + prod}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Deleted Successfully')
        self.assertEqual(data['movie'], mov.title)

    def test_404_delete_movie(self):

        response = self.client().delete(
            f'/movies/50',
            headers={"Authorization": " Bearer " + prod}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_Unauth_delete_movie(self):

        response = self.client().delete(
            '/movies/50',
            headers={"Authorization": " Bearer " + dirc}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], {
                'code': 'unauthorized', 'description': 'Permission not authorized.'})

    # Actors Test

    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + asnt})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_actor_byID(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().get(
            f'/actors/{actor_id}',
            headers={"Authorization": "Bearer " + asnt}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'], act.format())

    def test_404_get_actor_byID(self):
        response = self.client().get(
            '/actors/1000',
            headers={"Authorization": "Bearer " + asnt}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_actor(self):
        new_actor = {
            'name': 'name',
            'age': 50,
            'gender': 'male'
        }

        act = actor(name='name', age=50, gender='male')
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + prod}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'added Successfully')

    def test_422_post_actor(self):
        new_actor = {
            'age': 54
        }
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + prod}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_Unauth_post_actor(self):

        new_actor = {
            'name': 'name',
            'age': 50,
            'gender': 'male'
        }
        response = self.client().post(
            '/actors',
            headers={"Authorization": " Bearer " + asnt}, json=new_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], {
                'code': 'unauthorized', 'description': 'Permission not authorized.'})

    def test_patch_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        edit_actor = {
            'name': 'name2',
            'age': 34,
            'gender': 'Female'
        }
        response = self.client().patch(
            f'/actors/{actor_id }',
            headers={"Authorization": " Bearer " + prod}, json=edit_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Updated Successfully')
        self.assertEqual(data['actor'], act.format())

    def test_404_patch_actor(self):

        edit_actor = {
            'name': 'name2',
            'age': 34,
            'gender': 'Female'
        }
        response = self.client().patch(
            '/actors/1800',
            headers={"Authorization": " Bearer " + prod}, json=edit_actor
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().delete(
            f'/actors/{actor_id}',
            headers={"Authorization": " Bearer " + prod}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Deleted Successfully')
        self.assertEqual(data['actor'], act.name)

    def test_404_delete_actor(self):

        response = self.client().delete(
            f'/actors/20',
            headers={"Authorization": " Bearer " + prod}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "resource not found")

    def test_Unauth_delete_actor(self):

        act = actor(name='name', age=50,
                    gender='male')
        act.insert()
        actor_id = act.id

        response = self.client().delete(
            '/actors/50',
            headers={"Authorization": " Bearer " + asnt}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], {
                'code': 'unauthorized', 'description': 'Permission not authorized.'})


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
