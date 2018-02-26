from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Vehicle, Battery
from .forms import VehicleCreateForm, VehicleUpdateForm, BatteryFormSet
from django.urls import reverse_lazy
from django.shortcuts import redirect


class VehicleListView(generic.ListView):
    model = Vehicle
    context_object_name = 'vehicles_list'
    template_name = 'index.html'
    paginate_by = 30

    def get_queryset(self):
        return Vehicle.objects.all()


class VehicleCreate(CreateView):
    form_class = VehicleCreateForm
    model = Vehicle
    template_name = 'vehicle_create.html'
    success_url = reverse_lazy('index')


class VehicleUpdate(UpdateView):
    model = Vehicle
    template_name = 'vehicle_update.html'
    success_url = reverse_lazy('index')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(VehicleUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['battery_formset'] = BatteryFormSet(self.request.POST, instance=self.object)
            context['battery_formset'].full_clean()
        else:
            context['battery_formset'] = BatteryFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['battery_formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
