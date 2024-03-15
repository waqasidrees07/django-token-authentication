from django.core.exceptions import (
    ValidationError,
)

class NumericPasswordValidator:
    """
    Validate that the password is not entirely numeric.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                ("This password is entirely numeric."),
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return ("Your password can’t be entirely numeric.")


class CapitalLetterValidator:
    """
    Validate that the password is not contain capital letter.
    """

    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                ("Password should contain at least one uppercase letter."),
                code="password_contain_capital_letter",
            )

    def get_help_text(self):
        return ("Your password should contain at least one uppercase letter.")


class SpecialCharacterValidator:
    """
    Validate that the password is not contain special character.
    """

    def validate(self, password, user=None):
        if not any(char in "!@#$%^&*()-_+=<>?/[]{}|" for char in password):
            raise ValidationError(
                ("Password should contain special character."),
                code="password_contain_special_character",
            )

    def get_help_text(self):
        return ("Your password should contain special character.")

COMMON_PASSWORDS = [
    '123456', 'password', '12345678', '123456789', '12345',
    '1234', '111111', '1234567', 'dragon', '123123', 'abc123',
    '666666', 'q@wertyuiop', '123321', 'mustang', 
    '1234567890', '121212', '000000', 
]

class CommonCharacterValidator:
    """
    Validate that the password should be strong.
    """

    def validate(self, password, user=None):
        if password.lower() in COMMON_PASSWORDS:
            raise ValidationError(
                ("Please choose a stronger password."),
                code="password_should_strong",
                )

    def get_help_text(self):
        return ("Your password should be strong.")


from django.core.exceptions import ValidationError

class CombinedPasswordValidator:
    """
    Validate password concurrently for multiple criteria.
    """

    def __init__(self):
        self.numeric_validator = NumericPasswordValidator()
        self.capital_letter_validator = CapitalLetterValidator()
        self.special_character_validator = SpecialCharacterValidator()
        self.common_character_validator = CommonCharacterValidator()

    def validate(self, password, user=None):
        errors = []

        try:
            self.numeric_validator.validate(password, user)
        except ValidationError as e:
            errors.extend(e.error_list)

        try:
            self.capital_letter_validator.validate(password, user)
        except ValidationError as e:
            errors.extend(e.error_list)

        try:
            self.special_character_validator.validate(password, user)
        except ValidationError as e:
            errors.extend(e.error_list)

        try:
            self.common_character_validator.validate(password, user)
        except ValidationError as e:
            errors.extend(e.error_list)

        if errors:
            raise ValidationError(errors)

    def get_help_texts(self):
        help_texts = {
            'numeric': self.numeric_validator.get_help_text(),
            'capital_letter': self.capital_letter_validator.get_help_text(),
            'special_character': self.special_character_validator.get_help_text(),
            'common_character': self.common_character_validator.get_help_text(),
        }
        return help_texts
