// Sample product data
const products = [
  {
    id: 1,
    name: "Air Max Revolution",
    category: "running",
    price: 299.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis de corrida com tecnologia de amortecimento avançada",
  },
  {
    id: 2,
    name: "Urban Classic",
    category: "casual",
    price: 199.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis casual urbano com design minimalista",
  },
  {
    id: 3,
    name: "Sport Pro Elite",
    category: "sport",
    price: 399.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis esportivo profissional para alta performance",
  },
  {
    id: 4,
    name: "Runner's Choice",
    category: "running",
    price: 249.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis de corrida leve com mesh respirável",
  },
  {
    id: 5,
    name: "Street Style",
    category: "casual",
    price: 179.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis casual com design street wear moderno",
  },
  {
    id: 6,
    name: "Athletic Force",
    category: "sport",
    price: 349.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis para treino atlético e cross training",
  },
  {
    id: 7,
    name: "Marathon Master",
    category: "running",
    price: 429.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis de maratona com placa de carbono",
  },
  {
    id: 8,
    name: "Daily Comfort",
    category: "casual",
    price: 159.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis casual para uso diário com máximo conforto",
  },
  {
    id: 9,
    name: "Power Lift",
    category: "sport",
    price: 279.99,
    image: "/placeholder.svg?height=200&width=200",
    description: "Tênis para levantamento de peso com base estável",
  },
]

// Cart functionality
let cart = []
let currentFilter = "all"

// DOM elements
const productsGrid = document.getElementById("productsGrid")
const cartBtn = document.getElementById("cartBtn")
const cartModal = document.getElementById("cartModal")
const closeCart = document.getElementById("closeCart")
const cartCount = document.getElementById("cartCount")
const cartItems = document.getElementById("cartItems")
const cartTotal = document.getElementById("cartTotal")
const filterBtns = document.querySelectorAll(".filter-btn")
const contactForm = document.getElementById("contactForm")
const menuToggle = document.getElementById("menuToggle")

// Initialize the app
document.addEventListener("DOMContentLoaded", () => {
  renderProducts()
  updateCartUI()
  setupEventListeners()
  setupScrollEffects()
})

// Setup event listeners
function setupEventListeners() {
  // Filter buttons
  filterBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const filter = this.dataset.filter
      setActiveFilter(this)
      filterProducts(filter)
    })
  })

  // Cart modal
  cartBtn.addEventListener("click", () => {
    cartModal.style.display = "block"
    document.body.style.overflow = "hidden"
  })

  closeCart.addEventListener("click", () => {
    cartModal.style.display = "none"
    document.body.style.overflow = "auto"
  })

  // Close modal when clicking outside
  cartModal.addEventListener("click", (e) => {
    if (e.target === cartModal) {
      cartModal.style.display = "none"
      document.body.style.overflow = "auto"
    }
  })

  // Contact form
  contactForm.addEventListener("submit", handleContactForm)

  // Mobile menu toggle
  menuToggle.addEventListener("click", toggleMobileMenu)
}

// Render products
function renderProducts(productsToRender = products) {
  productsGrid.innerHTML = ""

  productsToRender.forEach((product) => {
    const productCard = createProductCard(product)
    productsGrid.appendChild(productCard)
  })
}

// Create product card
function createProductCard(product) {
  const card = document.createElement("div")
  card.className = "product-card"
  card.dataset.category = product.category

  card.innerHTML = `
        <div class="product-image">
            <img src="${product.image}" alt="${product.name}" loading="lazy">
        </div>
        <div class="product-info">
            <h3 class="product-name">${product.name}</h3>
            <p class="product-category">${getCategoryName(product.category)}</p>
            <p class="product-price">R$ ${product.price.toFixed(2).replace(".", ",")}</p>
            <button class="add-to-cart" onclick="addToCart(${product.id})">
                Adicionar ao Carrinho
            </button>
        </div>
    `

  return card
}

// Get category display name
function getCategoryName(category) {
  const categories = {
    running: "Corrida",
    casual: "Casual",
    sport: "Esporte",
  }
  return categories[category] || category
}

// Filter products
function filterProducts(filter) {
  currentFilter = filter
  const filteredProducts = filter === "all" ? products : products.filter((product) => product.category === filter)

  renderProducts(filteredProducts)
}

// Set active filter button
function setActiveFilter(activeBtn) {
  filterBtns.forEach((btn) => btn.classList.remove("active"))
  activeBtn.classList.add("active")
}

// Add to cart
function addToCart(productId) {
  const product = products.find((p) => p.id === productId)
  const existingItem = cart.find((item) => item.id === productId)

  if (existingItem) {
    existingItem.quantity += 1
  } else {
    cart.push({ ...product, quantity: 1 })
  }

  updateCartUI()
  showAddToCartFeedback()
}

// Remove from cart
function removeFromCart(productId) {
  cart = cart.filter((item) => item.id !== productId)
  updateCartUI()
  renderCartItems()
}

// Update cart quantity
function updateCartQuantity(productId, newQuantity) {
  const item = cart.find((item) => item.id === productId)
  if (item) {
    if (newQuantity <= 0) {
      removeFromCart(productId)
    } else {
      item.quantity = newQuantity
      updateCartUI()
      renderCartItems()
    }
  }
}

// Update cart UI
function updateCartUI() {
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0)
  const totalPrice = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)

  cartCount.textContent = totalItems
  cartTotal.textContent = totalPrice.toFixed(2).replace(".", ",")

  if (totalItems > 0) {
    cartCount.style.display = "flex"
  } else {
    cartCount.style.display = "none"
  }

  renderCartItems()
}

// Render cart items
function renderCartItems() {
  if (cart.length === 0) {
    cartItems.innerHTML = '<p style="text-align: center; padding: 2rem; color: #666;">Seu carrinho está vazio</p>'
    return
  }

  cartItems.innerHTML = cart
    .map(
      (item) => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">R$ ${item.price.toFixed(2).replace(".", ",")}</div>
            </div>
            <div class="cart-item-controls">
                <button onclick="updateCartQuantity(${item.id}, ${item.quantity - 1})" style="background: none; border: 1px solid #ddd; width: 30px; height: 30px; border-radius: 50%; cursor: pointer;">-</button>
                <span style="margin: 0 10px; font-weight: 600;">${item.quantity}</span>
                <button onclick="updateCartQuantity(${item.id}, ${item.quantity + 1})" style="background: none; border: 1px solid #ddd; width: 30px; height: 30px; border-radius: 50%; cursor: pointer;">+</button>
            </div>
        </div>
    `,
    )
    .join("")
}

// Show add to cart feedback
function showAddToCartFeedback() {
  // Create a temporary notification
  const notification = document.createElement("div")
  notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 3000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `
  notification.textContent = "Produto adicionado ao carrinho!"

  document.body.appendChild(notification)

  // Animate in
  setTimeout(() => {
    notification.style.transform = "translateX(0)"
  }, 100)

  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.transform = "translateX(100%)"
    setTimeout(() => {
      document.body.removeChild(notification)
    }, 300)
  }, 3000)
}

// Handle contact form
function handleContactForm(e) {
  e.preventDefault()

  const formData = new FormData(e.target)
  const data = Object.fromEntries(formData)

  // Simulate form submission
  const submitBtn = e.target.querySelector('button[type="submit"]')
  const originalText = submitBtn.textContent

  submitBtn.innerHTML = '<span class="loading"></span> Enviando...'
  submitBtn.disabled = true

  setTimeout(() => {
    submitBtn.textContent = "Mensagem Enviada!"
    submitBtn.style.background = "#28a745"

    setTimeout(() => {
      submitBtn.textContent = originalText
      submitBtn.style.background = ""
      submitBtn.disabled = false
      e.target.reset()
    }, 2000)
  }, 2000)
}

// Toggle mobile menu
function toggleMobileMenu() {
  const navMenu = document.querySelector(".nav-menu")
  navMenu.style.display = navMenu.style.display === "flex" ? "none" : "flex"
}

// Scroll effects
function setupScrollEffects() {
  const header = document.querySelector(".header")

  window.addEventListener("scroll", () => {
    if (window.scrollY > 100) {
      header.style.background = "rgba(255, 255, 255, 0.98)"
      header.style.boxShadow = "0 2px 20px rgba(0,0,0,0.1)"
    } else {
      header.style.background = "rgba(255, 255, 255, 0.95)"
      header.style.boxShadow = "none"
    }
  })
}

// Smooth scroll to section
function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId)
  const headerHeight = document.querySelector(".header").offsetHeight

  window.scrollTo({
    top: section.offsetTop - headerHeight,
    behavior: "smooth",
  })
}

// Intersection Observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1"
      entry.target.style.transform = "translateY(0)"
    }
  })
}, observerOptions)

// Observe elements for animation
document.addEventListener("DOMContentLoaded", () => {
  const animateElements = document.querySelectorAll(".product-card, .feature, .stat")

  animateElements.forEach((el) => {
    el.style.opacity = "0"
    el.style.transform = "translateY(30px)"
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease"
    observer.observe(el)
  })
})

// Keyboard navigation
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && cartModal.style.display === "block") {
    cartModal.style.display = "none"
    document.body.style.overflow = "auto"
  }
})

// Search functionality (bonus feature)
function searchProducts(query) {
  const filteredProducts = products.filter(
    (product) =>
      product.name.toLowerCase().includes(query.toLowerCase()) ||
      product.description.toLowerCase().includes(query.toLowerCase()),
  )
  renderProducts(filteredProducts)
}

// Price range filter (bonus feature)
function filterByPriceRange(min, max) {
  const filteredProducts = products.filter((product) => product.price >= min && product.price <= max)
  renderProducts(filteredProducts)
}

