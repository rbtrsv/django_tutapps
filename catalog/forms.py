from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms

# The declaration syntax for a Form is very similar to that for declaring a Model, and shares the same field types (and some similar parameters).
# To create a Form, we import the forms library, derive from the Form class, and declare the form's fields.
class RenewBookForm(forms.Form):
    """Form for a librarian to renew books."""
    # In this case, we have a single DateField for entering the renewal date that will render in HTML with a blank value, the default label "Renewal date:".
    # And some helpful usage text: "Enter a date between now and 4 weeks (default 3 weeks)."
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    # The easiest way to validate a single field is to override the method clean_<fieldname>() for the field you want to check.
    # For example, we can validate that entered renewal_date values are between now and 4 weeks by implementing clean_renewal_date()
    def clean_renewal_date(self):
        # There are two important things to note:
        # 1 We get our data using self.cleaned_data['renewal_date'] and we return this data whether or not we change it at the end of the function.
        # This step gets us the data "cleaned" and sanitized of potentially unsafe input using the default validators, and converted into the correct standard type for the data (in this case a Python datetime.datetime object).
        data = self.cleaned_data['renewal_date']

        # 2 If a value falls outside our range we raise a ValidationError, specifying the error text that we want to display in the form if an invalid value is entered.
        # Check date is not in past.
        if data < datetime.date.today():
            # The examples below also wrap the text in one of Django's translation functions ugettext_lazy() (imported as _()), which is good practice if you want to translate your site later.
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


# Alternative  method:

# Creating a Form class using the approach described above is very flexible, allowing you to create whatever sort of form page you like and associate it with any model or models.

# However, if you just need a form to map the fields of a single model then your model will already define most of the information that you need in your form: fields, labels, help text etc.
# Rather than recreating the model definitions in your form, it is easier to use the ModelForm helper class to create the form from your model. 
# This ModelForm can then be used within your views in exactly the same way as an ordinary Form.

# from django.forms import ModelForm

# from catalog.models import BookInstance

# class RenewBookModelForm(ModelForm):
#     def clean_due_back(self):
#        data = self.cleaned_data['due_back']

#        # Check if a date is not in the past.
#        if data < datetime.date.today():
#            raise ValidationError(_('Invalid date - renewal in past'))

#        # Check if a date is in the allowed range (+4 weeks from today).
#        if data > datetime.date.today() + datetime.timedelta(weeks=4):
#            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

#        # Remember to always return the cleaned data.
#        return data

#     class Meta:
#         # All you need to do to create the form is add class Meta with the associated model (BookInstance) and a list of the model fields to include in the form.
#         model = BookInstance
#         # You can also include all fields in the form using fields = '__all__', or you can use exclude (instead of fields) to specify the fields not to include from the model).
#         fields = ['due_back']
#         # In this form, we might want a label for our field of "Renewal date" (rather than the default based on the field name: Due Back), and we also want our help text to be specific to this use case. 
#         labels = {'due_back': _('Renewal date')}
#         help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}