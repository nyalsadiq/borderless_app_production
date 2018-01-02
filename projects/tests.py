from django.test import TestCase
from .models import Project
from django.urls import reverse
# Create your tests here.

def create_project(title, description, location):
    return Project.objects.create(title=title, description=description, location=location)

class ProjectModelTests(TestCase):

    def test_to_string(self):
        project = Project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        self.assertEqual(project.to_string(), "Star Wars Need a cameraman.")

    def test_no_projects(self):
        response = self.client.get(reverse('projects:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No projects are available.")
        self.assertQuerysetEqual(response.context['project_list'], [])

    def test_one_project(self):
        create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        response = self.client.get(reverse('projects:index'))
        self.assertQuerysetEqual(
            response.context['project_list'],
            ['<Project: Star Wars>']
        )

    def test_two_projects(self):
        create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        create_project(title="Sea Photoshoot", description="Need a diver.", location="Edinburgh")
        response = self.client.get(reverse('projects:index'))
        self.assertQuerysetEqual(
            response.context['project_list'],
            ['<Project: Star Wars>','<Project: Sea Photoshoot>']
        )  