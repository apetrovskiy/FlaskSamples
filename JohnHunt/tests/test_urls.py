import unittest

from random import randint
from JohnHunt.tests.status_codes import StatusCodes
from ..ch41code01 import create_bookshop_service


class TestURLs(StatusCodes):
    @staticmethod
    def get_random_isbn():
        return randint(100, 10000)

    def setUp(self):
        self.app = create_bookshop_service().test_client()
        self.isbn = self.get_random_isbn()

    def test_list(self):
        result = self.app.get('/book/list')
        assert result.status_code == self.OK

    def test_get_book(self):
        result = self.app.get('/book/2')
        assert result.status_code == self.OK

    def test_get_no_book(self):
        result = self.app.get('/book/' + str(self.isbn))
        assert result.status_code == self.NOT_FOUND

    def test_add_book(self):
        post_result = self.app.post('/book', json={
            'isbn': self.isbn, 'title': 'title001',
            'author': 'author001', 'price': 22.33})
        assert post_result.status_code == self.CREATED
        get_result = self.app.get('/book/' + str(self.isbn))
        print(get_result.status_code)
        assert get_result.status_code == self.OK

    def test_add_no_book_without_isbn(self):
        result = self.app.post('/book', json={
            'title': 'title0001',
            'author': 'author0001', 'price': 22.33})
        assert result.status_code == self.BAD_REQUEST

    def test_delete_book(self):
        post_result = self.app.post('/book', json={
            'isbn': self.isbn, 'title': 'title002',
            'author': 'author002', 'price': 33.22})
        assert post_result.status_code == self.CREATED
        delete_result = self.app.delete('/book/' + str(self.isbn))
        assert delete_result.status_code == self.OK

    def test_no_delete_book(self):
        result = self.app.delete('/book/' + str(self.isbn))
        assert result.status_code == self.OK

    def test_update_book(self):
        post_result = self.app.post('/book', json={
            'isbn': self.isbn, 'title': 'title003',
            'author': 'author003', 'price': 35.25})
        assert post_result.status_code == self.CREATED
        get_result = self.app.get('/book/' + str(self.isbn))
        print(get_result.status_code)
        assert get_result.status_code == self.OK
        put_result = self.app.put('/book', json={
            'isbn': self.isbn, 'title': 'title003u',
            'author': 'author003u', 'price': 44.44})
        print(put_result.status_code)
        assert put_result.status_code == self.CREATED

    def test_no_update_book_wrong_isbn(self):
        result = self.app.put('/book', json={
            'isbn': self.isbn, 'title': 'title004',
            'author': 'author004', 'price': 33.22})
        assert result.status_code == self.NOT_FOUND

    def test_no_update_book_missing_isbn(self):
        result = self.app.put('/book', json={
            'title': 'title005', 'author': 'author005', 'price': 33.22})
        assert result.status_code == self.BAD_REQUEST


if __name__ == '__main__':
    unittest.main()
