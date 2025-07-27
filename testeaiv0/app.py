from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from sqlalchemy import Numeric


# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '3306')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://root:protasete00@localhost/sneaker_store')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Inicializar extensões
db = SQLAlchemy(app)
cors = CORS(app)
jwt = JWTManager(app)

# Modelos do Banco de Dados
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    orders = db.relationship('Order', backref='user', lazy=True)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat()
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relacionamentos
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255))
    stock_quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand = db.Column(db.String(50))
    size_available = db.Column(db.String(100))  # JSON string com tamanhos disponíveis
    color = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'image_url': self.image_url,
            'stock_quantity': self.stock_quantity,
            'category': self.category.to_dict() if self.category else None,
            'brand': self.brand,
            'size_available': self.size_available,
            'color': self.color,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    size = db.Column(db.String(10))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'size': self.size,
            'subtotal': float(self.product.price * self.quantity),
            'added_at': self.added_at.isoformat()
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Decimal(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, shipped, delivered, cancelled
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')
    shipping_address = db.Column(db.Text, nullable=False)
    tracking_code = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'total_amount': float(self.total_amount),
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'shipping_address': self.shipping_address,
            'tracking_code': self.tracking_code,
            'notes': self.notes,
            'items': [item.to_dict() for item in self.order_items],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Decimal(10, 2), nullable=False)  # Preço no momento da compra
    size = db.Column(db.String(10))
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'price': float(self.price),
            'size': self.size,
            'subtotal': float(self.price * self.quantity)
        }

# Rotas de Autenticação
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Nome, email e senha são obrigatórios'}), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Criar novo usuário
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            address=data.get('address')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Criar token de acesso
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': user.to_dict(),
            'access_token': access_token
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'message': 'Login realizado com sucesso',
                'user': user.to_dict(),
                'access_token': access_token
            })
        else:
            return jsonify({'error': 'Email ou senha inválidos'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({'user': user.to_dict()})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rotas de Produtos
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        # Parâmetros de filtro
        category_slug = request.args.get('category')
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        
        # Query base
        query = Product.query.filter_by(is_active=True)
        
        # Aplicar filtros
        if category_slug:
            category = Category.query.filter_by(slug=category_slug).first()
            if category:
                query = query.filter_by(category_id=category.id)
        
        if search:
            query = query.filter(Product.name.contains(search))
        
        if min_price:
            query = query.filter(Product.price >= min_price)
        
        if max_price:
            query = query.filter(Product.price <= max_price)
        
        # Paginação
        products = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        
        if not product or not product.is_active:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        return jsonify({'product': product.to_dict()})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rotas de Categorias
@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rotas do Carrinho
@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        user_id = get_jwt_identity()
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        return jsonify({
            'cart_items': [item.to_dict() for item in cart_items],
            'total': float(total),
            'count': len(cart_items)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        size = data.get('size')
        
        if not product_id:
            return jsonify({'error': 'ID do produto é obrigatório'}), 400
        
        # Verificar se produto existe
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        # Verificar estoque
        if product.stock_quantity < quantity:
            return jsonify({'error': 'Estoque insuficiente'}), 400
        
        # Verificar se item já existe no carrinho
        existing_item = CartItem.query.filter_by(
            user_id=user_id, 
            product_id=product_id, 
            size=size
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                size=size
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        return jsonify({'message': 'Produto adicionado ao carrinho'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/update/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
        
        if not cart_item:
            return jsonify({'error': 'Item não encontrado no carrinho'}), 404
        
        new_quantity = data.get('quantity')
        if new_quantity is not None:
            if new_quantity <= 0:
                db.session.delete(cart_item)
            else:
                # Verificar estoque
                if cart_item.product.stock_quantity < new_quantity:
                    return jsonify({'error': 'Estoque insuficiente'}), 400
                cart_item.quantity = new_quantity
        
        db.session.commit()
        
        return jsonify({'message': 'Carrinho atualizado'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    try:
        user_id = get_jwt_identity()
        
        cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
        
        if not cart_item:
            return jsonify({'error': 'Item não encontrado no carrinho'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removido do carrinho'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    try:
        user_id = get_jwt_identity()
        
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({'message': 'Carrinho limpo'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rotas de Pedidos
@app.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('shipping_address'):
            return jsonify({'error': 'Endereço de entrega é obrigatório'}), 400
        
        # Buscar itens do carrinho
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        
        if not cart_items:
            return jsonify({'error': 'Carrinho vazio'}), 400
        
        # Calcular total
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Criar pedido
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            payment_method=data.get('payment_method', 'credit_card'),
            shipping_address=data['shipping_address'],
            notes=data.get('notes')
        )
        
        db.session.add(order)
        db.session.flush()  # Para obter o ID do pedido
        
        # Criar itens do pedido
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                size=cart_item.size
            )
            db.session.add(order_item)
            
            # Atualizar estoque
            cart_item.product.stock_quantity -= cart_item.quantity
        
        # Limpar carrinho
        CartItem.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Pedido criado com sucesso',
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        orders = Order.query.filter_by(user_id=user_id).order_by(
            Order.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    try:
        user_id = get_jwt_identity()
        
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        return jsonify({'order': order.to_dict()})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota de contato
@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        # Aqui você pode implementar o envio de email
        # Por enquanto, apenas retornamos sucesso
        
        return jsonify({'message': 'Mensagem enviada com sucesso'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota de saúde da API
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

# Inicializar banco de dados
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
