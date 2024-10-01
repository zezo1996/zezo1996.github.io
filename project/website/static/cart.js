const increase = document.querySelectorAll('.increase');
const decrease = document.querySelectorAll('.decrease');
const qty = document.querySelectorAll('.qty');

// buying panle
const totalPrice = document.querySelector('.total-price')
const shippingCost = document.querySelector('.shipping-cost')
const totalAddShipping = document.querySelector('.total-add-shiping')


// Event listener for the increase button
increase.forEach(function(item) {
  item.addEventListener('click', function() {
    let id = item.dataset.id; // Access the data-id attribute from the specific button
    sendQuantityUpdate('increase', id, item); // Pass the button to the update function
  });
});

// Event listener for the decrease button
decrease.forEach(function(item) {
  item.addEventListener('click', function() {
    let id = item.dataset.id; // Access the data-id attribute from the specific button
    sendQuantityUpdate('decrease', id, item); // Pass the button to the update function
  });
});

// Function to handle sending quantity updates via XMLHttpRequest
function sendQuantityUpdate(action, id, button) {
  // Create a new XMLHttpRequest object
  let xhr = new XMLHttpRequest();

  // Open a POST request to the specified endpoint
  xhr.open('POST', '/update-quantity', true);

  // Set the request header to indicate JSON data is being sent
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  // Prepare the data to send in the request body
  let data = JSON.stringify({
    id: id,  // Include the id in the data
    action: action  // Include the action ('increase' or 'decrease')
  });

  // Send the request with the data
  xhr.send(data);

  // Handle the response
  xhr.onload = function() {
    if (this.status === 200) {
      let value = JSON.parse(this.responseText);

      // Find the nearest qty element associated with the button clicked
      let quantityElement = button.parentElement.querySelector('.qty');
      if (quantityElement) {
        quantityElement.innerText = `Qty: ${value.quantity}`;  // Update the specific quantity element
      }

      // buying panle
      totalPrice.innerHTML = ` <b> Total Price: ${value.total_price}$</b>`
      shippingCost.innerHTML = ` <b> Shipping Cost: ${value.shipping_cost}$</b>`
      totalAddShipping.innerHTML = ` <b> Price with Shipping: ${value.total_with_shipping   }$</b>`
    }
  };

  // Handle errors (optional but recommended)
  xhr.onerror = function() {
    console.error('Request failed due to a network error.');
  };
}
