from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TopUpOrderSerializer, TopUpOrderResponseSerializer

@api_view(['POST'])
def create_topup_order(request):
    """
    Create a new top-up order with validation
    """
    serializer = TopUpOrderSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            order = serializer.save()
            response_serializer = TopUpOrderResponseSerializer(order)
            
            return Response({
                'success': True,
                'message': 'Top-up order created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error creating order: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'success': False,
        'message': 'Validation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
