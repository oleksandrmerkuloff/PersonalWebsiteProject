from django.test import TestCase
from django.urls import reverse

from .models import Post, Tag


class BlogEngineTests(TestCase):
    def setUp(self):
        # Create some tags
        self.python_tag = Tag.objects.create(name="python")
        self.life_tag = Tag.objects.create(name="life")

        # Create a Python-focused post
        self.post_one = Post.objects.create(
            title="Learning Django Backend Architecture",
            outline="A deep dive into writing clean backend code.",
            slug="learning-django-backend",
        )
        self.post_one.tags.add(self.python_tag)

        # Create a personal life post
        self.post_two = Post.objects.create(
            title="My Journey and Moving to Kyiv",
            outline="Reflecting on life, music, and software.",
            slug="my-journey-kyiv",
        )
        self.post_two.tags.add(self.life_tag)

        # Get the named URL route for your blog list view
        self.blog_url = reverse("post-list")

    # --- 1. MODEL TESTS ---
    def test_post_creation_and_tags(self):
        """Verify that models store data correctly and relations persist."""
        post = Post.objects.get(slug="learning-django-backend")
        self.assertEqual(post.title, "Learning Django Backend Architecture")
        self.assertEqual(post.tags.count(), 1)
        self.assertIn(self.python_tag, post.tags.all())

    # --- 2. VIEW & FILTER TESTS ---
    def test_blog_view_loads_successfully(self):
        """Act & Assert: Verify that the main blog page renders a 200 OK status."""
        response = self.client.get(self.blog_url)
        self.assertEqual(response.status_code, 200)
        # Check that both posts are visible on an unfiltered page
        self.assertContains(response, self.post_one.title)
        self.assertContains(response, self.post_two.title)

    def test_blog_view_filter_by_tag(self):
        """Act & Assert: Test that passing a ?tag= query string successfully restricts results."""
        # Request only posts tagged with 'python'
        response = self.client.get(self.blog_url, {"tag": "python"})

        self.assertEqual(response.status_code, 200)
        # Python post should be here
        self.assertContains(response, self.post_one.title)
        # Life post should NOT be here
        self.assertNotContains(response, self.post_two.title)

    def test_blog_view_search_query(self):
        """Act & Assert: Test that passing a ?q= query string filters by title context."""
        # Search for the keyword "Kyiv"
        response = self.client.get(self.blog_url, {"q": "Kyiv"})

        self.assertEqual(response.status_code, 200)
        # Kyiv post should match
        self.assertContains(response, self.post_two.title)
        # Django post should be excluded
        self.assertNotContains(response, self.post_one.title)

    def test_no_results_found_fallback(self):
        """Act & Assert: Test that an empty response correctly renders our empty message state."""
        # Search for something that doesn't exist
        response = self.client.get(self.blog_url, {"q": "nonexistent_keyword"})

        self.assertEqual(response.status_code, 200)
        # HTML template text fallback string should show up
        self.assertContains(response, "No posts matched your current filter criteria.")
