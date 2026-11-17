from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from notifications.services import notify, notify_many

from . import ai
from .forms import CommentForm, ServiceRequestForm, StaffUpdateForm
from .models import ServiceRequest


def _can_view(user, req: ServiceRequest) -> bool:
    return user.is_agent or req.requester_id == user.id


@login_required
def request_list(request):
    qs = ServiceRequest.objects.select_related("requester", "assigned_to")
    if not request.user.is_agent:
        qs = qs.filter(requester=request.user)

    status = request.GET.get("status", "")
    if status in ServiceRequest.Status.values:
        qs = qs.filter(status=status)

    return render(
        request,
        "requests_app/list.html",
        {"requests": qs, "status_choices": ServiceRequest.Status.choices, "current_status": status},
    )


@login_required
def request_create(request):
    form = ServiceRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.requester = request.user
        result = ai.triage(obj.title, obj.description)
        obj.category = result["category"]
        obj.priority = result["priority"]
        obj.ai_summary = result["summary"]
        obj.ai_suggested = True
        obj.save()

        agents = User.objects.filter(role__in=[User.Role.AGENT, User.Role.ADMIN])
        notify_many(agents, f"New {obj.get_priority_display()} request: {obj.title}", obj.get_absolute_url())
        messages.success(request, "Request submitted. GoBOT categorised it for the support team.")
        return redirect(obj)
    return render(request, "requests_app/form.html", {"form": form})


@login_required
def request_detail(request, pk):
    obj = get_object_or_404(ServiceRequest.objects.select_related("requester", "assigned_to"), pk=pk)
    if not _can_view(request.user, obj):
        raise PermissionDenied

    comment_form = CommentForm()
    update_form = StaffUpdateForm(instance=obj) if request.user.is_agent else None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "comment":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.request = obj
                comment.author = request.user
                comment.save()
                recipient = obj.requester if request.user.is_agent else obj.assigned_to
                if recipient and recipient != request.user:
                    notify(recipient, f"New reply on #{obj.pk}: {obj.title}", obj.get_absolute_url())
                return redirect(obj)

        elif action == "update" and request.user.is_agent:
            old_status, old_assignee = obj.status, obj.assigned_to_id
            update_form = StaffUpdateForm(request.POST, instance=obj)
            if update_form.is_valid():
                obj = update_form.save()
                if obj.status != old_status:
                    notify(obj.requester, f"Your request #{obj.pk} is now {obj.get_status_display()}.", obj.get_absolute_url())
                if obj.assigned_to_id and obj.assigned_to_id != old_assignee and obj.assigned_to != request.user:
                    notify(obj.assigned_to, f"You were assigned request #{obj.pk}: {obj.title}", obj.get_absolute_url())
                messages.success(request, "Request updated.")
                return redirect(obj)
        else:
            raise PermissionDenied

    return render(
        request,
        "requests_app/detail.html",
        {"req": obj, "comments": obj.comments.select_related("author"), "comment_form": comment_form, "update_form": update_form},
    )
