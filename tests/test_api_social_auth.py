import pytest
from rest_framework import status

from django.urls import reverse
from tests.utils import social_auth_vcr
from django.contrib.auth import get_user_model


@social_auth_vcr.use_cassette(match_on=('method', 'path'))
@pytest.mark.django_db
def test_sign_up_facebook_valid_access_token(rest_client, fb_access_token):
    # Testing
    # mocker.patch.object(ConsumerWrapper, 'create')
    # auth_backend = mocker.patch.object(AuthKey, 'create')
    # auth_backend.return_value = dict(key=uuid.uuid4())  # return any uuid
    # mocker.patch('urllib2.urlopen')

    response = rest_client.post(reverse('social_oauth2:register_by_access_token', args=('facebook',)), data={
        'access_token': fb_access_token,
    })
    assert response.status_code == status.HTTP_200_OK, response.content


# @social_auth_vcr.use_cassette(match_on=('method', 'path'))
# @pytest.mark.django_db
# def test_sign_up_facebook_valid_access_token_missing_email(rest_client, fb_access_token):
#     """
#     Tests that facebook does not return an email in the response
#     """
#
#     response = rest_client.post(reverse('social_oauth2:register_by_access_token', args=('facebook',)), data={
#         'access_token': fb_access_token,
#     })
#     assert response.status_code == 400, response.content
#     assert 'email' in response.data
#     assert get_user_model().objects.count() == 0


@social_auth_vcr.use_cassette()
@pytest.mark.django_db
def test_sign_up_facebook_wrong_access_token(rest_client):
    # Testing
    with pytest.raises(Exception) as exception:
        response = rest_client.post(reverse('social_oauth2:register_by_access_token', args=('facebook',)), data={
            'access_token': 'wrong_token',
        })
