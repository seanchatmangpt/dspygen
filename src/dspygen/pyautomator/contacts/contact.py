from __future__ import annotations

import objc
from Contacts import (CNMutableContact, CNContactStore, CNLabeledValue, CNSaveRequest,
                      CNContact, CNPostalAddress, CNContactFormatter, CNPostalAddressFormatter, 
                      CNLabelHome, CNLabelWork, CNPhoneNumber, CNMutablePostalAddress, CNContactFormatterStyleFullName)
from Foundation import NSString, NSDateComponents
from typing import Optional, List, Dict

class ContactError(Exception):
    pass

class Contact:
    def __init__(self):
        self.contact_store = CNContactStore.alloc().init()
        self.cn_contact = CNMutableContact.alloc().init()

    @classmethod
    def create(cls, given_name: str, family_name: str,
               email_addresses: Optional[List[tuple[str, str]]] = None, 
               phone_numbers: Optional[List[tuple[str, str]]] = None, 
               postal_address: Optional[Dict[str, str]] = None, 
               birthday: Optional[Dict[str, int]] = None, 
               image_data: Optional[bytes] = None):
        contact = cls()
        contact.given_name = given_name
        contact.family_name = family_name
        if email_addresses:
            contact.email_addresses = email_addresses
        if phone_numbers:
            contact.phone_numbers = phone_numbers
        if postal_address:
            contact.set_postal_address(**postal_address)
        if birthday:
            contact.set_birthday(**birthday)
        if image_data:
            contact.image_data = image_data
        return contact

    @classmethod
    def from_cn_contact(cls, cn_contact: CNContact):
        contact = cls()
        contact.cn_contact = cn_contact.mutableCopy()
        return contact

    @property
    def given_name(self) -> str:
        return self.cn_contact.givenName()

    @given_name.setter
    def given_name(self, value: str):
        self.cn_contact.setGivenName_(value)

    @property
    def family_name(self) -> str:
        return self.cn_contact.familyName()

    @family_name.setter
    def family_name(self, value: str):
        self.cn_contact.setFamilyName_(value)

    @property
    def email_addresses(self) -> List[tuple[str, str]]:
        return [(str(email.label()), str(email.value())) for email in self.cn_contact.emailAddresses()]

    @email_addresses.setter
    def email_addresses(self, emails: List[tuple[str, str]]):
        self.cn_contact.setEmailAddresses_([CNLabeledValue.labeledValueWithLabel_value_(label, email) for label, email in emails])

    @property
    def phone_numbers(self) -> List[tuple[str, str]]:
        return [(str(phone.label()), str(phone.value().stringValue())) for phone in self.cn_contact.phoneNumbers()]

    @phone_numbers.setter
    def phone_numbers(self, phones: List[tuple[str, str]]):
        self.cn_contact.setPhoneNumbers_([CNLabeledValue.labeledValueWithLabel_value_(label, CNPhoneNumber.phoneNumberWithStringValue_(phone)) for label, phone in phones])

    def set_postal_address(self, street: str, city: str, state: str, postal_code: str, country: Optional[str] = None):
        address = CNMutablePostalAddress.alloc().init()
        address.setStreet_(street)
        address.setCity_(city)
        address.setState_(state)
        address.setPostalCode_(postal_code)
        if country:
            address.setCountry_(country)
        self.cn_contact.setPostalAddresses_([CNLabeledValue.labeledValueWithLabel_value_(CNLabelHome, address)])

    def set_birthday(self, day: int, month: int, year: Optional[int] = None):
        birthday = NSDateComponents.alloc().init()
        birthday.setDay_(day)
        birthday.setMonth_(month)
        if year:
            birthday.setYear_(year)
        self.cn_contact.setBirthday_(birthday)

    @property
    def image_data(self) -> Optional[bytes]:
        return self.cn_contact.imageData()

    @image_data.setter
    def image_data(self, value: Optional[bytes]):
        self.cn_contact.setImageData_(value)

    def save(self) -> None:
        save_request = CNSaveRequest.alloc().init()
        save_request.addContact_toContainerWithIdentifier_(self.cn_contact, None)
        success, error = self.contact_store.executeSaveRequest_error_(save_request, None)
        if not success:
            raise ContactError(f"Failed to save contact: {error}")

    def remove(self) -> None:
        save_request = CNSaveRequest.alloc().init()
        save_request.deleteContact_(self.cn_contact)
        success, error = self.contact_store.executeSaveRequest_error_(save_request, None)
        if not success:
            raise ContactError(f"Failed to remove contact: {error}")

    @classmethod
    def fetch_contacts(cls, predicate, keys_to_fetch: List[str]):
        try:
            cn_contacts = cls().contact_store.unifiedContactsMatchingPredicate_keysToFetch_error_(predicate, keys_to_fetch, None)
            return [cls.from_cn_contact(cn_contact) for cn_contact in cn_contacts[0]]
        except objc.error as e:
            raise ContactError(f"Failed to fetch contacts: {str(e)}")

    def __str__(self) -> str:
        return CNContactFormatter.stringFromContact_style_(self.cn_contact, CNContactFormatterStyleFullName)

# Example usage
if __name__ == "__main__":
    try:
        # contact = Contact.create(
        #     given_name="John",
        #     family_name="Doe",
        #     email_addresses=[(CNLabelHome, "john.doe@example.com"), (CNLabelWork, "j.doe@work.com")],
        #     phone_numbers=[(CNLabelHome, "(555) 123-4567")],
        #     postal_address={"street": "123 Apple St", "city": "Cupertino", "state": "CA", "postal_code": "95014"},
        #     birthday={"day": 1, "month": 4, "year": 1988}
        # )
        # contact.save()
        # print(f"Saved contact: {contact}")

        # Fetch and print all contacts
        all_contacts = Contact.fetch_contacts(None, [CNContactFormatter.descriptorForRequiredKeysForStyle_(CNContactFormatterStyleFullName)])
        print("\nAll contacts:")
        for c in all_contacts:
            print(c)

    except ContactError as e:
        print(f"Error: {e}")