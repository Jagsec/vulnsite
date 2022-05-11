const loginToggler = document.querySelector('.bi')
const password = document.querySelector('#password')

loginToggler.addEventListener('click', () => {
    if (password.type === 'password'){
        password.type = 'text'
        loginToggler.className = 'bi bi-eye input-group-text'
    } else {
        password.type = 'password'
        loginToggler.className = 'bi bi-eye-slash input-group-text'
    }
})
