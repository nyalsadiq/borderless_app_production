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

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No projects are available.")
        self.assertQuerysetEqual(response.context['project_list'], [])

    def test_one_project(self):
        """
            Tests for appropriate response for one project.
        """
        create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        response = self.client.get(reverse('projects:index'))

        self.assertQuerysetEqual(
            response.context['project_list'],
            ['<Project: Star Wars>']
        )

    def test_two_projects(self):
        """
            Tests for appropriate response for two projects.
        """
        create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        create_project(title="Sea Photoshoot", description="Need a diver.", location="Edinburgh")
        response = self.client.get(reverse('projects:index'))

        self.assertQuerysetEqual(
            response.context['project_list'],
            ['<Project: Star Wars>','<Project: Sea Photoshoot>'],
            ordered=False
        )  

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

        self.assertContains(response, "No requirements")
        self.assertEqual(response.context['project'].title, "Star Wars")          

    def test_one_requirement(self):
        """
            Tests for good response when there is one requirement.
        """
        project = create_project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        requirement = create_requirements(text="Camera", project=project)
        response = self.client.get(reverse('projects:detail', args=(project.id,)))
        
        self.assertEqual(response.context['project'].title, "Star Wars")
        self.assertQuerysetEqual(
            response.context['requirements'],
            ['<Requirement: Camera>'],
            ordered=False 
        )   