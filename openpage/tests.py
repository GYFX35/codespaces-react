from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock # For mocking the AI service
import openai # For openai.APIError

from .models import Post
from .forms import PostForm
from .services import generate_image_from_prompt

class PostModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_create_post(self):
        """Test that a Post object can be created."""
        post = Post.objects.create(
            user=self.user,
            prompt="A test prompt for an image.",
            caption="This is a test caption."
            # ImageField can be left blank initially if allow_empty_file=True or if not required
            # For this test, we are focusing on model instance creation with text fields.
        )
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.prompt, "A test prompt for an image.")
        self.assertEqual(post.caption, "This is a test caption.")
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)
        self.assertEqual(str(post), f"Post by {self.user.username} at {post.created_at.strftime('%Y-%m-%d %H:%M')}")

class OpenPageServiceTests(TestCase):

    @patch('openpage.services.openai.OpenAI')
    @patch('openpage.services.requests.get')
    @patch('openpage.services.settings') # Mock settings for API key check
    def test_generate_image_from_prompt_success(self, mock_settings, mock_requests_get, MockOpenAI):
        """Test successful image generation from prompt."""
        mock_settings.OPENAI_API_KEY = "fake_test_key" # Ensure API key check passes

        # Configure the mock OpenAI client
        mock_openai_instance = MockOpenAI.return_value
        mock_image_response = MagicMock()
        mock_image_data = MagicMock()
        mock_image_data.url = "http://fakeurl.com/fakeimage.png"
        mock_image_response.data = [mock_image_data]
        mock_openai_instance.images.generate.return_value = mock_image_response

        # Configure the mock requests.get
        mock_response_content = b"fake image content"
        mock_requests_response = MagicMock()
        mock_requests_response.content = mock_response_content
        mock_requests_response.raise_for_status = MagicMock() # Ensure it doesn't raise error
        mock_requests_get.return_value = mock_requests_response

        prompt_text = "a cat wearing a hat"
        image_file = generate_image_from_prompt(prompt_text)

        self.assertIsNotNone(image_file)
        self.assertEqual(image_file.read(), mock_response_content)
        self.assertTrue(image_file.name.endswith("_dalle.png"))
        MockOpenAI.assert_called_once() # Check if OpenAI client was initialized
        mock_openai_instance.images.generate.assert_called_once_with(
            model="dall-e-3",
            prompt=prompt_text,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        mock_requests_get.assert_called_once_with("http://fakeurl.com/fakeimage.png", stream=True)

    @patch('openpage.services.openai.OpenAI')
    def test_generate_image_from_prompt_openai_api_error(self, MockOpenAI):
        """Test OpenAI API error during image generation."""
        mock_openai_instance = MockOpenAI.return_value
        mock_openai_instance.images.generate.side_effect = openai.APIError("Test API Error", request=None, body=None)

        image_file = generate_image_from_prompt("another prompt")
        self.assertIsNone(image_file)

    @patch('openpage.services.settings') # Mock settings directly if API key is checked first
    def test_generate_image_no_api_key(self, mock_settings):
        """Test image generation when API key is not configured."""
        mock_settings.OPENAI_API_KEY = "" # Simulate missing API key
        image_file = generate_image_from_prompt("prompt with no key")
        self.assertIsNone(image_file)


class OpenPageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewtestuser', password='password123')
        self.create_post_url = reverse('openpage:create_post')
        self.post_list_url = reverse('openpage:post_list')

    def test_post_list_view_get(self):
        """Test GET request for post list view."""
        # Create a post to be listed
        Post.objects.create(user=self.user, prompt="list test prompt", caption="list test caption")
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'openpage/post_list.html')
        self.assertContains(response, "list test prompt") # Check if post content is in response

    def test_create_post_view_get_unauthenticated(self):
        """Test GET request for create post view when not logged in (should redirect to login)."""
        response = self.client.get(self.create_post_url)
        # Expect redirect to admin login as per current base.html setup
        self.assertRedirects(response, f"{reverse('admin:login')}?next={self.create_post_url}")

    def test_create_post_view_get_authenticated(self):
        """Test GET request for create post view when logged in."""
        self.client.login(username='viewtestuser', password='password123')
        response = self.client.get(self.create_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'openpage/create_post.html')
        self.assertIsInstance(response.context['form'], PostForm)

    @patch('openpage.views.generate_image_from_prompt') # Mock the service call in views
    def test_create_post_view_post_success(self, mock_generate_image):
        """Test successful POST request to create post view."""
        self.client.login(username='viewtestuser', password='password123')

        # Mock the AI service to return a dummy ContentFile
        mock_image_content = b"fake ai image data"
        mock_file = SimpleUploadedFile("fake_image.png", mock_image_content, content_type="image/png")
        mock_generate_image.return_value = mock_file

        form_data = {
            'prompt': 'A beautiful landscape',
            'caption': 'Generated by AI'
        }
        response = self.client.post(self.create_post_url, data=form_data)

        self.assertRedirects(response, self.post_list_url) # Should redirect to post list on success
        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.prompt, 'A beautiful landscape')
        self.assertEqual(new_post.user, self.user)
        self.assertTrue(new_post.image.name.endswith('.png')) # Check if image was saved
        mock_generate_image.assert_called_once_with('A beautiful landscape')

    @patch('openpage.views.generate_image_from_prompt')
    def test_create_post_view_post_ai_failure(self, mock_generate_image):
        """Test POST request to create post view when AI generation fails."""
        self.client.login(username='viewtestuser', password='password123')
        mock_generate_image.return_value = None # Simulate AI service failure

        form_data = {
            'prompt': 'A complex prompt that fails',
            'caption': 'This should not be created'
        }
        response = self.client.post(self.create_post_url, data=form_data)

        self.assertEqual(response.status_code, 200) # Should re-render the form with an error
        # Check for the message in the response content directly or via context if using Django messages framework
        self.assertContains(response, "Could not generate image. Please try a different prompt or check API key.")
        self.assertEqual(Post.objects.count(), 0) # No post should be created

    def test_create_post_view_post_invalid_form(self):
        """Test POST request to create post view with invalid form data."""
        self.client.login(username='viewtestuser', password='password123')
        form_data = { # Missing prompt
            'caption': 'Caption without prompt'
        }
        response = self.client.post(self.create_post_url, data=form_data)
        self.assertEqual(response.status_code, 200) # Re-renders form
        self.assertFormError(response.context['form'], 'prompt', 'This field is required.')
        self.assertEqual(Post.objects.count(), 0)

    def test_post_detail_view_get(self):
        """Test GET request for post detail view."""
        post = Post.objects.create(user=self.user, prompt="detail test", caption="detail caption")
        detail_url = reverse('openpage:post_detail', kwargs={'pk': post.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'openpage/post_detail.html')
        self.assertContains(response, "detail test")
        self.assertEqual(response.context['post'], post)

class PostFormTests(TestCase):
    def test_post_form_valid(self):
        form_data = {'prompt': 'Test prompt', 'caption': 'Test caption'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_prompt_missing(self):
        form_data = {'caption': 'Test caption'} # Prompt is missing
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prompt', form.errors)

    def test_post_form_caption_optional(self):
        form_data = {'prompt': 'Test prompt'} # Caption is optional
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
