const forms = document.querySelectorAll('.form-item');
forms.forEach(function (form) {
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Product id
    let formId = this.id;
    const selectMenus = this.querySelectorAll('select');
    selectMenus.forEach(function (select) {
      // Select value
      const value = select.value;
      let statusElement = select.parentElement.parentElement.querySelector('.status-sec');
      statusElement.innerHTML = `<b> Status: ${value}</b>`;

      // Send the values to the function
      sendValues(formId, value);
    });
  });
});

function sendValues(id, value) {
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/sold-items', true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  let data = JSON.stringify({
    id: id,
    value: value
  });
  xhr.send(data);
}
