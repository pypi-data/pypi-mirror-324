from .tools import Executor

map = {
    # Account Operations
    "twilio_create_account": Executor.twilio_create_account,
    "twilio_list_account": Executor.twilio_list_account,
    "twilio_fetch_account": Executor.twilio_fetch_account,
    "twilio_update_account": Executor.twilio_update_account,
    
    # Phone Number Operations
    "twilio_list_available_phone_number_local": Executor.twilio_list_available_phone_number_local,
    "twilio_list_available_phone_number_mobile": Executor.twilio_list_available_phone_number_mobile,
    "twilio_list_available_phone_number_toll_free": Executor.twilio_list_available_phone_number_toll_free,
    "twilio_list_incoming_phone_number": Executor.twilio_list_incoming_phone_number,
    "twilio_fetch_incoming_phone_number": Executor.twilio_fetch_incoming_phone_number,
    "twilio_update_incoming_phone_number": Executor.twilio_update_incoming_phone_number,
    
    # Core Message Operations
    "twilio_create_message": Executor.twilio_create_message,
    "twilio_list_message": Executor.twilio_list_message,
    "twilio_fetch_message": Executor.twilio_fetch_message,
    "twilio_delete_message": Executor.twilio_delete_message,
    "twilio_update_message": Executor.twilio_update_message,
    "twilio_create_message_feedback": Executor.twilio_create_message_feedback,
    
    # Media Operations
    "twilio_list_media": Executor.twilio_list_media,
    "twilio_fetch_media": Executor.twilio_fetch_media,
    "twilio_delete_media": Executor.twilio_delete_media,
}
