## Django Rest Framework Serializer Error Messages

- **required**: The field is required.
- **null**: This field may not be null.
- **blank**: This field may not be blank.
- **invalid**: Enter a valid value.
- **invalid_choice**: "{input}" is not a valid choice.
- **max_length**: Ensure this field has no more than {max_length} characters.
- **min_length**: Ensure this field has at least {min_length} characters.
- **max_value**: Ensure this value is less than or equal to {max_value}.
- **min_value**: Ensure this value is greater than or equal to {min_value}.
- **max_digits**: Ensure that there are no more than {max_digits} digits in total.
- **max_decimal_places**: Ensure that there are no more than {max_decimal_places} decimal places.
- **max_whole_digits**: Ensure that there are no more than {max_whole_digits} digits before the decimal point.
- **invalid_date**: "{input}" is not a valid date.
- **invalid_datetime**: "{input}" is not a valid datetime.
- **invalid_time**: "{input}" is not a valid time.
- **missing_items**: This field is missing items.
- **invalid_image**: Upload a valid image. The file you uploaded was either not an image or a corrupted image.
- **does_not_exist**: Invalid pk "{pk_value}" - object does not exist.
- **incorrect_type**: Incorrect type. Expected {data_type}, received {input_type}.

## Password Related Error Messages

- **password_too_short**: This password is too short. It must contain at least {min_length} characters.
- **password_too_common**: This password is too common.
- **password_entirely_numeric**: This password is entirely numeric.
- **password_similar_to_username**: The password is too similar to the username.
- **password_similar_to_attributes**: The password is too similar to the user's personal information.
- **password_no_special_characters**: Password must contain at least %(min_characters)s special character (%(special_characters)s).

## Login Related Error Messages

- **invalid_login**: The username and password you entered did not match our records. Please double-check and try again.
- **inactive**: This account is inactive.
- **invalid**: Please enter a correct username and password. Note that both fields may be case-sensitive.
- **max_attempts**: You have exceeded the maximum number of login attempts. Please try again later.

## Other

- **missing_query_parameter**: This query parameter is missing.

## Example

The errors are returned in the following format. This are field level validation errors. The field name being as json key and values are diffrent errors that are raised.

```

{
  "organization": {
    "domain": [
      "unique"
    ]
  },
  "email": [
    "invalid"
  ],
  "first_name": [
    "blank"
  ],
  "last_name": [
    "blank"
  ],
  "password1": [
    "password_too_short",
    "password_too_common",
    "password_entirely_numeric",
    "password_no_special_characters"
  ]
}

```

For general errors that are related to any specific field are returned with key `detail` or `no_field_errors`.

```
{
    "detail": "not_authenticated"
}

```
