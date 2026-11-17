from django import forms

from accounts.models import User

from .models import Comment, ServiceRequest


class ServiceRequestForm(forms.ModelForm):
    """Customers only describe the problem; GoBOT fills in category/priority."""

    class Meta:
        model = ServiceRequest
        fields = ("title", "description")
        widgets = {"description": forms.Textarea(attrs={"rows": 6})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a reply…"})}
        labels = {"body": ""}


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ("status", "priority", "category", "assigned_to")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = User.objects.filter(role__in=[User.Role.AGENT, User.Role.ADMIN])
        self.fields["assigned_to"].required = False
