import vcr
import logging

logger = logging.getLogger(__name__)


social_auth_vcr = vcr.VCR(
    serializer='yaml',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    cassette_library_dir='tests/fixtures/vcr_cassettes/social_auth',
    record_mode='once',
    match_on=('method', 'scheme', 'port', 'path', 'query'),
)
