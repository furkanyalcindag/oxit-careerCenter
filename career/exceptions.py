class LanguageCodeException(Exception):
    """Exception raised for errors in the valid language."""

    def __str__(self):
        return 'Geçerli bir dil kodu gönderin'


class AppointmentValidationException(Exception):
    """Exception raised for errors in the valid appointment."""

    def __str__(self):
        return 'Geçerli bir zaman dilimi giriniz'


class ScholarshipCompanyDeleteException(Exception):
    """Exception raised for errors in the valid appointment."""

    def __str__(self):
        return 'Onaylanmış bir burs silinemez'

