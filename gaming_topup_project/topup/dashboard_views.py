from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import TopUpOrder, TopUpProduct

@staff_member_required
def analytics_dashboard(request):
    """
    Analytics dashboard showing key metrics and insights
    """
    # Top 5 Most Purchased Top-Up Products
    top_products = (
        TopUpProduct.objects
        .select_related('game')
        .annotate(
            total_orders=Count('orders', filter=Q(orders__status='success')),
            total_revenue=Sum('orders__product__price', filter=Q(orders__status='success'))
        )
        .filter(total_orders__gt=0)
        .order_by('-total_orders')[:5]
    )
    
    # Daily Revenue (last 7 days) from successful orders
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)  # Last 7 days including today
    
    daily_revenue = []
    for i in range(7):
        date = start_date + timedelta(days=i)
        revenue = (
            TopUpOrder.objects
            .filter(
                status='success',
                created_at__date=date
            )
            .select_related('product')
            .aggregate(total=Sum('product__price'))['total'] or 0
        )
        daily_revenue.append({
            'date': date,
            'revenue': revenue
        })
    
    # Failed Payment Count (current month)
    current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    failed_payments_count = TopUpOrder.objects.filter(
        status='failed',
        created_at__gte=current_month_start
    ).count()
    
    # Additional analytics
    total_orders = TopUpOrder.objects.count()
    successful_orders = TopUpOrder.objects.filter(status='success').count()
    pending_orders = TopUpOrder.objects.filter(status='pending').count()
    
    success_rate = (successful_orders / total_orders * 100) if total_orders > 0 else 0
    
    total_revenue = (
        TopUpOrder.objects
        .filter(status='success')
        .select_related('product')
        .aggregate(total=Sum('product__price'))['total'] or 0
    )
    
    context = {
        'top_products': top_products,
        'daily_revenue': daily_revenue,
        'failed_payments_count': failed_payments_count,
        'total_orders': total_orders,
        'successful_orders': successful_orders,
        'pending_orders': pending_orders,
        'success_rate': round(success_rate, 2),
        'total_revenue': round(total_revenue, 2),
    }
    
    return render(request, 'dashboard/analytics.html', context)
