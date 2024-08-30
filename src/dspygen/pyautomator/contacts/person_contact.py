from .contact import Contact, ContactError
from Contacts import CNContactType, CNLabelHome, CNLabelWork

class PersonContact(Contact):
    @classmethod
    def create(cls, given_name: str, family_name: str, **kwargs):
        contact = cls()
        contact.cn_contact.setContactType_(CNContactType.CNContactTypePerson)
        contact.given_name = given_name
        contact.family_name = family_name
        
        if 'email_addresses' in kwargs:
            contact.email_addresses = kwargs['email_addresses']
        if 'phone_numbers' in kwargs:
            contact.phone_numbers = kwargs['phone_numbers']
        if 'postal_address' in kwargs:
            contact.set_postal_address(**kwargs['postal_address'])
        if 'birthday' in kwargs:
            contact.set_birthday(**kwargs['birthday'])
        if 'image_data' in kwargs:
            contact.image_data = kwargs['image_data']
        if 'job_title' in kwargs:
            contact.job_title = kwargs['job_title']
        if 'department_name' in kwargs:
            contact.department_name = kwargs['department_name']
        
        return contact

    @property
    def full_name(self) -> str:
        return f"{self.given_name} {self.family_name}"

# Example usage
if __name__ == "__main__":
    try:
        person = PersonContact.create(
            given_name="John",
            family_name="Doe",
            email_addresses=[(CNLabelHome, "john.doe@example.com"), (CNLabelWork, "j.doe@work.com")],
            phone_numbers=[(CNLabelHome, "(555) 123-4567")],
            postal_address={"street": "123 Apple St", "city": "Cupertino", "state": "CA", "postal_code": "95014"},
            birthday={"day": 1, "month": 4, "year": 1988},
            job_title="Software Engineer"
        )
        person.save()
        print(f"Saved person contact: {person.full_name}")
    except ContactError as e:
        print(f"Error: {e}")