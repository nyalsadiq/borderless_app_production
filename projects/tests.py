from django.test import TestCase
from .models import Project, Requirement
from django.urls import reverse
import json
from rest_framework.test import APIClient
from profiles.models import User
# Create your tests here.

def create_project(title, owner,description, location):
    return Project.objects.create(title=title, owner = owner,description=description, location=location)

def create_requirements(text, project):
    return Requirement.objects.create(text=text, project=project)

def create_user():
    user = User.objects.create_user(
            username="koalabear",
            email="koalabear@example.com",
            password="secret")
    return user
    
class IndexPageTests(TestCase):
    """
        Tests for appropriate responses from index view.
    """
    def test_to_string(self):
        project = Project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        self.assertEqual(project.to_string(), "Star Wars Need a cameraman.")

    def test_no_projects(self):
        """
            Tests to see if we get an appropriate response to no projects.
        """
        response = self.client.get(reverse('projects:index'))
        
        self.assertJSONEqual(response.content, [])

    def test_one_project(self):
        """
            Tests for appropriate response for one project.
        """
        user = create_user()
        create_project(title="Star Wars",owner=user, description="Need a cameraman.", location="Edinburgh")
        response = self.client.get(reverse('projects:index'))
        self.assertJSONEqual(response.content, 
        [{
            "id": 1, "title": "Star Wars","owner":"koalabear", "description": "Need a cameraman.", "location": "Edinburgh"
        }])

    def test_two_projects(self):
        """
            Tests for appropriate response for two projects.
        """
        user = create_user()
        create_project(title="Star Wars",owner=user, description="Need a cameraman.", location="Edinburgh")
        create_project(title="Sea Photoshoot",owner=user, description="Need a diver.", location="Edinburgh")
        response = self.client.get(reverse('projects:index'))

        self.assertJSONEqual(response.content, 
        [{
            "id": 1,
            "title": "Star Wars",
            "owner":"koalabear",
            "description": "Need a cameraman.",
            "location": "Edinburgh"
        },
        {
            "id": 2,
            "title": "Sea Photoshoot",
            "owner":"koalabear",
            "description": "Need a diver.",
            "location": "Edinburgh"
        }])

class DetailPageTests(TestCase):
    """
        Tests for appropriate responses from detail view.
    """
    

    def test_no_requirements(self):
        """
            Tests for good response when there are no requirements.
        """
        user = create_user()
        project = create_project(title="Star Wars", owner=user, description="Need a cameraman.", location="Edinburgh")
        response = self.client.get(reverse('projects:detail', args=(project.id,)))

        self.assertJSONEqual(
            response.content,
            {
                "id": 1,
                "title": "Star Wars",
                "owner":"koalabear",
                "description": "Need a cameraman.",
                "location": "Edinburgh",
                "requirements": [],
                "comments": [],
                "likes": 0
            })

    def test_one_requirement(self):
        """
            Tests for good response when there is one requirement.
        """
        user = create_user()
        project = create_project(title="Star Wars",owner=user,description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)
        response = self.client.get(reverse('projects:detail', args=(project.id,)))

        self.assertJSONEqual(
           response.content,
           {
                "id": 1,
                "owner":"koalabear",
                "title": "Star Wars",
                "description": "Need a cameraman.",
                "location": "Edinburgh",
                "requirements": [
                    {
                        "id": 1,
                        "project": "Star Wars",
                        "text": "Camera"
                    }
                ],
                "comments": [],
                "likes": 0
            })


class DeletionTest(TestCase):

    def test_delete_project(self):
        user = create_user()
        project = create_project(title="Star Wars",owner=user, description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)

        client = APIClient()
        client.login(username="koalabear",password="secret")

        response = client.delete( reverse('projects:detail', args=(project.id,)))
        self.assertEqual(response.status_code, 204)

    def test_delete_requirement(self):
        user = create_user()
        project = create_project(title="Star Wars", owner=user,description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)
        create_requirements(text="Lightsaber", project=project)

        client=APIClient()
        client.login(username="koalabear",password="secret")

        response = client.delete( reverse('projects:detail', args=(requirement.id,)))
        self.assertEqual(response.status_code, 204)
          

class UpdateTest(TestCase):

    def test_update_title_description_and_location(self):
        user = create_user()
        project = create_project(title="Star Wars",owner=user, description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)
        create_requirements(text="Lightsaber", project=project)

        client = APIClient()
        client.login(username="koalabear",password="secret")
        response = client.patch( reverse('projects:detail', args=(project.id,)) , 
        {'title':'Star Trek','description':'New','location':'Glasgow'},
        format='json' )

        self.assertJSONEqual(response.content,
            {
                "id": 1,
                "title": "Star Trek",
                "owner": "koalabear",
                "description": "New",
                "location": "Glasgow",
                "requirements": [
                    {
                        "id": 1,
                        "project": "Star Trek",
                        "text": "Camera"
                    },
                    {
                        "id": 2,
                        "project": "Star Trek",
                        "text": "Lightsaber"
                    }
                ],
                "comments": [],
                "likes": 0
            })

class CreateTest(TestCase):

    def test_create_without_requirements(self):
        user = create_user()
        
        client = APIClient()
        client.login(username="koalabear",password="secret")

        response = client.post( reverse('projects:index') , 
        {'title':'Star Wars','owner':'koalabear','description':'Need a cameraman.','location':'Edinburgh'} , format='json')

        self.assertJSONEqual(response.content,
            {
                'id': 1,
                'title': 'Star Wars',
                'owner': 'koalabear',
                'description': 'Need a cameraman.',
                'location': 'Edinburgh',
                'requirements': [],
                "comments": [],
                "likes": 0
            }
        )