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

displayCartItems();

document.getElementById('home-btn').addEventListener('click', function(e) {
e.preventDefault();
alert('Your purchase is complete! Thank you for shopping with us.');
localStorage.removeItem('cart');
window.location.href = '/home/'; 

});