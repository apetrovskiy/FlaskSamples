import unittest

from JohnHunt.tests.status_codes import StatusCodes
from ..ch41code01 import create_bookshop_service


class TestURLs(StatusCodes):
    def setUp(self):
        self.app = create_bookshop_service().test_client()

    def test_list(self):
        result = self.app.get('/book/list')
        assert result.status_code == self.OK

    def test_get_book(self):
        result = self.app.get('/book/2')
        assert result.status_code == self.OK

    def test_get_no_book(self):
        result = self.app.get('/book/1000')
        assert result.status_code == self.NOT_FOUND

    def test_add_book(self):
        result = self.app.post('/book', json={
            'isbn': 8, 'title': 'title001',
            'author': 'author001', 'price': 22.33})
        assert result.status_code == self.CREATED

    def test_delete_book(self):
        res = self.app.post('/book', json={
            'isbn': 9, 'title': 'title002',
            'author': 'author002', 'price': 33.22})
        assert res.status_code == self.CREATED
        result = self.app.delete('/book/' + str(9))
        assert result.status_code == self.OK

    def test_no_delete_book(self):
        result = self.app.delete('/book/' + str(1000))
        assert result.status_code == self.OK


if __name__ == '__main__':
    unittest.main()
