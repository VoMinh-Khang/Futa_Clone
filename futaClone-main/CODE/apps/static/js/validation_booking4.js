const paymentSubmit = document.querySelector('.step-pay-btn');
const paymentInput = [...document.querySelectorAll('.payment-radio')];
const errorBox = document.querySelector('.error-list');

const errors = [];

paymentSubmit.onclick = () => {
    errors.splice(0, errors.length);

    let payMethod = paymentInput.filter(ele => {
        return ele.checked === true;
    });

    if (payMethod.length === 0) {
        errors.push('Vui lòng chọn phương thức thanh toán');
        alertError(errors);
    } else {
        console.log('Không có lỗi');
    }
}

function alertError(errors) {
    if (errors.length > 0) {
        errorBox.innerHTML = errors.map(err => {
            return `<li class="error-item">${err}</li>`
        }).join('');

        errorBox.parentElement.classList.add('error-validation-active');

        let timeAdd = setTimeout(() => {
            errorBox.parentElement.classList.remove('error-validation-active');
        }, 5000);
    }
}