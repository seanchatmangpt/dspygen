from .contact import Contact, ContactError
from Contacts import CNContactType, CNLabelWork

class OrganizationContact(Contact):
    @classmethod
    def create(cls, organization_name: str, **kwargs):
        contact = cls()
        contact.cn_contact.setContactType_(CNContactType.CNContactTypeOrganization)
        contact.organization_name = organization_name
        
        if 'email_addresses' in kwargs:
            contact.email_addresses = kwargs['email_addresses']
        if 'phone_numbers' in kwargs:
            contact.phone_numbers = kwargs['phone_numbers']
        if 'postal_address' in kwargs:
            contact.set_postal_address(**kwargs['postal_address'])
        if 'image_data' in kwargs:
            contact.image_data = kwargs['image_data']
        
        return contact

    @property
    def organization_name(self) -> str:
        return self.cn_contact.organizationName()

    @organization_name.setter
    def organization_name(self, value: str):
        self.cn_contact.setOrganizationName_(value)

# Example usage
if __name__ == "__main__":
    try:
        org = OrganizationContact.create(
            organization_name="Acme Corporation",
            email_addresses=[(CNLabelWork, "info@acme.com")],
            phone_numbers=[(CNLabelWork, "(555) 987-6543")],
            postal_address={"street": "456 Tech Blvd", "city": "San Francisco", "state": "CA", "postal_code": "94105"}
        )
        org.save()
        print(f"Saved organization contact: {org.organization_name}")
    except ContactError as e:
        print(f"Error: {e}")