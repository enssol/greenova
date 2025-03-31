<<<<<<< HEAD
# Test files are meant to use assertions, so we can safely ignore B101 warnings
# bandit: skip-file
import base64
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from mechanisms.figures import (encode_figure_to_base64, generate_pie_chart,
                                get_mechanism_chart, get_overall_chart)
from mechanisms.models import EnvironmentalMechanism, update_all_mechanism_counts
from obligations.constants import (STATUS_COMPLETED, STATUS_IN_PROGRESS,
                                   STATUS_NOT_STARTED)
from obligations.models import Obligation
from projects.models import Project
=======
import base64

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from mechanisms.figures import get_mechanism_chart, get_overall_chart
from mechanisms.models import EnvironmentalMechanism
from obligations.constants import STATUS_NOT_STARTED
from projects.models import Project
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)

User = get_user_model()

# Model Tests
@pytest.mark.django_db
class TestEnvironmentalMechanismModel:
    """Test the EnvironmentalMechanism model."""

<<<<<<< HEAD
    @staticmethod
    def test_mechanism_creation(admin_user: AbstractUser) -> None:
        """Test creating an environmental mechanism."""
        project = Project.objects.create(
            name='Test Project',
            description='Test Project Description'
        )
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')
=======
    def test_mechanism_creation(self, admin_user):
        """Test creating an environmental mechanism."""
        project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            created_by=admin_user
        )
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)

        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project,
            description='Test Description',
            category='Test Category',
            reference_number='TEST-001',
            status=STATUS_NOT_STARTED
        )

        assert isinstance(mechanism, EnvironmentalMechanism)
        assert mechanism.name == 'Test Mechanism'
        assert mechanism.project == project
        assert mechanism.description == 'Test Description'
        assert mechanism.category == 'Test Category'
        assert mechanism.reference_number == 'TEST-001'
        assert mechanism.status == STATUS_NOT_STARTED
        assert mechanism.not_started_count == 0
        assert mechanism.in_progress_count == 0
        assert mechanism.completed_count == 0
        assert mechanism.overdue_count == 0

<<<<<<< HEAD
    @staticmethod
    def test_str_method(admin_user: AbstractUser) -> None:
        """Test the string representation of a mechanism."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

=======
    def test_str_method(self, admin_user):
        """Test the string representation of a mechanism."""
        project = Project.objects.create(name='Test Project', created_by=admin_user)
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project
        )

        assert str(mechanism) == 'Test Mechanism'

<<<<<<< HEAD
    @staticmethod
    def test_total_obligations_property(admin_user: AbstractUser) -> None:
        """Test the total_obligations property."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

=======
    def test_total_obligations_property(self, admin_user):
        """Test the total_obligations property."""
        project = Project.objects.create(name='Test Project', created_by=admin_user)
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2
        )

        assert mechanism.total_obligations == 10

<<<<<<< HEAD
    @staticmethod
    def test_get_status_data(admin_user: AbstractUser) -> None:
        """Test the get_status_data method."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

=======
    def test_get_status_data(self, admin_user):
        """Test the get_status_data method."""
        project = Project.objects.create(name='Test Project', created_by=admin_user)
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2,
            overdue_count=1
        )

        status_data = mechanism.get_status_data()
        assert status_data['Overdue'] == 1
        assert status_data['Not Started'] == 4  # 5 - 1 overdue
        assert status_data['In Progress'] == 3
        assert status_data['Completed'] == 2

<<<<<<< HEAD
    @staticmethod
    def test_update_obligation_counts(admin_user: AbstractUser) -> None:
        """Test updating obligation counts based on related obligations."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project
        )

        # Create obligations with different statuses
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        # Not started, not overdue
        Obligation.objects.create(
            obligation_number='TEST-001',
            obligation='Not Started 1',
            project=project,
            primary_environmental_mechanism=mechanism,
            status=STATUS_NOT_STARTED,
            action_due_date=tomorrow,
            environmental_aspect='Air',
            accountability='Perdaman'
        )

        # Not started, overdue
        Obligation.objects.create(
            obligation_number='TEST-002',
            obligation='Not Started Overdue',
            project=project,
            primary_environmental_mechanism=mechanism,
            status=STATUS_NOT_STARTED,
            action_due_date=yesterday,
            environmental_aspect='Water',
            accountability='Perdaman'
        )

        # In progress
        Obligation.objects.create(
            obligation_number='TEST-003',
            obligation='In Progress',
            project=project,
            primary_environmental_mechanism=mechanism,
            status=STATUS_IN_PROGRESS,
            environmental_aspect='Waste',
            accountability='Perdaman'
        )

        # Completed
        Obligation.objects.create(
            obligation_number='TEST-004',
            obligation='Completed',
            project=project,
            primary_environmental_mechanism=mechanism,
            status=STATUS_COMPLETED,
            environmental_aspect='Energy',
            accountability='Perdaman'
        )

        # Update counts
        mechanism.update_obligation_counts()

        # Verify counts
        assert mechanism.not_started_count == 2
        assert mechanism.in_progress_count == 1
        assert mechanism.completed_count == 1
        assert mechanism.overdue_count == 1

    @staticmethod
    def test_update_all_mechanism_counts(admin_user: AbstractUser) -> None:
        """Test updating counts for all mechanisms."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        # Create multiple mechanisms
        mechanism1 = EnvironmentalMechanism.objects.create(
            name='Mechanism 1',
            project=project
        )

        mechanism2 = EnvironmentalMechanism.objects.create(
            name='Mechanism 2',
            project=project
        )

        # Create obligations with correct field names
        Obligation.objects.create(
            obligation_number='TEST-001',
            obligation='Obligation 1',
            project=project,
            primary_environmental_mechanism=mechanism1,
            status=STATUS_NOT_STARTED,
            environmental_aspect='Air',  # Required field
            accountability='Perdaman'    # Required field
        )

        Obligation.objects.create(
            obligation_number='TEST-002',
            obligation='Obligation 2',
            project=project,
            primary_environmental_mechanism=mechanism2,
            status=STATUS_COMPLETED,
            environmental_aspect='Water',  # Required field
            accountability='Perdaman'      # Required field
        )

        # Reset counts to ensure they're updated
        mechanism1.not_started_count = 0
        mechanism1.save()
        mechanism2.completed_count = 0
        mechanism2.save()

        # Update all counts
        updated = update_all_mechanism_counts()

        # Refresh from database
        mechanism1.refresh_from_db()
        mechanism2.refresh_from_db()

        # Verify counts
        assert updated == 2
        assert mechanism1.not_started_count == 1
        assert mechanism2.completed_count == 1

=======
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)

# View Tests
@pytest.mark.django_db
class TestMechanismChartView:
    """Test the MechanismChartView."""

<<<<<<< HEAD
    @staticmethod
    def test_view_requires_login(client, settings):
        """Test that the view requires authentication."""
        # Temporarily set a simple login URL for the test
        settings.LOGIN_URL = '/accounts/login/'

        response = client.get(reverse('mechanisms:mechanism_charts'))

        # Check that unauthenticated user is redirected to login page
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    @staticmethod
    def test_view_with_authenticated_user_no_project(client, admin_user):
=======
    def test_view_requires_login(self, client):
        """Test that the view requires authentication."""
        response = client.get(reverse('mechanisms:mechanism_charts'))
        assert response.status_code == 302  # Redirects to login page
        assert '/login/' in response['Location']

    def test_view_with_authenticated_user_no_project(self, client, admin_user):
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
        """Test view with authenticated user but no project specified."""
        client.force_login(admin_user)
        response = client.get(reverse('mechanisms:mechanism_charts'))

        assert response.status_code == 200
        assert 'error' in response.context
        assert 'No project selected' in response.context['error']

<<<<<<< HEAD
    @staticmethod
    def test_view_with_invalid_project_id(client, admin_user):
        """Test view with invalid project ID."""
        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id=999"
        )
=======
    def test_view_with_invalid_project_id(self, client, admin_user):
        """Test view with invalid project ID."""
        client.force_login(admin_user)
        response = client.get(f"{reverse('mechanisms:mechanism_charts')}?project_id=999")
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)

        assert response.status_code == 200
        assert 'error' in response.context
        assert 'Project with ID 999 not found' in response.context['error']

<<<<<<< HEAD
    @staticmethod
    def test_view_with_valid_project(client, admin_user):
        """Test view with valid project and mechanisms."""
        # Create project and mechanisms
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

=======
    def test_view_with_valid_project(self, client, admin_user):
        """Test view with valid project and mechanisms."""
        # Create project and mechanisms
        project = Project.objects.create(name='Test Project', created_by=admin_user)
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
        mechanism1 = EnvironmentalMechanism.objects.create(
            name='Mechanism 1',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2
        )
        mechanism2 = EnvironmentalMechanism.objects.create(
            name='Mechanism 2',
            project=project,
            not_started_count=1,
            in_progress_count=4,
            completed_count=5
        )

        client.force_login(admin_user)
<<<<<<< HEAD
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id={project.id}"
        )
=======
        response = client.get(f"{reverse('mechanisms:mechanism_charts')}?project_id={project.id}")
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)

        assert response.status_code == 200
        assert 'mechanism_charts' in response.context
        assert len(response.context['mechanism_charts']) == 3  # Overall + 2 mechanisms
        assert response.context['project'] == project
        assert 'table_data' in response.context
        assert len(response.context['table_data']) == 2

        # Verify table data
        table_data = response.context['table_data']
<<<<<<< HEAD
        assert any(
            item['id'] == mechanism1.id and item['name'] == 'Mechanism 1'
            for item in table_data
        )
        assert any(
            item['id'] == mechanism2.id and item['name'] == 'Mechanism 2'
            for item in table_data
        )

    @staticmethod
    def test_view_with_invalid_project_id_type(client, admin_user):
        """Test view with invalid project ID type."""
        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id=abc"
        )

        assert response.status_code == 200
        assert 'error' in response.context
        assert 'Invalid project ID' in response.context['error']

    @staticmethod
    def test_view_with_negative_project_id(client, admin_user):
        """Test view with negative project ID."""
        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id=-1"
        )

        assert response.status_code == 200
        assert 'error' in response.context
        assert 'No project selected' in response.context['error']

    @staticmethod
    def test_view_with_htmx_request(client, admin_user):
        """Test view with HTMX request headers."""
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        client.force_login(admin_user)
        response = client.get(
            f"{reverse('mechanisms:mechanism_charts')}?project_id={project.id}",
            HTTP_HX_REQUEST='true'
        )

        assert response.status_code == 200
        # Check for Vary header
        assert 'HX-Request' in response.get('Vary', '')
        # Check for Cache-Control header
        assert 'max-age=300' in response.get('Cache-Control', '')
=======
        assert any(item['id'] == mechanism1.id and item['name'] == 'Mechanism 1' for item in table_data)
        assert any(item['id'] == mechanism2.id and item['name'] == 'Mechanism 2' for item in table_data)
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)


# Figure Tests
@pytest.mark.django_db
class TestFigureGeneration:
    """Test figure generation functions."""

<<<<<<< HEAD
    @staticmethod
    def test_get_mechanism_chart(admin_user):
        """Test generating a chart for a mechanism."""
        # Create project and mechanism
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

=======
    def test_get_mechanism_chart(self, admin_user):
        """Test generating a chart for a mechanism."""
        # Create project and mechanism
        project = Project.objects.create(name='Test Project', created_by=admin_user)
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
        mechanism = EnvironmentalMechanism.objects.create(
            name='Test Mechanism',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2,
            overdue_count=1
        )

        # Generate chart
        fig, encoded_image = get_mechanism_chart(mechanism.id)

        # Basic validation
        assert fig is not None
        assert encoded_image is not None
        assert isinstance(encoded_image, str)

        # Decode the base64 string to verify it's valid
        try:
            image_data = base64.b64decode(encoded_image)
<<<<<<< HEAD
            assert image_data
        except ValueError as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    @staticmethod
    def test_get_overall_chart(admin_user):
        """Test generating an overall chart for a project."""
        # Create project and mechanisms
        project = Project.objects.create(name='Test Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

=======
            assert len(image_data) > 0
        except Exception as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    def test_get_overall_chart(self, admin_user):
        """Test generating an overall chart for a project."""
        # Create project and mechanisms
        project = Project.objects.create(name='Test Project', created_by=admin_user)
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
        EnvironmentalMechanism.objects.create(
            name='Mechanism 1',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2
        )
        EnvironmentalMechanism.objects.create(
            name='Mechanism 2',
            project=project,
            not_started_count=1,
            in_progress_count=4,
            completed_count=5
        )

        # Generate chart
        fig, encoded_image = get_overall_chart(project.id)

        # Basic validation
        assert fig is not None
        assert encoded_image is not None
        assert isinstance(encoded_image, str)

        # Decode the base64 string to verify it's valid
        try:
            image_data = base64.b64decode(encoded_image)
<<<<<<< HEAD
            assert image_data
        except ValueError as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    @staticmethod
    def test_nonexistent_mechanism_chart():
=======
            assert len(image_data) > 0
        except Exception as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    def test_nonexistent_mechanism_chart(self):
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
        """Test handling of nonexistent mechanism ID."""
        # Try to generate chart for nonexistent mechanism
        fig, encoded_image = get_mechanism_chart(999)

        # Should still return a figure and encoded image
        assert fig is not None
        assert encoded_image is not None

        # Decode the base64 string to verify it's valid
        try:
            image_data = base64.b64decode(encoded_image)
<<<<<<< HEAD
            assert image_data
        except ValueError as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    @staticmethod
    def test_generate_pie_chart_with_data():
        """Test generating a pie chart with data."""
        data = [5, 3, 2, 1]
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        fig = generate_pie_chart(data, labels, colors)

        # Basic validation
        assert fig is not None

    @staticmethod
    def test_generate_pie_chart_no_data():
        """Test generating a pie chart with no data."""
        data = [0, 0, 0, 0]
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        fig = generate_pie_chart(data, labels, colors)

        # Basic validation
        assert fig is not None

    @staticmethod
    def test_encode_figure_to_base64():
        """Test encoding a figure to base64."""
        # Create a simple figure
        data = [5, 3, 2, 1]
        labels = ['Not Started', 'In Progress', 'Completed', 'Overdue']
        colors = ['#f9c74f', '#90be6d', '#43aa8b', '#f94144']

        fig = generate_pie_chart(data, labels, colors)

        # Encode figure
        encoded_image = encode_figure_to_base64(fig)

        # Basic validation
        assert encoded_image is not None
        assert isinstance(encoded_image, str)

        # Decode the base64 string to verify it's valid
        try:
            image_data = base64.b64decode(encoded_image)
            assert image_data
        except ValueError as e:
            pytest.fail(f'Failed to decode base64 image: {e}')

    @staticmethod
    def test_get_overall_chart_with_empty_project(admin_user):
        """Test generating an overall chart for a project with no mechanisms."""
        project = Project.objects.create(name='Empty Project')
        # Add admin_user as a member after creation
        project.add_member(admin_user, 'admin')

        # Generate chart
        fig, encoded_image = get_overall_chart(project.id)

        # Basic validation
        assert fig is not None
        assert encoded_image is not None
        assert isinstance(encoded_image, str)
=======
            assert len(image_data) > 0
        except Exception as e:
            pytest.fail(f'Failed to decode base64 image: {e}')


# Selenium UI Tests
@pytest.mark.selenium
class TestMechanismSeleniumUI:
    """Test the mechanism charts UI using Selenium."""

    @pytest.mark.django_db
    def test_chart_display(self, live_server, selenium, admin_user):
        """Test that charts are displayed correctly."""
        # Create project and mechanisms
        project = Project.objects.create(name='Test Project', created_by=admin_user)
        mechanism = EnvironmentalMechanism.objects.create(
            name='Selenium Test Mechanism',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2
        )

        # Login
        selenium.get(f'{live_server.url}/authentication/login/')
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')
        username_input.send_keys(admin_user.username)
        password_input.send_keys('testpass')  # Assuming this is the password set up in conftest
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Navigate to mechanism charts page with project ID
        selenium.get(f"{live_server.url}{reverse('mechanisms:mechanism_charts')}?project_id={project.id}")

        # Wait for charts to load
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'charts-section'))
        )

        # Check that charts are displayed
        chart_headings = selenium.find_elements(By.TAG_NAME, 'h3')
        chart_heading_texts = [heading.text for heading in chart_headings]

        assert 'Overall Status' in chart_heading_texts
        assert 'Selenium Test Mechanism' in chart_heading_texts

        # Check that images are loaded
        chart_images = selenium.find_elements(By.CLASS_NAME, 'chart-image')
        assert len(chart_images) >= 2  # At least overall chart and mechanism chart

        # Check that data table is displayed
        table_rows = selenium.find_elements(By.XPATH, '//table//tbody//tr')
        assert len(table_rows) >= 1

        # Check mechanism name in table
        cell_text = table_rows[0].find_element(By.XPATH, './td[1]').text
        assert 'Selenium Test Mechanism' in cell_text

    @pytest.mark.django_db
    def test_chart_navigation(self, live_server, selenium, admin_user):
        """Test chart navigation buttons."""
        # Create project and multiple mechanisms to ensure scrolling is possible
        project = Project.objects.create(name='Test Project', created_by=admin_user)
        for i in range(5):  # Create 5 mechanisms to ensure gallery overflow
            EnvironmentalMechanism.objects.create(
                name=f'Mechanism {i+1}',
                project=project,
                not_started_count=i,
                in_progress_count=i + 1,
                completed_count=i + 2
            )

        # Login
        selenium.get(f'{live_server.url}/authentication/login/')
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')
        username_input.send_keys(admin_user.username)
        password_input.send_keys('testpass')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Navigate to mechanism charts page with project ID
        selenium.get(f"{live_server.url}{reverse('mechanisms:mechanism_charts')}?project_id={project.id}")

        # Wait for charts to load
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'chart-gallery'))
        )

        # Get chart gallery element and initial scroll position
        chart_gallery = selenium.find_element(By.ID, 'chartGallery')
        initial_scroll = selenium.execute_script('return arguments[0].scrollLeft', chart_gallery)

        # Click right scroll button
        right_button = selenium.find_element(By.XPATH, "//button[text()='→']")
        right_button.click()

        # Wait a moment for scrolling to happen
        selenium.implicitly_wait(1)

        # Check that scroll position has changed
        new_scroll = selenium.execute_script('return arguments[0].scrollLeft', chart_gallery)
        assert new_scroll > initial_scroll

        # Click left scroll button
        left_button = selenium.find_element(By.XPATH, "//button[text()='←']")
        left_button.click()

        # Wait a moment for scrolling to happen
        selenium.implicitly_wait(1)

        # Check that scroll position has changed back
        final_scroll = selenium.execute_script('return arguments[0].scrollLeft', chart_gallery)
        assert final_scroll < new_scroll

    @pytest.mark.django_db
    def test_accessibility_features(self, live_server, selenium, admin_user):
        """Test accessibility features of the mechanism charts page."""
        # Create project and mechanism
        project = Project.objects.create(name='Test Project', created_by=admin_user)
        EnvironmentalMechanism.objects.create(
            name='Accessibility Test Mechanism',
            project=project,
            not_started_count=5,
            in_progress_count=3,
            completed_count=2
        )

        # Login
        selenium.get(f'{live_server.url}/authentication/login/')
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')
        username_input.send_keys(admin_user.username)
        password_input.send_keys('testpass')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Navigate to mechanism charts page with project ID
        selenium.get(f"{live_server.url}{reverse('mechanisms:mechanism_charts')}?project_id={project.id}")

        # Wait for page to load
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'charts-section'))
        )

        # Check for proper heading structure
        h2_elements = selenium.find_elements(By.TAG_NAME, 'h2')
        assert len(h2_elements) >= 1

        # Check for ARIA attributes
        chart_gallery = selenium.find_element(By.ID, 'chartGallery')
        assert chart_gallery.get_attribute('role') == 'region'
        assert chart_gallery.get_attribute('aria-label') is not None

        # Check for image alt text
        chart_images = selenium.find_elements(By.CLASS_NAME, 'chart-image')
        for img in chart_images:
            assert img.get_attribute('alt') is not None and len(img.get_attribute('alt')) > 0

        # Check for button aria-labels
        nav_buttons = selenium.find_elements(By.XPATH, "//nav[@class='chart-nav']//button")
        for button in nav_buttons:
            assert button.get_attribute('aria-label') is not None

        # Check for table accessibility
        if len(selenium.find_elements(By.TAG_NAME, 'table')) > 0:
            table = selenium.find_element(By.TAG_NAME, 'table')
            assert table.get_attribute('role') == 'grid'
>>>>>>> 0294b58 (refactor(project): implement comprehensive project enhancements)
