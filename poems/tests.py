"""Importing modules"""
from django.test import TestCase
from django.urls import reverse
from mock import patch, MagicMock

# Create your tests here.


class PoemsTest(TestCase):
    """Class representing the tests for Poem application"""

    def test_render_index(self):
        """
        Render index successfuly
        """
        url = reverse('poems:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, '<label for="prompt">¿De qué quieres que se trate tu poema?</label>')
        self.assertContains(
            response, '<input type="text" name="prompt" value="" autocomplete="off">')
        self.assertContains(response, '<input type="submit" value="Generar">')

    @patch('requests.post')
    def test_render_prompt_violates_content_policy_message(self, request_mock):
        """
        Render index with message that says that prompt violates content policy
        """

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'violates_content_policy': True
        }
        request_mock.return_value = mock_response

        url = reverse('poems:generate')
        response = self.client.post(
            url, data={'prompt': 'my prompt'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['violates_content_policy'])
        self.assertContains(
            response, '<label for="prompt">¿De qué quieres que se trate tu poema?</label>')
        self.assertContains(
            response, '<input type="text" name="prompt" value="" autocomplete="off">')
        self.assertContains(response, '<input type="submit" value="Generar">')
        self.assertContains(
            response, "<label class='error'>El poema que quieres generar infringe las políticas de contenido</label>")

    @patch('requests.post')
    def test_render_poem_generated(self, request_mock):
        """
        Render template for poem generated successfuly
        """

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'violates_content_policy': False,
            'text': 'My Generated Poem',
            'image': 'Image of Generated Poem'
        }
        request_mock.return_value = mock_response

        url = reverse('poems:generate')
        response = self.client.post(
            url, data={'prompt': 'my prompt'})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['violates_content_policy'])
        self.assertEqual(response.context['text'], 'My Generated Poem')
        self.assertEqual(response.context['image'], 'Image of Generated Poem')
