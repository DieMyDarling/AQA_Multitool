import pytest

from screenshots_processing import image_comparer

basic_urls = ['/']


@pytest.mark.parametrize('url', basic_urls)
@pytest.mark.layout
def test_basic_url_test(url, screenshots_cache):
    domain_staging = 'https://translate.google.com'
    domain_production = 'https://www.google.com'
    production_url = domain_production + url
    staging_url = domain_staging + url

    image_comparer.compare_pages(screenshots_cache, production_url, staging_url)
