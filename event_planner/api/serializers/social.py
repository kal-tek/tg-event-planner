from dj_rest_auth.registration import serializers as social_serializers

from .common.mixins import ReadOnlySerializerMixin


class CustomSocialLoginSerializer(
    ReadOnlySerializerMixin,
    social_serializers.SocialLoginSerializer[None],
):
    access_token = None
    id_token = None
