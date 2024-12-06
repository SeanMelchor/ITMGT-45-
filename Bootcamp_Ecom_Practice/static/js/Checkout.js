function displayCartItems() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p>Your cart is empty!</p>';
        cartTotal.textContent = '';
        return;
    }

    cartItemsContainer.innerHTML = '';
    let totalPrice = 0;

    cart.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <h3>${item.name}</h3>
            <p>Price: $${item.price}</p>
            <p>Quantity: ${item.quantity}</p>
        `;
        cartItemsContainer.appendChild(cartItem);
        totalPrice += item.price * item.quantity;
    });

    cartTotal.textContent = `Total: $${totalPrice.toFixed(2)}`;
}

const cart = JSON.parse(localStorage.getItem('cart')) || [];
document.getElementById('cart_data').value = JSON.stringify(cart);

document.getElementById('checkout-form').addEventListener('submit', function(e) {
    // Ensure cart_data is populated before submission
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartDataInput = document.getElementById('cart_data');
    cartDataInput.value = JSON.stringify(cart);
});

displayCartItems();