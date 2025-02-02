from django.test import TestCase
from ..services.user_service import UserService
from ..utils.j_ulid_field import JULIDField
import datetime
from ulid import ULID

class UserBaseTest(TestCase):
    def setUp(self):
        pass

    __right = {
        "account": 'u001',
    }

    def test_add(self):
        result, err = UserService.user_add(self.__right)
        print("> UserBaseTest: test_add err:", result, err)
        # u12 = JULIDField.get_u12()
        # u26 = JULIDField.from_u12(u12)
        # print("> UserBaseTest: JULIDField:", u12, u26)
        # print("> UserBaseTest: JULIDField:", u26.datetime, u26.hex)
        self.assertEqual(err, None)

    def test_detail(self):
        UserService.user_add(self.__right)
        exist, err = UserService.check_account('u001')
        print("> UserBaseTest: test_detail:", exist, err)
        self.assertEqual(err, None)

    def test_edit(self):
        UserService.user_add(self.__right)
        exist, err = UserService.check_account(self.__right['account'])
        print("> UserBaseTest: test_edit: 1 exist:", exist)
        exist['fullname'] = '路乙'
        result, err = UserService.user_edit(exist, user_id=exist['user_id'])
        print("> UserBaseTest: test_edit: 2 result:", result)
        self.assertEqual(err, None)

    def test_delete(self):
        UserService.user_add(self.__right)
        exist, err = UserService.check_account(self.__right['account'])
        print("> UserBaseTest: test_delete: 1 exist:", exist)

        result, err = UserService.user_delete(exist['user_id'])
        print("> ThreadClassifyTest::test_delete:", result)
        self.assertEqual(err, None)