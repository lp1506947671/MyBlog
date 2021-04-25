//头像预览
$('#avatar').change(function () {
    let file_objects = $(this)[0].files[0];
    console.log(file_objects);
    let reader = new FileReader();
    reader.readAsDataURL(file_objects);
    reader.onload = function () {
        $("#avatar_img").attr("src", reader.result)
    }
});
