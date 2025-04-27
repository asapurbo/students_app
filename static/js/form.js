const signature = document.getElementById('signature');
const form = document.getElementById('form');
const alert = document.getElementById('alert');
const closeAlertButton = document.getElementById('closeAlert');
const form_div = document.getElementById('form-div');
const alert_box = document.querySelector('.alert-box');
const yes_btn = document.querySelector('.yes_btn');
const err_cl = document.querySelector('.err_cl');
const error = document.querySelector('.error');

let isAlert = true;

function closeAlert() {
    form_div.classList.remove('x-fjd34')
    alert_box.style.display = 'none';
}

signature.addEventListener('click', () => {
    if (isAlert) {
        form_div.classList.add('x-fjd34')
        alert_box.style.display = 'block';
        isAlert = false;
        return
    }

    form.submit();
});

closeAlertButton.addEventListener('click', () => {
    closeAlert();
});


yes_btn.addEventListener('click', () => {
    closeAlert();
    form.submit();
})

err_cl.addEventListener('click', () => {
    error.style.display = 'none';
})
