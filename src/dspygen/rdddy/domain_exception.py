class DomainException(Exception):
    """Acts as a base class for defining domain-specific exceptions. These exceptions are used to signal error
    conditions in a way that is meaningful within the domain context, providing clear and actionable feedback to the
    system or the end-user. Custom exceptions derived from DomainException enhance error handling by incorporating
    domain-relevant information and context."""
