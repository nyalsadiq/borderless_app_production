from django.test import TestCase
from .models import Project
# Create your tests here.

class ProjectModelTests(TestCase):

    def test_to_string(self):
        project = Project(title="Star Wars", description="Need a cameraman.", location="Edinburgh")
        self.assertEqual(project.to_string(), "Star Wars Need a cameraman.")