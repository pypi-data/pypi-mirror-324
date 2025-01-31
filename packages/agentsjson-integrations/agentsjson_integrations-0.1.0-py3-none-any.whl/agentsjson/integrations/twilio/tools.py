from typing import Any, Dict, List, Optional, Union
from twilio.rest import Client
import re

class Executor:
    @staticmethod
    def _convert_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert parameter keys from CamelCase/PascalCase to snake_case.
        Special handling for 'from' parameter to add underscore.
        """
        def camel_to_snake(name: str) -> str:
            # Special case for 'from' parameter
            if name.lower() == 'from':
                return 'from_'
            # Convert CamelCase/PascalCase to snake_case
            name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
            return name.lower()

        return {camel_to_snake(k): v for k, v in params.items() if v is not None}

    @staticmethod
    def create_client(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Client:
        """Creates a Twilio Client instance."""
        client = Client(account_sid, auth_token)
        return client

    # Account Methods
    @staticmethod
    def twilio_create_account(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new Twilio subaccount."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        return client.api.v2010.accounts.create(**params).__dict__

    @staticmethod
    def twilio_list_account(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """List all accounts associated with your account."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        return [a.__dict__ for a in client.api.v2010.accounts.list(**params)]

    @staticmethod
    def twilio_fetch_account(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch account details. If sid not provided, fetches authenticated account."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        sid = params.pop('sid', None)
        if sid:
            return client.api.v2010.accounts(sid).fetch(**params).__dict__
        return client.api.v2010.accounts(account_sid).fetch(**params).__dict__

    @staticmethod
    def twilio_update_account(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update an account's properties."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        sid = params.pop('sid')
        return client.api.v2010.accounts(sid).update(**params).__dict__

    # Phone Number Methods
    @staticmethod
    def twilio_list_available_phone_number_local(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """List available local phone numbers for purchase."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        country_code = params.pop('country_code')
        numbers = client.available_phone_numbers(country_code).local.list(**params)
        return [n.__dict__ for n in numbers]

    @staticmethod
    def twilio_list_available_phone_number_mobile(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """List available mobile phone numbers for purchase."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        country_code = params.pop('country_code')
        numbers = client.available_phone_numbers(country_code).mobile.list(**params)
        return [n.__dict__ for n in numbers]

    @staticmethod
    def twilio_list_available_phone_number_toll_free(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """List available toll-free phone numbers for purchase."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        country_code = params.pop('country_code')
        numbers = client.available_phone_numbers(country_code).toll_free.list(**params)
        return [n.__dict__ for n in numbers]

    @staticmethod
    def twilio_list_incoming_phone_number(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """List phone numbers owned by the account."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        return [n.__dict__ for n in client.incoming_phone_numbers.list(**params)]

    @staticmethod
    def twilio_fetch_incoming_phone_number(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch details of a specific phone number."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        sid = params.pop('sid')
        return client.incoming_phone_numbers(sid).fetch(**params).__dict__

    @staticmethod
    def twilio_update_incoming_phone_number(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update a phone number's configuration."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        sid = params.pop('sid')
        return client.incoming_phone_numbers(sid).update(**params).__dict__

    # Message Methods
    @staticmethod
    def twilio_create_message(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Send an SMS or MMS message with optional media attachments."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        message = client.messages.create(**params)
        return message.__dict__

    @staticmethod
    def twilio_list_message(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """List messages with optional filters for numbers and dates."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        return [m.__dict__ for m in client.messages.list(**params)]

    @staticmethod
    def twilio_fetch_message(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch a specific message by SID."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        sid = params.pop('sid')
        return client.messages(sid).fetch(**params).__dict__

    @staticmethod
    def twilio_delete_message(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Delete a message record from your account."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        sid = params.pop('sid')
        return client.messages(sid).delete()

    @staticmethod
    def twilio_update_message(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Update a message's properties."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        sid = params.pop('sid')
        return client.messages(sid).update(**params).__dict__

    @staticmethod
    def twilio_create_message_feedback(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Provide feedback about a message's delivery."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        message_sid = params.pop('message_sid')
        return client.messages(message_sid).feedback().create(**params).__dict__

    # Media Methods
    @staticmethod
    def twilio_list_media(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """List media attachments for a message with optional date filters."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        message_sid = params.pop('message_sid')
        return [m.__dict__ for m in client.messages(message_sid).media.list(**params)]

    @staticmethod
    def twilio_fetch_media(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch a specific media attachment by SID."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        message_sid = params.pop('message_sid')
        sid = params.pop('sid')
        return client.messages(message_sid).media(sid).fetch(**params).__dict__

    @staticmethod
    def twilio_delete_media(
        account_sid: str,
        auth_token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Delete a media attachment."""
        client = Executor.create_client(account_sid, auth_token)
        params = Executor._convert_params(kwargs)
        message_sid = params.pop('message_sid')
        sid = params.pop('sid')
        return client.messages(message_sid).media(sid).delete()
