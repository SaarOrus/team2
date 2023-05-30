from datetime import date
import pytest
from django.contrib.auth import get_user_model
from users.models import Profile

USER_NAME = 'testuser'
USER_PASSWORD = 'testpass'
PHONE_NUMBER = '1234567890'
PHONE_NUMBER_NEW = '0987654321'


@pytest.fixture
def user1():
    user = get_user_model().objects.create(username=USER_NAME, password=USER_PASSWORD)
    user.save()
    return user


@pytest.fixture
def profile_user1(user1):
    profile_user = Profile.objects.create(user=user1, date_of_birth=date.today(), phone_number=PHONE_NUMBER)
    profile_user.save()
    return profile_user


@pytest.mark.django_db()
class TestProfileModel:
    def test_profile_creation(self, profile_user1):
        new_profile = Profile.objects.get(user=profile_user1.user)
        assert new_profile.phone_number == PHONE_NUMBER

    def test_profile_image(self, profile_user1):
        new_profile = Profile.objects.get(user=profile_user1.user)
        assert str(new_profile.image) == 'default.jpg'

    def test_profile_string_representation(self, profile_user1):
        new_profile = Profile.objects.get(user=profile_user1.user)
        assert str(new_profile) == USER_NAME

    def test_update_profile(self, profile_user1):
        assert profile_user1.phone_number == PHONE_NUMBER
        profile_user1.phone_number = PHONE_NUMBER_NEW
        profile_user1.save()
        updated_profile = Profile.objects.get(user=profile_user1.user)
        assert updated_profile.phone_number == PHONE_NUMBER_NEW

    def test_delete_profile(self, profile_user1):
        profile_user1.delete()
        assert profile_user1 not in Profile.objects.all()

    def test_delete_user_deletes_profile(self, profile_user1):
        profile_user1.user.delete()
        assert profile_user1 not in Profile.objects.all()

    def test_static_profile(self):
        user = get_user_model().objects.filter(username='Danny').first()
        profile = Profile.objects.filter(user=user).first()
        assert profile.user == user
