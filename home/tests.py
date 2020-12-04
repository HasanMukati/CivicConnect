from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Category, Post, Comment, Suggestions



def createCategory(category_title, slug_value):
    return Category.objects.create(title=category_title, slug=slug_value)

def createPost(post_title, post_text, post_category, post_publish, post_slug):
    return Post.objects.create(title=post_title, text=post_text, category=post_category, publish=post_publish, slug=post_slug)


class CategoryCreationTests(TestCase):

    def testCategoryCreation(self):
        test = createCategory("Education", "Education")
        response = self.client.get(reverse('singleCategory', args=(test.slug,)), secure=True)
        self.assertEqual(response.status_code, 200)


class PostCreationTests(TestCase):

    def testPostCreation(self):
        test_cat = createCategory("Education", "Education")
        test_post = createPost("Education Template 1", "asdf", test_cat, timezone.now(), "Education0")
        response = self.client.get(reverse('comment', args=(test_cat.slug, test_post.slug,)), secure=True)
        self.assertEqual(response.status_code, 200)



"""
These tests ensure that each of the models are built correctly
Models covered:
    Comment
    Post
    Category
"""
class CommentModelTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        newCategory = createCategory("Education", "Education")
        newPost = createPost("Edu template 1", "test text", newCategory, timezone.now(), "Education0")
        testComment = Comment.objects.create(post=newPost, author="test author", text="test comment body", created_date=timezone.now())

    def test_name_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_text_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_post_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('post').verbose_name
        self.assertEqual(field_label, 'post')

    def test_created_date_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('created_date').verbose_name
        self.assertEqual(field_label, 'created date')

class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        newCategory = createCategory("Healthcare", "Healthcare")
        testPost = createPost("Health Template 1", "test text", newCategory, timezone.now(), "healthcare1")

    def test_text_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_text_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_category_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_publish_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('publish').verbose_name
        self.assertEqual(field_label, 'publish')

    def test_slug_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        testCategory = createCategory("Civil Rights", "Civil-Rights")

    def test_slug_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')

    def test_title_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

class SuggestionsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        testSuggestion = Suggestions.objects.create(name="test name", 
                                                    email="testemail@example.com",
                                                    subject="Test Subject",
                                                    message="Test message body")

    def test_name_label(self):
        suggestion = Suggestions.objects.get(id=1)
        field_label = suggestion._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_email_label(self):
        suggestion = Suggestions.objects.get(id=1)
        field_label = suggestion._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_subject_label(self):
        suggestion = Suggestions.objects.get(id=1)
        field_label = suggestion._meta.get_field('subject').verbose_name
        self.assertEqual(field_label, 'subject')

    def test_message_label(self):
        suggestion = Suggestions.objects.get(id=1)
        field_label = suggestion._meta.get_field('message').verbose_name
        self.assertEqual(field_label, 'message')




"""
These tests ensure that the views are accessible and respond correctly
"""
class CategoriesHomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass # leaving the stub here, nothing is needed to be set up

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/categories/', secure=True)
        self.assertEqual(response.status_code, 200)

    def test_url_requires_secure_connection(self):
        response = self.client.get('/categories/', secure=False)
        self.assertEqual(response.status_code, 301)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('categories'), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('categories'), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')

class TemplateListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_cat = createCategory("Education","education")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/categories/education/', secure=True)
        self.assertEqual(response.status_code, 200)

    def test_url_requires_secure_connection(self):
        response = self.client.get('/categories/education/', secure=False)
        self.assertEqual(response.status_code, 301)

    def test_view_uses_correct_template(self):
        response = self.client.get('/categories/education/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')