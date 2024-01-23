const password = document.querySelector("#sign-up-form #password");
const password2 = document.querySelector("#sign-up-form #password2");

const error1 = password.nextElementSibling;
const error2 = password2.nextElementSibling;

password.addEventListener("keyup", () => {
    validatePassword1();
    validatePassword2();
});

password2.addEventListener("keyup", validatePassword2);

function validatePassword2() {
    if (password.value !== password2.value) {
        error2.innerText = "Password is not the same";
    } else error2.innerText = "";

    if (password2.value === "") {
        error2.innerText = "";
    }
}

function validatePassword1() {
    if (!isPasswordSecure(password.value)) {
        error1.innerText = "Password is not secure";
    } else error1.innerText = "";

    if (password.value === "") {
        error1.innerText = "";
    }
}

function isPasswordSecure(password) {
    if (password.length < 4) return false;
    if (password === password.toLowerCase()) return false;
    return true;
}
