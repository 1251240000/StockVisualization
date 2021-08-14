/******************************************************/
/************** CHARTS: <ALL> JS START  ***************/
/******************************************************/
function initMAChart(stockCode = '', chartElementId = 'echarts', ) {
    if (!$('#' + chartElementId).length) {
        throw new Error("Element #" + chartElementId + " not found!");
    }
    var colorList = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3'];
    var labelFont = 'bold 12px Sans-serif';
    csrfAjax({
        url:  "/api/v1/stock/crawl/daily_quotation?code=" + stockCode,
        type: "GET",
        success: function(raw) {
            var results = raw.results;
            var length = results.ts_code.length;
            
            var k = [[]];
            for (var i = 0; i < length; i++) {
                k.push([
                    results.open[i],
                    results.close[i],
                    results.low[i],
                    results.high[i],
                    results.vol[i],
                ]);
            }
        
            var option = {
                animation: true,
                color: colorList,
                legend: {
                    top: 20,
                    data: ['日K', 'MA5', 'MA10', 'MA20']
                },
                tooltip: {
                    triggerOn: 'none',
                    transitionDuration: 0,
                    confine: true,
                    bordeRadius: 4,
                    borderWidth: 1,
                    borderColor: '#333',
                    backgroundColor: 'rgba(255,255,255,0.9)',
                    textStyle: {
                        fontSize: 12,
                        color: '#333'
                    },
                    position: function (pos, params, el, elRect, size) {
                        var obj = {
                            top: 60
                        };
                        obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 5;
                        return obj;
                    }
                },
                axisPointer: {
                    link: [{
                        xAxisIndex: [0, 1]
                    }]
                },
                dataZoom: [{
                    type: 'slider',
                    xAxisIndex: [0, 1],
                    realtime: false,
                    start: length < 60 ? 0:100-parseInt(6000/length),
                    end: 100,
                    top: 65,
                    height: 20,
                    handleIcon: 'M10.7,11.9H9.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4h1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                    handleSize: '120%'
                }, {
                    type: 'inside',
                    xAxisIndex: [0, 1],
                    start: 40,
                    end: 70,
                    top: 30,
                    height: 20
                }],
                xAxis: [{
                    type: 'category',
                    data: results.trade_date,
                    boundaryGap : false,
                    axisLine: { lineStyle: { color: '#777' } },
                    axisLabel: {
                        formatter: function (value) {
                            return echarts.format.formatTime('MM-dd', value);
                        }
                    },
                    min: 'dataMin',
                    max: 'dataMax',
                    axisPointer: {
                        show: true
                    }
                }, {
                    type: 'category',
                    gridIndex: 1,
                    data: results.trade_date,
                    scale: true,
                    boundaryGap : false,
                    splitLine: {show: false},
                    axisLabel: {show: false},
                    axisTick: {show: false},
                    axisLine: { lineStyle: { color: '#777' } },
                    splitNumber: 20,
                    min: 'dataMin',
                    max: 'dataMax',
                    axisPointer: {
                        type: 'shadow',
                        label: {show: false},
                        triggerTooltip: true,
                        handle: {
                            show: true,
                            margin: 30,
                            color: '#B80C00'
                        }
                    }
                }],
                yAxis: [{
                    scale: true,
                    splitNumber: 2,
                    axisLine: { lineStyle: { color: '#777' } },
                    splitLine: { show: true },
                    axisTick: { show: false },
                    axisLabel: {
                        inside: true,
                        formatter: '{value}\n'
                    }
                }, {
                    scale: true,
                    gridIndex: 1,
                    splitNumber: 2,
                    axisLabel: {show: false},
                    axisLine: {show: false},
                    axisTick: {show: false},
                    splitLine: {show: false}
                }],
                grid: [{
                    left: 25,
                    right: 25,
                    top: 110,
                    height: 300
                }, {
                    left: 25,
                    right: 25,
                    height: 100,
                    top: 440
                }],
                graphic: [{
                    type: 'group',
                    left: 'center',
                    top: 70,
                    width: 300,
                    bounding: 'raw',
                    children: [{
                        id: 'MA5',
                        type: 'text',
                        style: {fill: colorList[1], font: labelFont},
                        left: 0
                    }, {
                        id: 'MA10',
                        type: 'text',
                        style: {fill: colorList[2], font: labelFont},
                        left: 'center'
                    }, {
                        id: 'MA20',
                        type: 'text',
                        style: {fill: colorList[3], font: labelFont},
                        right: 0
                    }]
                }],
                series: [{
                    name: 'Volume',
                    type: 'bar',
                    xAxisIndex: 1,
                    yAxisIndex: 1,
                    itemStyle: {
                        normal: {
                            color: '#7fbe9e'
                        },
                        emphasis: {
                            color: '#140'
                        }
                    },
                    data: results.vol
                }, {
                    type: 'candlestick',
                    name: '日K',
                    data: k,
                    itemStyle: {
                        normal: {
                            color: '#ef232a',
                            color0: '#14b143',
                            borderColor: '#ef232a',
                            borderColor0: '#14b143'
                        },
                        emphasis: {
                            color: 'black',
                            color0: '#444',
                            borderColor: 'black',
                            borderColor0: '#444'
                        }
                    }
                }, {
                    name: 'MA5',
                    type: 'line',
                    data: results.ma5,
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                }, {
                    name: 'MA10',
                    type: 'line',
                    data: results.ma10,
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                }, {
                    name: 'MA20',
                    type: 'line',
                    data: results.ma20,
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        normal: {
                            width: 1
                        }
                    }
                }]
            };
            var myChart = echarts.init(document.getElementById(chartElementId));
            myChart.setOption(option);
            window.onresize = function () {
                myChart.resize();
            }
        }
    })
}
/**************** CHARTS: <ALL> JS END  ***************/



/******************************************************/
/*************** PAGE: <ALL>  JS START  ***************/
/******************************************************/
/*$(function() {
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
        };
        // var actualHeight = $('#inner-iframe').contents().height();
        // $('#inner-iframe').height(actualHeight);
    };
    $(window).ready(set);
    $(window).on("resize", set);
});*/


function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){return pair[1];}
    }
    return(false);
}
function getCsrfToken(){
    if (typeof $.cookie().csrftoken == "undefined") {
        $.ajax({
            url: "/do/get_csrf_token",
            async: false,
        });
    }
    return $.cookie().csrftoken; 
}
function csrfAjax(options) {
    if (options.type != "GET") {
        if (typeof options.data == "undefined") {
            options.data = {};
        }
        options.data.csrfmiddlewaretoken = getCsrfToken();
    }
    var errorFunction = options.error;
    options.error = function (xhr, ) {
        if (xhr.status == 403) {
            window.location.href='/login/?next=' + window.location.pathname;
        }
        if (typeof errorFunction != "undefined") {
            errorFunction(xhr, status, err);
        }
    }
    $.ajax(options);
}
function serializeFormData(form) {
    if (typeof form == "object") {
        var res = {};
        $.each(form.serializeArray(), function() {
            res[this.name] = this.value;
        })
        return res;
    } else {
        throw new Error("Form must be an object!");
    }
}

function digitFormatter(digit, target = 'float', decimal = 2, ) {
    var d = Number(digit);
    if (target == 'int') {
        return d.toFixed(0);
    }
    else if (target == 'float') {
        return d.toFixed(decimal);
    } 
    else if (target == 'percentage') {
        return (d * 100).toFixed(2) + '%';
    }
    else if (target == 'CNY') {
        if (digit > 10 ** 8) {
            return (d / 10 ** 8).toFixed(decimal) + "亿";
        }        
        else if (digit > 10 ** 4) {
            return (d / 10 ** 4).toFixed(decimal) + "万";
        } else {
            return d.toFixed(decimal) + "元";
        }
    }
}

var GlobalVariable = {};
var print = console.log;

GlobalVariable.currentPage = $('script')[$('script').length - 1].getAttribute('page');

/**************** PAGE: <ALL>  JS END  ****************/



/******************************************************/
/************** PAGE: <login-index>  JS START  ********/
/******************************************************/
function userLogin() {
    csrfAjax({
        url: "/do/login",
        type: "POST",
        data: serializeFormData($('#login-form')),
        success: function (data) {
            if (data.code == 200) {
                var nextPath = getQueryVariable('next');
                if (nextPath == '') {
                    nextPath = '/';
                }
                window.location.href = nextPath;
            } else {
                $('#message-alert').removeClass('d-none');
                $('#message-alert').text(data.msg);
            }
        }
    });
}

function userLogout() {
    csrfAjax({
        url: "/do/logout",
        type: "POST",
        success: function (data) {
            if (data.code == 200) {
                window.location.href='/login/';
            } else {
                
            }
        }
    });
}

$("body").keydown(function(event) {
    if (event.keyCode == "13") {
        $('#login-submit').click();
    }
});

/*************** PAGE: <login-index>  JS END  *********/





/******************************************************/
/************** PAGE: <index>  JS START  **************/
/******************************************************/
function switchPage(page) {
    $(".preloader").fadeIn('fast');
    $('#inner-iframe').attr('src', '/pages/' + page + '.html');
    $('.nav-btn').removeClass("pb-2 border-bottom-3 border-info");
    $('#' + page).addClass("pb-2 border-bottom-3 border-info");
}

if (GlobalVariable.currentPage == 'index') {
    $('#inner-iframe').on("load", function () {
        print('iframe load');
        var actualHeight = $('#inner-iframe').contents().height();
        $('#inner-iframe').height(actualHeight);
        $(".preloader").fadeOut('fast');
    });
    switchPage('index');
    $('.nav-btn').click(function () {
        switchPage(this.id);
    })
}
/*************** PAGE: <index>  JS END  ***************/


/******************************************************/
/************** PAGE: <pages-index>  JS START  ********/
/******************************************************/
function freezeRankTableHeader(){
    $("#table-rank-up").freezeHeader({ 'offset': '66px' });
    $("#table-rank-down").freezeHeader({ 'offset': '66px' });
}

function updateStockBasic(code=''){
    csrfAjax({
        url: "/api/v1/stock/crawl/basic?code=" + code,
        type: "GET",
        success: function (data) {
            if (data.code == 200) {
                var keys = ['name', 'code', 'price', 'date', 'time', 'open', 'preclose', 
                'high', 'low', 'volume', 'amount', 'pb', 'pe', 'eps', 'bvps', 'totals', 
                'outstanding', 'totalassets', 'liquidassets', 'change', 'pchange'];
                var stockInfo = data.results;

                stockInfo.change = stockInfo.price - stockInfo.preclose;
                stockInfo.pchange = (stockInfo.price - stockInfo.preclose) / stockInfo.preclose;
                
                for (var key of keys) {
                    if (['pchange'].includes(key)) {
                        stockInfo[key] = digitFormatter(stockInfo[key], 'percentage');
                    }
                    else if (['price', 'open', 'preclose', 'high', 'low', 'pb', 'pe', 'eps', 'bvps', 'change'].includes(key)) {
                        stockInfo[key] = digitFormatter(stockInfo[key], 'float');
                    }
                    else if (['volume', 'amount', 'totals', 'outstanding', 'totalassets', 'liquidassets'].includes(key)) {
                        stockInfo[key] = digitFormatter(stockInfo[key], 'CNY');
                    }
                    $('.stock-info-' + key).text(stockInfo[key]);
                    // print($('.stock-info-' + key), stockInfo[key]);
                }
                $(".stock-info-price,.stock-info-change,.stock-info-pchange,.stock-info-open").removeClass("text-danger text-success");

                $(".stock-info-price,.stock-info-change,.stock-info-pchange").addClass(stockInfo.preclose <= stockInfo.price?"text-danger":"text-success");
                $(".stock-info-open").addClass(stockInfo.preclose <= stockInfo.open?"text-danger":"text-success");
                //$(".stock-info-high").addClass(stockInfo.preclose <= stockInfo.high?"text-danger":"text-success");
                //$(".stock-info-low").addClass(stockInfo.preclose <= stockInfo.low?"text-danger":"text-success");
            }
            else {

            }
        }
    })    
}


function searchStock() {
    var searchCode = $('#stock-code').val();
    if (GlobalVariable.stockCodeSet.has(searchStock)) {
        initMAChart(stockCode = searchCode);
        updateStockBasic(searchCode);
    } else {
        $('#stock-code').css("border", "1px solid red");
    }
}

function fetchStockRegister() {
    csrfAjax({
        url: "/api/v1/stock/store/basic/register/",
        type: "GET",
        success: function (data) {
            GlobalVariable.registeredStock = data.results;
            GlobalVariable.stockCodeSet = new Set();
            for (var record of GlobalVariable.registeredStock) {
                record.index = record.symbol + record.name; // + record.tscode + record.sinacode
                GlobalVariable.stockCodeSet.add(record.symbol);
            }
        }
    })
}

function associativeSearch(input) {
    var res = [];
    for (var stock of GlobalVariable.registeredStock) {
        if (stock.index.indexOf(input) != -1) {
            res.push(stock);
        }
        if (res.length >= 10) {
            break;
        }
    }
    return res;
}

$("#stock-code").bind("input propertychange", function() {
    $('#result-list').addClass('show');
    var input = $('#stock-code').val();
    var res = associativeSearch(input);

    $('.dropdown-item').addClass('d-none');
    $('.dropdown-divider').addClass('d-none');

    $('.dropdown-item > .label').removeClass('label-info label-success');
    $('.dropdown-item > .text').removeClass('text-info text-success');

    for (var i = 0; i < res.length; i++) {
        $('.dropdown-item > .label').eq(i).text(res[i].name);
        $('.dropdown-item > .text').eq(i).text('[' + res[i].symbol + ']');
        
        if (res[i].tscode.indexOf('SZ') != -1) {
            $('.dropdown-item > .label').eq(i).addClass('label-info');
            $('.dropdown-item > .text').eq(i).addClass('text-info');
        } else {
            $('.dropdown-item > .label').eq(i).addClass('label-success');
            $('.dropdown-item > .text').eq(i).addClass('text-success');
        }
        
        $('.dropdown-item').eq(i).removeClass('d-none');
        if (i != 0) {
            $('.dropdown-divider').eq(i-1).removeClass('d-none');    
        }
    }
});

if (GlobalVariable.currentPage == 'pages-index') {
    // 固定个股异动表头
    freezeRankTableHeader();
    // 更新股票基本信息
    updateStockBasic();
    // 初始化均线图
    initMAChart();
    // 获取A股股票清单
    fetchStockRegister();
    // 绑定搜索事件
    $('#stock-search').click(function() {searchStock();});
    // 绑定回车触发搜索
    $("#stock-code").keydown(function(event) {
        if (event.keyCode == "13") {
            searchStock();
        }
    });
}
/*************** PATH: <pages-index>  JS END  *********/

                  
                  
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

$(".stock-index").each(function (){ $(this).mouseover(function () {$(this).find("img").removeClass("d-none"); }); });
$(".stock-index").each(function (){ $(this).mouseout(function () {$(this).find("img").addClass("d-none"); }); });

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


/******************************************************/
/************** PAGE: <profile>  JS START  ***************/
/******************************************************/
$('#btn-logout').click(function() { userLogout(); });

/************** PAGE: <profile>  JS END  *****************/
