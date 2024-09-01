from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
from .models import User 
from .serializer import UserSerializer
from django.conf import settings
from django.http import JsonResponse
import requests

logger = logging.getLogger(__name__)

@api_view(['POST'])
def register_user(request):
    logger.info('Received user registration request')
    
    if request.method == 'POST':        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('User created successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(f'User creation failed: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_users(request):
    logger.info('Received request to get all users')
    # console.log('Received request to get all users')
    if request.method == 'GET':
        
        gender = request.query_params.get('gender', None)
        
        # print(gender, gender)
        
        # users = User.objects.all()  # 모든 사용자 가져오기
        
        if gender:
            # gender 필드에 해당하는 사용자만 필터링
            users = User.objects.filter(gender=gender).order_by('-id')
        else:
            # gender가 제공되지 않은 경우 모든 사용자 가져오기
            users = User.objects.all().order_by('-id')
            
        serializer = UserSerializer(users, many=True)  # 사용자 데이터를 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)  # 직렬화된 데이터와 함께 응답 반환
    
    
    
@api_view(['POST'])
def kakaopay_ready(request):
    def prepare_kakaopay_payment(secret_key, payload):
        url = 'https://open-api.kakaopay.com/online/v1/payment/ready'
        
        headers = {
            'Authorization': f'SECRET_KEY {secret_key}',
            'Content-Type': 'application/json',
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': response.status_code, 'message': response.text}

    # 사용 예시
    secret_key = "DEV395B1DB3976D8D956D161AD61A15B0111641D"
    payload = {
        "cid": "TC0ONETIME",
        "partner_order_id": "partner_order_id",
        "partner_user_id": "partner_user_id",
        "item_name": "초코파이",
        "quantity": 1,
        "total_amount": 1000,
        "vat_amount": 100,
        "tax_free_amount": 0,
        "approval_url": "http://192.0.0.2:84/PaymentSuccess",
        "fail_url": "https://www.naver.com",
        "cancel_url": "https://www.naver.com"
    }

    result = prepare_kakaopay_payment(secret_key, payload)
    
    # 결과를 Response 객체로 반환
    
    print(f'하이하 {result}')
    return Response(result)

@api_view(['POST'])
def kakaopay_approve(request):
    def approve_kakaopay_payment(secret_key, payload):
        url = 'https://open-api.kakaopay.com/online/v1/payment/approve'
        
        headers = {
            'Authorization': f'SECRET_KEY {secret_key}',
            'Content-Type': 'application/json',
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': response.status_code, 'message': response.text}
    
    secret_key = "DEV395B1DB3976D8D956D161AD61A15B0111641D"
    
    tid = request.data.get('tid')
    pg_token = request.data.get('pg_token')
    
    print(tid, pg_token)
    if not tid or not pg_token:
        return Response({'error': 'Missing required parameters'}, status=400)
    
    payload = {
        "cid": "TC0ONETIME",
        "tid": tid,
        "partner_order_id": "partner_order_id",
        "partner_user_id": "partner_user_id",
        "pg_token": pg_token,
    }

    result = approve_kakaopay_payment(secret_key, payload)
    
    # 결과를 Response 객체로 반환
    return Response(result)
        
        