import pytest
from django.test import Client
from django.urls import NoReverseMatch, reverse


@pytest.mark.django_db
class TestMechanismCharts:
    def test_mechanism_urls_exist(self):
        """Test that the mechanisms URLs are properly configured."""
        # Test list URL
        try:
            url = reverse("mechanisms:list")
        except NoReverseMatch as e:
            pytest.fail(f"mechanisms:list URL pattern not found: {e!s}")
        assert url == "/mechanisms/"

        # Test charts URL
        try:
            url = reverse("mechanisms:mechanism_charts")
        except NoReverseMatch as e:
            pytest.fail(f"mechanisms:mechanism_charts URL pattern not found: {e!s}")
        assert url == "/mechanisms/charts/"

    def test_mechanism_charts_view(self, client: Client):
        """Test that mechanism charts view works with project_id."""
        # Test without project_id
        response = client.get(reverse("mechanisms:mechanism_charts"))
        assert response.status_code == 200
        assert "error" in response.context
        assert response.context["error"] == "No project selected"

        # Test with invalid project_id
        response = client.get(
            reverse("mechanisms:mechanism_charts") + "?project_id=invalid"
        )
        assert response.status_code == 200
        assert "error" in response.context
        assert response.context["error"] == "Invalid project ID"

        # Test with non-existent project_id
        response = client.get(
            reverse("mechanisms:mechanism_charts") + "?project_id=99999"
        )
        assert response.status_code == 200
        assert "error" in response.context
        assert "Project with ID 99999 not found" in response.context["error"]
