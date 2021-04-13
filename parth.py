from django.test.runner import DiscoverRunner
from HtmlTestRunner import HTMLTestRunner

class MyHTMLTestRunner(HTMLTestRunner):
    def __init__(self, **kwargs):
        # Pass any required options to HTMLTestRunner 
        super().__init__(combine_reports=True, report_name='all_tests', add_timestamp=False, **kwargs)

class HtmlTestReporter(DiscoverRunner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Patch over the test_runner in the super class.
        html_test_runner = MyHTMLTestRunner
        self.test_runner=html_test_runner