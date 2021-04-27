//头像预览
$('#avatar').change(function () {
    let file_objects = $(this)[0].files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file_objects);
    reader.onload = function () {
        $("#avatar_img").attr("src", reader.result)
    }
});
//注册按钮
$(".reg_btn").click(function () {
//    创建FormData对象
//    对id=form的表单值使用serializeArray序列化
//     将序列化后的数据依次追加到FormData中
//    需要注意序列化的数据中不存在文件数据
//    发送ajax请求
//         contentType:false,processData:false
//    注册成功  直接返回登录界面
//    注册失败
//             清空错误信息
//             输入框清除标红的类
//             遍历错误信息:
//                          field=="__all__",再次输入密码的旁边
//                          其他field则插入到对应字段后面

    let form = new FormData();
    let data = $("#form").serializeArray();
    $.each(data, function (index, dataItem) {
        form.append(dataItem.name, dataItem.value)
    });
    form.append("avatar", $("#avatar")[0].files[0]);
    $.ajax({
        url: "",
        type: "post",
        contentType: false,
        processData: false,//是否将数据转换成字符串(不支持二级制),
        data: form,
        success: function (data) {
            if (data.user) {
                location.href = "";
            } else {
                $(".error").text("");
                $(".form-group").removeClass("has-error");
                $.each(data.msg, function (field, error_list) {
                    if (field == "__all__") {
                        $("#id_re_pwd").next().html(error_list[0]).parent().addClass("has-error")
                    }
                    $("#id_" + field).next().html(error_list[0]);
                    $("#id_" + field).parent().addClass("has-error");
                })
            }
        }
    })
});