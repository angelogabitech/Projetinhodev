import requests
import json

# Configuração base
BASE_URL = 'http://localhost:5000/api'

def test_health():
    """Testar se a API está funcionando"""
    response = requests.get(f'{BASE_URL}/health')
    print(f"Health Check: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register_user():
    """Testar registro de usuário"""
    user_data = {
        'name': 'João Silva',
        'email': 'joao@teste.com',
        'password': '123456',
        'phone': '(11) 98765-4321',
        'address': 'Rua Teste, 123 - São Paulo, SP'
    }
    
    response = requests.post(f'{BASE_URL}/auth/register', json=user_data)
    print(f"Register User: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"User created: {data['user']['name']}")
        return data['access_token']
    else:
        print(f"Error: {response.json()}")
        return None

def test_login():
    """Testar login"""
    login_data = {
        'email': 'joao@teste.com',
        'password': '123456'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    print(f"Login: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Login successful: {data['user']['name']}")
        return data['access_token']
    else:
        print(f"Error: {response.json()}")
        return None

def test_get_products():
    """Testar listagem de produtos"""
    response = requests.get(f'{BASE_URL}/products')
    print(f"Get Products: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data['products'])} products")
        return data['products']
    else:
        print(f"Error: {response.json()}")
        return []

def test_get_categories():
    """Testar listagem de categorias"""
    response = requests.get(f'{BASE_URL}/categories')
    print(f"Get Categories: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data['categories'])} categories")
        return data['categories']
    else:
        print(f"Error: {response.json()}")
        return []

def test_cart_operations(token, product_id):
    """Testar operações do carrinho"""
    headers = {'Authorization': f'Bearer {token}'}
    
    # Adicionar ao carrinho
    cart_data = {
        'product_id': product_id,
        'quantity': 2,
        'size': '42'
    }
    
    response = requests.post(f'{BASE_URL}/cart/add', json=cart_data, headers=headers)
    print(f"Add to Cart: {response.status_code}")
    
    # Visualizar carrinho
    response = requests.get(f'{BASE_URL}/cart', headers=headers)
    print(f"Get Cart: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Cart has {data['count']} items, total: R$ {data['total']}")
        return data['cart_items']
    
    return []

def test_create_order(token):
    """Testar criação de pedido"""
    headers = {'Authorization': f'Bearer {token}'}
    
    order_data = {
        'shipping_address': 'Rua de Entrega, 456 - São Paulo, SP',
        'payment_method': 'credit_card',
        'notes': 'Entregar no período da manhã'
    }
    
    response = requests.post(f'{BASE_URL}/orders', json=order_data, headers=headers)
    print(f"Create Order: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"Order created: #{data['order']['id']}")
        return data['order']['id']
    else:
        print(f"Error: {response.json()}")
        return None

def run_all_tests():
    """Executar todos os testes"""
    print("=== INICIANDO TESTES DA API ===\n")
    
    # Teste 1: Health Check
    print("1. Testando Health Check...")
    if not test_health():
        print("❌ API não está funcionando!")
        return
    print("✅ API funcionando!\n")
    
    # Teste 2: Categorias
    print("2. Testando Categorias...")
    categories = test_get_categories()
    print("✅ Categorias OK!\n")
    
    # Teste 3: Produtos
    print("3. Testando Produtos...")
    products = test_get_products()
    if not products:
        print("❌ Nenhum produto encontrado!")
        return
    print("✅ Produtos OK!\n")
    
    # Teste 4: Registro de usuário
    print("4. Testando Registro...")
    token = test_register_user()
    if not token:
        print("❌ Falha no registro!")
        return
    print("✅ Registro OK!\n")
    
    # Teste 5: Login
    print("5. Testando Login...")
    token = test_login()
    if not token:
        print("❌ Falha no login!")
        return
    print("✅ Login OK!\n")
    
    # Teste 6: Carrinho
    print("6. Testando Carrinho...")
    cart_items = test_cart_operations(token, products[0]['id'])
    print("✅ Carrinho OK!\n")
    
    # Teste 7: Pedido
    print("7. Testando Pedido...")
    order_id = test_create_order(token)
    if order_id:
        print("✅ Pedido OK!\n")
    
    print("=== TODOS OS TESTES CONCLUÍDOS ===")

if __name__ == '__main__':
    run_all_tests()
