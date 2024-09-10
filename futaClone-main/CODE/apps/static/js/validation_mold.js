const mainFom = document.querySelector('.form-validation');
const submitButton = document.querySelector('.form-submit-validation');
const errorBox = document.querySelector('.error-list');
const formGroup = [...mainFom.querySelectorAll('.form-group')];

const errors = [];

submitButton.onclick = () => {
    onFormSubmit();
}

function onFormSubmit() {
    clearErrors(errors);

    formGroup.forEach(field => {
        let inputField = field.querySelector('input') || field.querySelector('select');
        checkError(inputField, errors);
    });

    alertError(errors);

    if (errors.length === 0) {
        console.log('Khong co loi');
    } else {
        console.error('On User Input Error!');
    }
}

function checkError(input, errors) {
    for (const rule in validateRules) {
        let error = validateRules[rule](input);

        if (error) {
            errors.push(error);
        }
    }
}

function clearErrors(errors) {
    errors.splice(0, errors.length);
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

function CheckEmpty(valueCheck) {
    return valueCheck === '';
}

// Rules
var validateRules = {
    isRequired: function (input) {
        let value = input.value.trim();
        let name = input.getAttribute('name');

        if (input.dataset.type === 'terms') {
            return (input.checked === false) ? `Chưa đồng ý điều khoản ${name}` : undefined;
        }

        return (value === '') ? `Chưa nhập thông tin ${name}` : undefined;
    },

    name: function (input) {
        if (input.dataset.type !== 'name') return;

        let value = input.value.trim();
        let name = input.getAttribute('name');

        return (value.length <= 5 && !CheckEmpty(value)) ? `Thông tin ${name} chưa đúng` : undefined;
    },

    phone: function (input) {
        if (input.dataset.type !== 'phone') return;

        let value = input.value.trim();
        let name = input.getAttribute('name');

        if (CheckEmpty(value)) return undefined;

        if (value.length <= 9 || isNaN(value)) {
            return `${name} phải là số và tối thiểu 10 số`;
        } else {
            return undefined;
        }
    },

    email: function (input) {
        if (input.dataset.type !== 'mail') return;

        let value = input.value.trim();
        let name = input.getAttribute('name');
        let regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (CheckEmpty(value)) return undefined;

        if (regex.test(value)) {
            return undefined;
        } else {
            return `Vui lòng nhập đúng ${name}`;
        }
    },

    // password: function (input) {
    //     if (input.dataset.type !== 'password') return;

    //     let value = input.value;
    //     let name = input.getAttribute('name');
    // },

    // select: function (input) {
    //     if (input.dataset.type !== 'select') return;

    //     let value = input.value;
    //     let name = input.getAttribute('name');

    //     if(CheckEmpty(value)) return undefined;

    // },

    // checkbox: function (input) {
    //     if (input.dataset.type !== 'terms') return;

    //     let value = input.checked;
    //     let name = input.getAttribute('name');

    //     if()
    // }
}