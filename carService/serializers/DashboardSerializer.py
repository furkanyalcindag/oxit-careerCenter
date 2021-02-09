from rest_framework import serializers


class AdminDashboardSerializer(serializers.Serializer):
    productCount = serializers.CharField()
    outOfStockCount = serializers.CharField()
    carCount = serializers.CharField()
    customerCount = serializers.CharField()
    canceledServiceCount = serializers.CharField()
    remainingDebt = serializers.DecimalField(max_digits=10, decimal_places=2)
    uncompletedServiceCount = serializers.CharField()
    completedServiceCount = serializers.CharField()
    waitingApproveServiceCount = serializers.CharField()
    totalCheckingAccountDaily = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalCheckingAccountMonthly = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalCheckingAccountYearly = serializers.DecimalField(max_digits=10, decimal_places=2)
