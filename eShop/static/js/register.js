const usernameField = document.querySelector('#usernameField');
const invalid = document.querySelector('#invalid');
const invalid1 = document.querySelector('#invalid1');
const emailField = document.querySelector('#emailField');
const show = document.querySelector("#show");
const passwordField = document.querySelector('#passwordField');
const submit = document.querySelector('.submit');

passwordField.addEventListener("keyup", (e) => {
    const pass = e.target.value.length;
    show.style.display="none";
    if ( pass > 0  ){
        show.style.display="block";
    }
});

show.addEventListener('click',(e) => {
    if (show.textContent === "show"){
        show.textContent="hide";
        passwordField.setAttribute("type","text");
    }
    else{
        show.textContent="show";
        passwordField.setAttribute("type","password");
    }
});

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    invalid.style.display= "none";
    submit.disabled=false;
    if (usernameVal.length > 0) {
        fetch('/auth/validate-username', {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
    
            if(data.username_error){
                submit.disabled=true;
                usernameField.classList.add("is-invalid");
                invalid.style.display= "block";
                invalid.innerHTML = data.username_error;
            }
        });
    }

});

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    invalid.style.display= "none";
    submit.disabled=false;
    if (emailVal.length > 0) {
        fetch('/auth/validate-email', {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
    
            if(data.email_error){
                submit.disabled=true;
                emailField.classList.add("is-invalid");
                invalid1.style.display= "block";
                invalid1.innerHTML = data.email_error;
            }
        });
    }
});

