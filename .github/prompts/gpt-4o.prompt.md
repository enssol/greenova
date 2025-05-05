# Prompt for GPT-4o

**Goal:** Interactively cherry-pick all changes in code in `greenova/procedures/templates/procedures/procedure_charts.html`, `greenova/obligations/templates/obligations/partials/obligation_list.html`, `greenova/obligations/urls.py`, `greenova/obligations/views.py`, and `greenova/static/css/components/obligations.css` from <https://github.com/enveng-group/dev_greenova/pull/99> that resolves <https://github.com/enveng-group/dev_greenova/issues/37>.

**Context:**

```diff
diff --git a/greenova/obligations/templates/obligations/partials/obligation_list.html b/greenova/obligations/templates/obligations/partials/obligation_list.html
old mode 100755
new mode 100644
index 5e71ad7..4602dad
--- a/greenova/obligations/templates/obligations/partials/obligation_list.html
+++ b/greenova/obligations/templates/obligations/partials/obligation_list.html
@@ -1,26 +1,9 @@
-{% if error %}
-  <div class="notice error" role="alert">
-    <p>
-{{ error }}
-    </p>
+{% for obligation in obligations %}
+  <div class="obligation-item">
+    <strong>{{ obligation.name }}</strong> - {{ obligation.due_date }}
   </div>
-{% else %}
-  {% for obligation in obligations %}
-    <div class="obligation-item">
-      <strong>{{ obligation.obligation_number }}</strong>
-      <div>
-{{ obligation.obligation|truncatechars:50 }}
-      </div>
-      <div>
-Due: {{ obligation.action_due_date|date:"M d, Y" }}
-      </div>
-      <div>
-Status: {{ obligation.status }}
-      </div>
-    </div>
-  {% empty %}
-    <p>
+{% empty %}
+  <p>
 No obligations match this filter.
-    </p>
-  {% endfor %}
-{% endif %}
+  </p>
+{% endfor %}
diff --git a/greenova/obligations/urls.py b/greenova/obligations/urls.py
old mode 100755
new mode 100644
index 34ff405..d7bd549
--- a/greenova/obligations/urls.py
+++ b/greenova/obligations/urls.py
@@ -2,7 +2,7 @@
 from django.urls import path

 from . import views
-from .views import ToggleCustomAspectView
+from .views import ObligationSummaryView, ToggleCustomAspectView

 app_name = 'obligations'

@@ -15,7 +15,7 @@ def root_redirect(request):

 urlpatterns = [
     # Summary view that shows obligations list
-    path('summary/', views.ObligationSummaryView.as_view(), name='summary'),
+    path('summary/', ObligationSummaryView.as_view(), name='summary'),
     path('count-overdue/', views.TotalOverdueObligationsView.as_view(), name='overdue'),
     # Make the root URL properly handle project_id parameter by redirecting
     path('', root_redirect, name='index'),
diff --git a/greenova/obligations/views.py b/greenova/obligations/views.py
old mode 100755
new mode 100644
index 6f28462..e5b64e5
--- a/greenova/obligations/views.py
+++ b/greenova/obligations/views.py
@@ -1,403 +1,394 @@
 import logging
-import os
-from typing import Any
+from datetime import timedelta
+from typing import Any, Dict, Optional, Union

+from core.types import HttpRequest  # Use the enhanced HttpRequest with htmx property
 from django.contrib import messages
 from django.contrib.auth.mixins import LoginRequiredMixin
-from django.core.exceptions import ValidationError
 from django.core.paginator import Paginator
 from django.db.models import Q, QuerySet
-from django.http import JsonResponse
+from django.forms import inlineformset_factory
+from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
 from django.shortcuts import get_object_or_404, redirect, render
-from django.urls import reverse
+from django.urls import reverse, reverse_lazy
+from django.utils import timezone
 from django.utils.decorators import method_decorator
 from django.views import View
 from django.views.decorators.cache import cache_control
 from django.views.decorators.vary import vary_on_headers
-from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
-from django.views.generic.edit import DeleteView
-from mechanisms.models import EnvironmentalMechanism
+from django.views.generic import (CreateView, DeleteView, DetailView, TemplateView,
+                                  UpdateView)
+from django_htmx.http import trigger_client_event
+from mechanisms.models import EnvironmentalMechanism  # Added missing import
 from projects.models import Project

 from .forms import EvidenceUploadForm, ObligationForm
 from .models import Obligation, ObligationEvidence
-from .utils import is_obligation_overdue
-
-# Ensure the Django settings module is correctly configured.
-os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenova.settings")
-
+from .utils import \
+    is_obligation_overdue  # Add explicit import for is_obligation_overdue

+# Create a logger for this module
 logger = logging.getLogger(__name__)

-# Add type hints or mock objects for Obligation and EnvironmentalMechanism to resolve the missing `objects` and `DoesNotExist` members.
-Obligation.objects = Obligation.objects if hasattr(Obligation, "objects") else None
-Obligation.DoesNotExist = (
-    Obligation.DoesNotExist if hasattr(Obligation, "DoesNotExist") else None
-)
-EnvironmentalMechanism.objects = (
-    EnvironmentalMechanism.objects
-    if hasattr(EnvironmentalMechanism, "objects")
-    else None
-)
-EnvironmentalMechanism.DoesNotExist = (
-    EnvironmentalMechanism.DoesNotExist
-    if hasattr(EnvironmentalMechanism, "DoesNotExist")
-    else None
-)
-
-
-@method_decorator(cache_control(max_age=300), name="dispatch")
-@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
-class ObligationSummaryView(LoginRequiredMixin, TemplateView):
-    template_name = "obligations/components/_obligations_summary.html"
+@method_decorator(cache_control(max_age=300), name='dispatch')
+@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
+class ObligationSummaryView(View):
+    def get(self, request, *args, **kwargs):
+        status = request.GET.get('status')
+        procedure = request.GET.get('procedure')
+        project_id = request.GET.get('project_id')
+
+        obligations = Obligation.objects.filter(
+            status=status,
+            procedure__name=procedure,
+            project__id=project_id
+        )

-    def get_template_names(self):
-        if self.request.htmx:
-            return ["obligations/components/_obligations_summary.html"]
-        return [self.template_name]
+        return render(request, 'obligations/obligation_list.html', {
+            'obligations': obligations
+        })

-    def _filter_by_status(self, queryset: QuerySet, status_values: list) -> QuerySet:
-        """Filter queryset by status values including overdue check."""
-        if "overdue" not in status_values:
-            return queryset.filter(status__in=status_values)
-
-        filtered_ids = [
-            obligation.obligation_number
-            for obligation in queryset
-            if is_obligation_overdue(obligation)
-        ]
-        status_filter = Q(status__in=status_values)
-        id_filter = Q(obligation_number__in=filtered_ids)
-        return queryset.filter(status_filter | id_filter)
-
-    def apply_filters(self, queryset: QuerySet, filters: dict[str, Any]) -> QuerySet:
-        if filters["status"]:
-            queryset = self._filter_by_status(queryset, filters["status"])
-
-        if filters["mechanism"]:
+    def apply_filters(self, queryset: QuerySet, filters: Dict[str, Any]) -> QuerySet:
+        """Apply filters to the queryset."""
+        # Handle the date filter first (14-day lookahead)
+        if filters['date_filter'] == '14days':
+            today = timezone.now().date()
+            two_weeks = today + timedelta(days=14)
             queryset = queryset.filter(
-                primary_environmental_mechanism__id__in=filters["mechanism"]
+                action_due_date__gte=today,
+                action_due_date__lte=two_weeks
             )

-        if filters["phase"]:
-            queryset = queryset.filter(project_phase__in=filters["phase"])
-
-        # Fixing search filter to avoid Q object binary operation issues
-        if filters["search"]:
-            search_query = Q()
-            searchable_fields = [
-                "obligation_number",
-                "obligation",
-                "supporting_information",
-            ]
-            for field in searchable_fields:
-                search_query |= Q(**{f"{field}__icontains": filters["search"]})
-            queryset = queryset.filter(search_query)
+        # Apply status filter
+        if filters['status']:
+            # Handle the special case of 'overdue' status which isn't in the database
+            if 'overdue' in filters['status'] and len(filters['status']) == 1:
+                from obligations.utils import is_obligation_overdue
+
+                # Filter for items that are overdue
+                filtered_ids = []
+                for obligation in queryset:
+                    if is_obligation_overdue(obligation):
+                        filtered_ids.append(obligation.obligation_number)
+                queryset = queryset.filter(obligation_number__in=filtered_ids)
+            elif 'overdue' in filters['status'] and len(filters['status']) > 1:
+                # Handle mix of 'overdue' and other statuses
+                other_statuses = [s for s in filters['status'] if s != 'overdue']
+                filtered_ids = []
+                for obligation in queryset.filter(status__in=other_statuses):
+                    if is_obligation_overdue(obligation):
+                        filtered_ids.append(obligation.obligation_number)
+                queryset = queryset.filter(
+                    Q(status__in=other_statuses) | Q(obligation_number__in=filtered_ids)
+                )
+            else:
+                # Normal status filtering
+                queryset = queryset.filter(status__in=filters['status'])
+
+        # Apply mechanism filter if provided
+        if filters['mechanism']:
+            queryset = queryset.filter(
+                primary_environmental_mechanism__id__in=filters['mechanism']
+            )
+
+        # Apply phase filter if provided
+        if filters['phase']:
+            queryset = queryset.filter(project_phase__in=filters['phase'])
+
+        # Apply search if provided
+        if filters['search']:
+            queryset = queryset.filter(
+                Q(obligation_number__icontains=filters['search']) |
+                Q(obligation__icontains=filters['search']) |
+                Q(supporting_information__icontains=filters['search'])
+            )

         return queryset

-    def get_filters(self) -> dict[str, Any]:
+    def get_filters(self) -> Dict[str, Any]:
+        """Extract filters from request."""
         return {
-            "status": self.request.GET.getlist("status"),
-            "mechanism": self.request.GET.getlist("mechanism"),
-            "phase": self.request.GET.getlist("phase"),
-            "search": self.request.GET.get("search", ""),
-            "sort": self.request.GET.get("sort", "action_due_date"),
-            "order": self.request.GET.get("order", "asc"),
-            "date_filter": self.request.GET.get("date_filter", ""),
+            'status': self.request.GET.getlist('status'),
+            'mechanism': self.request.GET.getlist('mechanism'),
+            'phase': self.request.GET.getlist('phase'),
+            'search': self.request.GET.get('search', ''),
+            'sort': self.request.GET.get('sort', 'action_due_date'),
+            'order': self.request.GET.get('order', 'asc'),
+            'date_filter': self.request.GET.get('date_filter', ''),
         }

     def get_context_data(self, **kwargs):
+        """Get context data for the template."""
         context = super().get_context_data(**kwargs)
-        mechanism_id = self.request.GET.get("mechanism_id")

+        mechanism_id = self.request.GET.get('mechanism_id')
+
+        '''
+        if not mechanism_id:
+            context['error'] = "No procedure selected"
+            return context
+        '''
         try:
+            # Verify project exists
             project = get_object_or_404(EnvironmentalMechanism, id=mechanism_id)
+
+            # Get filters from request
             filters = self.get_filters()
-            base_queryset = Obligation.objects.filter(
-                primary_environmental_mechanism=mechanism_id
-            )
-            queryset = self.apply_filters(base_queryset, filters)

-            sort_field = filters["sort"]
-            if filters["order"] == "desc":
-                sort_field = f"-{sort_field}"
+            # Get obligations for this project
+            queryset = Obligation.objects.filter(primary_environmental_mechanism=mechanism_id)
+
+            # Apply filters
+            queryset = self.apply_filters(queryset, filters)
+
+            # Sort results
+            sort_field = filters['sort']
+            if filters['order'] == 'desc':
+                sort_field = f'-{sort_field}'
             queryset = queryset.order_by(sort_field)

+            # Paginate results
             paginator = Paginator(queryset, 15)
-            page_number = self.request.GET.get("page", 1)
+            page_number = self.request.GET.get('page', 1)
             page_obj = paginator.get_page(page_number)

-            context.update(
-                {
-                    "obligations": page_obj,
-                    "page_obj": page_obj,
-                    "project": project,
-                    "mechanism_id": mechanism_id,
-                    "filters": filters,
-                    "total_count": paginator.count,
-                }
-            )
-
-            # Get unique project phases
-            phases_queryset = (
-                Obligation.objects.filter(primary_environmental_mechanism=mechanism_id)
-                .exclude(project_phase__isnull=True)
-                .exclude(project_phase="")
-                .values_list("project_phase", flat=True)
-                .distinct()
-            )
-            context["phases"] = list({phase.strip() for phase in phases_queryset})
-            context["user_can_edit"] = self.request.user.has_perm(
-                "obligations.change_obligation"
-            )
-
-        except EnvironmentalMechanism.DoesNotExist as exc:
-            logger.error("EnvironmentalMechanism not found: %s", str(exc))
-            context["error"] = "Error loading obligations: Mechanism not found."
-
+            context.update({
+                'obligations': page_obj,
+                'page_obj': page_obj,
+                'project': project,
+                # 'project_id': project_id,
+                'mechanism_id': mechanism_id,
+                'filters': filters,
+                'total_count': paginator.count,
+            })
+            # Get only unique phases
+            phases = Obligation.objects.filter(primary_environmental_mechanism=mechanism_id).exclude(project_phase__isnull=True).exclude(project_phase='').values_list('project_phase', flat=True).distinct()
+            phases_cleaned = {phase.strip() for phase in phases}
+            context['phases'] = list(phases_cleaned)
+
+            context['user_can_edit'] = self.request.user.has_perm('obligations.change_obligation')
+
+        except Exception as e:
+            logger.error(f'Error in ObligationSummaryView: {str(e)}')
+            context['error'] = f'Error loading obligations: {str(e)}'
         return context

-
 class TotalOverdueObligationsView(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
-        project_id = request.GET.get("project_id")
+        project_id = request.GET.get('project_id')

         if not project_id:
-            return JsonResponse({"error": "Project ID is required"}, status=400)
+            return JsonResponse({'error': 'Project ID is required'}, status=400)

         obligations = Obligation.objects.filter(project_id=project_id)

-        overdue_count = sum(
-            1 for obligation in obligations if is_obligation_overdue(obligation)
-        )
+        overdue_count = sum(1 for obligation in obligations if is_obligation_overdue(obligation))

         return JsonResponse(overdue_count, safe=False)

-
 class ObligationCreateView(LoginRequiredMixin, CreateView):
     """View for creating a new obligation."""
-
     model = Obligation
     form_class = ObligationForm
-    template_name = "obligations/form/new_obligation.html"
+    template_name = 'obligations/form/new_obligation.html'

     def get_form_kwargs(self):
         kwargs = super().get_form_kwargs()
-        project_id = self.request.GET.get("project_id")
+        project_id = self.request.GET.get('project_id')
         if project_id:
             try:
                 project = Project.objects.get(id=project_id)
-                kwargs["project"] = project
+                kwargs['project'] = project
             except Project.DoesNotExist:
                 pass
         return kwargs

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
-        project_id = self.request.GET.get("project_id")
+        project_id = self.request.GET.get('project_id')
         if project_id:
-            context["project_id"] = project_id
+            context['project_id'] = project_id
         return context

-    # Proper exception handling and logging in form_valid
     def form_valid(self, form):
         try:
+            # Save the form
             obligation = form.save()
-            messages.success(
-                self.request, f"Obligation {obligation.obligation_number} created."
-            )
-            return redirect("dashboard:home")
-        except ValidationError as exc:
-            logger.error("Validation error in ObligationCreateView: %s", str(exc))
-            messages.error(self.request, f"Validation failed: {exc}")
-            return self.form_invalid(form)

-        except OSError as exc:
-            logger.error("IO error updating obligation: %s", str(exc))
-            messages.error(self.request, "System error occurred")
+            # Add success message
+            messages.success(self.request, f'Obligation {obligation.obligation_number} created successfully.')
+
+            # Redirect to appropriate page
+            if 'project_id' in self.request.GET:
+                return redirect(f"{reverse('dashboard:home')}?project_id={self.request.GET['project_id']}")
+            return redirect('dashboard:home')
+
+        except Exception as e:
+            logger.exception(f'Error in ObligationCreateView: {e}')
+            messages.error(self.request, f'Failed to create obligation: {str(e)}')
             return self.form_invalid(form)

     def form_invalid(self, form):
-        messages.error(self.request, "Please correct the errors below.")
+        messages.error(self.request, 'Please correct the errors below.')
         return super().form_invalid(form)


 class ObligationDetailView(LoginRequiredMixin, DetailView):
     """View for viewing a single obligation."""
-
     model = Obligation
-    template_name = "obligations/form/view_obligation.html"
-    context_object_name = "obligation"
-    pk_url_kwarg = "obligation_number"
+    template_name = 'obligations/form/view_obligation.html'
+    context_object_name = 'obligation'
+    pk_url_kwarg = 'obligation_number'

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         # Add project_id to context for back navigation
-        context["project_id"] = self.object.project_id
+        context['project_id'] = self.object.project_id
         return context


 class ObligationUpdateView(LoginRequiredMixin, UpdateView):
     """Update an existing obligation."""
-
     model = Obligation
     form_class = ObligationForm
-    template_name = "obligations/form/update_obligation.html"
-    slug_field = "obligation_number"
-    slug_url_kwarg = "obligation_number"
-
-    def __init__(self, **kwargs):
-        super().__init__(**kwargs)
-        self.object = None
+    template_name = 'obligations/form/update_obligation.html'
+    slug_field = 'obligation_number'
+    slug_url_kwarg = 'obligation_number'

     def get_template_names(self):
         if self.request.htmx:
-            return ["obligations/form/partial_update_obligation.html"]
+            return ['obligations/form/partial_update_obligation.html']
         return [self.template_name]

     def get_form_kwargs(self):
         kwargs = super().get_form_kwargs()
-        kwargs["project"] = self.get_object().project
+        kwargs['project'] = self.object.project
         return kwargs

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
-        context["project_id"] = self.get_object().project_id
+        # Add project_id to context for back navigation
+        context['project_id'] = self.object.project_id
         return context

-    def _update_mechanism_counts(
-        self, old_mechanism: EnvironmentalMechanism, updated_obligation: Obligation
-    ):
-        """Update obligation counts for mechanisms."""
-        if (
-            old_mechanism
-            and old_mechanism != updated_obligation.primary_environmental_mechanism
-        ):
-            old_mechanism.update_obligation_counts()
-            if updated_obligation.primary_environmental_mechanism:
-                mech = updated_obligation.primary_environmental_mechanism
-                mech.update_obligation_counts()
-        elif updated_obligation.primary_environmental_mechanism:
-            updated_obligation.primary_environmental_mechanism.update_obligation_counts()  # pylint: disable=no-member
-
     def form_valid(self, form):
-        try:
-            self.object = self.get_object()
-            old_mechanism = self.object.primary_environmental_mechanism
+        """Process the form submission."""
+        response = super().form_valid(form)

-            # Save the updated obligation
-            updated_obligation = form.save()
-            self._update_mechanism_counts(old_mechanism, updated_obligation)
+        # If this is an HTMX request, return appropriate headers
+        if self.request.htmx:
+            # Using path-deps to refresh dependent components
+            response = HttpResponse('Obligation updated successfully')

-            messages.success(
-                self.request,
-                f"Obligation {updated_obligation.obligation_number} updated.",
-            )
+            # Explicitly trigger a refresh for path-deps components
+            trigger_client_event(response, 'path-deps-refresh', {
+                'path': '/obligations/'
+            })

-            # Build redirect URL
-            if "project_id" in self.request.GET:
-                base_url = reverse("dashboard:home")
-                proj_id = self.request.GET["project_id"]
-                return redirect(f"{base_url}?project_id={proj_id}")
-            return redirect("dashboard:home")
+            return response

-        except ValidationError as exc:
-            logger.error("Validation error updating obligation: %s", str(exc))
-            messages.error(self.request, f"Validation failed: {exc}")
-            return self.form_invalid(form)
+        return response
+
+    def form_valid(self, form):
+        try:
+            old_mechanism = None
+            if self.object.primary_environmental_mechanism:
+                old_mechanism = self.object.primary_environmental_mechanism
+
+            # Save the updated obligation
+            obligation = form.save()

-        except OSError as exc:
-            logger.error("IO error updating obligation: %s", str(exc))
-            messages.error(self.request, "System error occurred")
+            # Update mechanism counts
+            if old_mechanism and old_mechanism != obligation.primary_environmental_mechanism:
+                if old_mechanism:
+                    old_mechanism.update_obligation_counts()
+                if obligation.primary_environmental_mechanism:
+                    obligation.primary_environmental_mechanism.update_obligation_counts()
+            elif obligation.primary_environmental_mechanism:
+                obligation.primary_environmental_mechanism.update_obligation_counts()
+
+            # Add success message
+            messages.success(self.request, f'Obligation {obligation.obligation_number} updated successfully.')
+
+            # Redirect back to the appropriate page
+            if 'project_id' in self.request.GET:
+                return redirect(f"{reverse('dashboard:home')}?project_id={self.request.GET['project_id']}")
+            return redirect('dashboard:home')
+
+        except Exception as e:
+            logger.exception(f'Error in ObligationUpdateView: {e}')
+            messages.error(self.request, f'Failed to update obligation: {str(e)}')
             return self.form_invalid(form)

     def form_invalid(self, form):
-        messages.error(self.request, "Please correct the errors below.")
+        messages.error(self.request, 'Please correct the errors below.')
         return super().form_invalid(form)


 class ObligationDeleteView(LoginRequiredMixin, DeleteView):
     """View for deleting an obligation."""
-
     model = Obligation
-    pk_url_kwarg = "obligation_number"
-
-    def __init__(self, **kwargs):
-        super().__init__(**kwargs)
-        self.object = None
+    pk_url_kwarg = 'obligation_number'

     def post(self, request, *args, **kwargs):
         try:
             self.object = self.get_object()
             project_id = self.object.project_id
             mechanism = self.object.primary_environmental_mechanism
-            obl_number = kwargs.get("obligation_number")

             # Delete the obligation
             self.object.delete()
-            logger.info("Obligation %s deleted successfully", obl_number)
+            logger.info(f"Obligation {kwargs.get('obligation_number')} deleted successfully")

             # Update mechanism counts
             if mechanism:
                 mechanism.update_obligation_counts()

-            base_url = reverse("dashboard:home")
-            return JsonResponse(
-                {
-                    "status": "success",
-                    "message": f"Obligation {obl_number} deleted successfully",
-                    "redirect_url": f"{base_url}?project_id={project_id}",
-                }
-            )
-
-        except (Obligation.DoesNotExist, ValidationError) as exc:
-            logger.error("Error deleting obligation: %s", str(exc))
-            msg = f"Delete failed: {exc}"
-            return JsonResponse({"status": "error", "message": msg}, status=400)
-
-
-@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
+            # Return JSON response for AJAX calls
+            return JsonResponse({
+                'status': 'success',
+                'message': f"Obligation {kwargs.get('obligation_number')} deleted successfully",
+                'redirect_url': f"{reverse('dashboard:home')}?project_id={project_id}"
+            })
+
+        except Exception as e:
+            logger.error(f'Error deleting obligation: {str(e)}')
+            return JsonResponse({
+                'status': 'error',
+                'message': f'Error deleting obligation: {str(e)}'
+            }, status=400)
+
+@method_decorator(vary_on_headers('HX-Request'), name='dispatch')
 class ToggleCustomAspectView(View):
-    """View for toggling custom aspect field visibility."""
-
     def get(self, request):
-        aspect = request.GET.get("environmental_aspect")
-        show_field = aspect == "Other"
-        return render(
-            request,
-            "obligations/partials/custom_aspect_field.html",
-            {"show_field": show_field},
-        )
-
+        aspect = request.GET.get('environmental_aspect')
+        if aspect == 'Other':
+            return render(request, 'obligations/partials/custom_aspect_field.html', {
+                'show_field': True
+            })
+        return render(request, 'obligations/partials/custom_aspect_field.html', {
+            'show_field': False
+        })

 def upload_evidence(request, obligation_id):
-    """Handle evidence file uploads for an obligation."""
     obligation = get_object_or_404(Obligation, pk=obligation_id)
-    evidence_count = ObligationEvidence.objects.filter(obligation=obligation).count()

     # Check if obligation already has 5 files
-    if evidence_count >= 5:
-        messages.error(
-            request, "This obligation already has the maximum of 5 evidence files"
-        )
-        return redirect("obligation_detail", obligation_id=obligation_id)
+    if ObligationEvidence.objects.filter(obligation=obligation).count() >= 5:
+        messages.error(request, 'This obligation already has the maximum of 5 evidence files')
+        return redirect('obligation_detail', obligation_id=obligation_id)

-    if request.method == "POST":
+    if request.method == 'POST':
         form = EvidenceUploadForm(request.POST, request.FILES)
         if form.is_valid():
             evidence = form.save(commit=False)
             evidence.obligation = obligation
             evidence.save()
-            messages.success(request, "Evidence file uploaded successfully")
-            return redirect("obligation_detail", obligation_id=obligation_id)
-
-    form = EvidenceUploadForm()
-    return render(
-        request,
-        "upload_evidence.html",
-        {
-            "obligation": obligation,
-            "form": form,
-        },
-    )
+            messages.success(request, 'Evidence file uploaded successfully')
+            return redirect('obligation_detail', obligation_id=obligation_id)
+    else:
+        form = EvidenceUploadForm()
+        return render(request, 'upload_evidence.html', {
+            'obligation': obligation,
+            'form': form,
+        })
diff --git a/greenova/procedures/templates/procedures/procedure_charts.html b/greenova/procedures/templates/procedures/procedure_charts.html
old mode 100755
new mode 100644
index 1423078..102916b
--- a/greenova/procedures/templates/procedures/procedure_charts.html
+++ b/greenova/procedures/templates/procedures/procedure_charts.html
@@ -80,7 +80,7 @@ <h2 id="filter-heading">
               </option>
               {% for resp in available_responsibilities %}
                 <option value="{{ resp }}"
-                        {% if filter_responsibility == resp %}selected{% endif %}>
+                        {% if filter_responsibility == resp %} selected {% endif %}>
                   {{ resp }}

                 </option>
@@ -98,7 +98,7 @@ <h2 id="filter-heading">
               </option>
               {% for status_value, status_label in status_options %}
                 <option value="{{ status_value }}"
-                        {% if filter_status == status_value %}selected{% endif %}>
+                        {% if filter_status == status_value %} selected {% endif %}>
                   {{ status_label }}

                 </option>
@@ -111,14 +111,14 @@ <h2 id="filter-heading">
               <input type="checkbox"
                      name="lookahead"
                      value="14days"
-                     {% if filter_lookahead %}checked{% endif %} />
+                     {% if filter_lookahead %} checked {% endif %} />
               14-Day Lookahead
             </label>
             <label>
               <input type="checkbox"
                      name="overdue"
                      value="true"
-                     {% if filter_overdue %}checked{% endif %} />
+                     {% if filter_overdue %} checked {% endif %} />
               Overdue Only
             </label>
           </div>
@@ -226,7 +226,7 @@ <h2>
                        hx-swap="innerHTML"
                        hx-trigger="click"
                        _="on click add .selected to me remove .selected from .status-count-link where it is not me set #current-filter.innerText to 'Not Started obligations for {{ item.name }}'">
-                      {{ item.not_started }}
+                        {{ item.not_started }}
                     </a>
                   </td>
                   <td>
@@ -237,7 +237,7 @@ <h2>
                        hx-swap="innerHTML"
                        hx-trigger="click"
                        _="on click add .selected to me remove .selected from .status-count-link where it is not me set #current-filter.innerText to 'In Progress obligations for {{ item.name }}'">
-                      {{ item.in_progress }}
+                        {{ item.in_progress }}
                     </a>
                   </td>
                   <td>
@@ -248,7 +248,7 @@ <h2>
                        hx-swap="innerHTML"
                        hx-trigger="click"
                        _="on click add .selected to me remove .selected from .status-count-link where it is not me set #current-filter.innerText to 'Completed obligations for {{ item.name }}'">
-                      {{ item.completed }}
+                        {{ item.completed }}
                     </a>
                   </td>
                   <td>
@@ -259,7 +259,7 @@ <h2>
                        hx-swap="innerHTML"
                        hx-trigger="click"
                        _="on click add .selected to me remove .selected from .status-count-link where it is not me set #current-filter.innerText to 'Overdue obligations for {{ item.name }}'">
-                      {{ item.overdue }}
+                        {{ item.overdue }}
                     </a>
                   </td>
                   <td>
@@ -281,13 +281,16 @@ <h2>
             <!-- Obligations will be loaded here -->
           </div>
         </div>
+        <div id="current-filter" class="filter-label">
+          <!-- Will be set dynamically -->
+        </div>
+
+        <div id="obligation-list-container"
+             aria-live="polite"
+             class="obligations-container">
+          <!-- Filtered obligations will be loaded here via HTMX -->
+        </div>
       </article>
-      <!-- Add container for filtered obligations -->
-      <div id="obligation-list-container"
-           aria-live="polite"
-           class="obligations-container">
-        <!-- Filtered obligations will be loaded here via HTMX -->
-      </div>
     {% endif %}
   </article>
   <script>
diff --git a/greenova/static/css/components/obligations.css b/greenova/static/css/components/obligations.css
old mode 100755
new mode 100644
index 714cf67..bbd08fc
--- a/greenova/static/css/components/obligations.css
+++ b/greenova/static/css/components/obligations.css
@@ -245,7 +245,7 @@ @media print {
   }
 }

-/* Interactive status count styles */
+/* Add styles for .status-count-link and .obligations-container */
 .status-count-link {
   cursor: pointer;
   text-decoration: underline;
```

**Objective:**
**Objective:** Add interactive filtering capabilities to the obligations dashboard by making status count displays clickable, which dynamically load filtered obligation lists using HTMX. This enhancement improves data exploration by providing direct access to filtered data, reduces navigation steps, and creates a more engaging user experience while maintaining accessibility and mobile optimization.

**Source:**

- <https://github.com/enveng-group/dev_greenova/issues/37>
- <https://github.com/enveng-group/dev_greenova/pull/99>

1. **`greenova/procedures/templates/procedures/procedure_charts.html`**

- Updated `<option>` elements to include spacing for better readability.
- Added dynamic filter labels and a container for filtered obligations with HTMX integration.

2. **`greenova/obligations/templates/obligations/partials/obligation_list.html`**

- Simplified obligation list rendering.
- Improved empty state messaging for better user feedback.

3. **`greenova/obligations/urls.py`**

- Added `ObligationSummaryView` to handle obligation summaries.
- Updated URL patterns for consistency and clarity.

4. **`greenova/obligations/views.py`**

- Refactored `ObligationSummaryView` to include filtering, sorting, and pagination.
- Enhanced error handling and logging for better maintainability.
- Added HTMX support for dynamic obligation updates.

5. **`greenova/static/css/components/obligations.css`**

- Introduced styles for `.status-count-link` and `.obligations-container`.
- Enhanced hover effects and visual feedback for interactive elements.

**Expectations**: GitHub Copilot can delete and consolidate files where
multiple implementations are found and can be merged into a single file
globally. Always use `use context7` to lookup documentation from the context7
MCP server, which provides access to all project-specific configuration files
and standards. Additional resources such as the github, filesystem, JSON,
context7, sqlite, git, fetch, sequential-thinking, and docker MCP servers have
been activated and are available for use by GitHub Copilot.

**Instructions**:

1. Identify and remove unnecessary or outdated files, code, or documentation
   that no longer serves the project's objectives. Clearly define the task's
   scope to focus only on relevant elements flagged in pre-commit checks.
2. Organize project resources, including tools, code, and documentation, into a
   logical structure. Ensure naming conventions and folder hierarchies are
   consistent, making it easier to locate and work with files.
3. Create stub files (.pyi files) for internal modules that don't have proper
   type information.
4. Add a py.typed marker file to indicate these modules have type information
5. Refactor the code to address issues such as readability, maintainability,
   and technical debt. Implement clean coding practices and resolve any flagged
   issues in the pre-commit output, such as formatting or style violations.
6. Use automated tools like bandit, autopep8, mypy, eslint, djlint,
   markdownlint, ShellCheck, and pylint to enforce coding standards. Validate
   compliance with the project's guidelines and ensure all pre-commit checks
   pass without errors. Iterate running `pre-commit` to check for any remaining
   issues after each change. Do not use the command
   `pre-commit run --all-files`.
7. Ensure that the code is well-documented, with clear explanations of
   functions, classes, and modules. Use docstrings and comments to clarify
   complex logic or important decisions made during development.
8. Test the code thoroughly to ensure it works as intended and meets the
   project's requirements. Write unit tests and integration tests as needed,
   and ensure that all tests pass before finalizing the changes.
9. Iterate until resolved.
