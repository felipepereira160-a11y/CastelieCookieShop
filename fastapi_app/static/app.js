const cart = new Map();

const grid = document.getElementById('product-grid');
const categorySelect = document.getElementById('category');
const searchInput = document.getElementById('search');
const cartEl = document.getElementById('cart');
const orderForm = document.getElementById('order-form');
const statusEl = document.getElementById('order-status');

let products = [];

function formatBRL(value) {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function renderCategories() {
  const categories = ['Todos', ...new Set(products.map((p) => p.category))];
  categorySelect.innerHTML = '';
  categories.forEach((cat) => {
    const opt = document.createElement('option');
    opt.value = cat;
    opt.textContent = cat;
    categorySelect.appendChild(opt);
  });
}

function buildImageTag(productId, name) {
  const exts = ['jpg', 'jpeg', 'png', 'webp'];
  const bases = [`/assets/products/${productId}`, `/static/products/${productId}`];
  const img = document.createElement('img');
  img.alt = name;
  img.dataset.baseIndex = '0';
  img.dataset.extIndex = '0';
  img.src = `${bases[0]}.${exts[0]}`;
  img.onerror = () => {
    let baseIndex = parseInt(img.dataset.baseIndex, 10);
    let extIndex = parseInt(img.dataset.extIndex, 10) + 1;
    if (extIndex < exts.length) {
      img.dataset.extIndex = String(extIndex);
      img.src = `${bases[baseIndex]}.${exts[extIndex]}`;
      return;
    }
    baseIndex += 1;
    if (baseIndex < bases.length) {
      img.dataset.baseIndex = String(baseIndex);
      img.dataset.extIndex = '0';
      img.src = `${bases[baseIndex]}.${exts[0]}`;
      return;
    }
    img.style.display = 'none';
  };
  return img;
}

function renderProducts() {
  const query = (searchInput.value || '').toLowerCase();
  const category = categorySelect.value || 'Todos';
  grid.innerHTML = '';

  products
    .filter((p) => (category === 'Todos' ? true : p.category === category))
    .filter((p) => (p.name + ' ' + p.description).toLowerCase().includes(query))
    .forEach((p) => {
      const card = document.createElement('div');
      card.className = 'card product-card';

      const img = buildImageTag(p.id, p.name);
      card.appendChild(img);

      const stockInfo = p.available ? `Estoque: ${p.stock ?? 0}` : 'Indisponivel';
      const disabled = !p.available || (p.stock ?? 0) <= 0;

      card.insertAdjacentHTML(
        'beforeend',
        `
        <h3>${p.name}</h3>
        <div class="meta">${p.category} • ${p.size}</div>
        <p>${p.description}</p>
        <div class="price">${formatBRL(p.price)} <span class="badge">${p.highlight}</span></div>
        <div class="meta">${stockInfo}</div>
        <div class="actions">
          <input type="number" min="1" value="1" ${disabled ? 'disabled' : ''} />
          <button ${disabled ? 'disabled' : ''}>${disabled ? 'Indisponivel' : 'Adicionar'}</button>
        </div>
      `
      );

      const qtyInput = card.querySelector('input');
      const addBtn = card.querySelector('button');
      addBtn.addEventListener('click', () => {
        const qty = parseInt(qtyInput.value, 10) || 1;
        if (disabled) return;
        const existing = cart.get(p.id) || { ...p, qty: 0 };
        existing.qty += qty;
        cart.set(p.id, existing);
        renderCart();
      });

      grid.appendChild(card);
    });
}

function renderCart() {
  if (cart.size === 0) {
    cartEl.innerHTML = '<p>Carrinho vazio.</p>';
    return;
  }

  let total = 0;
  const items = Array.from(cart.values());
  const rows = items
    .map((item) => {
      total += item.price * item.qty;
      return `<div class="cart-row">
        <span>${item.name} x${item.qty}</span>
        <strong>${formatBRL(item.price * item.qty)}</strong>
      </div>`;
    })
    .join('');

  cartEl.innerHTML = `
    <div>${rows}</div>
    <div class="divider"></div>
    <div class="cart-row total">
      <span>Total</span>
      <strong>${formatBRL(total)}</strong>
    </div>
  `;
}

orderForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  statusEl.textContent = '';

  const formData = new FormData(orderForm);
  const payload = Object.fromEntries(formData.entries());
  payload.items = Array.from(cart.values());
  payload.subtotal = payload.items.reduce((sum, item) => sum + item.price * item.qty, 0);

  if (!payload.client_name || !payload.whatsapp) {
    statusEl.textContent = 'Informe nome e WhatsApp.';
    statusEl.className = 'error';
    return;
  }

  try {
    const resp = await fetch('/api/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await resp.json();
    if (!data.ok) {
      statusEl.textContent = data.message || 'Falha ao enviar pedido.';
      statusEl.className = 'error';
      return;
    }

    const emailStatus = data.email_ok ? '' : ` Email nao enviado: ${data.email_msg}`;
    statusEl.textContent = `Pedido ${data.order_id} enviado. Total ${formatBRL(data.total)}.${emailStatus}`;
    statusEl.className = data.email_ok ? 'success' : 'error';
    cart.clear();
    renderCart();
    await init();
  } catch (err) {
    statusEl.textContent = 'Falha ao enviar pedido.';
    statusEl.className = 'error';
  }
});

searchInput.addEventListener('input', renderProducts);
categorySelect.addEventListener('change', renderProducts);

async function init() {
  try {
    const resp = await fetch('/api/catalog');
    products = await resp.json();
  } catch (err) {
    products = [];
  }
  renderCategories();
  renderProducts();
  renderCart();
}

init();
