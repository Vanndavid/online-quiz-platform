function validate(){

    var errMsg = "";
    var result = true;

    var username=document.getElementById("username").value;

    if(username==""){
        errMsg+="You must enter a username."
    }

    if(errMsg!=""){
        alert(errMsg)
    }
    return result;

}

function init(){
    var submitForm = document.getElementById("register");
    console.log(submitForm)
    submitForm.onsubmit=validate;
}

window.onload=init;