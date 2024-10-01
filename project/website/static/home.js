const btnCart = document.querySelectorAll('.btn-cart');

btnCart.forEach(function(item){
  item.addEventListener('click',function(){
    let item_id = item.dataset.id
    sendItemId(item_id)
  })
})


function sendItemId(item_id){

  let xhr = new XMLHttpRequest();
  xhr.open('POST','/add-cart',true)
  xhr.setRequestHeader("content-type", "application/json;charset=UTF8")

  let data = JSON.stringify({
    id:item_id
  })
  xhr.send(data)
}

// ------message-------------------------
function showMessage(action) {
  const messageSuccess = document.querySelector('.hidden-success')
  const messageLogIn = document.querySelector('.hidden-log-in')
  if(action === 'success'){
    messageSuccess.classList.remove('hidden-success');

    setTimeout(() => {
      messageSuccess.classList.add('hidden-success');

    }, 1000);
  }else{
    messageLogIn.classList.remove('hidden-log-in');

    setTimeout(() => {
      messageLogIn.classList.add('hidden-log-in');

    }, 1000);

  }

}
