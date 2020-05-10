/******************************************************/
/*************** PAGE: <ALL>  JS START  ***************/
/******************************************************/

$(function() {
    "use strict";
    $(function() {
        $(".preloader").fadeOut();
    });
    var set = function() {
        var width = (window.innerWidth > 0) ? window.innerWidth : this.screen.width;
        var topOffset = 55;
        if (width < 1170) {
            $("body").addClass("mini-sidebar");
            $('.navbar-brand span').hide();
        } else {
            $("body").removeClass("mini-sidebar");
            $('.navbar-brand span').show();
        }
        var height = ((window.innerHeight > 0) ? window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $(".page-wrapper").css("min-height", (height) + "px");
        }
    };
    $(window).ready(set);
    $(window).on("resize", set);
});

if ($(".stock-pclose").length == 1){
    $(".stock-price").addClass(parseFloat($(".stock-pclose").text()) <= parseFloat($(".stock-price").text())?"text-danger":"text-success");
    $(".stock-change").addClass(parseFloat($(".stock-pclose").text()) <= parseFloat($(".stock-price").text())?"text-danger":"text-success");
    $(".stock-pchange").addClass(parseFloat($(".stock-pclose").text()) <= parseFloat($(".stock-price").text())?"text-danger":"text-success");
    
    $(".stock-open").addClass(parseFloat($(".stock-pclose").text()) <= parseFloat($(".stock-open").text())?"text-danger":"text-success");
    $(".stock-high").addClass(parseFloat($(".stock-pclose").text()) <= parseFloat($(".stock-high").text())?"text-danger":"text-success");
    $(".stock-low").addClass(parseFloat($(".stock-pclose").text()) <= parseFloat($(".stock-low").text())?"text-danger":"text-success");
}


$(".stock-index").each(function (){ $(this).mouseover(function () {$(this).find("img").removeClass("d-none"); }); });
$(".stock-index").each(function (){ $(this).mouseout(function () {$(this).find("img").addClass("d-none"); }); });
/**************** PAGE: <ALL>  JS END  ****************/





/******************************************************/
/************** PAGE: <login>  JS START  **************/
/******************************************************/
                  

$("#mlogin-btn").click(function () {
    $("#plogin-btn").removeClass("border-info pb-2 border-bottom-3");
    $("#mlogin-btn").addClass("border-info pb-2 border-bottom-3")
    $("#mlogin-form").removeClass("d-none");
    $("#plogin-form").addClass("d-none");
});
$("#forget-btn").click(function () {
    $("#plogin-btn").removeClass("border-info pb-2 border-bottom-3");
    $("#mlogin-btn").addClass("border-info pb-2 border-bottom-3")
    $("#mlogin-form").removeClass("d-none");
    $("#plogin-form").addClass("d-none");
});
$("#plogin-btn").click(function () {
    $("#mlogin-btn").removeClass("border-info pb-2 border-bottom-3");
    $("#plogin-btn").addClass("border-info pb-2 border-bottom-3")
    $("#mlogin-form").addClass("d-none");
    $("#plogin-form").removeClass("d-none");
});
$("#mlogin-submit").click(function () {
    $.cookie("lastLoginType", "messLogin", { expires: 1/144, path: "/login/" });
    $.cookie("lastLoginAccount", $("#mlogin-account").val(), { expires: 1/144, path: "/login/" });
    $("#mlogin-form").submit();
});
$("#plogin-submit").click(function () {
    $.cookie("lastLoginType", "passLogin", { expires: 1/144, path: "/login/" });
    $.cookie("lastLoginAccount", $("#plogin-account").val(), { expires: 1/144, path: "/login/" });
    $("#plogin-form").submit();
});
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}
function countdown (times){
    if(times!=0){
        $("#get-code").addClass("text-muted");
        $("#get-code").text(times+"秒后重试");
        sleep(1000).then(()=>{times--;countdown(times);});
    }else{
        $("#get-code").removeClass("text-muted");
        $("#get-code").text("获取验证码");
    }
}
$("#get-code").click(function() {
    if ($.cookie("getCodeLimit") != "disabled" && $("[name='pnum']")[0].value != ""){
        $.ajax({
            url: '/login/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']")[0].value,
                submitType: 'getCode',
                pnum: $("[name='pnum']")[0].value,
            },
            success: function () {
                $.cookie("getCodeLimit", "disabled", { expires: 1/1440, path: "/login/" });
                countdown(60);
            }
        })
    }
})

function getLastLoginInfo(){
    if ($.cookie("lastLoginType") == "messLogin"){
        $("#mlogin-account").val($.cookie("lastLoginAccount"));
    }else if ($.cookie("lastLoginType") == "passLogin"){
        $("#mlogin-btn").removeClass("border-info pb-2 border-bottom-3");
        $("#plogin-btn").addClass("border-info pb-2 border-bottom-3")
        $("#mlogin-form").addClass("d-none");
        $("#plogin-form").removeClass("d-none");
        $("#plogin-account").val($.cookie("lastLoginAccount"));
    }
}
/*************** PAGE: <login>  JS END  ***************/

        
        
        
        
/******************************************************/
/************** PAGE: <index>  JS START  **************/
/******************************************************/
        
function freezeRankTableHeade(){
    $("#table-rank-up").freezeHeader({ 'offset': '66px' });
    $("#table-rank-down").freezeHeader({ 'offset': '66px' });
}
/*************** PAGE: <index>  JS END  ***************/


                  
                  
                  
/******************************************************/
/************** PAGE: <pick>  JS START  ***************/
/******************************************************/
                  
function stockSelect(s){
    $("#card-stockinfo-"+s).parents("tr").siblings().css("background-color", "");
    $("#card-stockinfo-"+s).parents("tr").css("background-color", "#ecedef");
    $("#inner-iframe")[0].src = "/pick/inner" + (s=="news"?"":"?stockcode="+s);
}

function delStock(code){
    $.ajax({
        url: '/pick/',
        type: 'post',
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']")[0].value,
            submitType: 'removeStock',
            scode: code
        },
        success: function () {
            $("#stock-"+code).remove();
        }
    })
}

for (var i = 0; i < $(".pick-stock-pchange").length; i++){
    if ($(".pick-stock-pchange:eq(" + i + ")").text()[0] == "-"){
        $(".pick-stock-price:eq(" + i + ")").addClass("text-success");
        $(".pick-stock-pchange:eq(" + i + ")").addClass("text-success");
    }
    else{
        $(".pick-stock-price:eq(" + i + ")").addClass("text-danger");
        $(".pick-stock-pchange:eq(" + i + ")").addClass("text-danger");
    }
}
/*************** PAGE: <pick>  JS END  ****************/
                  
                  
                  

/******************************************************/
/************** PAGE: <hold>  JS START  ***************/
/******************************************************/
                  
for (var i=0;i<$(".record").length;i++){
    $(".record-change:eq("+i+")").text(((parseFloat($(".record-price:eq("+i+")").text()) - parseFloat($(".record-bprice:eq("+i+")").text())) * parseFloat($(".record-bvolume:eq("+i+")").text())).toFixed(2));
    if ($(".record-change:eq("+i+")").text()[0] == "-") {
        $(".record-change:eq("+i+")").addClass("text-success");
        $(".record-btn:eq("+i+")").addClass("btn-success");
    } else {
        $(".record-change:eq("+i+")").addClass("text-danger");
        $(".record-btn:eq("+i+")").addClass("btn-danger");
    }
}
/************** PAGE: <hold>  JS END  *****************/
