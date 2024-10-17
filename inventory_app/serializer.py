from rest_framework import serializers
from .models import Item

from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity', 'price','stock_status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    # Custom field to determine stock status
    def get_stock_status(self, obj):
        if obj.quantity > 0:
            return "In Stock"
        return "Out of Stock"

    def validate_name(self, value):
        """Check that the item name is not empty."""
        if not value:
            raise serializers.ValidationError("Item name cannot be empty.")
        return value

    def validate_quantity(self, value):
        """Check that the quantity is a non-negative integer."""
        if value < 0:
            raise serializers.ValidationError("Quantity must be a non-negative integer.")
        return value

    def validate_price(self, value):
        """Check that the price is a non-negative float."""
        if value < 0:
            raise serializers.ValidationError("Price must be a non-negative float.")
        return value
