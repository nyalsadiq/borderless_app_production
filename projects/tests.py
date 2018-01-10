from django.test import TestCase
from .models import Project, Requirement
from django.urls import reverse
import json
from rest_framework.test import APIClient
# Create your tests here.

def create_project(title, description, location):
    return Project.objects.create(title=title, description=description, location=location)

def create_requirements(text, project):
    return Requirement.objects.create(text=text, project=project)
    
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
        create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        response = self.client.get(reverse('projects:index'))
        self.assertJSONEqual(response.content, 
        [{
            "id": 1, "title": "Star Wars", "description": "Need a cameraman.", "location": "Edinburgh"
        }])

    def test_two_projects(self):
        """
            Tests for appropriate response for two projects.
        """
        create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        create_project(title="Sea Photoshoot", description="Need a diver.", location="Edinburgh")
        response = self.client.get(reverse('projects:index'))

        self.assertJSONEqual(response.content, 
        [{
            "id": 1,
            "title": "Star Wars",
            "description": "Need a cameraman.",
            "location": "Edinburgh"
        },
        {
            "id": 2,
            "title": "Sea Photoshoot",
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
        project = create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        response = self.client.get(reverse('projects:detail', args=(project.id,)))

        self.assertJSONEqual(
            response.content,
            {
                "id": 1,
                "title": "Star Wars",
                "description": "Need a cameraman.",
                "location": "Edinburgh",
                "requirements": []
            })

    def test_one_requirement(self):
        """
            Tests for good response when there is one requirement.
        """
        project = create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)
        response = self.client.get(reverse('projects:detail', args=(project.id,)))

        self.assertJSONEqual(
           response.content,
           {
                "id": 1,
                "title": "Star Wars",
                "description": "Need a cameraman.",
                "location": "Edinburgh",
                "requirements": [
                    {
                        "id": 1,
                        "text": "Camera"
                    }
                ]
            })


class DeletionTest(TestCase):

    def test_delete_project(self):
        project = create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)

        client = APIClient()
        response = client.delete( reverse('projects:detail', args=(project.id,)) , {'type': 'project'} , format='json' )
        self.assertEqual(response.status_code, 204)

    def test_delete_requirement(self):
        project = create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)
        create_requirements(text="Lightsaber", project=project)

        client=APIClient()
        response = client.delete( reverse('projects:detail', args=(requirement.id,)) , {'type': 'requirement'} , format='json' )
        self.assertEqual(response.status_code, 204)
        
        response = client.get( reverse('projects:detail', args=(project.id,)) )
        self.assertJSONEqual(response.content,
            {
                "id": 1,
                "title": "Star Wars",
                "description": "Need a cameraman.",
                "location": "Edinburgh",
                "requirements": [
                    {
                        "id": 2,
                        "text": "Lightsaber"
                    }
                ]
            })

class UpdateTest(TestCase):

    def test_update_title_description_and_location(self):
        project = create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)
        create_requirements(text="Lightsaber", project=project)

        client = APIClient()
        response = client.patch( reverse('projects:detail', args=(project.id,)) , 
        {'title':'Star Trek','description':'New','location':'Glasgow'},
        format='json' )

        self.assertJSONEqual(response.content,
            {
                "id": 1,
                "title": "Star Trek",
                "description": "New",
                "location": "Glasgow",
                "requirements": [
                    {
                        "id": 1,
                        "text": "Camera"
                    },
                    {
                        "id": 2,
                        "text": "Lightsaber"
                    }
                ]
            })

    def test_update_requirements(self):
        project = create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)
        create_requirements(text="Lightsaber", project=project)

        client = APIClient()
        response = client.patch( reverse('projects:detail', args=(project.id,)) , 
        {'requirements': [{"text":"Yoda"},{"text":"Samuel L Jackson"}]},
        format='json' )

        '''
            Patch does not return updated requirements values.
        '''
        self.assertJSONEqual(response.content,
            {
                "id": 1,
                "title": "Star Wars",
                "description": "Need a cameraman.",
                "location": "Edinburgh",
                "requirements": [
                    {
                        "id": 1,
                        "text": "Camera"
                    },
                    {
                        "id": 2,
                        "text": "Lightsaber"
                    }
                ]
            })

class CreateTest(TestCase):

    def test_create_without_requirements(self):
        client = APIClient()
        response = client.post( reverse('projects:index') , 
        {'title':'Star Wars','description':'Need a cameraman.','location':'Edinburgh'} , format='json')

        self.assertJSONEqual(response.content,
            {
                'id': 1,
                'title': 'Star Wars',
                'description': 'Need a cameraman.',
                'location': 'Edinburgh',
                'requirements': []
            }
        )

    def test_create_with_requirements(self):
        client = APIClient()
        response = client.post( reverse('projects:index') , 
        {'title':'Star Wars','description':'Need a cameraman.','location':'Edinburgh', 
        'requirements': [{'text':'Yoda'},{'text':'Helmet'}]} , format='json')

        self.assertJSONEqual(response.content,
            {
                'id': 1,
                'title': 'Star Wars',
                'description': 'Need a cameraman.',
                'location': 'Edinburgh',
                'requirements': [
                    {
                        'id': 1,
                        'text': 'Yoda'
                    },
                    {
                        'id': 2,
                        'text': 'Helmet'
                    }
                ]
            }
        )