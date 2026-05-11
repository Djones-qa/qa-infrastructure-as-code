"""
Performance tests using Locust.
Simulates realistic user load patterns against the application.

Run with:
    locust -f tests/performance/locustfile.py --host=https://staging.example.com
    locust -f tests/performance/locustfile.py --host=https://staging.example.com --headless -u 50 -r 5 --run-time 5m
"""
import json
import random
from locust import HttpUser, TaskSet, task, between, events
from locust.exception import RescheduleTask


class UserBehavior(TaskSet):
    """Simulates typical user behavior patterns."""

    def on_start(self):
        """Log in before running tasks."""
        self.login()

    def on_stop(self):
        """Log out after tasks complete."""
        self.logout()

    def login(self):
        """Authenticate and store session token."""
        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": "loadtest@example.com",
                "password": "LoadTestPass123!",
            },
            name="/api/v1/auth/login",
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            self.client.headers.update({"Authorization": f"Bearer {token}"})
        else:
            raise RescheduleTask()

    def logout(self):
        """Invalidate the session."""
        self.client.post("/api/v1/auth/logout", name="/api/v1/auth/logout")

    @task(5)
    def view_dashboard(self):
        """Simulate viewing the dashboard (high frequency)."""
        self.client.get("/api/v1/dashboard", name="/api/v1/dashboard")

    @task(3)
    def list_users(self):
        """Simulate listing users."""
        self.client.get(
            "/api/v1/users?page=1&limit=20",
            name="/api/v1/users [list]",
        )

    @task(2)
    def view_user_profile(self):
        """Simulate viewing a user profile."""
        user_id = random.randint(1, 100)
        self.client.get(
            f"/api/v1/users/{user_id}",
            name="/api/v1/users/[id]",
        )

    @task(1)
    def search_users(self):
        """Simulate searching for users."""
        search_terms = ["john", "jane", "test", "admin"]
        term = random.choice(search_terms)
        self.client.get(
            f"/api/v1/users/search?q={term}",
            name="/api/v1/users/search",
        )

    @task(1)
    def health_check(self):
        """Simulate health check polling."""
        self.client.get("/api/v1/health", name="/api/v1/health")


class APIUser(HttpUser):
    """Represents a typical API user."""

    tasks = [UserBehavior]
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks

    def on_start(self):
        """Set common headers."""
        self.client.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })


class HeavyUser(HttpUser):
    """Represents a power user with higher request frequency."""

    tasks = [UserBehavior]
    wait_time = between(0.5, 1.5)
    weight = 1  # Lower weight = fewer instances of this user type


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Log test start."""
    print(f"\n🚀 Performance test starting against: {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Log test completion and check thresholds."""
    stats = environment.stats.total

    print(f"\n📊 Performance Test Results:")
    print(f"   Total requests: {stats.num_requests}")
    print(f"   Failures: {stats.num_failures}")
    print(f"   Avg response time: {stats.avg_response_time:.0f}ms")
    print(f"   95th percentile: {stats.get_response_time_percentile(0.95):.0f}ms")
    print(f"   Requests/sec: {stats.current_rps:.1f}")

    # Fail if error rate exceeds 1%
    if stats.num_requests > 0:
        error_rate = stats.num_failures / stats.num_requests
        if error_rate > 0.01:
            print(f"❌ Error rate {error_rate:.1%} exceeds 1% threshold!")
            environment.process_exit_code = 1

    # Fail if 95th percentile exceeds 2 seconds
    p95 = stats.get_response_time_percentile(0.95)
    if p95 > 2000:
        print(f"❌ P95 response time {p95:.0f}ms exceeds 2000ms threshold!")
        environment.process_exit_code = 1
