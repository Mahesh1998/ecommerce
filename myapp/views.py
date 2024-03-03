from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, User, ProductsBought
from django.http import QueryDict
from django.db import transaction

# Create your views here.

def home(request):
    return render(request, "home.html")

@csrf_exempt
def product_api(request, pk=None):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'products.html', {'products': products})
    elif request.method == 'POST':
        return create_product(request)
    elif request.method == 'PUT':
        return update_product(request, pk)
    elif request.method == 'DELETE':
        return delete_product(request, pk)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

def get_product(request):
    try:
        product_id = request.GET.get('product_id')
        if product_id:
            product = Product.objects.get_product(product_id=product_id)
            return JsonResponse({'product_id': product.product_id, 'name': product.name, 'description': product.description,
                                 'manufacturer_name': product.manufacturer_name, 'inventory_count': product.inventory_count})
        else:
            return JsonResponse({'message': 'Product ID is required'}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

def create_product(request):
    try:
        data = request.POST
        product = Product.objects.create_product(name=data['name'], description=data['description'],
                                                  manufacturer_name=data['manufacturer_name'], inventory_count=data['inventory_count'])
        return JsonResponse({'product_id': product.product_id, 'message': 'Product created successfully'})
    except Exception as e:
        return JsonResponse({'message': f'Error creating product: {str(e)}'}, status=500)

def update_product(request, pk):
    try:
        data = QueryDict(request.body)
        product_id = pk
        if not product_id:
            return JsonResponse({'message': 'Product ID is required for update'}, status=400)
        update_data = {key: data[key] for key in data.keys()}
        product = Product.objects.update_product(product_id=product_id, **update_data)
        return JsonResponse({'message': 'Product updated successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error updating product: {str(e)}'}, status=500)

def delete_product(request, pk):
    try:
        product_id = pk
        if not product_id:
            return JsonResponse({'message': 'Product ID is required for deletion'}, status=400)
        Product.objects.delete_product(product_id=product_id)
        return JsonResponse({'message': 'Product deleted successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error deleting product: {str(e)}'}, status=500)


@csrf_exempt
def user_api(request, pk=None):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})
    elif request.method == 'POST':
        return create_user(request)
    elif request.method == 'PUT':
        return update_user(request, pk)
    elif request.method == 'DELETE':
        return delete_user(request, pk)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

def get_user(request):
    try:
        user_id = request.GET.get('user_id')
        if user_id:
            user = User.objects.get_user(user_id=user_id)
            return JsonResponse({'user_id': user.user_id, 'user_name': user.user_name, 'user_preferences': user.user_preferences})
        else:
            return JsonResponse({'message': 'User ID is required'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

def create_user(request):
    try:
        data = request.POST
        user = User.objects.create_user(user_name=data['user_name'], user_password=data['user_password'],
                                        user_preferences=data['user_preferences'])
        return JsonResponse({'user_id': user.user_id, 'message': 'User created successfully'})
    except Exception as e:
        return JsonResponse({'message': f'Error creating user: {str(e)}'}, status=500)

def update_user(request, pk):
    try:
        data = QueryDict(request.body)
        user_id = pk
        if not user_id:
            return JsonResponse({'message': 'User ID is required for update'}, status=400)
        update_data = {key: data[key] for key in data.keys()}
        user = User.objects.update_user(user_id=user_id, **update_data)
        return JsonResponse({'message': 'User updated successfully'})
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error updating user: {str(e)}'}, status=500)

def delete_user(request, pk):
    try:
        user_id = pk
        if not user_id:
            return JsonResponse({'message': 'User ID is required for deletion'}, status=400)
        User.objects.delete_user(user_id=user_id)
        return JsonResponse({'message': 'User deleted successfully'})
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error deleting user: {str(e)}'}, status=500)

@csrf_exempt
def products_bought_api(request, pk=None):
    if request.method == 'GET':
        orders = ProductsBought.objects.all()
        users = User.objects.all()
        products = Product.objects.all()
        return render(request, 'orders.html', {'orders': orders, 'users': users, 'products': products})
    elif request.method == 'POST':
        return create_products_bought(request)
    elif request.method == 'PUT':
        return update_products_bought(request)
    elif request.method == 'DELETE':
        return delete_products_bought(request, pk)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

def get_products_bought(request):
    try:
        products_bought_id = request.GET.get('products_bought_id')
        if products_bought_id:
            products_bought = ProductsBought.objects.get_products_bought(products_bought_id=products_bought_id)
            return JsonResponse({'products_bought_id': products_bought.id, 'user_id': products_bought.user.user_id,
                                 'product_id': products_bought.product.product_id, 'user_name': products_bought.user_name,
                                 'product_name': products_bought.product_name, 'quantity': products_bought.quantity,
                                 'date_of_purchase': products_bought.date_of_purchase})
        else:
            return JsonResponse({'message': 'Products bought ID is required'}, status=400)
    except ProductsBought.DoesNotExist:
        return JsonResponse({'message': 'Products bought not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

def create_products_bought(request):
    try:
        data = request.POST
        if data['user'] and data['product']:
            user_obj = User.objects.get_user(data['user'])
            product_obj = Product.objects.get_product(data['product'])
            if not int(data['quantity']) < product_obj.inventory_count:
                return JsonResponse({'message': f'Quantity should not exceed {product_obj.inventory_count}'}, status=500)
            products_bought = ProductsBought.objects.create_products_bought(user=user_obj, product=product_obj,
                                                                            user_name=user_obj.user_name, product_name=product_obj.name,
                                                                            quantity=int(data['quantity']), date_of_purchase=data['date_of_purchase'])
            Product.objects.update_product(product_id = product_obj.product_id,inventory_count = product_obj.inventory_count - int(data['quantity']))
            return JsonResponse({'products_bought_id': products_bought.id, 'message': 'Products bought created successfully'})
        else:
            return JsonResponse({'message': 'Both User and Product are required'}, status=400)
    except Exception as e:
        return JsonResponse({'message': f'Error creating products bought: {str(e)}'}, status=500)

def update_products_bought(request):
    try:
        data = request.POST
        products_bought_id = data.get('products_bought_id')
        if not products_bought_id:
            return JsonResponse({'message': 'Products bought ID is required for update'}, status=400)
        products_bought = ProductsBought.objects.update_products_bought(products_bought_id=products_bought_id, **data)
        return JsonResponse({'message': 'Products bought updated successfully'})
    except ProductsBought.DoesNotExist:
        return JsonResponse({'message': 'Products bought not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error updating products bought: {str(e)}'}, status=500)

@transaction.atomic
def delete_products_bought_logic(pk):
    products_bought = ProductsBought.objects.get_products_bought(id = pk)
    Product.objects.update_product(product_id = products_bought.product.product_id,inventory_count = products_bought.product.inventory_count + products_bought.quantity)
    ProductsBought.objects.delete_products_bought(id=pk)


def delete_products_bought(request, pk):
    try:
        if not pk:
            return JsonResponse({'message': 'Invalid row selected for deletion'}, status=400)

        delete_products_bought_logic(pk)
        return JsonResponse({'message': 'Products bought deleted successfully'})

    except ProductsBought.DoesNotExist:
        return JsonResponse({'message': 'Products bought not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error deleting products bought: {str(e)}'}, status=500)

