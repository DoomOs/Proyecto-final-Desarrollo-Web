from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Project

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'project-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', css_class='form-control', title='Nombre Personalizado'),
            Field('description', css_class='form-control', title='Descripción Personalizada'),
            Submit('submit', 'Guardar Proyecto')
        )
        self.fields['name'].label = 'Nombre del Proyecto'  
        self.fields['description'].label = 'Descripción del Proyecto'  
    class Meta:
        model = Project
        fields = ['name', 'description']
