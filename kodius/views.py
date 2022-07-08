from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Order
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


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


@login_required
def my_orders(request):
    logged_in_user = request.user
    context: dict = {
        'orders': Order.objects.filter(user=logged_in_user)
    }
    return render(request, 'kodius/my_orders.html', context)


class OrderListView(ListView):
    model: Order = Order
    context_object_name: str = 'orders'


class OrderDetailView(DetailView):
    model: Order = Order


class OrderCreateView(LoginRequiredMixin, CreateView):
    model: Order = Order
    fields: list = [
        'brand',
        'model',
        'model_year',
        'mileage',
        'choose_date',
        'chain_change_price',
        'oil_and_oil_filter_change_price',
        'air_filter_change_price',
        'brake_fluid_change_price'
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model: Order = Order
    fields: list = [
        'mileage',
        'choose_date',
        'chain_change_price',
        'oil_and_oil_filter_change_price',
        'air_filter_change_price',
        'brake_fluid_change_price',
        'status'
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order: Order = self.get_object()
        if self.request.user == order.user:
            return True
        return False


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model: Order = Order

    def test_func(self):
        order: Order = self.get_object()
        if self.request.user == order.user:
            return True
        return False

