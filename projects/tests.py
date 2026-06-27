from django.test import TestCase
from django.urls import reverse

from .models import Project



class ProjectsCoreTests(TestCase):
    def setUp(self):
        self.project_one = Project.objects.create(
            name="My Website",
        )
        self.project_two = Project.objects.create(
            name="Test Project 2"
        )
        self.projects_url = reverse("projects-list")
    
    def test_project_creation(self):
        """Verify that models store data correctly and relations persist."""
        project = Project.objects.get(name="My Website")
        self.assertEqual(project.name, "My Website")
        self.assertEqual(project.description, "")
    
    def test_projects_view_loads_successfully(self):
        """Act & Assert: Verify that the main projects page renders a 200 OK status."""
        response = self.client.get(self.projects_url)
        self.assertEqual(response.status_code, 200)
        # Check that both posts are visible on an unfiltered page
        self.assertContains(response, self.project_one.name)
        self.assertContains(response, self.project_two.name)
