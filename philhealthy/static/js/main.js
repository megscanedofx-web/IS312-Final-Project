/* PhilHealthy JavaScript */

// Mobile nav toggle
document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');
  if (hamburger) {
    hamburger.addEventListener('click', () => navLinks.classList.toggle('active'));
  }

  // Sidebar toggle
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => sidebar.classList.toggle('active'));
  }
});

// Chatbot
function toggleChatbot() {
  document.getElementById('chatbotWindow').classList.toggle('active');
}

function closeChatbot() {
  document.getElementById('chatbotWindow').classList.remove('active');
}

function sendMessage() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;

  const messages = document.getElementById('chatMessages');

  // User message
  const userDiv = document.createElement('div');
  userDiv.className = 'chat-message user';
  userDiv.textContent = msg;
  messages.appendChild(userDiv);

  input.value = '';
  messages.scrollTop = messages.scrollHeight;

  // Bot response
  fetch('/api/chatbot', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: msg})
  })
  .then(r => r.json())
  .then(data => {
    const botDiv = document.createElement('div');
    botDiv.className = 'chat-message bot';
    botDiv.textContent = data.reply;
    messages.appendChild(botDiv);
    messages.scrollTop = messages.scrollHeight;
  })
  .catch(() => {
    const botDiv = document.createElement('div');
    botDiv.className = 'chat-message bot';
    botDiv.textContent = 'Sorry, I could not process your request right now.';
    messages.appendChild(botDiv);
  });
}

// Enter to send
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && document.activeElement.id === 'chatInput') {
    sendMessage();
  }
});

// Modal helpers
function openModal(id) {
  document.getElementById(id).classList.add('active');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('active');
}

// CRUD: Add Product
function addProduct(e) {
  e.preventDefault();
  const form = e.target;
  const data = {
    name: form.name.value,
    category: form.category.value,
    price: form.price.value,
    stock: form.stock.value,
    expiry: form.expiry.value,
  };
  fetch('/api/products', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  })
  .then(r => r.json())
  .then(() => location.reload())
  .catch(err => alert('Error adding product'));
}

// CRUD: Delete Product
function deleteProduct(id) {
  if (!confirm('Are you sure you want to delete this product?')) return;
  fetch(`/api/products/${id}`, { method: 'DELETE' })
    .then(r => r.json())
    .then(() => location.reload())
    .catch(err => alert('Error deleting product'));
}

// CRUD: Approve Delivery
function approveDelivery(id) {
  fetch(`/api/deliveries/${id}/approve`, { method: 'POST' })
    .then(r => r.json())
    .then(() => location.reload())
    .catch(err => alert('Error approving delivery'));
}

// Auto-dismiss flash messages
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 4000);
  });
});
