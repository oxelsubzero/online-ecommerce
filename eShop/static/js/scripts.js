/*!
* Start Bootstrap - Shop Item v5.0.6 (https://startbootstrap.com/template/shop-item)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-item/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project



const coupon = document.querySelector('#coupon');
const total = document.querySelector('#total');
const invalid = document.querySelector('#invalid');
const last = total.innerHTML
const coupontag = document.querySelector('#reduc')
const check = document.querySelector('#checkout');

coupon.addEventListener('keyup',(e) => {
    let totalval = total.innerHTML;
    const couponval = e.target.value;
    total.innerHTML = last;
    invalid.style.display = "none";
    coupontag.style.display = "none"
    if (couponval.length > 0) {
        fetch('/validate-coupon', {
            body: JSON.stringify({ coupon: couponval }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
    
            if(data.coupon_error){
                coupon.classList.add("is-invalid");
                invalid.style.display= "block";
                invalid.innerHTML = data.coupon_error;
                fetch('/update_total', {
                    body: JSON.stringify({ total: Number(last) }),
                    method: "POST",
                })
                .then((res)=>res.json())
            }

            else {
                valred = (Number(totalval)*data.reduc)/100;
                newtotal = Number(totalval) - valred;
                fetch('/update_total', {
                    body: JSON.stringify({ total: newtotal }),
                    method: "POST",
                })
                .then((res)=>res.json())

                coupontag.style.display = 'block';
                coupontag.innerHTML = "Coupon <span> -"+String(data.reduc)+"%</span>";
                total.innerHTML =  String(newtotal) + "€  (" + '<s>' + String(last) +'€</s>)';
            }
        });
    }

});


check.addEventListener('click',(e) => {
    console.log("hello")
    fetch('/update_total', {
        body: JSON.stringify({ total: Number(last) }),
        method: "POST",
    })
    .then((res)=>res.json())

});

