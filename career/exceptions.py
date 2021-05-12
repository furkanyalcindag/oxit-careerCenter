
class LanguageCodeException(Exception):
    """Exception raised for errors in the valid language."""

    def __str__(self):
        return 'Geçerli bir dil kodu gönderin'