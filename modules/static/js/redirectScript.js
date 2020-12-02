function DelayedRedirect(delay, url){

    setTimeout(function () {
    window.location.href = url;
    }, delay*1000);

};
