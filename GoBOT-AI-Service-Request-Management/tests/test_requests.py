from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from notifications.models import Notification
from requests_app.models import ServiceRequest


class RequestFlowTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user("cust", password="pass12345", role=User.Role.CUSTOMER)
        self.other = User.objects.create_user("other", password="pass12345", role=User.Role.CUSTOMER)
        self.agent = User.objects.create_user("agent", password="pass12345", role=User.Role.AGENT)

    def _create(self):
        self.client.login(username="cust", password="pass12345")
        return self.client.post(
            reverse("requests_app:create"),
            {"title": "Cannot log in", "description": "Password reset fails. Urgent please."},
        )

    def test_login_required(self):
        resp = self.client.get(reverse("requests_app:list"))
        self.assertEqual(resp.status_code, 302)

    def test_create_triages_and_notifies_agents(self):
        self._create()
        req = ServiceRequest.objects.get()
        self.assertEqual(req.requester, self.customer)
        self.assertEqual(req.category, "account")
        self.assertEqual(req.priority, "urgent")
        self.assertTrue(Notification.objects.filter(user=self.agent).exists())

    def test_other_customer_cannot_view(self):
        self._create()
        req = ServiceRequest.objects.get()
        self.client.logout()
        self.client.login(username="other", password="pass12345")
        self.assertEqual(self.client.get(req.get_absolute_url()).status_code, 403)

    def test_agent_update_notifies_requester(self):
        self._create()
        req = ServiceRequest.objects.get()
        self.client.logout()
        self.client.login(username="agent", password="pass12345")
        self.client.post(
            req.get_absolute_url(),
            {"action": "update", "status": "in_progress", "priority": "high", "category": "account", "assigned_to": self.agent.pk},
        )
        req.refresh_from_db()
        self.assertEqual(req.status, "in_progress")
        self.assertTrue(Notification.objects.filter(user=self.customer, message__contains="In Progress").exists())

    def test_customer_cannot_update_status(self):
        self._create()
        req = ServiceRequest.objects.get()
        resp = self.client.post(req.get_absolute_url(), {"action": "update", "status": "closed"})
        self.assertEqual(resp.status_code, 403)
        req.refresh_from_db()
        self.assertEqual(req.status, "open")
