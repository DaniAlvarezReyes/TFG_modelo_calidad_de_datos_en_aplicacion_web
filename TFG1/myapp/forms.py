from django import forms

"""class CreateNewTask(forms.Form):
    title = forms.CharField(label="Titulo de tarea", max_length=200)
    description = forms.CharField(widget=forms.Textarea, label="Descipción de la tarea")

class CreateNewAnalisis(forms.Form):
    name = forms.CharField(label="Titulo", max_length=200)
    """
class NewRegistro(forms.Form):
    username = forms.CharField(label="Nombre", max_length=50)
    lastname = forms.CharField(label="Apellido", max_length=70)
    user = forms.CharField(label="Usuario", max_length=70)
    password = forms.CharField(label="Contraseña", max_length=20)
    email = forms.EmailField(label="Email", max_length=100)

class iniciarSesion(forms.Form):
    user = forms.CharField(label="Usuario", max_length=70)
    password = forms.CharField(label="Contraseña", max_length=20)