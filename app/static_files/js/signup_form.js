const password = document.querySelector("#sign-up-form #password");
const password2 = document.querySelector("#sign-up-form #password2");

const error1 = password.nextElementSibling;
const error2 = password2.nextElementSibling;

const passwordMinLength = 10;
const punctuationSet = new Set("!@#$%^&*()_+-=[]{}|;:,.<>?");
const numbersSet = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9]);

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
    if (password.length <= passwordMinLength) return false;
    if (
        password === password.toLowerCase() &&
        password === password.toUpperCase()
    )
        return false;

    let passwordSet = new Set(password);

    if (passwordSet.size <= password.length / 2) return false;
    if (setIntersection(punctuationSet, passwordSet).size === 0) return false;

    let numbersInPassword = password
        .split("")
        .filter((ch) => !isNaN(ch))
        .map((ch) => +ch);
    console.log(numbersInPassword);

    if (setIntersection(numbersSet, new Set(numbersInPassword)).size === 0)
        return false;

    return true;
}

function setIntersection(set1, set2) {
    let intersection = new Set();

    for (let item of set1) {
        if (set2.has(item)) {
            intersection.add(item);
        }
    }

    return intersection;
}
