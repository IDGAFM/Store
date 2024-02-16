document.getElementById('x').addEventListener('click', () => {
    document.getElementById('x').style.display = 'none'
    document.getElementById('bars').style.display = 'block'
    document.getElementById('nav').style.maxHeight = '37px'
})

document.getElementById('bars').addEventListener('click', () => {
    document.getElementById('bars').style.display = 'none'
    document.getElementById('x').style.display = 'block'
    document.getElementById('nav').style.maxHeight = '1200px'
})

let catalogs = document.getElementById('catalogs')
let catalogBtnFirst = document.getElementById('changesidelinks1')
let catalogBtnSecond = document.getElementById('changesidelinks2')

if(catalogBtnFirst) {
    catalogBtnFirst.addEventListener('click', () => {
        catalogs.scrollLeft = catalogs.clientWidth
    })
}

if(catalogBtnSecond) {
    catalogBtnSecond.addEventListener('click', () => {
        catalogs.scrollLeft = -catalogs.clientWidth
    })
}

let showMobileFilter = document.getElementById('showmobilefilter')
let arrow = document.getElementById('arrow')
let showFilter = () => {
    mobileFilter.style.maxHeight = '1000px'
    showMobileFilter.addEventListener('click', hideFilter)
    showMobileFilter.removeEventListener('click', showFilter)
    arrow.style.rotate = '180deg'
}

let hideFilter = () => {
    mobileFilter.style.maxHeight = '18px'
    showMobileFilter.addEventListener('click', showFilter)
    showMobileFilter.removeEventListener('click', hideFilter)
    arrow.style.rotate = '360deg'
}

let mobileFilter = document.getElementById('mobilefilter')

if (showMobileFilter) {
    showMobileFilter.addEventListener('click', showFilter)
}

let tovarscrollbtn2 = document.getElementById('tovarscrollbtn2')

let tovarscrollbtn1 = document.getElementById('tovarscrollbtn1')

let tovarscroll = document.getElementById('tovarscroll')

let targetElement = document.getElementById('targetElement')

if (tovarscroll) {
    let isScrolling = false;

    tovarscrollbtn2.addEventListener('click', () => {
        if (!isScrolling) {
            isScrolling = true;
            const scrollAmount = targetElement.offsetWidth + 0.2;
            tovarscroll.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
            setTimeout(() => {
                isScrolling = false;
            }, 600); // Через 0.6 секунды разблокируем кнопки
        }
    });

    tovarscrollbtn1.addEventListener('click', () => {
        if (!isScrolling) {
            isScrolling = true;
            const scrollAmount = -targetElement.offsetWidth;
            tovarscroll.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
            setTimeout(() => {
                isScrolling = false;
            }, 600); // Через 0.6 секунды разблокируем кнопки
        }
    });
}

document.getElementById('contactsnav').addEventListener('click', () => {
    document.getElementById('x').style.display = 'none'
    document.getElementById('bars').style.display = 'block'
    document.getElementById('nav').style.maxHeight = '37px'
})

let leftBuyScrollBtnLeft = document.getElementById('buytovarscrollbtn1')

let leftBuyScrollBtnRight = document.getElementById('buytovarscrollbtn2')

let buyTovarImages = document.getElementById('buytovarscroll')

let offerBtn = document.getElementById('offerBtn')

let offercard = document.getElementById('offercard')

let closeOfferCard = document.getElementById('closeOfferCard')

if(offercard) {
    offerBtn.addEventListener('click' , () => {
        offercard.style.cssText = 'transform: translate(-50%, -50%);'
    })

    closeOfferCard.addEventListener('click' , () => {
        offercard.style.cssText = 'transform: translate(-50%, 4000px);'
    })
}

if(buyTovarImages) {
    let isScrolling2 = false;
    leftBuyScrollBtnLeft.addEventListener('click' , () => {
        if (!isScrolling2) {
            isScrolling2 = true;
            const scrollAmount = -(buyTovarImages.clientWidth + 15);
            buyTovarImages.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
            setTimeout(() => {
                isScrolling2 = false;
            }, 600); // Через 0.6 секунды разблокируем кнопки
        }
    })

    leftBuyScrollBtnRight.addEventListener('click' , () => {
        if (!isScrolling2) {
            isScrolling2 = true;
            const scrollAmount = buyTovarImages.clientWidth + 15;
            buyTovarImages.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
            setTimeout(() => {
                isScrolling2 = false;
            }, 600); // Через 0.6 секунды разблокируем кнопки
        }
    })
}

function addReview(name, id) {
    document.getElementById("contactparent").value = id;
    document.getElementById("contactcomment").innerText = `${name}, `
}

function showNotification(message) {
  // Создаем элемент уведомления
  let notification = document.createElement('div');
  notification.className = 'notification';
  notification.textContent = message;

  // Добавляем элемент уведомления в документ
  document.body.appendChild(notification);

  // Задаем время отображения уведомления (в миллисекундах)
  let duration = 3000;

  // Задаем таймер для удаления уведомления после указанного времени
  setTimeout(function() {
    notification.parentNode.removeChild(notification);
  }, duration);
}

function enableEditing() {
  // Разблокируем поля ввода
  document.getElementById("phoneField").readOnly = false;
  document.getElementById("emailField").readOnly = false;
  document.getElementById("usernameField").readOnly = false;

  // Изменяем текст кнопки
  document.getElementById("editSaveButton").innerText = "Сохранить";
  // Заменяем обработчик события
  document.getElementById("editSaveButton").onclick = saveChanges;
}

function saveChanges() {
  // Получаем значения полей ввода
  let phone = document.getElementById("phoneField").value;
  let email = document.getElementById("emailField").value;
  let username = document.getElementById("usernameField").value;

  // Отправляем данные на сервер (предполагая использование AJAX)
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/settings/", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        // Данные успешно сохранены
        // Добавляем дополнительную логику здесь, например:
        showNotification("Изменения сохранены успешно");
        updateProfileInfo(phone, email, username);
      } else {
        // Произошла ошибка при сохранении данных
        // Добавляем обработку ошибки здесь, например:
        showNotification("Ошибка при сохранении данных");
      }
    }
  };

  const params = 'phone=' + encodeURIComponent(phone) +
                 '&email=' + encodeURIComponent(email) +
                 '&username=' + encodeURIComponent(username);
  xhr.send(params);

  // Блокируем поля ввода
  document.getElementById("phoneField").readOnly = true;
  document.getElementById("emailField").readOnly = true;
  document.getElementById("usernameField").readOnly = true;

  // Возвращаем исходный текст кнопки
  document.getElementById("editSaveButton").innerText = "Редактировать";
  // Возвращаем исходный обработчик события
  document.getElementById("editSaveButton").onclick = enableEditing;
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function updateProfileInfo(phone, email, username) {
  // Обновляем информацию на странице с новыми значениями
  document.getElementById("phoneField").value = phone;
  document.getElementById("emailField").value = email;
  document.getElementById("usernameField").value = username;
}
