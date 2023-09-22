function togglepass(id1, id2) {
    var passfield = document.getElementById(id1);
    if (passfield.type == "password") {
        passfield.type = "text"
        document.getElementById(id2).className = "fa fa-eye-slash field-icon";
    }
    else {
        passfield.type = "password"
        document.getElementById(id2).className = "fa fa-eye field-icon";
    };
};
function validateSearch(formname, fieldname) {
    if (document.forms[formname][fieldname].value != "") {
        return true;
    };
    return false;
}
function clearinput(id){
    document.getElementById(id).value = '';
};