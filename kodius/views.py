from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Order, Model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import OrderForm, OrderUpdateForm


def load_models(request):
    brand_id = request.GET.get('brand_id')
    models = Model.objects.filter(brand_id=brand_id)
    context = {'models': models}
    return render(request, 'kodius/model_dropdown.html', context)


# Create your views here.
def register(request):
    if request.method == 'POST':
        form: UserRegistrationForm = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form: UserRegistrationForm = UserRegistrationForm()

    context: dict = {'form': form}
    return render(request, 'kodius/register.html', context)


class OrderListView(ListView):
    orders: Order = Order
    context_object_name: str = 'orders'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        print(context)
        # Add in a QuerySet of all the books
        context['last_order_id'] = Order.objects.last()
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView):
    model: Order = Order


class OrderCreateView(LoginRequiredMixin, CreateView):
    model: Order = Order
    form_class = OrderForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        print(form.cleaned_data)

        chain_change_price = form.cleaned_data['chain_change_price']
        oil_and_oil_filter_change_price = form.cleaned_data['oil_and_oil_filter_change_price']
        air_filter_change_price = form.cleaned_data['air_filter_change_price']
        brake_fluid_change_price = form.cleaned_data['brake_fluid_change_price']

        if chain_change_price \
                and oil_and_oil_filter_change_price \
                and air_filter_change_price \
                and brake_fluid_change_price == True:
            print('40 EUR OFF')
        elif chain_change_price \
                and oil_and_oil_filter_change_price \
                and air_filter_change_price:
            print('20% OFF')
        elif oil_and_oil_filter_change_price \
                and air_filter_change_price:
            print('20 EUR OFF')
        elif chain_change_price \
                and brake_fluid_change_price:
            print('15% OFF')

        print(form.cleaned_data['model'])

        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model: Order = Order
    template_name = 'kodius/update_form.html'
    form_class: OrderUpdateForm = OrderUpdateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        print('FORM IS VALID')
        if 'cancel_order' in form.data:
            print(self.object)
            print(self.object.order_status)
            self.object.order_status = False
            return super().form_valid(form)
        return super().form_valid(form)

    def test_func(self):
        order: Order = self.get_object()
        if self.request.user == order.user:
            return True
        return False

