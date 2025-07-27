from app import app, db, User, Category, Product, CartItem, Order, OrderItem
from werkzeug.security import generate_password_hash
import json

def init_database():
    """Inicializar o banco de dados com dados básicos"""
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existem dados
        if Category.query.count() > 0:
            print("Banco de dados já inicializado!")
            return
        
        # Criar categorias
        categories_data = [
            {'name': 'Corrida', 'slug': 'running', 'description': 'Tênis especializados para corrida e atividades aeróbicas'},
            {'name': 'Casual', 'slug': 'casual', 'description': 'Tênis para uso diário e ocasiões casuais'},
            {'name': 'Esporte', 'slug': 'sport', 'description': 'Tênis para atividades esportivas e treinos'}
        ]
        
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
        
        db.session.commit()
        
        # Buscar categorias criadas
        running_cat = Category.query.filter_by(slug='running').first()
        casual_cat = Category.query.filter_by(slug='casual').first()
        sport_cat = Category.query.filter_by(slug='sport').first()
        
        # Criar produtos
        products_data = [
            {
                'name': 'Air Max Revolution',
                'description': 'Tênis de corrida com tecnologia de amortecimento avançada. Ideal para longas distâncias com máximo conforto.',
                'price': 299.99,
                'image_url': '/placeholder.svg?height=200&width=200',
                'stock_quantity': 50,
                'category_id': running_cat.id,
                'brand': 'Nike',
                'size_available': '["36", "37", "38", "39", "40", "41", "42", "43", "44"]',
                'color': 'Azul/Branco'
            },
            {
                'name': 'Urban Classic',
                'description': 'Tênis casual urbano com design minimalista. Perfeito para o dia a dia com estilo e conforto.',
                'price': 199.99,
                'image_url': '/placeholder.svg?height=200&width=200',
                'stock_quantity': 75,
                'category_id': casual_cat.id,
                'brand': 'Adidas',
                'size_available': '["35", "36", "37", "38", "39", "40", "41", "42", "43", "44"]',
                'color': 'Branco'
            },
            {
                'name': 'Sport Pro Elite',
                'description': 'Tênis esportivo profissional para alta performance. Desenvolvido para atletas exigentes.',
                'price': 399.99,
                'image_url': '/placeholder.svg?height=200&width=200',
                'stock_quantity': 30,
                'category_id': sport_cat.id,
                'brand': 'Puma',
                'size_available': '["37", "38", "39", "40", "41", "42", "43", "44", "45"]',
                'color': 'Preto/Vermelho'
            },
            {
                'name': 'Runner\'s Choice',
                'description': 'Tênis de corrida leve com mesh respirável. Tecnologia de ventilação superior.',
                'price': 249.99,
                'image_url': '/placeholder.svg?height=200&width=200',
                'stock_quantity': 60,
                'category_id': running_cat.id,
                'brand': 'Asics',
                'size_available': '["36", "37", "38", "39", "40", "41", "42", "43", "44"]',
                'color': 'Cinza/Verde'
            },
            {
                'name': 'Street Style',
                'description': 'Tênis casual com design street wear moderno. Para quem busca estilo urbano.',
                'price': 179.99,
                'image_url': '/placeholder.svg?height=200&width=200',
                'stock_quantity': 80,
                'category_id': casual_cat.id,
                'brand': 'Vans',
                'size_available': '["35", "36", "37", "38", "39", "40", "41", "42", "43"]',
                'color': 'Preto'
            },
            {
                'name': 'Athletic Force',
                'description': 'Tênis para treino atlético e cross training. Estabilidade e resistência garantidas.',
                'price': 349.99,
                'image_url': '/placeholder.svg?height=200&width=200',
                'stock_quantity': 40,
                'category_id': sport_cat.id,
                'brand': 'Reebok',
                'size_available': '["37", "38", "39", "40", "41", "42", "43", "44", "45"]',
                'color': 'Azul/Amarelo'
            }
        ]
        
        for prod_data in products_data:
            product = Product(**prod_data)
            db.session.add(product)
        
        # Criar usuário administrador
        admin_user = User(
            name='Administrador',
            email='admin@sneakerhub.com',
            phone='(11) 99999-9999',
            address='Rua das Sneakers, 123 - São Paulo, SP'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        db.session.commit()
        print("Banco de dados inicializado com sucesso!")

def reset_database():
    """Resetar o banco de dados"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Banco de dados resetado!")

if __name__ == '__main__':
    init_database()
