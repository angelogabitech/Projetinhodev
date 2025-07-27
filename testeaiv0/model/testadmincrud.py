import requests
import json
from datetime import datetime

# Configuração base
BASE_URL = 'http://localhost:5000/api'

def get_admin_token():
    """Fazer login como administrador"""
    login_data = {
        'email': 'admin@sneakerhub.com',
        'password': 'admin123'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Erro ao fazer login como admin:", response.json())
        return None

def test_product_crud():
    """Testar CRUD de produtos"""
    token = get_admin_token()
    if not token:
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("=== TESTANDO CRUD DE PRODUTOS ===")
    
    # 1. Criar produto
    product_data = {
        'name': 'Tênis Teste CRUD',
        'description': 'Produto criado para teste do CRUD',
        'price': 199.99,
        'stock_quantity': 25,
        'category_id': 1,
        'brand': 'TestBrand',
        'color': 'Azul',
        'size_available': '["38", "39", "40", "41", "42"]'
    }
    
    response = requests.post(f'{BASE_URL}/admin/products', json=product_data, headers=headers)
    print(f"Criar produto: {response.status_code}")
    
    if response.status_code == 201:
        product_id = response.json()['product']['id']
        print(f"✅ Produto criado com ID: {product_id}")
        
        # 2. Atualizar produto
        update_data = {
            'name': 'Tênis Teste CRUD - Atualizado',
            'price': 249.99,
            'stock_quantity': 30
        }
        
        response = requests.put(f'{BASE_URL}/admin/products/{product_id}', json=update_data, headers=headers)
        print(f"Atualizar produto: {response.status_code}")
        if response.status_code == 200:
            print("✅ Produto atualizado com sucesso")
        
        # 3. Buscar produto específico
        response = requests.get(f'{BASE_URL}/products/{product_id}')
        print(f"Buscar produto: {response.status_code}")
        if response.status_code == 200:
            product = response.json()['product']
            print(f"✅ Produto encontrado: {product['name']} - R$ {product['price']}")
        
        # 4. Listar todos os produtos (admin)
        response = requests.get(f'{BASE_URL}/admin/products', headers=headers)
        print(f"Listar produtos (admin): {response.status_code}")
        if response.status_code == 200:
            products = response.json()['products']
            print(f"✅ Total de produtos: {len(products)}")
        
        # 5. Deletar produto
        response = requests.delete(f'{BASE_URL}/admin/products/{product_id}', headers=headers)
        print(f"Deletar produto: {response.status_code}")
        if response.status_code == 200:
            print("✅ Produto deletado com sucesso")
    
    print()

def test_category_crud():
    """Testar CRUD de categorias"""
    token = get_admin_token()
    if not token:
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("=== TESTANDO CRUD DE CATEGORIAS ===")
    
    # 1. Criar categoria
    category_data = {
        'name': 'Categoria Teste',
        'slug': 'categoria-teste',
        'description': 'Categoria criada para teste do CRUD'
    }
    
    response = requests.post(f'{BASE_URL}/admin/categories', json=category_data, headers=headers)
    print(f"Criar categoria: {response.status_code}")
    
    if response.status_code == 201:
        category_id = response.json()['category']['id']
        print(f"✅ Categoria criada com ID: {category_id}")
        
        # 2. Atualizar categoria
        update_data = {
            'name': 'Categoria Teste - Atualizada',
            'description': 'Descrição atualizada'
        }
        
        response = requests.put(f'{BASE_URL}/admin/categories/{category_id}', json=update_data, headers=headers)
        print(f"Atualizar categoria: {response.status_code}")
        if response.status_code == 200:
            print("✅ Categoria atualizada com sucesso")
        
        # 3. Listar categorias
        response = requests.get(f'{BASE_URL}/categories')
        print(f"Listar categorias: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()['categories']
            print(f"✅ Total de categorias: {len(categories)}")
        
        # 4. Deletar categoria
        response = requests.delete(f'{BASE_URL}/admin/categories/{category_id}', headers=headers)
        print(f"Deletar categoria: {response.status_code}")
        if response.status_code == 200:
            print("✅ Categoria deletada com sucesso")
    
    print()

def test_user_management():
    """Testar gestão de usuários"""
    token = get_admin_token()
    if not token:
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("=== TESTANDO GESTÃO DE USUÁRIOS ===")
    
    # 1. Listar usuários
    response = requests.get(f'{BASE_URL}/admin/users', headers=headers)
    print(f"Listar usuários: {response.status_code}")
    
    if response.status_code == 200:
        users = response.json()['users']
        print(f"✅ Total de usuários: {len(users)}")
        
        if users:
            user_id = users[0]['id']
            
            # 2. Buscar detalhes do usuário
            response = requests.get(f'{BASE_URL}/admin/users/{user_id}', headers=headers)
            print(f"Detalhes do usuário: {response.status_code}")
            if response.status_code == 200:
                user = response.json()['user']
                print(f"✅ Usuário: {user['name']} - {user['email']}")
                print(f"   Pedidos: {user['stats']['total_orders']}")
                print(f"   Total gasto: R$ {user['stats']['total_spent']}")
            
            # 3. Atualizar usuário
            update_data = {
                'phone': '(11) 99999-8888'
            }
            
            response = requests.put(f'{BASE_URL}/admin/users/{user_id}', json=update_data, headers=headers)
            print(f"Atualizar usuário: {response.status_code}")
            if response.status_code == 200:
                print("✅ Usuário atualizado com sucesso")
    
    print()

def test_order_management():
    """Testar gestão de pedidos"""
    token = get_admin_token()
    if not token:
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("=== TESTANDO GESTÃO DE PEDIDOS ===")
    
    # 1. Listar pedidos
    response = requests.get(f'{BASE_URL}/admin/orders', headers=headers)
    print(f"Listar pedidos: {response.status_code}")
    
    if response.status_code == 200:
        orders = response.json()['orders']
        print(f"✅ Total de pedidos: {len(orders)}")
        
        if orders:
            order_id = orders[0]['id']
            
            # 2. Atualizar status do pedido
            update_data = {
                'status': 'confirmed',
                'payment_status': 'paid',
                'tracking_code': 'BR123456789'
            }
            
            response = requests.put(f'{BASE_URL}/admin/orders/{order_id}', json=update_data, headers=headers)
            print(f"Atualizar pedido: {response.status_code}")
            if response.status_code == 200:
                print("✅ Pedido atualizado com sucesso")
    
    print()

def test_dashboard():
    """Testar dashboard administrativo"""
    token = get_admin_token()
    if not token:
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("=== TESTANDO DASHBOARD ===")
    
    response = requests.get(f'{BASE_URL}/admin/dashboard', headers=headers)
    print(f"Dashboard: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        stats = data['stats']
        
        print("✅ Dashboard carregado com sucesso:")
        print(f"   Usuários: {stats['total_users']}")
        print(f"   Produtos: {stats['total_products']}")
        print(f"   Pedidos: {stats['total_orders']}")
        print(f"   Receita: R$ {stats['total_revenue']}")
        
        if data['low_stock_products']:
            print(f"   ⚠️  Produtos com estoque baixo: {len(data['low_stock_products'])}")
        
        if data['top_products']:
            print("   🏆 Top produtos:")
            for product in data['top_products'][:3]:
                print(f"      - {product['name']}: {product['total_sold']} vendidos")
    
    print()

def test_reports():
    """Testar relatórios"""
    token = get_admin_token()
    if not token:
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("=== TESTANDO RELATÓRIOS ===")
    
    # Relatório de vendas
    response = requests.get(f'{BASE_URL}/admin/reports/sales', headers=headers)
    print(f"Relatório de vendas: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        summary = data['summary']
        
        print("✅ Relatório de vendas:")
        print(f"   Total de vendas: R$ {summary['total_sales']}")
        print(f"   Total de pedidos: {summary['total_orders']}")
        print(f"   Ticket médio: R$ {summary['average_order_value']}")
        
        if data['sales_by_category']:
            print("   Vendas por categoria:")
            for cat in data['sales_by_category']:
                print(f"      - {cat['category']}: R$ {cat['total']}")
    
    print()

def run_admin_tests():
    """Executar todos os testes administrativos"""
    print("=== INICIANDO TESTES DO CRUD ADMINISTRATIVO ===\n")
    
    # Verificar se consegue fazer login como admin
    token = get_admin_token()
    if not token:
        print("❌ Não foi possível fazer login como administrador!")
        print("Certifique-se de que o usuário admin existe no banco de dados.")
        return
    
    print("✅ Login administrativo realizado com sucesso!\n")
    
    # Executar todos os testes
    test_product_crud()
    test_category_crud()
    test_user_management()
    test_order_management()
    test_dashboard()
    test_reports()
    
    print("=== TODOS OS TESTES ADMINISTRATIVOS CONCLUÍDOS ===")

if __name__ == '__main__':
    run_admin_tests()
