from django.test import TestCase
from .models import Project, Requirement
from django.urls import reverse
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
        
        self.assertJSONEqual(response.content, {'result':'no projects'})

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
                        "text": "Camera"
                    }
                ]
            })