from unittest import TestCase, main

from DropByDrop.ch1_4_1.code1_4_1 import app


class Code141Test(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_app(self):
        response = self.client.get("/")
        self.assertEquals(response.status, '200 OK')
        self.assertEqual(response.json, None)


if __name__ == '__main__':
    main()
