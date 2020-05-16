from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from key_gen_apis.models import Key


factory = APIRequestFactory()
client = APIClient()


class QuestionTypeDetailAPITestCase(APITestCase):
    """ :- To test all Http methods defined inside CreateUpdateDeleteKey APIView
    """

    url = "/api/v1/generate_random_key/"

    def setUp(self):
        Key.objects.create(api_key="oWAHAwhREo76srbE5xR6")

    def test_get_method_question_type(self):
        # if key is available
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method(self):
        # new record successfully created test case
        response = client.post(
            self.url, {"api_key": "CcSTJ4FJL2cbOXLZ5UWA"}, format="json"
        )
        self.assertEqual(response.status_code, 201)
        # duplicate key error test case
        response = client.post(
            self.url, {"api_key": "CcSTJ4FJL2cbOXLZ5UWA"}, format="json"
        )
        self.assertEqual(response.status_code, 201)

    def test_put_method(self):
        Key.objects.create(api_key="oWAHAwhREo76srbE5xxy")
        self.url = self.url + "?api_key=oWAHAwhREo76srbE5xxy"
        # successfully updated
        response = client.put(self.url, {"is_blocked": False}, format="json")
        self.assertEqual(response.status_code, 200)
        # key to be updated not found
        self.url = self.url + "?api_key=NonExistingKey"
        response = client.put(self.url, {"is_blocked": False}, format="json")
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        Key.objects.create(api_key="oWAHAwhREo76srbE5xxy")
        self.url = self.url + "?api_key=oWAHAwhREo76srbE5xxy"
        # successfully deleted
        response = client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        # if key to deleted does not exist
        self.url = self.url + "?api_key=NonExistingKey"
        response = client.delete(self.url)
        self.assertEqual(response.status_code, 404)
