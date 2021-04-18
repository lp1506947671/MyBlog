$("#validate_code_img").click(function () {
    let my_src = $(this)[0].src;
    if (!my_src.endsWith("?")) {
        $(this)[0].src += '?';
    } else {
        $(this)[0].src = "/blog/get_validate_code/";
    }

});
console.log(1)