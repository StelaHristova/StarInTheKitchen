from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    def __init__(self, *args, **kwargs):
        self.is_default = kwargs.pop('is_default', False)
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if self.is_default:
            context['widget']['is_initial'] = False
            context['widget']['clear_checkbox_label'] = ''
            context['widget']['input_text'] = ''
        return context
