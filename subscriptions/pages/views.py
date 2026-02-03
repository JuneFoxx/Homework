from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Subscription, MonthlyExpenseSummary
from .forms import SubscriptionCreateForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from collections import OrderedDict

class IndexView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'pages/index.html'
    context_object_name = 'subscriptions'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subs = self.object_list

        active_subs_count = subs.filter(is_active=True).count()
        context['active_subscriptions'] = active_subs_count

        totals = {}

        currencies = ['RUB', 'USD', 'EUR', 'UAH']

        for currency in currencies:
            totals[currency] = 0

        for sub in subs:
            if not sub.is_active:
                continue
            if getattr(sub, 'period', None) == 'monthly':
                monthly_pay = sub.price
            elif getattr(sub, 'period', None) == 'quarterly':
                monthly_pay = sub.price / 3
            elif getattr(sub, 'period', None) == 'semi_annual':
                monthly_pay = sub.price / 6
            elif getattr(sub, 'period', None) == 'annual':
                monthly_pay = sub.price / 12
            elif getattr(sub, 'period', None) == 'one_time':
                continue

            totals[sub.currency] += monthly_pay

        context['monthly_total_by_currency'] = totals
        
        today = timezone.now().date()
        start_date = today - relativedelta(months=11)   # 12 месяцев включая текущий
        
        monthly_expenses = OrderedDict()
        
        current = start_date.replace(day=1)
        while current <= today:
            year = current.year
            month = current.month
            key = current.strftime("%Y-%m")
            label = current.strftime("%b %Y") 
            monthly_expenses[key] = {"label": label, "amount": 0.0}
            current += relativedelta(months=1)

        summaries = MonthlyExpenseSummary.objects.filter(
            year__gte=start_date.year,
            year__lte=today.year,
        ).order_by('year', 'month')

        for summary in summaries:
            key = f"{summary.year}-{summary.month:02d}"
            if key in monthly_expenses:
                monthly_expenses[key]["amount"] += float(summary.total_amount)

        chart_labels = [data["label"] for data in monthly_expenses.values()]
        chart_data = [data["amount"] for data in monthly_expenses.values()]

        context['monthly_chart'] = {
            'labels': chart_labels,
            'data': chart_data,
            'currency': 'RUB', 
        }
            
        return context
    
class SubscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionCreateForm
    template_name = 'pages/subscription_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SubscriptionDeleteView(DeleteView):
    model = Subscription
    success_url = '/'

class SubscriptionUpdateView(UpdateView):
    model = Subscription
    fields = ['name', 'price', 'currency', 'period', 'next_payment_date', 'is_active', 'note']
    template_name = 'pages/subscription_form.html'
    success_url = '/'

@login_required
def deactivate_subscription(request, pk):
    if request.method == 'POST':
        sub = get_object_or_404(Subscription, pk=pk, user=request.user)
        if sub.is_active:
            sub.is_active = False
        else:
            sub.is_active = True
        sub.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@method_decorator(require_POST, name='dispatch')
class ConfirmPaymentView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        subscription = get_object_or_404(
            Subscription,
            pk=pk,
            user=request.user,
            is_active=True
        )

        old_next_date = subscription.next_payment_date

        if not old_next_date:
            return JsonResponse(
                {"success": False, "error": "Нет даты следующей оплаты"},
                status=400
            )

        new_next_date = self._calculate_next_date(subscription, old_next_date)

        subscription.next_payment_date = new_next_date
        subscription.save(update_fields=['next_payment_date'])

        self._update_monthly_summary(old_next_date, subscription)

        return JsonResponse({
            "success": True,
            "new_next_date": new_next_date.strftime("%Y-%m-%d") if new_next_date else None,
            "new_days_until": subscription.days_until_next_payment,
            "message": "Оплата подтверждена, дата следующей оплаты обновлена"
        })

    def _calculate_next_date(self, subscription, current_date):
        """Логика прибавления периода"""
        period = subscription.period

        if period == 'monthly':
            return current_date + relativedelta(months=1)
        elif period == 'quarterly':
            return current_date + relativedelta(months=3)
        elif period == 'semi_annual':
            return current_date + relativedelta(months=6)
        elif period == 'annual':
            return current_date + relativedelta(years=1)
        elif period == 'one_time':
            subscription.is_active = False
            subscription.save(update_fields=['is_active'])
            return None
        else:
            raise ValueError(f"Неизвестный период подписки: {period}")

    def _update_monthly_summary(self, paid_date, subscription):
        """Добавляет цену в итог за месяц, в котором произошла оплата"""
        if not paid_date:
            return

        year = paid_date.year
        month = paid_date.month
        currency = subscription.currency or 'RUB'

        summary, created = MonthlyExpenseSummary.objects.get_or_create(
            year=year,
            month=month,
            currency=currency,
            defaults={
                'total_amount': 0,
                'updated_at': timezone.now(),
            }
        )

        summary.total_amount += subscription.price
        summary.updated_at = timezone.now()
        summary.save(update_fields=['total_amount', 'updated_at'])    