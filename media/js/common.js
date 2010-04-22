function reload_verifycode(oVerifycode) {
    //var oVerifycode = document.getElementById(sVerifycode);
    var now = new Date();
	if (oVerifycode) {
        oVerifycode.src = "/utils/vcode/?date=" + now.getTime(); 
    }
}