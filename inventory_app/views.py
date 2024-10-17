from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Item
from django.core.cache import cache
from .serializer import ItemSerializer
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def uniform_response(self, status_code, message, data=None):
        return Response({
            "status": status_code,
            "message": message,
            "data": data
        }, status=status_code)

    # Retrieve an item with caching
    def retrieve(self, request, pk=None):
        cache_key = f"item_{pk}"
        item = cache.get(cache_key)

        if not item:
            logger.info(f"Item {pk} not found in cache. Fetching from database.")
            try:
                item = Item.objects.get(id=pk)
                serializer = ItemSerializer(item)
                cache.set(cache_key, serializer.data, timeout=60 * 15)

                logger.info(f"Item {pk} fetched from database and cached.")
                return self.uniform_response(status.HTTP_200_OK, "Item retrieved successfully.", serializer.data)
            except Item.DoesNotExist:
                logger.error(f"Item {pk} not found.")
                return self.uniform_response(status.HTTP_404_NOT_FOUND, "Item not found.", None)
            except Exception as e:
                logger.error(f"Error retrieving item {pk}: {str(e)}")
                return self.uniform_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error retrieving item.", None)

        logger.info(f"Item {pk} retrieved from cache.")
        return self.uniform_response(status.HTTP_200_OK, "Item retrieved successfully.", item)

    def create(self, request):
        serializer = ItemSerializer(data=request.data)

        if Item.objects.filter(name=request.data.get('name')).exists():
            logger.error("Attempt to create an item that already exists.")
            return self.uniform_response(status.HTTP_400_BAD_REQUEST, "Item already exists", None)

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info(f"Item {serializer.data['id']} created successfully.")
                return self.uniform_response(status.HTTP_201_CREATED, "Item created successfully.", serializer.data)
        except IntegrityError:
            logger.error("Integrity error occurred while creating item.")
            return self.uniform_response(status.HTTP_400_BAD_REQUEST,
                                         "Item creation failed due to integrity constraints.", None)
        except Exception as e:
            logger.error(f"Failed to create item: {str(e)}")
            return self.uniform_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create item.", None)

        logger.error(f"Failed to create item: {serializer.errors}")
        return self.uniform_response(status.HTTP_400_BAD_REQUEST, "Failed to create item.", serializer.errors)

    def update(self, request, pk=None):
        try:
            item = Item.objects.get(id=pk)
            serializer = ItemSerializer(item, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                cache_key = f"item_{pk}"
                cache.delete(cache_key)

                logger.info(f"Item {pk} updated successfully.")
                return self.uniform_response(status.HTTP_200_OK, "Item updated successfully.", serializer.data)
        except Item.DoesNotExist:
            logger.error(f"Item {pk} not found.")
            return self.uniform_response(status.HTTP_404_NOT_FOUND, "Item not found.", None)
        except Exception as e:
            logger.error(f"Failed to update item {pk}: {str(e)}")
            return self.uniform_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update item.", None)

        logger.error(f"Failed to update item {pk}: {serializer.errors}")
        return self.uniform_response(status.HTTP_400_BAD_REQUEST, "Failed to update item.", serializer.errors)

    def destroy(self, request, pk=None):
        try:
            item = Item.objects.get(id=pk)
            item.delete()

            cache_key = f"item_{pk}"
            cache.delete(cache_key)

            logger.info(f"Item {pk} deleted successfully.")
            return self.uniform_response(status.HTTP_200_OK, "Item deleted successfully.", None)
        except Item.DoesNotExist:
            logger.error(f"Item {pk} not found.")
            return self.uniform_response(status.HTTP_404_NOT_FOUND, "Item not found.", None)
        except Exception as e:
            logger.error(f"Failed to delete item {pk}: {str(e)}")
            return self.uniform_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete item.", None)
