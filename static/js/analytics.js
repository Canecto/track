var activeTime = 0;
var url = "https://canecto.pythonanywhere.com/api/";
function calculateTime(){
	if(document.hasFocus()){
		activeTime++;
	}
    setTimeout(function(){
        calculateTime();
    }, 1000);
}
calculateTime();

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

window.onload = function (event){
	var cookie = readCookie("__ccto");
	if (cookie == null) {
	    var xmlHttpGet = new XMLHttpRequest();
		xmlHttpGet.onreadystatechange = function() {
			if (xmlHttpGet.readyState == 4 && xmlHttpGet.status == 200) {
				var data = JSON.parse(xmlHttpGet.responseText);
				var cookie = "__ccto=" + data["cookie"] + "; expires=Fri, 31 Dec 9999 23:59:59 GMT";
				document.cookie = cookie;
			}
		}
		xmlHttpGet.open("GET", url, true);
		xmlHttpGet.send();
	}
};

var isOnIOS = navigator.userAgent.match(/iPad/i)|| navigator.userAgent.match(/iPhone/i);
var eventName = isOnIOS ? "pagehide" : "beforeunload";

window.addEventListener(eventName, function (event){
	var cookie = readCookie("__ccto");
	var xmlHttpPost = new XMLHttpRequest();
	xmlHttpPost.open("POST", url, false);
	xmlHttpPost.setRequestHeader("Content-type", "application/json");
	var postData = {
		page_url: window.location.href,
		time_on_page: activeTime,
		cookie: cookie
	}
	xmlHttpPost.onreadystatechange = function() {
    	if (xmlHttpPost.readyState == 4 && XMLHttpRequest.DONE) {
    			console.log('');
    	}
	}
	xmlHttpPost.send(JSON.stringify(postData));
});