"""Tests for google3.third_party.py.smbios_validation_tool.error_bucket."""

from smbios_validation_tool.error_bucket import ErrorBucket
from google3.testing.pybase import googletest


class ErrorBucketTest(googletest.TestCase):

  def setUp(self):
    super(ErrorBucketTest, self).setUp()
    self.error_bucket = ErrorBucket()

  def test_adding_errors_in_bucket(self):
    self.assertEmpty(self.error_bucket.bucket)

    self.error_bucket.add_error('1', ('err_1', 'action_1'))
    self.error_bucket.add_error('1', ('err_2', 'action_2'))
    self.error_bucket.add_error('2', ('err_3', 'action_3'))

    current_bucket = self.error_bucket.bucket
    self.assertLen(current_bucket, 2)
    self.assertEqual(current_bucket['1'], [('err_1', 'action_1'),
                                           ('err_2', 'action_2')])
    self.assertEqual(current_bucket['2'], [('err_3', 'action_3')])


if __name__ == '__main__':
  googletest.main()
