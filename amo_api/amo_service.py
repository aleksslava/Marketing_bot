from amo_api.amo_api import AmoCRMWrapper



def processing_contact(amo_api: AmoCRMWrapper,
                       contact_phone_number: str,) -> dict|None:
    contact_amo: tuple[bool, dict|str] = amo_api.get_contact_by_phone(phone_number=contact_phone_number)
    if contact_amo[0]: # Контакт найден
        contact = contact_amo[1]
        first_name = contact.get("first_name", "")
        last_name = contact.get("last_name", "")
        amo_id = contact.get('id', '')

        return {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": contact_phone_number,
            "amo_contact_id": amo_id,
        }
    else:
        return None