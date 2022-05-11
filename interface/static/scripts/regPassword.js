const regToggler1 = document.querySelector('#toggler1')
const regToggler2 = document.querySelector('#toggler2')
const password = document.querySelector('#password')
const passwordConfirm = document.querySelector('#password_confirm')

regToggler1.addEventListener('click', () => {
    if (password.type === 'password'){
        password.type = 'text'
        regToggler1.className = 'bi bi-eye input-group-text'
    } else {
        password.type = 'password'
        regToggler1.className = 'bi bi-eye-slash input-group-text'
    }
})

regToggler2.addEventListener('click', () => {
    if (passwordConfirm.type === 'password'){
        passwordConfirm.type = 'text'
        regToggler2.className = 'bi bi-eye input-group-text'
    } else {
        passwordConfirm.type = 'password'
        regToggler2.className = 'bi bi-eye-slash input-group-text'
    }
})