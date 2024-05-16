## Social Authentication

To enable social authentication, follow the steps below:

### Configuration

1. Navigate to the settings directory and open `rest_auth.py`.
2. Set `SOCIAL_ACCOUNT_ENABLED` to `True`.

### Google Authentication Setup

1. **Environment Variables**:
   For Google sign-in functionality, set the following environment variables:

    ```bash
    SOCIAL_ACCOUNT_GOOGLE_CLIENT_ID=""
    SOCIAL_ACCOUNT_GOOGLE_CLIENT_SECRET=""
    ```

2. **Google Cloud Console**:
   Obtain the values for the environment variables from the [Google Cloud Console](https://console.cloud.google.com/) by registering your application and performing the necessary configurations.

    Additionally, set the callback URI:

    ```bash
    SOCIAL_ACCOUNT_CALLBACK_GOOGLE=""
    ```

    This variable should redirect to the responsible backend or frontend entity catching the authorization code from Google. Ensure the same callback URI is set in the Google Cloud Console.

3. **Authorization Code**:
   To get the authorization code, make a `GET` request to the following URL:

    ```
    https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=<SOCIAL_ACCOUNT_CALLBACK_GOOGLE>&prompt=consent&response_type=code&client_id=<SOCIAL_ACCOUNT_GOOGLE_CLIENT_ID>&scope=openid%20email%20profile&access_type=offline
    ```

    This step is only required for the initial authentication.

4. **Capture Authorization Code**:
   Retrieve the authorization code from the callback URL.

5. **Post Request**:
   With the authorization code, make a POST request to:

    ```
    /api/auth/google/code/
    ```

With these steps completed, your application should be set up for Google authentication.
