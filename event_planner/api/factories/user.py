import datetime
import secrets
import string

import factory as f
from allauth.account.models import EmailAddress
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime

from ..models import User

KNOWN_PASSWORD = "ThisPasswordIsKnown"  # noqa: S105


def create_password(*, with_known_password: bool = False, use_md5: bool = True) -> str:
    """
    Create a password for a user.

    Args:
        with_known_password: If True, the password will be KNOWN_PASSWORD.
        use_md5: If True, the password will be encrypted with md5.

    Returns:
        The encrypted and salted password.

    """
    if with_known_password:
        password = KNOWN_PASSWORD
    else:
        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(8))

    return make_password(password, None, "md5") if use_md5 else make_password(password)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = f.Faker("email")
    password = f.LazyFunction(create_password)
    last_login = FuzzyDateTime(
        datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC),
    )
    is_superuser = f.Faker("pybool")
    first_name = f.Faker("first_name")
    last_name = f.Faker("last_name")
    is_staff = f.Faker("pybool")
    is_active = f.Faker("pybool")
    date_joined = FuzzyDateTime(
        datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC),
    )
    email_address_set = f.RelatedFactoryList(
        "event_planner.api.factories.user.EmailAddressFactory",
        "user",
        size=1,
        email=f.SelfAttribute("..email"),
        verified=True,
    )

    class Params:
        with_known_password = f.Trait(
            password=create_password(with_known_password=True),
        )
        with_unverified_email = f.Trait(
            email_address_set=f.RelatedFactoryList(
                "event_planner.api.factories.user.EmailAddressFactory",
                "user",
                size=1,
                email=f.SelfAttribute("..email"),
                verified=False,
            ),
        )


class EmailAddressFactory(DjangoModelFactory):
    class Meta:
        model = EmailAddress

    user = f.SubFactory(UserFactory)
    email = f.Faker("email")
    primary = True
    verified = False
