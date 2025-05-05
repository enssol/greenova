import logging
import os
from datetime import timedelta
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from django_htmx.http import trigger_client_event
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project

from .forms import EvidenceUploadForm, ObligationForm
from .models import Obligation, ObligationEvidence
from .utils import is_obligation_overdue

# Ensure the Django settings module is correctly configured.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")


logger = logging.getLogger(__name__)

# Add type hints or mock objects for Obligation and EnvironmentalMechanism to
# resolve the missing `objects` and `DoesNotExist` members.
Obligation.objects = Obligation.objects if hasattr(Obligation, "objects") else None
Obligation.DoesNotExist = (
    Obligation.DoesNotExist if hasattr(Obligation, "DoesNotExist") else None
)
EnvironmentalMechanism.objects = (
    EnvironmentalMechanism.objects
    if hasattr(EnvironmentalMechanism, "objects")
    else None
)
EnvironmentalMechanism.DoesNotExist = (
    EnvironmentalMechanism.DoesNotExist
    if hasattr(EnvironmentalMechanism, "DoesNotExist")
    else None
)


@method_decorator(cache_control(max_age=300), name="dispatch")
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ObligationSummaryView(LoginRequiredMixin, View):
    """View for displaying obligation summary with filtering capabilities.

    This view handles both standard requests and HTMX requests for
    dynamically loading filtered obligations.
    """

    def get(self, request, *args, **kwargs):
        """Handle GET requests for obligation summary.

        When accessed via HTMX from procedure charts, this returns filtered obligations.
        Otherwise, it provides the full obligation summary view.

        Args:
            request: The HTTP request

        Returns:
            Rendered template with appropriate context
        """
        # Check if this is a filtered request from procedure charts
        status = request.GET.get("status")
        procedure = request.GET.get("procedure")
        project_id = request.GET.get("project_id")

        if status and procedure and project_id:
            try:
                # Filter obligations based on parameters
                obligations = Obligation.objects.filter(project_id=project_id)

                # Apply status filter (handle overdue special case)
                if status == "overdue":
                    # Find obligations that are overdue
                    filtered_ids = []
                    for obligation in obligations:
                        if is_obligation_overdue(obligation):
                            filtered_ids.append(obligation.obligation_number)
                    obligations = obligations.filter(obligation_number__in=filtered_ids)
                else:
                    obligations = obligations.filter(status=status)

                # Apply procedure filter (adjusted for TextField)
                if procedure:
                    obligations = obligations.filter(procedure__icontains=procedure)

                return render(
                    request,
                    "obligations/partials/obligation_list.html",
                    {"obligations": obligations},
                )
            except Exception as exc:
                logger.error("Error filtering obligations: %s", str(exc))
                return render(
                    request,
                    "obligations/partials/obligation_list.html",
                    {
                        "error": f"Error loading obligations: {str(exc)}",
                        "obligations": [],
                    },
                )

        # For regular requests, proceed with full view
        context = self.get_context_data(**kwargs)

        if self.request.htmx:
            return render(
                request, "obligations/components/_obligations_summary.html", context
            )

        return render(
            request, "obligations/components/_obligations_summary.html", context
        )

    def _filter_by_status(self, queryset: QuerySet, status_values: list) -> QuerySet:
        """Filter queryset by status values including overdue check.

        Args:
            queryset: The base queryset to filter
            status_values: List of status values to include

        Returns:
            Filtered queryset
        """
        if "overdue" not in status_values:
            return queryset.filter(status__in=status_values)

        # Handle overdue status specially since it's calculated not stored
        filtered_ids = [
            obligation.obligation_number
            for obligation in queryset
            if is_obligation_overdue(obligation)
        ]
        status_filter = Q(status__in=[s for s in status_values if s != "overdue"])
        id_filter = Q(obligation_number__in=filtered_ids)

        return queryset.filter(status_filter | id_filter)

    def apply_filters(self, queryset: QuerySet, filters: dict[str, Any]) -> QuerySet:
        """Apply various filters to the obligation queryset.

        Args:
            queryset: Base obligation queryset
            filters: Dictionary of filter parameters

        Returns:
            Filtered queryset
        """
        # Handle the date filter for 14-day lookahead
        if filters.get("date_filter") == "14days":
            today = timezone.now().date()
            two_weeks = today + timedelta(days=14)
            queryset = queryset.filter(
                action_due_date__gte=today, action_due_date__lte=two_weeks
            )

        # Apply status filter
        if filters["status"]:
            queryset = self._filter_by_status(queryset, filters["status"])

        # Apply mechanism filter
        if filters["mechanism"]:
            queryset = queryset.filter(
                primary_environmental_mechanism__id__in=filters["mechanism"]
            )

        # Apply phase filter
        if filters["phase"]:
            queryset = queryset.filter(project_phase__in=filters["phase"])

        # Apply search filter with proper Q objects
        if filters["search"]:
            queryset = queryset.filter(
                Q(obligation_number__icontains=filters["search"])
                | Q(obligation__icontains=filters["search"])
                | Q(supporting_information__icontains=filters["search"])
            )

        return queryset

    def get_filters(self) -> dict[str, Any]:
        """Extract filter parameters from request.

        Returns:
            Dictionary of filter parameters
        """
        return {
            "status": self.request.GET.getlist("status"),
            "mechanism": self.request.GET.getlist("mechanism"),
            "phase": self.request.GET.getlist("phase"),
            "search": self.request.GET.get("search", ""),
            "sort": self.request.GET.get("sort", "action_due_date"),
            "order": self.request.GET.get("order", "asc"),
            "date_filter": self.request.GET.get("date_filter", ""),
        }

    def get_context_data(self, **kwargs):
        """Get context data for the template.

        Returns:
            Context dictionary for rendering template
        """
        context = {}
        mechanism_id = self.request.GET.get("mechanism_id")

        try:
            # Verify mechanism exists
            mechanism = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)

            # Get filters and base queryset
            filters = self.get_filters()
            queryset = Obligation.objects.filter(
                primary_environmental_mechanism=mechanism_id
            )

            # Apply filters and sorting
            queryset = self.apply_filters(queryset, filters)

            sort_field = filters["sort"]
            if filters["order"] == "desc":
                sort_field = f"-{sort_field}"

            queryset = queryset.order_by(sort_field)

            # Paginate results
            paginator = Paginator(queryset, 15)
            page_number = self.request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)

            # Update context
            context.update(
                {
                    "obligations": page_obj,
                    "page_obj": page_obj,
                    "project": mechanism,
                    "mechanism_id": mechanism_id,
                    "filters": filters,
                    "total_count": paginator.count,
                }
            )

            # Get unique project phases
            phases = (
                Obligation.objects.filter(primary_environmental_mechanism=mechanism_id)
                .exclude(project_phase__isnull=True)
                .exclude(project_phase="")
                .values_list("project_phase", flat=True)
                .distinct()
            )
            context["phases"] = list({phase.strip() for phase in phases})

            # Add user permissions
            context["user_can_edit"] = self.request.user.has_perm(
                "obligations.change_obligation"
            )

        except Exception as exc:
            logger.error("Error in ObligationSummaryView: %s", str(exc))
            context["error"] = f"Error loading obligations: {str(exc)}"

        return context


class TotalOverdueObligationsView(LoginRequiredMixin, View):
    """View to get the count of overdue obligations for a project."""

    def get(self, request, *args, **kwargs):
        """Handle GET request to count overdue obligations.

        Args:
            request: HTTP request with project_id parameter

        Returns:
            JsonResponse with count or error
        """
        project_id = request.GET.get("project_id")

        if not project_id:
            return JsonResponse({"error": "Project ID is required"}, status=400)

        obligations = Obligation.objects.filter(project_id=project_id)
        overdue_count = sum(
            1 for obligation in obligations if is_obligation_overdue(obligation)
        )

        return JsonResponse(overdue_count, safe=False)


class ObligationCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/new_obligation.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_id = self.request.GET.get("project_id")
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                kwargs["project"] = project
            except Project.DoesNotExist:
                pass
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.request.GET.get("project_id")
        if project_id:
            context["project_id"] = project_id
        return context

    def form_valid(self, form):
        """Process valid form submission with error handling.

        Args:
            form: The validated form

        Returns:
            Redirect to appropriate page on success
        """
        try:
            # Save the form
            obligation = form.save()

            # Add success message
            messages.success(
                self.request,
                f"Obligation {obligation.obligation_number} created successfully.",
            )

            # Redirect to appropriate page
            if "project_id" in self.request.GET:
                project_id = self.request.GET["project_id"]
                return redirect(f"{reverse('dashboard:home')}?project_id={project_id}")
            return redirect("dashboard:home")

        except ValidationError as exc:
            logger.error("Validation error in ObligationCreateView: %s", str(exc))
            messages.error(self.request, f"Validation failed: {exc}")
            return self.form_invalid(form)

        except Exception as exc:
            logger.exception("Error creating obligation: %s", str(exc))
            messages.error(self.request, f"Failed to create obligation: {str(exc)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDetailView(LoginRequiredMixin, DetailView):
    """View for viewing a single obligation."""

    model = Obligation
    template_name = "obligations/form/view_obligation.html"
    context_object_name = "obligation"
    pk_url_kwarg = "obligation_number"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add project_id to context for back navigation
        context["project_id"] = self.object.project_id
        return context


class ObligationUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing obligation."""

    model = Obligation
    form_class = ObligationForm
    template_name = "obligations/form/update_obligation.html"
    slug_field = "obligation_number"
    slug_url_kwarg = "obligation_number"

    def get_template_names(self):
        if self.request.htmx:
            return ["obligations/form/partial_update_obligation.html"]
        return [self.template_name]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.object.project
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_id"] = self.object.project_id
        return context

    def _update_mechanism_counts(
        self, old_mechanism: EnvironmentalMechanism, updated_obligation: Obligation
    ):
        """Update obligation counts for mechanisms.

        Args:
            old_mechanism: Previous mechanism (if any)
            updated_obligation: The updated obligation
        """
        if (
            old_mechanism
            and old_mechanism != updated_obligation.primary_environmental_mechanism
        ):
            old_mechanism.update_obligation_counts()
            if updated_obligation.primary_environmental_mechanism:
                mech = updated_obligation.primary_environmental_mechanism
                mech.update_obligation_counts()
        elif updated_obligation.primary_environmental_mechanism:
            updated_obligation.primary_environmental_mechanism.update_obligation_counts()

    def form_valid(self, form):
        """Process the form submission with HTMX support.

        Args:
            form: The validated form

        Returns:
            Appropriate response based on request type
        """
        try:
            old_mechanism = None
            if self.object.primary_environmental_mechanism:
                old_mechanism = self.object.primary_environmental_mechanism

            # Save the updated obligation
            obligation = form.save()
            self._update_mechanism_counts(old_mechanism, obligation)

            messages.success(
                self.request,
                f"Obligation {obligation.obligation_number} updated successfully.",
            )

            # If this is an HTMX request, return appropriate headers
            if self.request.htmx:
                response = HttpResponse("Obligation updated successfully")
                # Explicitly trigger a refresh for dependent components
                trigger_client_event(
                    response, "path-deps-refresh", {"path": "/obligations/"}
                )
                return response

            # Standard response for regular requests
            if "project_id" in self.request.GET:
                base_url = reverse("dashboard:home")
                proj_id = self.request.GET["project_id"]
                return redirect(f"{base_url}?project_id={proj_id}")
            return redirect("dashboard:home")

        except ValidationError as exc:
            logger.error("Validation error updating obligation: %s", str(exc))
            messages.error(self.request, f"Validation failed: {exc}")
            return self.form_invalid(form)

        except Exception as exc:
            logger.exception("Error updating obligation: %s", str(exc))
            messages.error(self.request, f"Failed to update obligation: {str(exc)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class ObligationDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting an obligation."""

    model = Obligation
    pk_url_kwarg = "obligation_number"

    def post(self, request, *args, **kwargs):
        """Handle POST request for obligation deletion.

        Args:
            request: The HTTP request

        Returns:
            JsonResponse with success or error status
        """
        try:
            self.object = self.get_object()
            project_id = self.object.project_id
            mechanism = self.object.primary_environmental_mechanism
            obl_number = kwargs.get("obligation_number")

            # Delete the obligation
            self.object.delete()
            logger.info("Obligation %s deleted successfully", obl_number)

            # Update mechanism counts
            if mechanism:
                mechanism.update_obligation_counts()

            base_url = reverse("dashboard:home")
            return JsonResponse(
                {
                    "status": "success",
                    "message": f"Obligation {obl_number} deleted successfully",
                    "redirect_url": f"{base_url}?project_id={project_id}",
                }
            )

        except Exception as exc:
            logger.error("Error deleting obligation: %s", str(exc))
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Error deleting obligation: {str(exc)}",
                },
                status=400,
            )


@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class ToggleCustomAspectView(View):
    """View for toggling custom aspect field visibility."""

    def get(self, request):
        """Handle GET request for toggling custom aspect field.

        Args:
            request: HTTP request with environmental_aspect parameter

        Returns:
            Rendered partial template
        """
        aspect = request.GET.get("environmental_aspect")
        show_field = aspect == "Other"
        return render(
            request,
            "obligations/partials/custom_aspect_field.html",
            {"show_field": show_field},
        )


def upload_evidence(request, obligation_id):
    """Handle evidence file uploads for an obligation.

    Args:
        request: HTTP request
        obligation_id: ID of the obligation to attach evidence to

    Returns:
        Redirect to appropriate page
    """
    obligation = get_object_or_404(Obligation, pk=obligation_id)
    evidence_count = ObligationEvidence.objects.filter(obligation=obligation).count()

    # Check if obligation already has 5 files
    if evidence_count >= 5:
        messages.error(
            request, "This obligation already has the maximum of 5 evidence files"
        )
        return redirect("obligation_detail", obligation_id=obligation_id)

    if request.method == "POST":
        form = EvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            evidence = form.save(commit=False)
            evidence.obligation = obligation
            evidence.save()
            messages.success(request, "Evidence file uploaded successfully")
            return redirect("obligation_detail", obligation_id=obligation_id)

    form = EvidenceUploadForm()
    return render(
        request,
        "upload_evidence.html",
        {
            "obligation": obligation,
            "form": form,
        },
    )
