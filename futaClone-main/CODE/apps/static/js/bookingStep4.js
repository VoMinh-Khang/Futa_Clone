// handle click payment card and visible linking
let paymentMethods = [...document.querySelectorAll('.payment-item')];
let radioPayments = [...document.querySelectorAll('.payment-radio')];
let paymentLinking = document.querySelector('.payment-linking');

paymentMethods.forEach((item, index) => {
    item.onclick = () => {
        radioPayments[index].checked = true;
        removePaymentAndActive(paymentMethods, item);
        paymentTypeVisible(paymentLinking, item);
    }
});

function removePaymentAndActive(payments, current) {
    payments.forEach(item => {
        item.classList.remove('payment-method-active');
    })
    current.classList.add('payment-method-active');
}

function paymentTypeVisible(linking, current) {
    linking.classList.remove('type-international-active');
    linking.classList.remove('type-inland-active');

    if (current.classList.contains('payment-type-international')) {
        linking.classList.add('type-international-active');
    }

    if (current.classList.contains('payment-type-inland')) {
        linking.classList.add('type-inland-active');
    }
}