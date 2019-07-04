document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#form').onsubmit = () => {

    // Initialize new request
    const request = new XMLHttpRequest();
    const number = document.querySelector('#number').value;


    request.open('DELETE','/delete_product');

    //Callback function from when request completes
    request.onload = () => {

      //Extract JSON data from XMLHttpRequest
      const data = JSON.parse(request.responseText);

      //Update the result in dev
      if (data.success) {
        document.querySelector('#result').innerHTML = `ID: ${data.id}, NAME: ${data.name}, DESCRIPTION: ${data.description}, PRICE: ${data.price}, QUANTITY: ${data.qty}`;
      } else {
        document.querySelector('#result').innerHTML = 'There was an error.';
      }
    }

    // Add data to send with request
    const data = new FormData();
    data.append('number', number);


    //Send Request
    request.send(data);
    return false;


 };

});
