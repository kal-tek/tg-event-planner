from typing import cast

from django.conf import settings
from django.db.models.query import QuerySet

if settings.SOCIAL_ACCOUNT_ENABLED:
    from allauth.socialaccount import models as allauth_models
    from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
    from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
    from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client
    from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
    from dj_rest_auth.registration import views as registration_views
    from dj_rest_auth.social_serializers import TwitterLoginSerializer

    from ..serializers import CustomSocialLoginSerializer

    class SocialLoginView(registration_views.SocialLoginView): ...

    class GoogleLoginAuthorizationCodeView(SocialLoginView):
        """Authorization code flow for Google login."""

        adapter_class = GoogleOAuth2Adapter
        callback_url = settings.SOCIAL_ACCOUNT_CALLBACK_GOOGLE
        client_class = OAuth2Client
        serializer_class = CustomSocialLoginSerializer

    class GoogleLoginImplicitView(
        SocialLoginView,
    ):  # if you want to use Implicit Grant, use this
        adapter_class = GoogleOAuth2Adapter

    class GitHubLoginView(SocialLoginView):
        adapter_class = GitHubOAuth2Adapter
        client_class = OAuth2Client
        callback_url = getattr(settings, "SOCIAL_ACCOUNT_CALLBACK_GITHUB", None)

    class FacebookLoginView(SocialLoginView):
        adapter_class = FacebookOAuth2Adapter

    class TwitterLoginView(SocialLoginView):
        serializer_class = TwitterLoginSerializer
        adapter_class = TwitterOAuthAdapter

    class SocialAccountListView(registration_views.SocialAccountListView):
        def get_queryset(self) -> QuerySet[allauth_models.SocialAccount]:
            """Return all social accounts for the current user."""
            if self.request.user.is_authenticated:
                queryset = allauth_models.SocialAccount.objects.filter(
                    user=self.request.user,
                )
            else:
                queryset = allauth_models.SocialAccount.objects.none()

            return cast(
                QuerySet[allauth_models.SocialAccount],
                queryset,
            )

    class SocialAccountDisconnectView(registration_views.SocialAccountDisconnectView):
        def get_queryset(self) -> QuerySet[allauth_models.SocialAccount]:
            """Return all social accounts for the current user."""
            if self.request.user.is_authenticated:
                queryset = allauth_models.SocialAccount.objects.filter(
                    user=self.request.user,
                )
            else:
                queryset = allauth_models.SocialAccount.objects.none()

            return cast(
                QuerySet[allauth_models.SocialAccount],
                queryset,
            )
