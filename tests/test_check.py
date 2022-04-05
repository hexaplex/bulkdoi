import unittest
from .context.batchdoi import check


class TestCheckHeader(unittest.TestCase):
    def test_good_header(self):
        header = ['URL', 'Creators', 'Title', 'Publisher', 'Publication Year', 'Resource Type', 'Description']
        errors = check.checkheader(header)
        self.assertFalse(errors)

    def test_empty_header(self):
        header = []
        errors = check.checkheader(header)
        self.assertTrue(errors)

    def test_bad_field_name(self):
        header = ['URL', 'Creators', 'XXX', 'Publisher', 'Publication Year', 'Resource Type', 'Description']
        errors = check.checkheader(header)
        self.assertTrue(errors)

    def test_case_insensitive(self):
        header = ['url', 'creators', 'title', 'publisher', 'publication year', 'resource Type', 'description']
        errors = check.checkheader(header)
        self.assertFalse(errors)


class TestUrlIsMalformed(unittest.TestCase):
    def test_http_accepted(self):
        response = check.url_is_malformed('http://example.com')
        self.assertIsNone(response)

    def test_https_accepted(self):
        response = check.url_is_malformed('https://example.com')
        self.assertIsNone(response)

    def test_ftp_accepted(self):
        response = check.url_is_malformed('ftp://example.com')
        self.assertIsNone(response)

    def test_empty_rejected(self):
        response = check.url_is_malformed('')
        self.assertIsNotNone(response)

    def test_bad_protocol_rejected(self):
        response = check.url_is_malformed('feed://example.com/rss.xml')
        self.assertIsNotNone(response)


class TestCreatorsIsMalformed(unittest.TestCase):
    def test_normal_organization(self):
        response = check.creators_is_malformed('[Some Organization]')
        self.assertIsNone(response)

    def test_normal_single_name(self):
        response = check.creators_is_malformed('Madonna')
        self.assertIsNone(response)

    def test_normal_double_name(self):
        response = check.creators_is_malformed('Smith, Joe')
        self.assertIsNone(response)

    def test_multiple_items(self):
        response = check.creators_is_malformed('[Some Organization];Smith, Joe')
        self.assertIsNone(response)

    def test_empty_rejected(self):
        response = check.creators_is_malformed('')
        self.assertIsNotNone(response)

    def test_extra_left_bracket(self):
        response = check.creators_is_malformed('[[Some Organization]')
        self.assertIsNotNone(response)

    def test_double_brackets(self):
        response = check.creators_is_malformed('[First][Second]')
        self.assertIsNotNone(response)

    def test_multiple_commas(self):
        response = check.creators_is_malformed('Brown, Alice, Mary')
        self.assertIsNotNone(response)

    def test_name_with_embedded_left_bracket(self):
        response = check.creators_is_malformed('Brown, Al[ice')
        self.assertIsNotNone(response)

    def test_name_with_embedded_right_bracket(self):
        response = check.creators_is_malformed('Brown], Alice')
        self.assertIsNotNone(response)


class TestTitleIsMalformed(unittest.TestCase):
    def test_normal(self):
        response = check.title_is_malformed('This is a title')
        self.assertIsNone(response)

    def test_empty_rejected(self):
        response = check.title_is_malformed('')
        self.assertIsNotNone(response)


class TestPublisherIsMalformed(unittest.TestCase):
    def test_normal(self):
        response = check.publisher_is_malformed('This is a publisher')
        self.assertIsNone(response)

    def test_empty_rejected(self):
        response = check.publisher_is_malformed('')
        self.assertIsNotNone(response)


class TestPubyearIsMalformed(unittest.TestCase):
    def test_normal(self):
        response = check.pubyear_is_malformed(1999)
        self.assertIsNone(response)

    def test_float(self):
        response = check.pubyear_is_malformed(1999.0)
        self.assertIsNone(response)

    def test_low_number_rejected(self):
        response = check.pubyear_is_malformed(0)
        self.assertIsNotNone(response)

    def test_string_rejected(self):
        response = check.pubyear_is_malformed('')
        self.assertIsNotNone(response)


class TestRestypeIsMalformed(unittest.TestCase):
    def test_normal(self):
        accepted_values = [
            'Audiovisual',
            'Collection',
            'DataPaper',
            'Dataset',
            'Event',
            'Image',
            'InteractiveResource',
            'Model',
            'PhysicalObject',
            'Service',
            'Software',
            'Sound',
            'Text',
            'Workflow'
        ]
        for item in accepted_values:
            response = check.restype_is_malformed(item)
            self.assertIsNone(response)

    def test_not_in_list_rejected(self):
        response = check.restype_is_malformed('SomeWeirdValue')
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()